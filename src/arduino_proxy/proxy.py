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

# pylint: disable=C0302

# TODO: _unindent() could be a annotation

import logging
import math
import pprint
import random
import serial
import time

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

class WrappedBoolean(object):
    """Wraps a boolean, to emulate passing variables by reference"""
    
    def __init__(self, value):
        assert value is True or value is False
        self._value = value
    
    def setTrue(self):
        self._value = True
    
    def setFalse(self):
        self._value = False
    
    def get(self):
        return self._value

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ArduinoProxyException(Exception):
    """Base class for all the exception raised in the project."""

class InvalidCommand(ArduinoProxyException):
    """
    Raised when the Arduino reported an error in the command.
    """
    
    def __init__(self, msg, error_code=None):
        ArduinoProxyException.__init__(self, msg)
        self.error_code = error_code

class InvalidParameter(ArduinoProxyException):
    """
    Raised when the Arduino reported an invalid parameter.
    """

    def __init__(self, msg, error_param=None):
        ArduinoProxyException.__init__(self, msg)
        self.error_param = error_param

class InvalidResponse(ArduinoProxyException):
    """
    Raised when the response from the Arduino wasn't valid.
    """

class EmptyResponse(ArduinoProxyException):
    """
    Raised when the response from the Arduino was empty.
    """

class CommandTimeout(ArduinoProxyException):
    """
    Raised when a timeout occurs while waiting for Arduino's response.
    """

class InvalidArgument(ArduinoProxyException):
    """
    Raised when a method was called with invalid argument type or values.
    This is detected in Python, and thus no data was sent to the Arduino.
    """

class UnsupportedCommand(ArduinoProxyException):
    """
    Raised when there is no support for the given command in the Arduino.
    
    Raised when lcdWrite() is used, but the uploaded program to the Arduino wans't generated with
    support for LCD. This means that the command is valid, but the program in the Arduino lacks
    the functionality to run it.
    """

    def __init__(self, msg, error_param=None):
        ArduinoProxyException.__init__(self, msg)
        self.error_param = error_param

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ArduinoProxy(object): # pylint: disable=R0904
    """
    Proxy class for accessing Arduino.
    """
    
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
    
    @classmethod
    def create_emulator(cls, initial_input_buffer_contents=None):
        # We use '***ARDUINO_EMULATOR***' to let ArduinoProxy.__init__() known
        # that the setup of the instace will be done HERE .
        
        #    proxy.serial_port = SerialConnectionMock()
        #    proxy.emulator = ArduinoEmulator(self.serial_port.get_other_side())
        #    proxy.emulator.start()
        
        from arduino_proxy.emulator import SerialConnectionMock, ArduinoEmulator
        
        proxy = cls(tty='***ARDUINO_EMULATOR***', wait_after_open=0, call_validate_connection=False)
        if initial_input_buffer_contents:
            proxy.serial_port = SerialConnectionMock(
                initial_in_buffer_contents=initial_input_buffer_contents)
        else:
            proxy.serial_port = SerialConnectionMock()
        proxy.emulator = ArduinoEmulator(proxy.serial_port.get_other_side())
        proxy.emulator.start()
        proxy.validateConnection()
        return proxy
    
    def __init__(self, tty, speed=9600, wait_after_open=3, timeout=5, # pylint: disable=R0913
            call_validate_connection=True):
        """
        
        Creates a proxy instance, using the serial port specified with 'tty'.
        
        If call_validate_connection is true, a call to validateConnection() is done, to ensures
        the created instance could communicate to Arduino after established the serial connection.
        
        Parameters:
            - speed: serial port speed.
            - wait_after_open: this is needed in Ubuntu, because the Arduino resets itself when connecting.
            - timeout: default timeout (in seconds). Configure how many seconds we wait for a response.
            - call_validate_connection: call validateConnection() after opening the port.
        """
        # For communicating with the computer, use one of these rates: 300, 1200, 2400, 4800,
        #    9600, 14400, 19200, 28800, 38400, 57600, or 115200.
        logger.debug("Instantiating ArduinoProxy('%s', %d)..." % (tty, speed))
        self.tty = tty
        self.speed = speed
        self.serial_port = None
        self.timeout = timeout
        self.emulator = None
        if tty == 'ARDUINO_EMULATOR':
            # Creating emulator from ArduinoProxy constructor
            from arduino_proxy.emulator import SerialConnectionMock, ArduinoEmulator
            logger.debug("Creating EMULATOR instance")
            self.serial_port = SerialConnectionMock()
            self.emulator = ArduinoEmulator(self.serial_port.get_other_side())
            self.emulator.start()
        elif tty == '***ARDUINO_EMULATOR***':
            # Creating emulator from ArduinoProxy.create_emulator()
            # The setup is done by ArduinoProxy.create_emulator()
            logger.debug("Creating EMULATOR instance")
            self.tty = tty = 'ARDUINO_EMULATOR'
        else:
            self.emulator = None
            logger.debug("Opening serial port %s...", tty)
            self.serial_port = serial.Serial(port=tty, baudrate=speed, bytesize=8, parity='N',
                stopbits=1, timeout=timeout)
            # self.serial_port.open() - The port is opened when the instance is created!
            # This has no efect on Linux, but raises an exception on other os.
            if wait_after_open > 0:
                logger.debug("Open OK. Now waiting for Arduino's reset")
                time.sleep(wait_after_open)
        
        if call_validate_connection:
            self.validateConnection()
        logger.debug("Done.")

    def _validate_analog_pin(self, pin, pin_name='pin'): # pylint: disable=R0201
        # FIXME: validate pin value (depends on the model of Arduino)
        if not type(pin) is int:
            raise(InvalidArgument("%s must be an int" % pin_name))
        if pin < 0:
            raise(InvalidArgument("%s must be greater or equals to 0" % pin_name))

    def _validate_digital_pin(self, pin, pin_name='pin'): # pylint: disable=R0201
        # FIXME: validate pin value (depends on the model of Arduino)
        # TODO: Remember: all analog pins works as digital pins.
        if not type(pin) is int:
            raise(InvalidArgument("%s must be an int" % pin_name))
        if pin < 0:
            raise(InvalidArgument("%s must be greater or equals to 0" % pin_name))

    def setTimeout(self, new_timeout): # pylint: disable=C0103
        """
        Changes the timeout (in seconds).
        """
        self.timeout = new_timeout
        self.serial_port.timeout = new_timeout
    
    def get_next_response(self, timeout=None):
        """
        Note: this is a **low level** method. The only situation you may need to call this method
        is if you are creating new methods.
        
        Waits for a response from the serial connection.
        
        Parameters:
            - timeout (int): timeout in seconds to use (instead of the configured for this instance of ArduinoProxy).
        
        Raises:
            - CommandTimeout if a timeout while reading is detected.
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
        logger.debug("get_next_response() - Got response: %s - Took: %.2f secs.",
            pprint.pformat(response), (end-start))
        return response
    
    def _check_response_for_errors(self, response, cmd): # pylint: disable=R0201
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
    
    #    def start_streaming(self, cmd, streamEndMark, timeout=None):
    #        """
    #        Note: this is a **low level** method. The only situation you may need to call this method
    #        is if you are creating new methods.
    #        
    #        Streaming: streamEndMark is set, the command is sent and the responses are read until
    #        we get string specified by 'streamEndMark'.
    #        
    #        In each iteration, a (response, continue_streaming) is running.
    #        **response** is the received response, **continue_streaming** is a boolean wrapper to
    #        stop the streaming, using continue_streaming.setFalse().
    #        """
    #        
    #        # FIXME: streaming: check this implementation!
    #        # FIXME: streaming: do the transmation, check errors, etc!
    #        
    #        logger.debug("start_streaming() called. cmd: %r. streamEndMark: %r", cmd, streamEndMark)
    #        
    #        self.serial_port.write(cmd)
    #        self.serial_port.write("\n")
    #        self.serial_port.flush()
    #        
    #        continue_streaming = WrappedBoolean(True)
    #        response = self.get_next_response(timeout=timeout) # Raises CommandTimeout
    #        while response != streamEndMark:
    #            if response.startswith('> '):
    #                logger.info("[DEBUG-TEXT-RECEIVED] %s", pprint.pformat(response))
    #                continue
    #            yield response, continue_streaming
    #            if not continue_streaming.get():
    #                self.serial_port.write("_ping")
    #                self.serial_port.write("\n")
    #                self.serial_port.flush()
    #                continue_streaming.setTrue()
    #            response = self.get_next_response(timeout=timeout) # Raises CommandTimeout
    
    def send_cmd(self, cmd, expected_response=None, timeout=None, response_transformer=None):
        """
        Note: this is a **low level** method. The only situation you may need to call this method
        is if you are creating new methods.
        
        Sends a command to the Arduino. The command is terminated with a 0x00.
        Returns the response as a string.
        
        Parameters:
            - cmd: the command to send (string)
            - expected_response: the response we expect from the Arduino. If response_transformer is
                not None, the response is first transformed, and then compared to 'expected_response'.
                If expected_response is a list or tuple, check that the response is one of its items.
            - response_transformer: the method to call to transform. Must receive a string (the
                valuerecieved from the Arduino).
            - timeout (int): timeout in seconds to use (instead of the configured for this instance of ArduinoProxy).
        
        Raises:
            - CommandTimeout: if a timeout is detected while reading response.
            - InvalidCommand: if the Arduino reported the sent command as invalid.
            - InvalidParameter: if the Arduino reported that some parameter was invalid.
            - InvalidResponse: raised when 'expected_response is not None, an the response doesn't equals to 'expected_response'.
            - UnsupportedCommand: if the Arduino reported that the command isn't supported.
        """
        logger.debug("send_cmd() called. cmd: '%s'", cmd)
        
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
            except BaseException, exception:
                raise(InvalidResponse("The response couldn't be transformed. " + \
                    "Response: %s. Exception: %s" % (pprint.pformat(exception),
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
        """Closes the connection to the Arduino."""
        if self.emulator:
            self.emulator.stop_running()
            logger.info("Running emulator... Will join the threads...")
            self.emulator.join()
            logger.info("Threads joined OK.")
        else:
            if self.serial_port:
                self.serial_port.close()
    
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def get_proxy_functions(self):
        """
        Returns a list of proxy functions. This is used internally to generate the sketch files.
        """
        all_attributes = [ getattr(self, an_attribute_name) for an_attribute_name in dir(self) ]
        proxy_functions = [an_attribute for an_attribute in all_attributes
            if getattr(an_attribute, 'arduino_code', False)]
        return proxy_functions

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    ## HERE STARTS PROXIED FUNCTIONS
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def pinMode(self, pin, mode): # pylint: disable=C0103
        """
        Proxy function for Arduino's **pinMode()**.
        
        Configures the specified pin to behave either as an input or an output.
        
        See: http://arduino.cc/en/Reference/PinMode and
        http://arduino.cc/en/Tutorial/DigitalPins
        
        Parameters:
            - pin (int): pin to configure
            - mode: ArduinoProxy.INPUT or ArduinoProxy.OUTPUT
        """
        # TODO: The analog input pins can be used as digital pins, referred to as A0, A1, etc.
        # FIXME: validate pin and value
        # FIXME: add doc for parameters and exceptions
        self._validate_digital_pin(pin)
        if not mode in [ArduinoProxy.INPUT, ArduinoProxy.OUTPUT]:
            raise(InvalidArgument())
        cmd = "_pMd\t%d\t%d" % (pin, mode)
        
        return self.send_cmd(cmd, expected_response="PM_OK")
        # raises CommandTimeout,InvalidCommand,InvalidResponse
    
    pinMode.arduino_function_name = '_pMd'
    pinMode.arduino_code = _unindent(12, """
            void _pMd() {
                int pin = atoi(received_parameters[1]);
                int mode = atoi(received_parameters[2]);
                if(mode != INPUT && mode != OUTPUT) {
                    send_invalid_parameter_response(1); // received_parameters[2]
                    return;
                }
                // FIXME: validate pin
                pinMode(pin, mode);
                send_char_array_response("PM_OK");
            }
        """)
    
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def digitalWrite(self, pin, value): # pylint: disable=C0103
        """
        Proxy function for Arduino's **digitalWrite()**.
        Write a HIGH or a LOW value to a digital pin.
        
        See: http://arduino.cc/en/Reference/DigitalWrite
        
        Parameters:
            - pin (int): pin to write
            - value (ArduinoProxy.LOW or ArduinoProxy.HIGH): value to write
        """
        # FIXME: validate pin and value
        # FIXME: add doc for parameters and exceptions
        self._validate_digital_pin(pin)
        if not value in [ArduinoProxy.LOW, ArduinoProxy.HIGH]:
            raise(InvalidArgument("Invalid value for 'value' parameter."))
        cmd = "_dWrt\t%d\t%d" % (pin, value)
        return self.send_cmd(cmd, expected_response="DW_OK")
        # raises CommandTimeout,InvalidCommand,InvalidResponse
    
    digitalWrite.arduino_function_name = '_dWrt'
    digitalWrite.arduino_code = _unindent(12, """
            void _dWrt() {
                int pin = atoi(received_parameters[1]);
                int value = atoi(received_parameters[2]);
                
                if(value != HIGH && value != LOW) {
                    send_invalid_parameter_response(1); // received_parameters[2]
                    return;
                }
                
                digitalWrite(pin, value);
                send_char_array_response("DW_OK");
            }
        """)

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def digitalRead(self, pin): # pylint: disable=C0103
        """
        Proxy function for Arduino's **digitalRead()**.
        Reads the value from a specified digital pin, either HIGH or LOW.
        
        See: http://arduino.cc/en/Reference/DigitalRead
        
        Parameters:
            - pin (int): digital pin to read
        
        Returns:
            - Either ArduinoProxy.HIGH or ArduinoProxy.LOW
        """
        # FIXME: add doc for exceptions
        self._validate_digital_pin(pin)
        cmd = "_dRd\t%d" % (pin)
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
        Proxy function for Arduino's **analogRead()**.
        Reads the value from the specified analog pin.
        
        See: http://arduino.cc/en/Reference/AnalogRead
        
        Parameters:
            - pin (integer): analog pin to read.
        
        Returns: (int)
            - analog value (0 to 1023)
        """
        # FIXME: add doc for exceptions
        self._validate_analog_pin(pin)
        cmd = "_aRd\t%d" % (pin)
        response = self.send_cmd(cmd, response_transformer=int)
        
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
        Proxy function for Arduino's **analogWrite()**.
        Writes an analog value (PWM wave) to a pin
        
        See: http://arduino.cc/en/Reference/AnalogWrite
        
        Parameters:
            - pin (integer): pin to write
            - value (integer): value to write, 0 to 255.
        """
        # FIXME: validate pin
        # FIXME: add doc for exceptions
        if not type(pin) is int or not type(value) is int or value < 0 or value > 255:
            raise(InvalidArgument())
        cmd = "_aWrt\t%d\t%d" % (pin, value)
        
        return self.send_cmd(cmd, expected_response="AW_OK")
        # raises CommandTimeout,InvalidCommand,InvalidResponse
    
    analogWrite.arduino_function_name = '_aWrt'
    analogWrite.arduino_code = _unindent(12, """
            void _aWrt() {
                int pin = atoi(received_parameters[1]);
                int value = atoi(received_parameters[2]);
                
                if(value < 0 || value > 255) {
                    send_invalid_parameter_response(1); // received_parameters[2]
                    return;
                }
                
                analogWrite(pin, value);
                send_char_array_response("AW_OK");
            }
        """)
    
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    ## CONNECTION TESTING FUNCTIONS
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def ping(self): # pylint: disable=C0103
        """
        Sends a 'ping' to the Arduino. May be used to check if the connection is alive.
        """
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
    
    def validateConnection(self): # pylint: disable=C0103
        """
        Asserts that the current connection is valid, discarding any existing information in the 
        buffer of the serial connection.
        
        This method must be called to continue using a proxy instance after an error, specially
        on CommandTimeout errors (otherwise, if not called, the response for the timed out command
        will be read as a response of subsequent commands).
        
        Example:
        * (1a) Python send 'PING'
        * (1b) Arduino responds 'PING_OK'
        * (1c) Python reads 'PING_OK', everything works as expected
        * (2a) Python send 'PING'
        * (2b) Arduino is busy, and after 3 seconds responds with 'PING_OK'
        * (2c) Python detects a timeout, and raises CommandTimeout
        * (3a) Python send 'READ DIGITAL PIN 1'
        * (3b) Arduino responds 'HIGH'
        * (3c) Python reads the previous response 'PING_OK': ERROR!
        
        This can be solved calling :func:`validateConnection` after (2c), to discard
        any 'old' response.
        
        """
        # FIXME: add doc
        random_str = str(random.randint(0, 10000000))
        cmd = "_vCnt\t%s" % random_str
        response = self.send_cmd(cmd) # raises CommandTimeout,InvalidCommand
        
        while response != random_str:
            logger.warn("validateConnection(): Ignoring invalid response: %s",
                pprint.pformat(response))
            # Go for the string, or a timeout exception!
            response = self.get_next_response()
        
        return response
    
    validateConnection.arduino_function_name = '_vCnt'
    validateConnection.arduino_code = _unindent(12, """
            void _vCnt() {
                send_char_array_response(received_parameters[1]);
            }
        """)

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    ## TIME RELATED FUNCTIONS
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def delay(self, value): # pylint: disable=C0103
        """
        Proxy function for Arduino's **delay()**.
        Pauses the program for the amount of time (in miliseconds) specified as parameter.
        (There are 1000 milliseconds in a second.)
        
        If the delay is greater than the default timeout of the serial connection, the timeout
        is automatically increased to avoid CommandTimeout.

        See: http://arduino.cc/en/Reference/Delay

        Parameters:
            - value (int): how many miliseconds to pause.
        """
        if not type(value) is int:
            raise(InvalidArgument("value must be an integer"))
        if not value >= 0:
            raise(InvalidArgument("value must be greater or equals than 0"))
        
        delay_in_seconds = math.ceil(value/1000.0)
        if self.timeout > delay_in_seconds:
            response = self.send_cmd("_dy\t%d" % value, expected_response="D_OK")
            # raises CommandTimeout,InvalidCommand,InvalidResponse
        else:
            response = self.send_cmd("_dy\t%d" % value, expected_response="D_OK",
                timeout=(delay_in_seconds+1))
            # raises CommandTimeout,InvalidCommand,InvalidResponse
        return response
    
    delay.arduino_function_name = '_dy'
    delay.arduino_code = _unindent(12, """
            void _dy() {
                int value = atoi(received_parameters[1]);
                
                if(value < 0) {
                    send_invalid_parameter_response(0); // received_parameters[1]
                    return;
                }
                
                delay(value);
                send_char_array_response("D_OK");
            }
        """)

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def delayMicroseconds(self, value): # pylint: disable=C0103
        """
        Proxy function for Arduino's **delayMicroseconds()**.
        Pauses the program for the amount of time (in microseconds) specified as parameter. There
        are a thousand microseconds in a millisecond, and a million microseconds in a second.
        
        If the delay is greater than the default timeout of the serial connection, the timeout
        is automatically increased to avoid CommandTimeout.
        
        See: http://arduino.cc/en/Reference/DelayMicroseconds
        
        Parameters:
            - value (int): how many microseconds to pause.
        """
        if not type(value) is int:
            raise(InvalidArgument("value must be an integer"))
        if not value >= 0:
            raise(InvalidArgument("value must be greater or equals than 0"))
        
        delay_in_seconds = math.ceil(value/1000000.0)
        if self.timeout > delay_in_seconds:
            return self.send_cmd("_dMs\t%d" % value, expected_response="DMS_OK")
            # raises CommandTimeout,InvalidCommand,InvalidResponse
        else:
            return self.send_cmd("_dMs\t%d" % value, expected_response="DMS_OK",
                timeout=(delay_in_seconds+1))
            # raises CommandTimeout,InvalidCommand,InvalidResponse
    
    delayMicroseconds.arduino_function_name = '_dMs'
    delayMicroseconds.arduino_code = _unindent(12, """
            void _dMs() {
                int value = atoi(received_parameters[1]);
                
                if(value < 0) {
                    send_invalid_parameter_response(0); // received_parameters[1]
                    return;
                }
                
                delayMicroseconds(value);
                send_char_array_response("DMS_OK");
            }
        """)
    
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def millis(self): # pylint: disable=C0103
        """
        Proxy function for Arduino's **millis()**.
        Returns the number of milliseconds since the Arduino board began running the
        current program.
        
        See: http://arduino.cc/en/Reference/Millis
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
        Proxy function for Arduino's **micros()**.
        
        Returns the number of microseconds since the Arduino board began running the current
        program.
        
        See: http://arduino.cc/en/Reference/Micros
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
    ## INTERRUPT RELATED FUNCTIONS
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def watchInterrupt(self, interrupt, mode): # pylint: disable=C0103
        """
        Begin to watch if an interrupt occurs. Use :func:`getInterruptMark` to check if an interrupt
        actually occured.
        
        Parameters:
            - interrupt: 0 or 1
            - mode: one of ATTACH_INTERRUPT_MODE_LOW,ATTACH_INTERRUPT_MODE_CHANGE,
                ATTACH_INTERRUPT_MODE_RISING,ATTACH_INTERRUPT_MODE_FALLING
        """
        # TODO: Arduino Mega has more than 2 interrupts!
        if not type(interrupt) is int:
            raise(InvalidArgument("interrupt must be an integer"))
        if interrupt < 0 or interrupt > 1:
            raise(InvalidArgument("interrupt must be between 0 and 1"))
        if not mode in [ArduinoProxy.ATTACH_INTERRUPT_MODE_LOW,
                ArduinoProxy.ATTACH_INTERRUPT_MODE_CHANGE,
                ArduinoProxy.ATTACH_INTERRUPT_MODE_RISING,
                ArduinoProxy.ATTACH_INTERRUPT_MODE_FALLING]:
            raise(InvalidArgument("invalid mode: %s" % str(mode)))
        
        return self.send_cmd("_wI\t%d\t%s" % (interrupt, mode), expected_response="WI_OK")
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
                    send_invalid_parameter_response(1); // received_parameters[2]
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
                    send_invalid_parameter_response(0); // received_parameters[1]
                    return;
                }
            }
        """)

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def getInterruptMark(self, interrupt): # pylint: disable=C0103
        """
        Check if an interrupt was detected on the Arduino.
        If an interrupt has ocurred, the 'mark' in the Arduino is cleared, so you can call 
        :func:`getInterruptMark` again, to check if another interrupt occurred.
        
        :func:`watchInterrupt` must be called before :func:`getInterruptMark`.
        
        Parameters:
            - interrupt (int): interrupt number to check.
        
        Returns:
            - True: if an interrupt was detected. False otherwise.
        """
        if not type(interrupt) is int:
            raise(InvalidArgument("interrupt must be an integer"))
        if interrupt < 0 or interrupt > 1:
            raise(InvalidArgument("interrupt must be between 0 and 1"))
        
        ret = self.send_cmd("_gIM\t%d" % interrupt,
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
                    send_invalid_parameter_response(0); // received_parameters[1]
                    return;
                }
            }
        """)

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    ## DEBUG FUNCTIONS
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
        Enable transmision of debug messages from the Arduino, and the display of some
        info in the LCD.
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
    ## LCD FUNCTIONS
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def lcdMessage(self, message):
        """
        Clear the content of the LCD and write the given message.
        If message is a string, it'll be displayed in the first line of the LCD.
        If message is a list, each item will be displayed in a different line.
        
        See :func:`lcdWrite` for more info.
        
        Parameters:
            - message (string or list): message to display
        """
        if isinstance(message, basestring):
            self.lcdWrite(message, 0, 0, clear_lcd=True)
        elif isinstance(message, (list, tuple, )):
            self.lcdClear()
            for i in range(0, len(message)):
                self.lcdWrite(message[i], 0, i)
        else:
            raise(InvalidArgument("message parameter must be string, list or tuple"))
    
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def lcdWrite(self, message, col, row, clear_lcd=False): # pylint: disable=C0103
        """
        Write a message to the LCD, starting in the given row and column.
        An exception may be raised if the message is larger than the buffer used in the Arduino
        to keep the receivded data. And each world of the message is sent as a different parameter;
        if the message has many words (an thus, many parameters), an exception may be raised.
        
        See :func:`lcdMessage`.
        
        For this to work, the sketch uploaded to the Arduino must be build
        using the '--lcd' option. See https://github.com/hgdeoro/py-arduino-proxy/wiki/LCD-Support
        for more information.
        
        Parameters:
            - message (str): message to display
            - col (int): column
            - row (int): row
        """
        if not type(col) is int:
            raise(InvalidArgument("col must be an integer"))
        if not type(row) is int:
            raise(InvalidArgument("row must be an integer"))
        
        # FIXME: check 'message' type and length
        # FIXME: check parameters
        # FIXME: test detection of invalid parameters
        
        if clear_lcd:
            self.lcdClear()
        
        return self.send_cmd("_lcdW\t%d\t%d\t%s" % (col, row, message),  "LWOK")
            # raises CommandTimeout,InvalidCommand,InvalidResponse
    
    lcdWrite.arduino_function_name = '_lcdW'
    lcdWrite.arduino_code = _unindent(12, """
            void _lcdW() {
                #if PY_ARDUINO_PROXY_LCD_SUPPORT == 1
                    int col = atoi(received_parameters[1]);
                    int row = atoi(received_parameters[2]);
                    lcd.setCursor(col, row);
                    // reuse 'col' variable
                    for(col=3; col<MAX_RECEIVED_PARAMETERS; col++) {
                        if(received_parameters[col] == NULL)
                            break;
                        lcd.print(received_parameters[col]);
                        if(col+1<MAX_RECEIVED_PARAMETERS && received_parameters[col+1] != NULL) {
                            lcd.print(" ");
                        }
                    }
                    send_char_array_response("LWOK");
                #else
                    send_unsupported_cmd_response();
                #endif
            }
        """)
    
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def lcdClear(self): # pylint: disable=C0103
        """
        Clear the LCD.
        
        For this to work, the sketch uploaded to the Arduino must be build
        using the '--lcd' option. See https://github.com/hgdeoro/py-arduino-proxy/wiki/LCD-Support
        for more information.
        """
        return self.send_cmd("_lcdClr", "LCLROK")
            # raises CommandTimeout,InvalidCommand,InvalidResponse
    
    lcdClear.arduino_function_name = '_lcdClr'
    lcdClear.arduino_code = _unindent(12, """
            void _lcdClr() {
                #if PY_ARDUINO_PROXY_LCD_SUPPORT == 1
                    lcd.clear();
                    send_char_array_response("LCLROK");
                #else
                    send_unsupported_cmd_response();
                #endif
            }
        """)

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def shiftOut(self, dataPin, clockPin, bitOrder, value, set_pin_mode=False): # pylint: disable=C0103,C0301,R0913
        """
        Proxy function for Arduino's **shiftOut()**.
        Shifts out a byte of data one bit at a time.
        
        See: http://arduino.cc/en/Reference/ShiftOut and
        http://www.arduino.cc/en/Tutorial/ShiftOut
        
        Parameters:
            - dataPin (int): the pin on which to output each bit.
            - clockPin (int): the pin to toggle once the dataPin has been set to the correct value.
            - bitOrder: which order to shift out the bits; either ArduinoProxy.LSBFIRST or ArduinoProxy.MSBFIRST.
            - value (int): the data to shift out.
        """
        self._validate_digital_pin(dataPin, 'dataPin')
        self._validate_digital_pin(clockPin, 'clockPin')
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
        return self.send_cmd("_sftO\t%d\t%d\t%d\t%d" % (dataPin, clockPin, bitOrder, value, ), "SOOK")
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
    ## HARDWARD INFO FUNCTIONS
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def getAvrCpuType(self): # pylint: disable=C0103
        """
        Returns the value of _AVR_CPU_NAME_
        """
        return self.send_cmd("_gACT")
            # raises CommandTimeout,InvalidCommand,InvalidResponse
    
    getAvrCpuType.arduino_function_name = '_gACT'
    getAvrCpuType.arduino_code = _unindent(12, """
            void _gACT() {
                send_char_array_response(_AVR_CPU_NAME_);
            }
        """)

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def getArduinoTypeStruct(self): # pylint: disable=C0103
        """
        Returns a dict with the value of **this_arduino_type** struct.
        
        The dict contains:
            - analog_pins: how many analog pins the Arduino has.
            - digital_pins: how many digital pins the Arduino has.
            - pwm_pins_bitmap: bitmap of digital pin that supports PWM.
            - pwm_pin_list: tuple of pin numbers that supports PWM.
            - ram_size: RAM size in KiB.
            - ram_size_bytes: RAM size in bytes.
            - eeprom_size: EEPROM size in KiB.
            - eeprom_size_bytes: EEPROM size in bytes.
            - flash_size: FLASH size in KiB.
            - flash_size_bytes: FLASH size in bytes.
        """
        value = self.send_cmd("_gATS")
        splitted = [item for item in value.split() if item]

        arduino_type_struct = {
            'analog_pins': int(splitted[0]), 
            'digital_pins': int(splitted[1]), 
            'pwm_pins_bitmap': splitted[2], 
            'eeprom_size': int(splitted[3]), # KiB
            'flash_size': int(splitted[4]), # KiB
            'ram_size': int(splitted[5]), # KiB
        }
        
        pwm_pin_list = []
        pwm_pins_bitmap = arduino_type_struct['pwm_pins_bitmap']
        pwm_pins_bitmap = list(pwm_pins_bitmap)
        
        index = 0
        while pwm_pins_bitmap:
            if pwm_pins_bitmap.pop() == '1':
                pwm_pin_list.append(index)
            index += 1
        
        arduino_type_struct['pwm_pin_list'] = tuple(pwm_pin_list)
        arduino_type_struct['eeprom_size_bytes'] = arduino_type_struct['eeprom_size'] * 1024
        arduino_type_struct['flash_size_bytes'] = arduino_type_struct['flash_size'] * 1024
        arduino_type_struct['ram_size_bytes'] = arduino_type_struct['ram_size'] * 1024
        
        return arduino_type_struct
    
    getArduinoTypeStruct.arduino_function_name = '_gATS'
    getArduinoTypeStruct.arduino_code = _unindent(12, """
            void _gATS() {
                Serial.print(this_arduino_type.analog_pins, DEC);
                Serial.print(" ");
                Serial.print(this_arduino_type.digital_pins, DEC);
                Serial.print(" ");
                Serial.print(this_arduino_type.pwm_pins_bitmap, BIN);
                Serial.print(" ");
                Serial.print(this_arduino_type.eeprom_size, DEC);
                Serial.print(" ");
                Serial.print(this_arduino_type.flash_size, DEC);
                Serial.print(" ");
                Serial.print(this_arduino_type.ram_size, DEC);
                Serial.println("");
            }
        """)
    
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    
    def getFreeMemory(self): # pylint: disable=C0103
        """
        Returns the available free memory.
        """
        return self.send_cmd("_gFM")
            # raises CommandTimeout,InvalidCommand,InvalidResponse
    
    getFreeMemory.arduino_function_name = '_gFM'
    getFreeMemory.arduino_code = _unindent(12, """
            void _gFM() {
                send_int_response(freeMemory());
            }
        """)
    
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

    def send_streaming_cmd(self, cmd, count, timeout=None, response_transformer=None):
        """
        Note: this is a **low level** method. The only situation you may need to call this method
        is if you are creating new methods.
        
        FIXME: DOCUMENT THIS!
        
        """
        logger.debug("send_streaming_cmd() called. cmd: '%s'", cmd)
        
        self.serial_port.write(cmd)
        self.serial_port.write("\n")
        self.serial_port.flush()
        
        pending_reads = count
        
        while pending_reads > 0:
            while True:
                response = self.get_next_response(timeout=timeout) # Raises CommandTimeout
                if response.startswith('> '):
                    logger.info("[DEBUG-TEXT-RECEIVED] %s", pprint.pformat(response))
                else:
                    break
            
            self._check_response_for_errors(response, cmd)
            
            pending_reads -= 1
            
            transformed_response = None
            if response_transformer is not None: # must transform the response
                try:
                    transformed_response = response_transformer(response)
                except BaseException, exception:
                    raise(InvalidResponse("The response couldn't be transformed. " + \
                        "Response: %s. Exception: %s" % (pprint.pformat(exception),
                        pprint.pformat(response))))
            
            if response_transformer is not None:
                yield transformed_response
            else:
                yield response
        
        # Read final response
        while True:
            response = self.get_next_response(timeout=timeout) # Raises CommandTimeout
            if response.startswith('> '):
                logger.info("[DEBUG-TEXT-RECEIVED] %s", pprint.pformat(response))
            else:
                break
        
        # While streaming, the final response should be "SR_OK"
        if response != "SR_OK":
            raise(InvalidResponse(
                "The response wasn't the expected. " + \
                "Expected: %s. " % "SR_OK" + \
                "Response: %s." % pprint.pformat(response) \
            ))

    def streamingAnalogRead(self, pin, count): # pylint: disable=C0103
        """
        Start reading from the specified analog pin.
        
        See: http://arduino.cc/en/Reference/AnalogRead
        
        Parameters:
            - pin (integer): analog pin to read.
            - count (integer): how many values to read.
        
        Returns:
            - a generator that returns the read values.
        """
        return self.send_streaming_cmd("_srtRAP\t%d\t%d" % (pin, count,), count, response_transformer=int)
            # raises CommandTimeout,InvalidCommand,InvalidResponse
    
    streamingAnalogRead.arduino_function_name = '_srtRAP'
    streamingAnalogRead.arduino_code = _unindent(12, """
            void _srtRAP() {
                int pin = atoi(received_parameters[1]);
                int count = atoi(received_parameters[2]);
                int value;
                int i;
                for(i=0; i<count; i++) {
                    value = analogRead(pin);
                    send_int_response(value);
                }
                send_char_array_response("SR_OK"); // streaming read ok
            }
        """)

    def streamingDigitalRead(self, pin, count): # pylint: disable=C0103
        """
        Start reading from the specified digital pin.
        
        See: http://arduino.cc/en/Reference/DigitalRead
        
        Parameters:
            - pin (integer): analog pin to read.
            - count (integer): how many values to read.
        
        Returns:
            - a generator that returns the read values.
        """
        return self.send_streaming_cmd("_strDR\t%d\t%d" % (pin, count,), count, response_transformer=int)
            # raises CommandTimeout,InvalidCommand,InvalidResponse
    
    streamingDigitalRead.arduino_function_name = '_strDR'
    streamingDigitalRead.arduino_code = _unindent(12, """
            void _strDR() {
                int pin = atoi(received_parameters[1]);
                int count = atoi(received_parameters[2]);
                int value;
                int i;
                for(i=0; i<count; i++) {
                    int value = digitalRead(pin);
                    send_int_response(value);
                }
                send_char_array_response("SR_OK"); // streaming read ok
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
