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
import random
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

class ArduinoProxyException(Exception):
    """Base exception"""

class InvalidCommand(ArduinoProxyException):
    """The Arduino reported an error in the command"""
    
    def __init__(self, msg, error_code=None):
        ArduinoProxyException.__init__(self, msg)
        self.error_code = error_code

class InvalidParameter(ArduinoProxyException):
    """The Arduino reported an invalid parameter"""

    def __init__(self, msg, error_param=None):
        ArduinoProxyException.__init__(self, msg)
        self.error_param = error_param

class InvalidResponse(ArduinoProxyException):
    """The response from the Arduino isn't valid."""

class EmptyResponse(ArduinoProxyException):
    """The response from the Arduino was empty."""

class CommandTimeout(ArduinoProxyException):
    """Timeout detected while waiting for Arduino's response."""

class InvalidArgument(ArduinoProxyException):
    """A method was called with invalid argument type or values."""

class UnsupportedCommand(ArduinoProxyException):
    """There is no support for the given command in the Arduino."""

    def __init__(self, msg, error_param=None):
        ArduinoProxyException.__init__(self, msg)
        self.error_param = error_param

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
    
    #define LSBFIRST 0
    #define MSBFIRST 1
    LSBFIRST = 0x00
    MSBFIRST = 0x01
    
    ATTACH_INTERRUPT_MODE_LOW = 'L'
    ATTACH_INTERRUPT_MODE_CHANGE = 'C'
    ATTACH_INTERRUPT_MODE_RISING = 'R'
    ATTACH_INTERRUPT_MODE_FALLING = 'F'
    
    INVALID_CMD = "INVALID_CMD"
    INVALID_PARAMETER = "INVALID_PARAMETER"
    UNSUPPORTED_CMD = "UNSUPPORTED_CMD"
    
    def __init__(self, tty, speed=9600, wait_after_open=3, timeout=5, # pylint: disable=R0913
            call_connect=True):
        # For communicating with the computer, use one of these rates: 300, 1200, 2400, 4800,
        #    9600, 14400, 19200, 28800, 38400, 57600, or 115200.
        logger.debug("Instantiating ArduinoProxy('%s', %d)..." % (tty, speed))
        self.tty = tty
        self.speed = speed
        self.serial_port = None
        self.timeout = timeout
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
    
    def setTimeout(self, new_timeout):
        self.timeout = new_timeout
        self.serial_port.timeout = new_timeout
    
    def get_next_response(self, timeout=None):
        """
        Waits for a response from the serial.
        Raises CommandTimeout if a timeout while reading is detected.
        """
        logger.debug("get_next_response() - waiting for response...")
        start = time.time()
        response = StringIO()
        if timeout is None: # Use default timeout
            if self.serial_port.getTimeout() != self.timeout:
                self.serial_port.timeout = self.timeout
        else: # Use custom timeout
            if self.serial_port.getTimeout() != timeout:
                self.serial_port.timeout = timeout
        
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
        logger.debug("get_next_response() - Got response: '%s' - Took: %.2f secs.",
            response, (end-start))
        return response
    
    def _check_response_for_errors(self, response, cmd):
        splitted = [item for item in response.split() if item]
        if splitted[0] == ArduinoProxy.INVALID_CMD:
            if len(splitted) == 1:
                logger.warn("Received ArduinoProxy.INVALID_CMD, but without error code. " + \
                    "The command was: %s" % pprint.pformat(cmd))
                raise(InvalidCommand("Arduino responded with INVALID_CMD. " + \
                    "The command was: %s" % pprint.pformat(cmd)))
            else:
                raise(InvalidCommand("Arduino responded with INVALID_CMD. " + \
                    "The command was: %s. Error code: %s" % (pprint.pformat(cmd), splitted[1]),
                    error_code=splitted[1]))
        
        if splitted[0] == ArduinoProxy.INVALID_PARAMETER:
            if len(splitted) == 1:
                logger.warn("Received ArduinoProxy.INVALID_PARAMETER, but without error code. " + \
                    "The command was: %s" % pprint.pformat(cmd))
                raise(InvalidParameter("Arduino responded with INVALID_PARAMETER. " + \
                    "The command was: %s" % pprint.pformat(cmd)))
            else:
                raise(InvalidParameter("Arduino responded with INVALID_PARAMETER." + \
                    "The command was: %s. The invalid parameter is %s" % (pprint.pformat(cmd),
                    splitted[1]), error_param=splitted[1]))
        
        if splitted[0] == ArduinoProxy.UNSUPPORTED_CMD:
            raise(UnsupportedCommand("Arduino responded with UNSUPPORTED_CMD." + \
                "The unsupported command is: %s" % splitted[1], error_param=splitted[1]))
    
    def send_cmd(self, cmd, expected_response=None, timeout=None, response_transformer=None):
        """
        Sends a command to the arduino. The command is terminated with a 0x00.
        Returns the response as a string.
        
        Parameters:
        - cmd: the command to send (string)
        - expected_response: the response we expect from the Arduino. If response_transformer is
            not None, the response is first transformed, and then compared to 'expected_response'.
            If expected_response is a list or tuple, check that the response is one of its items.
        - response_transformer: the method to call to transform. Must receive a string (the value
            recieved from the Arduino).
        
        Raises:
        - CommandTimeout: if a timeout is detected while reading response.
        - InvalidCommand: if the Arduino reported the sent command as invalid.
        - InvalidParameter: if the Arduino reported that some parameter was invalid.
        - InvalidResponse: raised when 'expected_response is not None, an
            the response doesn't equals to 'expected_response'.
        """
        logger.debug("send_cmd() called. cmd: '%s'" % cmd)
        
        self.serial_port.write(cmd)
        self.serial_port.write("\n")
        self.serial_port.flush()
        
        while True:
            response = self.get_next_response(timeout=timeout) # Raises CommandTimeout
            if response.startswith('> '):
                logger.info("[DEBUG-TEXT-RECEIVED] %s", pprint.pformat(response))
            else:
                break
        
        self._check_response_for_errors(response, cmd)
        
        transformed_response = None
        if response_transformer is not None: # must transform the response
            try:
                transformed_response = response_transformer(response)
            except BaseException, e:
                raise(InvalidResponse("The response couldn't be transformed. " + \
                    "Response: %s. Exception: %s" % (pprint.pformat(e),
                    pprint.pformat(response))))
        
        if expected_response is not None: # must check the response
            if type(expected_response) not in [list, tuple]:
                # ensure expected_response is a list or tuple, so 'in' works
                expected_response = [expected_response]
            if transformed_response is not None:
                if transformed_response not in expected_response:
                    raise(InvalidResponse(
                        "The response (after transforming) wasn't the expected. " + \
                        "Expected: '%s'. " % pprint.pformat(expected_response) + \
                        "Transformed response: %s. " % pprint.pformat(transformed_response) + \
                        "Original response: %s. " % pprint.pformat(response) \
                    ))
            elif response not in expected_response:
                raise(InvalidResponse(
                    "The response wasn't the expected. " + \
                    "Expected: %s. " % pprint.pformat(expected_response) + \
                    "Response: %s." % pprint.pformat(response) \
                ))
        
        if response_transformer is not None:
            return transformed_response
        else:
            return response
    
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def close(self):
        """Closes the serial port."""
        if self.serial_port:
            self.serial_port.close()

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def get_proxy_functions(self):
        """Returns a list of proxy functions"""
        all_attributes = [ getattr(self, an_attribute_name) for an_attribute_name in dir(self) ]
        proxy_functions = [an_attribute for an_attribute in all_attributes
            if getattr(an_attribute, 'arduino_code', False)]
        return proxy_functions

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    ## HERE STARTS PROXIED FUNCTIONS
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
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
        cmd = "_pMd %d %d" % (pin, mode)
        
        return self.send_cmd(cmd, expected_response="PM_OK")
        # raises CommandTimeout,InvalidCommand,InvalidResponse
    
    pinMode.arduino_function_name = '_pMd'
    pinMode.arduino_code = _unindent(12, """
            void _pMd() {
                int pin = atoi(received_parameters[1]);
                int mode = atoi(received_parameters[2]);
                if(mode != INPUT && mode != OUTPUT) {
                    send_invalid_parameter_response(1);
                    return;
                }
                // FIXME: validate pin
                pinMode(pin, mode);
                send_char_array_response("PM_OK");
            }
        """)
    
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def digitalWrite(self, pin, value): # pylint: disable=C0103
        # FIXME: validate pin and value
        # FIXME: add doc for parameters and exceptions
        if not type(pin) is int or not value in [ArduinoProxy.LOW, ArduinoProxy.HIGH]:
            raise(InvalidArgument())
        cmd = "_dWrt %d %d" % (pin, value)
        return self.send_cmd(cmd, expected_response="DW_OK")
        # raises CommandTimeout,InvalidCommand,InvalidResponse
    
    digitalWrite.arduino_function_name = '_dWrt'
    digitalWrite.arduino_code = _unindent(12, """
            void _dWrt() {
                int pin = atoi(received_parameters[1]);
                int value = atoi(received_parameters[2]);
                
                if(value != HIGH && value != LOW) {
                    send_invalid_parameter_response(1);
                    return;
                }
                
                digitalWrite(pin, value);
                send_char_array_response("DW_OK");
            }
        """)

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
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
        cmd = "_dRd %d" % (pin)
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
    
    digitalRead.arduino_function_name = '_dRd'
    digitalRead.arduino_code = _unindent(12, """
            void _dRd() {
                int pin = atoi(received_parameters[1]);
                int value = digitalRead(pin);
                send_int_response(value);
                return;
            }
        """)
    
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    # TODO: implement analogReference()
    #Analog I/O
    # def analogReference(self): # pylint: disable=C0103
    #     pass
    
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def analogRead(self, pin): # pylint: disable=C0103
        """
        * map input voltages between 0 and 5 volts into integer values between 0 and 1023.
        """
        # FIXME: validate pin
        # FIXME: add doc for parameters and exceptions
        if not type(pin) is int:
            raise(InvalidArgument())
        cmd = "_aRd %d" % (pin)
        response = self.send_cmd(cmd, response_transformer=int) # raises CommandTimeout,InvalidCommand
        
        if response >= 0 and response <= 1023:
            return response
        
        raise(InvalidResponse("The response isn't in the valid range of 0-1023. " + \
            "Response: %d" % response))
    
    analogRead.arduino_function_name = '_aRd'
    analogRead.arduino_code = _unindent(12, """
            void _aRd() {
                int pin = atoi(received_parameters[1]);
                int value = analogRead(pin);
                send_int_response(value);
                return;
            }
        """)
    
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def analogWrite(self, pin, value): # pylint: disable=C0103
        """
        Writes an analog value (PWM wave) to a pin
        """
        # FIXME: validate pin and value
        # FIXME: add doc for parameters and exceptions
        if not type(pin) is int or not type(value) is int or value < 0 or value > 255:
            raise(InvalidArgument())
        cmd = "_aWrt %d %d" % (pin, value)
        
        return self.send_cmd(cmd, expected_response="AW_OK")
        # raises CommandTimeout,InvalidCommand,InvalidResponse
    
    analogWrite.arduino_function_name = '_aWrt'
    analogWrite.arduino_code = _unindent(12, """
            void _aWrt() {
                int pin = atoi(received_parameters[1]);
                int value = atoi(received_parameters[2]);
                
                if(value < 0 || value > 255) {
                    send_invalid_parameter_response(1);
                    return;
                }
                
                analogWrite(pin, value);
                send_char_array_response("AW_OK");
            }
        """)
    
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def ping(self): # pylint: disable=C0103
        # FIXME: add doc
        cmd = "_ping"
        return self.send_cmd(cmd, expected_response="PING_OK")
        # raises CommandTimeout,InvalidCommand,InvalidResponse
    
    ping.arduino_function_name = '_ping'
    ping.arduino_code = _unindent(12, """
            void _ping() {
                send_char_array_response("PING_OK");
            }
        """)
    
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def connect(self): # pylint: disable=C0103
        # FIXME: add doc
        random_str = str(random.randint(0, 10000000))
        cmd = "_cnt %s" % random_str
        response = self.send_cmd(cmd) # raises CommandTimeout,InvalidCommand
        
        while response != random_str:
            logger.warn("connect(): Ignoring invalid response: %s", pprint.pformat(response))
            # Go for the uuid, or a timeout exception!
            response = self.get_next_response()
        
        return response
    
    connect.arduino_function_name = '_cnt'
    connect.arduino_code = _unindent(12, """
            void _cnt() {
                send_char_array_response(received_parameters[1]);
            }
        """)

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def delay(self, value): # pylint: disable=C0103
        """
        http://arduino.cc/en/Reference/Delay
        Pauses the program for the amount of time (in miliseconds) specified as parameter.
        (There are 1000 milliseconds in a second.)

        Parameters:
        - value: how much to pause, in miliseconds.
        """
        if not type(value) is int:
            raise(InvalidArgument("value must be an integer"))
        if not value >= 0:
            raise(InvalidArgument("value must be greater or equals than 0"))
        
        response = self.send_cmd("_dy %d" % value, expected_response="D_OK")
        # raises CommandTimeout,InvalidCommand,InvalidResponse
        
        return response
    
    delay.arduino_function_name = '_dy'
    delay.arduino_code = _unindent(12, """
            void _dy() {
                int value = atoi(received_parameters[1]);
                
                if(value < 0) {
                    send_invalid_parameter_response(0);
                    return;
                }
                
                delay(value);
                send_char_array_response("D_OK");
            }
        """)

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def delayMicroseconds(self, value): # pylint: disable=C0103
        """
        http://arduino.cc/en/Reference/DelayMicroseconds
        Pauses the program for the amount of time (in microseconds) specified as parameter. There
        are a thousand microseconds in a millisecond, and a million microseconds in a second.
        Currently, the largest value that will produce an accurate delay is 16383. This could change
        in future Arduino releases. For delays longer than a few thousand microseconds, you should
        use delay() instead.
        
        Parameters:
        - value: how much to pause, in microseconds.
        """
        if not type(value) is int:
            raise(InvalidArgument("value must be an integer"))
        if not value >= 0:
            raise(InvalidArgument("value must be greater or equals than 0"))
        
        return self.send_cmd("_dMs %d" % value, expected_response="DMS_OK")
        # raises CommandTimeout,InvalidCommand,InvalidResponse
    
    delayMicroseconds.arduino_function_name = '_dMs'
    delayMicroseconds.arduino_code = _unindent(12, """
            void _dMs() {
                int value = atoi(received_parameters[1]);
                
                if(value < 0) {
                    send_invalid_parameter_response(0);
                    return;
                }
                
                delayMicroseconds(value);
                send_char_array_response("DMS_OK");
            }
        """)
    
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def millis(self): # pylint: disable=C0103
        """
        http://arduino.cc/en/Reference/Millis
        Returns the number of milliseconds since the Arduino board began running the current
        program. This number will overflow (go back to zero), after approximately 50 days.
        """
        return self.send_cmd("_ms", response_transformer=int)
        # raises CommandTimeout,InvalidCommand,InvalidResponse
    
    millis.arduino_function_name = '_ms'
    millis.arduino_code = _unindent(12, """
            void _ms() {
                send_debug();
                Serial.println(millis());
            }
        """)

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def micros(self): # pylint: disable=C0103
        """
        http://arduino.cc/en/Reference/Micros
        Returns the number of microseconds since the Arduino board began running the current
        program. This number will overflow (go back to zero), after approximately 70 minutes.
        On 16 MHz Arduino boards (e.g. Duemilanove and Nano), this function has a resolution of
        four microseconds (i.e. the value returned is always a multiple of four). On 8 MHz Arduino
        boards (e.g. the LilyPad), this function has a resolution of eight microseconds.
        Note: there are 1,000 microseconds in a millisecond and 1,000,000 microseconds in a second.
        """
        return self.send_cmd("_mc", response_transformer=int)
        # raises CommandTimeout,InvalidCommand,InvalidResponse
    
    micros.arduino_function_name = '_mc'
    micros.arduino_code = _unindent(12, """
            void _mc() {
                send_debug();
                Serial.println(micros());
            }
        """)

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def watchInterrupt(self, interrupt, mode): # pylint: disable=C0103
        """
        Watch if an interrupt was occured.
        
        Parameters:
        - interrupt: 0 or 1- TODO: Arduino Mega has more than 2 interrupts!
        - mode: one of ATTACH_INTERRUPT_MODE_LOW,ATTACH_INTERRUPT_MODE_CHANGE,
            ATTACH_INTERRUPT_MODE_RISING,ATTACH_INTERRUPT_MODE_FALLING
        """
        if not type(interrupt) is int:
            raise(InvalidArgument("interrupt must be an integer"))
        if interrupt < 0 or interrupt > 1:
            raise(InvalidArgument("interrupt must be between 0 and 1"))
        if not mode in [ArduinoProxy.ATTACH_INTERRUPT_MODE_LOW,
                ArduinoProxy.ATTACH_INTERRUPT_MODE_CHANGE, ArduinoProxy.ATTACH_INTERRUPT_MODE_RISING,
                ArduinoProxy.ATTACH_INTERRUPT_MODE_FALLING]:
            raise(InvalidArgument("invalid mode: %s" % str(mode)))
        
        return self.send_cmd("_wI %d %s" % (interrupt, mode), expected_response="WI_OK")
                                            # raises CommandTimeout,InvalidCommand,InvalidResponse
    
    watchInterrupt.arduino_function_name = '_wI'
    watchInterrupt.arduino_code = _unindent(12, """
            void _wI() {
                int mode;
                if(received_parameters[2][0] == ATTACH_INTERRUPT_MODE_LOW) {
                    mode = LOW;
                } else if(received_parameters[2][0] == ATTACH_INTERRUPT_MODE_CHANGE) {
                    mode = CHANGE;
                } else if(received_parameters[2][0] == ATTACH_INTERRUPT_MODE_RISING) {
                    mode = RISING;
                } else if(received_parameters[2][0] == ATTACH_INTERRUPT_MODE_FALLING) {
                    mode = FALLING;
                } else {
                    send_invalid_parameter_response(1);
                    return;
                }
                int interrupt = atoi(received_parameters[1]);
                if (interrupt == 0) {
                    attachInterrupt(interrupt, set_mark_interrupt_0, mode);
                    send_char_array_response("WI_OK");
                } else if (interrupt == 1) {
                    attachInterrupt(interrupt, set_mark_interrupt_1, mode);
                    send_char_array_response("WI_OK");
                } else {
                    send_invalid_parameter_response(0);
                    return;
                }
            }
        """)

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def getInterruptMark(self, interrupt): # pylint: disable=C0103
        """
        Check if an interrupt was detected.
        Returns:
        - True: if an interrupt was detected. False otherwise.
        """
        if not type(interrupt) is int:
            raise(InvalidArgument("interrupt must be an integer"))
        if interrupt < 0 or interrupt > 1:
            raise(InvalidArgument("interrupt must be between 0 and 1"))
        
        ret = self.send_cmd("_gIM %d" % interrupt,
            expected_response=["GIM_ON", "GIM_OFF"])
            # raises CommandTimeout,InvalidCommand,InvalidResponse
        
        return bool(ret == "GIM_ON")
    
    getInterruptMark.arduino_function_name = '_gIM'
    getInterruptMark.arduino_code = _unindent(12, """
            void _gIM() {
                int interrupt = atoi(received_parameters[1]);
                if (interrupt == 0) {
                    if(check_mark_interrupt_0()) {
                        clear_mark_interrupt_0();
                        send_char_array_response("GIM_ON");
                    } else {
                        send_char_array_response("GIM_OFF");
                    }
                    return;
                } else if (interrupt == 1) {
                    if(check_mark_interrupt_1()) {
                        clear_mark_interrupt_1();
                        send_char_array_response("GIM_ON");
                    } else {
                        send_char_array_response("GIM_OFF");
                    }
                    return;
                } else {
                    send_invalid_parameter_response(0);
                    return;
                }
            }
        """)

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def enableDebug(self): # pylint: disable=C0103
        """
        Enable transmision of debug messages from the Arduino.
        """
        return self.send_cmd("_eD", "ENA")
            # raises CommandTimeout,InvalidCommand,InvalidResponse
    
    enableDebug.arduino_function_name = '_eD'
    enableDebug.arduino_code = _unindent(12, """
            void _eD() {
                debug_enabled = 1;
                send_char_array_response("ENA");
            }
        """)

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def enableDebugToLcd(self): # pylint: disable=C0103
        """
        Enable transmision of debug messages from the Arduino, and show info in the LCD.
        """
        return self.send_cmd("_eDL", "ENA")
            # raises CommandTimeout,InvalidCommand,InvalidResponse
    
    enableDebugToLcd.arduino_function_name = '_eDL'
    enableDebugToLcd.arduino_code = _unindent(12, """
            void _eDL() {
                #if PY_ARDUINO_PROXY_LCD_SUPPORT == 1
                    debug_enabled = 2;
                    send_char_array_response("ENA");
                #else
                    send_unsupported_cmd_response();
                #endif
            }
        """)
    
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def disableDebug(self): # pylint: disable=C0103
        """
        Disable transmision of debug messages from the Arduino.
        """
        return self.send_cmd("_dD", "DIS")
            # raises CommandTimeout,InvalidCommand,InvalidResponse
    
    disableDebug.arduino_function_name = '_dD'
    disableDebug.arduino_code = _unindent(12, """
            void _dD() {
                debug_enabled = 0;
                send_char_array_response("DIS");
            }
        """)

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def lcdWrite(self, message, col, row): # pylint: disable=C0103
        """
        Write a message to the LCD.
        """
        if not type(col) is int:
            raise(InvalidArgument("col must be an integer"))
        if not type(row) is int:
            raise(InvalidArgument("row must be an integer"))
        
        # FIXME: check 'message' type and length
        # FIXME: check parameters
        # FIXME: test detection of invalid parameters

        return self.send_cmd("_lcdW %s %d %d" % (message.replace(' ', '_'), col, row), "LWOK")
            # raises CommandTimeout,InvalidCommand,InvalidResponse
    
    lcdWrite.arduino_function_name = '_lcdW'
    lcdWrite.arduino_code = _unindent(12, """
            void _lcdW() {
                #if PY_ARDUINO_PROXY_LCD_SUPPORT == 1
                    int col = atoi(received_parameters[2]);
                    int row = atoi(received_parameters[3]);
                    lcd.setCursor(col, row);
                    lcd.print(received_parameters[1]);
                    send_char_array_response("LWOK");
                #else
                    send_unsupported_cmd_response();
                #endif
            }
        """)

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def shiftOut(self, dataPin, clockPin, bitOrder, value, set_pin_mode=False): # pylint: disable=C0103
        """
        shiftOut(dataPin, clockPin, bitOrder, value).
        Shifts out a byte of data one bit at a time. Starts from either the most (i.e. the leftmost)
        or least (rightmost) significant bit. Each bit is written in turn to a data pin, after which
        a clock pin is pulsed to indicate that the bit is available.
        """
        if not type(dataPin) is int:
            raise(InvalidArgument("dataPin must be an integer"))
        if not type(clockPin) is int:
            raise(InvalidArgument("clockPin must be an integer"))
        if not type(value) is int:
            raise(InvalidArgument("value must be an integer"))
        if value < 0 or value > 255:
            raise(InvalidArgument("value must be between 0 and 255"))
        if not bitOrder in [ArduinoProxy.LSBFIRST, ArduinoProxy.MSBFIRST]:
            raise(InvalidArgument("bitOrder must be ArduinoProxy.LSBFIRST or " + \
                "ArduinoProxy.MSBFIRST"))
        
        # FIXME: test detection of invalid parameters
        
        if set_pin_mode:
            self.pinMode(dataPin, ArduinoProxy.OUTPUT)
            self.pinMode(clockPin, ArduinoProxy.OUTPUT)
        return self.send_cmd("_sftO %d %d %d %d" % (dataPin, clockPin, bitOrder, value, ), "SOOK")
            # raises CommandTimeout,InvalidCommand,InvalidResponse
    
    shiftOut.arduino_function_name = '_sftO'
    shiftOut.arduino_code = _unindent(12, """
            void _sftO() {
                int dataPin = atoi(received_parameters[1]);
                int clockPin = atoi(received_parameters[2]);
                int bitOrder = atoi(received_parameters[3]);
                int value = atoi(received_parameters[4]);
                shiftOut(dataPin, clockPin, bitOrder, value);
                send_char_array_response("SOOK");
            }
        """)

## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
## EXAMPLE CODE FOR NEW FUNCTIONS
## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
## Replace '_XXXXXXXXXX' and 'newMethodName' as needed.
## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
#    def newMethodName(self):
#        return self.send_cmd("_XXXXXXXXXX", expected_response="OK_RESPONSE")
#    
#    newMethodName.arduino_function_name = '_XXXXXXXXXX'
#    newMethodName.arduino_code = """
#            void _XXXXXXXXXX() {
#                // here
#                // goes
#                // Arduino
#                // code
#                
#                // Send 'OK' to the PC.
#                send_char_array_response("OK_RESPONSE");
#            }
#        """

## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
## If the Arduino may take some time to respond, you can
##  use a larger timeout. Example: with timeout=60 we will
##  wait for 1 minute.
## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
#    def newMethodName(self):
#        return self.send_cmd("_XXXXXXXXXX", expected_response="OK_RESPONSE", timeout=60)
#    
#    newMethodName.arduino_function_name = '_XXXXXXXXXX'
#    newMethodName.arduino_code = """
#            void _XXXXXXXXXX() {
#                // here
#                // goes
#                // Arduino
#                // code
#                
#                // Send 'OK' to the PC.
#                send_char_array_response("OK_RESPONSE");
#            }
#        """
