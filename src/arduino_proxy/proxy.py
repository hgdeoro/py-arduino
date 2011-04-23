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

class InvalidCommand(Exception):
    """
    The Arduino reported an error in the command
    """
    pass

class InvalidResponse(Exception):
    """
    The response from the Arduino isn't valid.
    """
    pass

class EmptyResponse(Exception):
    """
    The response from the Arduino was empty.
    """
    pass

class CommandTimeout(Exception):
    """
    Timeout detected while waiting for Arduino's response.
    """
    pass

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ArduinoProxy(object):
    
    INPUT = "I"
    OUTPUT = "O"
    
    HIGH = "H"
    LOW = "L"
    
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
    
    def _setup(self):
        return _unindent(8, """
        
        #define PIN_ONBOARD_LED 13  // DIGITAL
        #define PIN_START_BUTTON 12 // DIGITAL
        
        char lastCmd[128]; // buffer size of Serial
        
        void wait_start() {
            digitalWrite(PIN_START_BUTTON, HIGH); // turn on pullup resistors
            int state = HIGH;
            while(digitalRead(PIN_START_BUTTON) == HIGH) {
                digitalWrite(PIN_ONBOARD_LED, state); // turn the onboard led ON/OFF
                state = !state;
                delay(100);
            }
            digitalWrite(PIN_ONBOARD_LED, HIGH); // turn the onboard led ON
        }
        
        void setup() {
            // Pin 13 has an LED connected on most Arduino boards.
            pinMode(PIN_ONBOARD_LED, OUTPUT);
            pinMode(PIN_START_BUTTON, INPUT);

            wait_start();
        
            Serial.begin(%(speed)d);
        }
        
        void readCmd() {
            int incomingByte = -1;
            int pos = 0;
            
            while (pos < 127) {
                incomingByte = Serial.read();
                if(incomingByte == -1) {
                    if(pos == 0)
                        delay(10);
                    continue;
                }
                // "\\n" == 10
                if(incomingByte == 10) {
                    lastCmd[pos] = 0x00;
                    return;
                }
                lastCmd[pos++] = incomingByte;
            }
            
            if(pos == 127)
                lastCmd[pos] = 0x00;
        }

        void sendInvalidCmdResponse() {
            Serial.println("%(INVALID_CMD)s");
        }
        
        void sendOkResponse() {
            Serial.println("OK");
        }
        
        void sendPingOkResponse() {
            Serial.println("PING_OK");
        }
        
        void sendStringResponse(String the_string) {
            Serial.println(the_string);
        }
        
        int stringToInt(String str) {
            char buff[str.length() + 1];
            str.toCharArray(buff, (str.length() + 1));
            return atoi(buff); 
        }
        
        void sendIntResponse(int value) {
            Serial.println(value, DEC);
        }
        
        void sendConnectOkResponse(String cmd) {
            int index_of_uuid = cmd.indexOf(' ');
            String uuid = cmd.substring(index_of_uuid);
            sendStringResponse(uuid);
        }
        """ % {
            'speed': self.speed, 
            'INVALID_CMD': ArduinoProxy.INVALID_CMD, 
        })
    
    _setup.include_in_pde = True # pylint: disable=W0612
    _setup.proxy_function = False # pylint: disable=W0612
    
    def getNextResponse(self):
        """
        Waits for a response from the serial.
        Raises CommandTimeout if a timeout while reading is detected.
        """
        logger.debug("getNextResponse() - waiting for response...")
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
        logger.debug("sendCmd() - Got response: '%s' - Took: %.2f secs." % (response, (end-start)))
        return response
    
    def sendCmd(self, cmd): # pylint: disable=C0103
        """
        Sends a command to the arduino. The command is terminated with a 0x00.
        Returns the response as a string.
        
        Raises:
        - CommandTimeout: if a timeout is detected while reading response.
        """
        logger.debug("sendCmd() called. cmd: '%s'" % cmd)
        
        self.serial_port.write(cmd)
        self.serial_port.write("\n")
        self.serial_port.flush()
        
        response = self.getNextResponse() # Raises CommandTimeout
        
        if response == ArduinoProxy.INVALID_CMD:
            raise(InvalidCommand())
        
        return response
    
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    # Digital I/O
    def _pinMode(self): # pylint: disable=C0103,R0201
        return _unindent(12, """
            void _pinMode(String cmd) {
                if(!cmd.startsWith("%(method)s")) {
                    return;
                }
                int index_of_pin = cmd.indexOf(' ');
                int index_of_mode = cmd.indexOf(' ', index_of_pin+1);
                String pin = cmd.substring(index_of_pin, index_of_mode);
                String mode = cmd.substring(index_of_mode);
                if(mode.equals("%(INPUT)s")) {
                    pinMode(stringToInt(pin), INPUT);
                    sendOkResponse();
                    return;
                }
                if(mode.equals("%(OUTPUT)s")) {
                    pinMode(stringToInt(pin), OUTPUT);
                    sendOkResponse();
                    return;
                }
                sendInvalidCmdResponse();
            }
        """ % {
        'method': '_pinMode', 
        'INPUT': ArduinoProxy.INPUT, 
        'OUTPUT': ArduinoProxy.OUTPUT, 
        })
    
    _pinMode.include_in_pde = True # pylint: disable=W0612
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
        
        TODO: The analog input pins can be used as digital pins, referred to as A0, A1, etc.
        """
        cmd = "_pinMode %d %s" % (pin, mode)
        ret = self.sendCmd(cmd)
        return ret
    
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def _digitalWrite(self): # pylint: disable=C0103,R0201
        return _unindent(12, """
            void _digitalWrite(String cmd) {
                if(!cmd.startsWith("%(method)s")) {
                    return;
                }
                int index_of_pin = cmd.indexOf(' ');
                int index_of_value = cmd.indexOf(' ', index_of_pin+1);
                String pin = cmd.substring(index_of_pin, index_of_value);
                String value = cmd.substring(index_of_value);
                if(value.equals("%(HIGH)s")) {
                    digitalWrite(stringToInt(pin), HIGH);
                    sendOkResponse();
                    return;
                }
                if(value.equals("%(LOW)s")) {
                    digitalWrite(stringToInt(pin), LOW);
                    sendOkResponse();
                    return;
                }
                sendInvalidCmdResponse();
            }
        """ % {
        'method': '_digitalWrite', 
        'HIGH': ArduinoProxy.HIGH, 
        'LOW': ArduinoProxy.LOW, 
        })
    
    _digitalWrite.include_in_pde = True # pylint: disable=W0612
    _digitalWrite.proxy_function = True # pylint: disable=W0612
    
    def digitalWrite(self, pin, value): # pylint: disable=C0103
        # FIXME: validate pin and value
        cmd = "_digitalWrite %d %s" % (pin, value)
        ret = self.sendCmd(cmd)
        return ret
    
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def digitalRead(self): # pylint: disable=C0103
        pass
    
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    #Analog I/O
    def analogReference(self): # pylint: disable=C0103
        pass
    
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def _analogRead(self): # pylint: disable=C0103,R0201
        return _unindent(12, """
            void _analogRead(String cmd) {
                if(!cmd.startsWith("%(method)s")) {
                    return;
                }
                int index_of_pin = cmd.indexOf(' ');
                String pin = cmd.substring(index_of_pin);
                int value = analogRead(stringToInt(pin));
                sendIntResponse(value);
                return;
            }
        """ % {
        'method': '_analogRead', 
    })
    
    _analogRead.include_in_pde = True # pylint: disable=W0612
    _analogRead.proxy_function = True # pylint: disable=W0612
    
    def analogRead(self, pin): # pylint: disable=C0103
        """
        * map input voltages between 0 and 5 volts into integer values between 0 and 1023.
        """
        cmd = "_analogRead %d" % (pin)
        ret = self.sendCmd(cmd)
        return ret
    
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def analogWrite(self): # pylint: disable=C0103
        pass
    
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def _ping(self): # pylint: disable=C0103,R0201
        return _unindent(12, """
            void _ping(String cmd) {
                if(!cmd.startsWith("%(method)s")) {
                    return;
                }
                sendPingOkResponse();
            }
        """ % {
        'method': '_ping', 
        })
    
    _ping.include_in_pde = True # pylint: disable=W0612
    _ping.proxy_function = True # pylint: disable=W0612
    
    def ping(self): # pylint: disable=C0103
        # FIXME: validate pin and value
        cmd = "_ping"
        ret = self.sendCmd(cmd)
        if ret != 'PING_OK':
            raise(InvalidResponse("The response to a ping() should be an 'PING_OK', not '%s'" %
                ret))
        return ret
    
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def _connect(self): # pylint: disable=C0103,R0201
        return _unindent(12, """
            void _connect(String cmd) {
                if(!cmd.startsWith("%(method)s")) {
                    return;
                }
                sendConnectOkResponse(cmd);
            }
        """ % {
        'method': '_connect', 
        })
    
    _connect.include_in_pde = True # pylint: disable=W0612
    _connect.proxy_function = True # pylint: disable=W0612
    
    def connect(self): # pylint: disable=C0103
        # FIXME: validate pin and value
        random_uuid = str(uuid.uuid4())
        cmd = "_connect %s" % random_uuid
        ret = self.sendCmd(cmd)
        
        while ret != random_uuid:
            logger.warn("connect(): Ignoring invalid response: %s", pprint.pformat(ret))
            # Go for the uuid, or a timeout exception!
            ret = self.getNextResponse()
        
        return ret
    
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def close(self):
        if self.serial_port:
            self.serial_port.close()

def main():
    proxy = ArduinoProxy('')

    print _unindent(8, """
        /*
         * THIS FILE IS GENERATED AUTOMATICALLI WITH generate-pde.sh
         * WHICH IS PART OF THE PROJECT "PyArduinoProxy"
         */
    """)
    
    # All this functions have 'include_in_pde' == True
    pde_functions = [getattr(proxy, a_function) for a_function in dir(proxy)
        if getattr(getattr(proxy, a_function), 'include_in_pde', None) is True]
    
    # First functions that have 'proxy_function' == False
    for function in [a_function for a_function in pde_functions
            if getattr(a_function, 'proxy_function', None) is False]:
        print function()
    
    # Now the real, interesting functions...
    for function in [a_function for a_function in pde_functions
            if getattr(a_function, 'proxy_function', None) is True]:
        print function()
    
    # Now, generate the loop()
    print "void loop() {"
    print "    readCmd();"
    
    for function in [a_function for a_function in pde_functions
            if getattr(a_function, 'proxy_function', None) is True]:
        print "    " + function.__name__ + "(String(lastCmd));"
    print "}"

if __name__ == '__main__':
    main()
