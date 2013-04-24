##-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
##    PyArduinoProxy - Access your Arduino from Python
##    Copyright (C) 2011-2012 - Horacio Guillermo de Oro <hgdeoro@gmail.com>
##
##    This file is part of PyArduinoProxy.
##
##    PyArduinoProxy is free software; you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation version 2.
##
##    PyArduinoProxy is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License version 2 for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with PyArduinoProxy; see the file LICENSE.txt.
##-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# pylint: disable=C0302

# TODO: _unindent() could be a annotation

import logging as _logging
import math
import pprint
import random
import serial
import time
import threading

from serial.tools.list_ports import comports

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

logger = _logging.getLogger(__name__) # pylint: disable=C0103

DEFAULT_SERIAL_SPEED = 9600

ARDUINO_PROXY_LOCK = threading.RLock()

# Device to use to launch an emulator instad of connecting to a real Arduino
DEVICE_FOR_EMULATOR = '/dev/ARDUINO_EMULATOR'


def synchronized(lock):
    '''Synchronization decorator.'''

    def wrap(f):
        def new_function(*args, **kw):
            lock.acquire()
            try:
                return f(*args, **kw)
            finally:
                lock.release()
        return new_function
    return wrap


def _unindent(spaces, the_string):
    lines = []
    start = ' ' * spaces
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


class NotConnected(ArduinoProxyException):
    """
    Raised when a method that required a connection was called, but the
    instance wasn't connected.
    """

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

    def __init__(self, tty=None, speed=DEFAULT_SERIAL_SPEED,
        wait_after_open=2, timeout=5, call_validate_connection=True):
        """
        Creates a proxy instance, BUT DOESN'T CONNECT IT.

        If call_validate_connection is true, a call to validateConnection() is done, to ensures
        the created instance could communicate to Arduino after established the serial connection.

        Parameters:
            - device name (serial port) to connect. May be None (and `connect` should be False)
            - speed: serial port speed.
            - wait_after_open: this is needed because the Arduino resets itself when connecting the USB.
            - timeout: default timeout (in seconds). Configure how many seconds we wait for a response.
            - call_validate_connection: call validateConnection() after opening the port.
            - connect: if the connection should be established
        """
        # For communicating with the computer, use one of these rates: 300, 1200, 2400, 4800,
        #    9600, 14400, 19200, 28800, 38400, 57600, or 115200.
        logger.debug("Instantiating ArduinoProxy('%s', %d)...", tty, speed)
        self.tty = tty
        self.speed = speed
        self.wait_after_open = wait_after_open
        self.timeout = timeout
        self.call_validate_connection = call_validate_connection

        # One, and only one of (self.serial_port, self.emulator) should be not None
        self.serial_port = None
        self.emulator = None

    def _connect_emulator(self, initial_input_buffer_contents=None):
        """Common method to be used from `create_emulator()` and `__init__()`"""
        from arduino_proxy.emulator import SerialConnectionMock, ArduinoEmulator
        if initial_input_buffer_contents:
            self.serial_port = SerialConnectionMock(
                initial_in_buffer_contents=initial_input_buffer_contents)
        else:
            self.serial_port = SerialConnectionMock()
        self.emulator = ArduinoEmulator(self.serial_port.get_other_side())
        self.emulator.start()
        self.validateConnection()

    @classmethod
    def create_emulator(cls, initial_input_buffer_contents=None):
        """
        Returns an instance of ArduinoProxy CONNECTED to the Arduino emulator.

        You should NOT call to `connect()` on the returned instance.
        """
        proxy = cls(tty=DEVICE_FOR_EMULATOR, wait_after_open=0, call_validate_connection=False)
        proxy._connect_emulator(initial_input_buffer_contents=initial_input_buffer_contents)
        return proxy

    @synchronized(ARDUINO_PROXY_LOCK)
    def connect(self):
        """
        Estabishes serial connection to the Arduino, and returns the proxy instance.
        This allow the instantiation and connection in one line:

        >>> proxy = ArduinoProxy('/dev/ttyACM0').connect()
        """
        assert self.tty is not None
        assert not self.is_connected()

        if self.tty == DEVICE_FOR_EMULATOR:
            self._connect_emulator()

        else:
            logger.debug("Opening serial port %s...", self.tty)
            self.serial_port = serial.Serial(port=self.tty, baudrate=self.speed, bytesize=8, parity='N',
                stopbits=1, timeout=self.timeout)
            # self.serial_port.open() - The port is opened when the instance is created!
            # This has no efect on Linux, but raises an exception on other os.
            if self.wait_after_open > 0:
                logger.debug("Open OK. Now waiting for Arduino's reset")
                time.sleep(self.wait_after_open)

        if self.call_validate_connection:
            logger.debug("Calling validateConnection()...")
            self.validateConnection()

        logger.debug("connect() OK")
        return self

    @synchronized(ARDUINO_PROXY_LOCK)
    def close(self):
        """Closes the connection to the Arduino."""
        self._assert_connected()
        if self.emulator:
            self.emulator.stop_running()
            logger.info("Running emulator... Will join the threads...")
            self.emulator.join()
            logger.info("Threads joined OK.")
            self.emulator = None
        else:
            self.serial_port.close()
            self.serial_port = None

    @synchronized(ARDUINO_PROXY_LOCK)
    def _assert_connected(self):
        if not self.is_connected():
            raise(NotConnected())

    @synchronized(ARDUINO_PROXY_LOCK)
    def is_connected(self):
        """Return whenever the proxy is connected"""
        # FIXME: self.serial_port is ALWAYS non-None if connected (even with emulator)
        return bool(self.emulator) or bool(self.serial_port)

    @synchronized(ARDUINO_PROXY_LOCK)
    def autoconnect(self):
        """
        Try to connect on every available serial port.
        Returns: True if connection was posible, False otherwise.
        """
        if self.is_connected():
            raise(ArduinoProxyException("The instance is already connected"))

        initial_tty = self.tty
        for a_serial_port, _, _ in comports():
            # TODO: this 'filtering' of devices should be done in a more extensible way
            if a_serial_port.startswith('/dev/ttyACM'):
                logger.info("autoconnect(): trying to connect to %s", a_serial_port)
                try:
                    self.tty = a_serial_port
                    self.connect()
                    return True
                except:
                    # Ignore and continue with next serial port
                    logger.info("autoconnect(): couldn't connect to %s", a_serial_port)
                    self.tty = initial_tty

        return False

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

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

    @synchronized(ARDUINO_PROXY_LOCK)
    def setTimeout(self, new_timeout): # pylint: disable=C0103
        """
        Changes the timeout (in seconds).
        """
        self.timeout = new_timeout
        if self.serial_port:
            self.serial_port.timeout = new_timeout

    @synchronized(ARDUINO_PROXY_LOCK)
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
        self._assert_connected()
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
            pprint.pformat(response), (end - start))
        return response

    def _check_response_for_errors(self, response, cmd): # pylint: disable=R0201
        splitted = [item for item in response.split() if item]
        if splitted[0] == ArduinoProxy.INVALID_CMD:
            if len(splitted) == 1:
                logger.warn("Received ArduinoProxy.INVALID_CMD, but without error code. " + \
                    "The command was: %s", pprint.pformat(cmd))
                raise(InvalidCommand("Arduino responded with INVALID_CMD. " + \
                    "The command was: %s" % pprint.pformat(cmd)))
            else:
                raise(InvalidCommand("Arduino responded with INVALID_CMD. " + \
                    "The command was: %s. Error code: %s" % (pprint.pformat(cmd), splitted[1]),
                    error_code=splitted[1]))

        if splitted[0] == ArduinoProxy.INVALID_PARAMETER:
            if len(splitted) == 1:
                logger.warn("Received ArduinoProxy.INVALID_PARAMETER, but without error code. " + \
                    "The command was: %s", pprint.pformat(cmd))
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

    @synchronized(ARDUINO_PROXY_LOCK)
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
            - InvalidResponse: raised when 'expected_response is not None, an the response
                doesn't equals to 'expected_response'.
            - UnsupportedCommand: if the Arduino reported that the command isn't supported.
        """
        self._assert_connected()
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

    @synchronized(ARDUINO_PROXY_LOCK)
    def get_proxy_functions(self):
        """
        Returns a list of proxy functions. This is used internally to generate the sketch files.
        """
        # FIXME: this should be moved to the module (no need to be an instance method)
        all_attributes = [getattr(self, an_attribute_name) for an_attribute_name in dir(self)]
        proxy_functions = [an_attribute for an_attribute in all_attributes
            if getattr(an_attribute, 'arduino_code', False)]
        return proxy_functions

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    ## HERE STARTS PROXIED FUNCTIONS
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

    @synchronized(ARDUINO_PROXY_LOCK)
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
        self._assert_connected()
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

    @synchronized(ARDUINO_PROXY_LOCK)
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
        self._assert_connected()
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

    @synchronized(ARDUINO_PROXY_LOCK)
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
        self._assert_connected()
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

    @synchronized(ARDUINO_PROXY_LOCK)
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
        self._assert_connected()
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

    @synchronized(ARDUINO_PROXY_LOCK)
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
        self._assert_connected()
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

    @synchronized(ARDUINO_PROXY_LOCK)
    def ping(self): # pylint: disable=C0103
        """
        Sends a 'ping' to the Arduino. May be used to check if the connection is alive.
        """
        self._assert_connected()
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

    @synchronized(ARDUINO_PROXY_LOCK)
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
        self._assert_connected()
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

    @synchronized(ARDUINO_PROXY_LOCK)
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
        self._assert_connected()
        if not type(value) is int:
            raise(InvalidArgument("value must be an integer"))
        if not value >= 0:
            raise(InvalidArgument("value must be greater or equals than 0"))

        delay_in_seconds = math.ceil(value / 1000.0)
        if self.timeout > delay_in_seconds:
            response = self.send_cmd("_dy\t%d" % value, expected_response="D_OK")
            # raises CommandTimeout,InvalidCommand,InvalidResponse
        else:
            response = self.send_cmd("_dy\t%d" % value, expected_response="D_OK",
                timeout=(delay_in_seconds + 1))
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

    @synchronized(ARDUINO_PROXY_LOCK)
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
        self._assert_connected()
        if not type(value) is int:
            raise(InvalidArgument("value must be an integer"))
        if not value >= 0:
            raise(InvalidArgument("value must be greater or equals than 0"))

        delay_in_seconds = math.ceil(value / 1000000.0)
        if self.timeout > delay_in_seconds:
            return self.send_cmd("_dMs\t%d" % value, expected_response="DMS_OK")
            # raises CommandTimeout,InvalidCommand,InvalidResponse
        else:
            return self.send_cmd("_dMs\t%d" % value, expected_response="DMS_OK",
                timeout=(delay_in_seconds + 1))
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

    @synchronized(ARDUINO_PROXY_LOCK)
    def millis(self): # pylint: disable=C0103
        """
        Proxy function for Arduino's **millis()**.
        Returns the number of milliseconds since the Arduino board began running the
        current program.
        
        See: http://arduino.cc/en/Reference/Millis
        """
        self._assert_connected()
        return self.send_cmd("_ms", response_transformer=int)
        # raises CommandTimeout,InvalidCommand,InvalidResponse

    millis.arduino_function_name = '_ms'
    millis.arduino_code = _unindent(12, """
            void _ms() {
                send_debug();
                Serial.print(millis());
                Serial.print("\\n");
            }
        """)

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

    @synchronized(ARDUINO_PROXY_LOCK)
    def micros(self): # pylint: disable=C0103
        """
        Proxy function for Arduino's **micros()**.
        
        Returns the number of microseconds since the Arduino board began running the current
        program.
        
        See: http://arduino.cc/en/Reference/Micros
        """
        self._assert_connected()
        return self.send_cmd("_mc", response_transformer=int)
        # raises CommandTimeout,InvalidCommand,InvalidResponse

    micros.arduino_function_name = '_mc'
    micros.arduino_code = _unindent(12, """
            void _mc() {
                send_debug();
                Serial.print(micros());
                Serial.print("\\n");
            }
        """)

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    ## INTERRUPT RELATED FUNCTIONS
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

    @synchronized(ARDUINO_PROXY_LOCK)
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
        self._assert_connected()
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

    @synchronized(ARDUINO_PROXY_LOCK)
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
        self._assert_connected()
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

    @synchronized(ARDUINO_PROXY_LOCK)
    def enableDebug(self): # pylint: disable=C0103
        """
        Enable transmision of debug messages from the Arduino.
        """
        self._assert_connected()
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

    @synchronized(ARDUINO_PROXY_LOCK)
    def enableDebugToLcd(self): # pylint: disable=C0103
        """
        Enable transmision of debug messages from the Arduino, and the display of some
        info in the LCD.
        """
        self._assert_connected()
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

    @synchronized(ARDUINO_PROXY_LOCK)
    def disableDebug(self): # pylint: disable=C0103
        """
        Disable transmision of debug messages from the Arduino.
        """
        self._assert_connected()
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

    @synchronized(ARDUINO_PROXY_LOCK)
    def lcdMessage(self, message):
        """
        Clear the content of the LCD and write the given message.
        If message is a string, it'll be displayed in the first line of the LCD.
        If message is a list, each item will be displayed in a different line.
        
        See :func:`lcdWrite` for more info.
        
        Parameters:
            - message (string or list): message to display
        """
        self._assert_connected()
        if isinstance(message, basestring):
            self.lcdWrite(message, 0, 0, clear_lcd=True)
        elif isinstance(message, (list, tuple,)):
            self.lcdClear()
            for i in range(0, len(message)):
                self.lcdWrite(message[i], 0, i)
        else:
            raise(InvalidArgument("message parameter must be string, list or tuple"))

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

    @synchronized(ARDUINO_PROXY_LOCK)
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
        self._assert_connected()
        if not type(col) is int:
            raise(InvalidArgument("col must be an integer"))
        if not type(row) is int:
            raise(InvalidArgument("row must be an integer"))

        # FIXME: check 'message' type and length
        # FIXME: check parameters
        # FIXME: test detection of invalid parameters

        if clear_lcd:
            self.lcdClear()

        return self.send_cmd("_lcdW\t%d\t%d\t%s" % (col, row, message), "LWOK")
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

    @synchronized(ARDUINO_PROXY_LOCK)
    def lcdClear(self): # pylint: disable=C0103
        """
        Clear the LCD.
        
        For this to work, the sketch uploaded to the Arduino must be build
        using the '--lcd' option. See https://github.com/hgdeoro/py-arduino-proxy/wiki/LCD-Support
        for more information.
        """
        self._assert_connected()
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

    @synchronized(ARDUINO_PROXY_LOCK)
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
        self._assert_connected()
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
        return self.send_cmd("_sftO\t%d\t%d\t%d\t%d" % (dataPin, clockPin, bitOrder, value,), "SOOK")
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

    @synchronized(ARDUINO_PROXY_LOCK)
    def getAvrCpuType(self): # pylint: disable=C0103
        """
        Returns the value of _AVR_CPU_NAME_
        """
        self._assert_connected()
        return self.send_cmd("_gACT")
            # raises CommandTimeout,InvalidCommand,InvalidResponse

    getAvrCpuType.arduino_function_name = '_gACT'
    getAvrCpuType.arduino_code = _unindent(12, """
            void _gACT() {
                send_char_array_response(_AVR_CPU_NAME_);
            }
        """)

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

    @synchronized(ARDUINO_PROXY_LOCK)
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
        self._assert_connected()
        value = self.send_cmd("_gATS")
        splitted = [item for item in value.split() if item]

        arduino_type_struct = {
            'analog_pins': int(splitted[0]),
            'digital_pins': int(splitted[1]),
            'pwm_pins_bitmap': splitted[2],
            'eeprom_size': int(splitted[3]), # KiB
            'flash_size': int(splitted[4]), # KiB
            'ram_size': int(splitted[5]), # KiB
            'pwm_pin_list': None,
            'eeprom_size_bytes': None,
            'flash_size_bytes': None,
            'ram_size_bytes': None,
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

        assert None not in arduino_type_struct.keys()
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
                Serial.print("\\n");
            }
        """)

    def enhanceArduinoTypeStruct(self, arduino_type_struct):
        """
        Enhance the 'type struct' with utilities and user-friendly data.
        """
        arduino_type_struct = arduino_type_struct.copy()
        arduino_type_struct['analog_pins_items'] = range(0, arduino_type_struct['analog_pins'])
        arduino_type_struct['digital_pins_items'] = range(0, arduino_type_struct['digital_pins'])
        return arduino_type_struct

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

    @synchronized(ARDUINO_PROXY_LOCK)
    def getFreeMemory(self): # pylint: disable=C0103
        """
        Returns the available free memory.
        """
        self._assert_connected()
        return self.send_cmd("_gFM")
            # raises CommandTimeout,InvalidCommand,InvalidResponse

    getFreeMemory.arduino_function_name = '_gFM'
    getFreeMemory.arduino_code = _unindent(12, """
            void _gFM() {
                send_int_response(freeMemory());
            }
        """)

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

    @synchronized(ARDUINO_PROXY_LOCK)
    def send_streaming_cmd(self, cmd, count, timeout=None, response_transformer=None):
        """
        Note: this is a **low level** method. The only situation you may need to call this method
        is if you are creating new methods.
        
        FIXME: DOCUMENT THIS!
        
        """
        self._assert_connected()
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

    @synchronized(ARDUINO_PROXY_LOCK)
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
        self._assert_connected()
        return self.send_streaming_cmd("_strAR\t%d\t%d" % (pin, count,), count, response_transformer=int)
            # raises CommandTimeout,InvalidCommand,InvalidResponse

    streamingAnalogRead.arduino_function_name = '_strAR'
    streamingAnalogRead.arduino_code = _unindent(12, """
            void _strAR() {
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

    @synchronized(ARDUINO_PROXY_LOCK)
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
        self._assert_connected()
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

    @synchronized(ARDUINO_PROXY_LOCK)
    def dht11_read(self, pin): # pylint: disable=C0103
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
        self._assert_connected()
        self._validate_digital_pin(pin)
        cmd = "_dht11Rd\t%d" % (pin)

        response = self.send_cmd(cmd) # raises CommandTimeout,InvalidCommand

        splitted_response = response.split(",")
        if splitted_response[0] == 'DHTLIB_OK':
            if len(splitted_response) == 3:
                try:
                    return int(splitted_response[1]), int(splitted_response[2])
                except ValueError:
                    raise(InvalidResponse("DHTLIB_OK received, but data couldn't be transformed to int"))
            else:
                raise(InvalidResponse("DHTLIB_OK received, but without data"))

        raise(InvalidResponse(splitted_response[0]))

    dht11_read.arduino_function_name = '_dht11Rd'
    dht11_read.arduino_code = _unindent(12, """
            void _dht11Rd() {
                int pin = atoi(received_parameters[1]);
                dht11 DHT11;
                int checksum_ok = DHT11.read(pin);
                switch (checksum_ok)
                {
                    case DHTLIB_OK:
                        Serial.print("DHTLIB_OK,");
                        break;
                    case DHTLIB_ERROR_CHECKSUM:
                        send_char_array_response("DHTLIB_ERROR_CHECKSUM");
                        return;
                    case DHTLIB_ERROR_TIMEOUT:
                        send_char_array_response("DHTLIB_ERROR_TIMEOUT");
                        return;
                    default:
                        send_char_array_response("DHTLIB_UNKNOWN_ERROR");
                        return;
                }
                Serial.print(DHT11.temperature);
                Serial.print(",");
                Serial.print(DHT11.humidity);
                Serial.print("\\n");
                return;
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
