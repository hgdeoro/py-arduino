##-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
##    Py-Arduino-Proxy - Access your Arduino from Python
##    Copyright (C) 2011 - Horacio Guillermo de Oro <hgdeoro@gmail.com>
##
##    This file is part of Py-Arduino-Proxy.
##
##    Py-Arduino-Proxy is free software; you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation version 2.
##
##    Py-Arduino-Proxy is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License version 2 for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with Py-Arduino-Proxy; see the file LICENSE.txt.
##-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# TODO: _unindent() could be a annotation

import logging
import pprint
import serial
import time
import uuid

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

logger = logging.getLogger(__name__) # pylint: disable=C0103

def _unindent(spaces, the_string):
    lines = []
    start = ' '*spaces
    for a_line in the_string.splitlines():
        if a_line.startswith(start):
            lines.append(a_line[spaces:])
        else:
            lines.append(a_line)
    return '\n'.join(lines)

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class InvalidCommand(Exception):
    """The Arduino reported an error in the command"""

class InvalidResponse(Exception):
    """The response from the Arduino isn't valid."""

class EmptyResponse(Exception):
    """The response from the Arduino was empty."""

class CommandTimeout(Exception):
    """Timeout detected while waiting for Arduino's response."""

class InvalidArgument(Exception):
    """A method was called with invalid argument type or values."""

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ArduinoProxy(object):
    
    #define HIGH 0x1
    #define LOW  0x0
    HIGH = 0x01
    LOW = 0x00

    #define INPUT 0x0
    #define OUTPUT 0x1
    INPUT = 0x00
    OUTPUT = 0x01
    
    #define CHANGE 1
    #define FALLING 2
    #define RISING 3
    CHANGE = 1
    FALLING = 2
    RISING = 3
    
    INVALID_CMD = "INVALID_CMD"
    
    def __init__(self, tty, speed=9600, wait_after_open=3, timeout=5, call_connect=True):
        # For communicating with the computer, use one of these rates: 300, 1200, 2400, 4800,
        #    9600, 14400, 19200, 28800, 38400, 57600, or 115200.
        logger.debug("Instantiating ArduinoProxy('%s', %d)..." % (tty, speed))
        self.tty = tty
        self.speed = speed
        self.serial_port = None
        if tty != '':
            logger.debug("Opening serial port...")
            self.serial_port = serial.Serial(port=tty, baudrate=speed, bytesize=8, parity='N',
                stopbits=1, timeout=timeout)
            self.serial_port.open()
            if wait_after_open > 0:
                logger.debug("Open OK. Now waiting for Arduino's reset")
                time.sleep(wait_after_open)
            if call_connect:
                self.connect()
            logger.debug("Done.")
    
    def get_next_response(self):
        """
        Waits for a response from the serial.
        Raises CommandTimeout if a timeout while reading is detected.
        """
        logger.debug("get_next_response() - waiting for response...")
        start = time.time()
        response = StringIO()
        while True:
            char = self.serial_port.read()
            if len(char) == 1:
                # Got a char
                if char in ['\n', '\r']:
                    if response.getvalue(): # response.len doesn't works for cStringIO
                        # If got '\n' or '\r' after some valid text, break the loop
                        break
                else:
                    response.write(char)
            else:
                # Got '' -> Timeout
                if response.getvalue():
                    msg = "Timeout detected, with parcial response: %s" % \
                        pprint.pformat(response.getvalue())
                    logger.warn(msg)
                    raise(CommandTimeout(msg))
                else:
                    raise(CommandTimeout())
        
        response = response.getvalue().strip()
        end = time.time()
        logger.debug("get_next_response() - Got response: '%s' - Took: %.2f secs." % (
            response, (end-start)))
        return response
    
    def send_cmd(self, cmd):
        """
        Sends a command to the arduino. The command is terminated with a 0x00.
        Returns the response as a string.
        
        Raises:
        - CommandTimeout: if a timeout is detected while reading response.
        - InvalidCommand: if the Arduino reported the sent command as invalid.
        """
        logger.debug("send_cmd() called. cmd: '%s'" % cmd)
        
        self.serial_port.write(cmd)
        self.serial_port.write("\n")
        self.serial_port.flush()
        
        response = self.get_next_response() # Raises CommandTimeout
        
        if response == ArduinoProxy.INVALID_CMD:
            raise(InvalidCommand())
        
        return response
    
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    # Digital I/O
    def _pinMode(self): # pylint: disable=C0103,R0201
        return _unindent(12, """
            void _pinMode() {
                int pin = atoi(received_parameters[1]);
                int mode = atoi(received_parameters[2]);
                if(mode != INPUT && mode != OUTPUT) {
                    send_invalid_parameter_response();
                    return;
                }
                // FIXME: validate pin
                pinMode(pin, mode);
                send_ok_response();
            }
        """)
    
    _pinMode.proxy_function = True # pylint: disable=W0612
    
    def pinMode(self, pin, mode): # pylint: disable=C0103
        """
        * ...vast majority of Arduino (Atmega) analog pins, may be configured, and used,
        in exactly the same manner as digital pins.
        * Arduino (Atmega) pins default to inputs: high-impedance state (extremely small demands
        on the circuit)
        * NOTE: Digital pin 13 is harder to use as a digital input than the other digital pins
        because it has an LED and resistor attached to it that's soldered to the board
        * it is a good idea to connect OUTPUT pins to other devices with 470omh or 1k resistors
        """
        # TODO: The analog input pins can be used as digital pins, referred to as A0, A1, etc.
        # FIXME: validate pin and value
        # FIXME: add doc for parameters and exceptions
        if not type(pin) is int or not mode in [ArduinoProxy.INPUT, ArduinoProxy.OUTPUT]:
            raise(InvalidArgument())
        cmd = "_pinMode %d %d" % (pin, mode)
        response = self.send_cmd(cmd) # raises CommandTimeout,InvalidCommand
        
        if response != "OK":
            raise(InvalidResponse("The response wasn't 'OK'. Response: %s" % \
                pprint.pformat(response)))
        
        return response
    
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def _digitalWrite(self): # pylint: disable=C0103,R0201
        return _unindent(12, """
            void _digitalWrite() {
                int pin = atoi(received_parameters[1]);
                int value = atoi(received_parameters[2]);
                
                if(value != HIGH && value != LOW) {
                    send_invalid_parameter_response();
                    return;
                }
                
                digitalWrite(pin, value);
                send_ok_response();
            }
        """)
    
    _digitalWrite.proxy_function = True # pylint: disable=W0612
    
    def digitalWrite(self, pin, value): # pylint: disable=C0103
        # FIXME: validate pin and value
        # FIXME: add doc for parameters and exceptions
        if not type(pin) is int or not value in [ArduinoProxy.LOW, ArduinoProxy.HIGH]:
            raise(InvalidArgument())
        cmd = "_digitalWrite %d %d" % (pin, value)
        response = self.send_cmd(cmd) # raises CommandTimeout,InvalidCommand
        
        if response != "OK":
            raise(InvalidResponse("The response wasn't 'OK'. Response: %s" % \
                pprint.pformat(response)))
        
        return response
    
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def _digitalRead(self): # pylint: disable=C0103,R0201
        return _unindent(12, """
            void _digitalRead() {
                int pin = atoi(received_parameters[1]);
                int value = digitalRead(pin);
                send_int_response(value);
                return;
            }
        """)
    
    _digitalRead.proxy_function = True # pylint: disable=W0612
    
    def digitalRead(self, pin): # pylint: disable=C0103
        """
        * Reads the value from a specified digital pin, either HIGH or LOW.
        
        Parameters:
        - pin: the pin to be read
        
        Raises:
        - InvalidResponse: if the response isn't valid
        """
        # FIXME: validate pin
        # FIXME: add doc for parameters and exceptions
        if not type(pin) is int:
            raise(InvalidArgument())
        cmd = "_digitalRead %d" % (pin)
        response = self.send_cmd(cmd) # raises CommandTimeout,InvalidCommand
        
        try:
            int_response = int(response)
        except ValueError:
            raise(InvalidResponse("The response couldn't be converted to int. Response: %s" % \
                pprint.pformat(response)))
        
        if int_response in [ArduinoProxy.HIGH, ArduinoProxy.LOW]:
            return int_response
        
        raise(InvalidResponse("The response isn't HIGH (%d) nor LOW (%d). Response: %s" % (
            ArduinoProxy.HIGH, ArduinoProxy.LOW, int_response)))
    
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    #Analog I/O
    def analogReference(self): # pylint: disable=C0103
        pass
    
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def _analogRead(self): # pylint: disable=C0103,R0201
        return _unindent(12, """
            void _analogRead() {
                int pin = atoi(received_parameters[1]);
                int value = analogRead(pin);
                send_int_response(value);
                return;
            }
        """)
    
    _analogRead.proxy_function = True # pylint: disable=W0612
    
    def analogRead(self, pin): # pylint: disable=C0103
        """
        * map input voltages between 0 and 5 volts into integer values between 0 and 1023.
        """
        # FIXME: validate pin
        # FIXME: add doc for parameters and exceptions
        if not type(pin) is int:
            raise(InvalidArgument())
        cmd = "_analogRead %d" % (pin)
        response = self.send_cmd(cmd) # raises CommandTimeout,InvalidCommand
        
        try:
            int_response = int(response)
        except ValueError:
            raise(InvalidResponse("The response couldn't be converted to int. Response: %s" % \
                pprint.pformat(response)))
        
        if int_response >= 0 and int_response <= 1023:
            return int_response
        
        raise(InvalidResponse("The response isn't in the valid range of 0-1023. " + \
            "Response: %d" % int_response))
    
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def analogWrite(self): # pylint: disable=C0103
        pass
    
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def _ping(self): # pylint: disable=C0103,R0201
        return _unindent(12, """
            void _ping() {
                Serial.println("PING_OK");
            }
        """)
    
    _ping.proxy_function = True # pylint: disable=W0612
    
    def ping(self): # pylint: disable=C0103
        # FIXME: add doc
        cmd = "_ping"
        response = self.send_cmd(cmd) # raises CommandTimeout,InvalidCommand
        if response != 'PING_OK':
            raise(InvalidResponse("The response to a ping() wasn't 'PING_OK'. Response: %s" %
                pprint.pformat(response)))
        return response
    
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def _connect(self): # pylint: disable=C0103,R0201
        return _unindent(12, """
            void _connect() {
                Serial.println(received_parameters[1]);
            }
        """)
    
    _connect.proxy_function = True # pylint: disable=W0612
    
    def connect(self): # pylint: disable=C0103
        # FIXME: add doc
        random_uuid = str(uuid.uuid4())
        cmd = "_connect %s" % random_uuid
        response = self.send_cmd(cmd) # raises CommandTimeout,InvalidCommand
        
        while response != random_uuid:
            logger.warn("connect(): Ignoring invalid response: %s", pprint.pformat(response))
            # Go for the uuid, or a timeout exception!
            response = self.get_next_response()
        
        return response
    
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def close(self):
        """Closes the serial port."""
        if self.serial_port:
            self.serial_port.close()
