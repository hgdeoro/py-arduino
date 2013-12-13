##-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
##    py-arduino - Access your Arduino from Python
##    Copyright (C) 2011-2013 - Horacio Guillermo de Oro <hgdeoro@gmail.com>
##
##    This file is part of py-arduino.
##
##    py-arduino is free software; you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation version 2.
##
##    py-arduino is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License version 2 for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with py-arduino; see the file LICENSE.txt.
##-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# pylint: disable=C0302

import copy
import logging as _logging
import math
import pprint
import random
import serial
import time
import threading
import textwrap
import datetime
import weakref

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from serial.tools.list_ports import comports

from py_arduino import INPUT, OUTPUT, DEVICE_FOR_EMULATOR, \
    ATTACH_INTERRUPT_MODE_LOW, ATTACH_INTERRUPT_MODE_CHANGE, \
    ATTACH_INTERRUPT_MODE_RISING, ATTACH_INTERRUPT_MODE_FALLING, LSBFIRST, \
    MSBFIRST, DEFAULT_SERIAL_SPEED, LOW, HIGH, NotConnected, PyArduinoException, \
    InvalidArgument, InvalidResponse, InvalidCommand, InvalidParameter, \
    UnsupportedCommand, CommandTimeout, INVALID_CMD, INVALID_PARAMETER, \
    UNSUPPORTED_CMD, MODE_UNKNOWN
from py_arduino.utils import  synchronized
from py_arduino.emulator import SerialConnectionArduinoEmulator

logger = _logging.getLogger(__name__)  # pylint: disable=C0103

#===============================================================================
# Locks
#===============================================================================

STATUS_TRACKER_LOCK = threading.RLock()

ARDUINO_LOCK = threading.RLock()


class BackgroundTask(object):
    """
    Represents a background task
    """

    def __init__(self, name=None, status=None):
        self.name = name
        self.last_alive = None
        self.status = status
        self.pins = weakref.WeakSet()

    def touch(self):
        self.last_alive = datetime.datetime.now()

    def set_status(self, status):
        self.status = status
        self.last_alive = datetime.datetime.now()


class PinStatus(object):
    """
    Class to hold transient information of pin status.
    The information we have here is from the point of view
    of the PyArduino, NOT the real Arduino (see note below).

    Attributes:
    - pin: the pin number
    - digital: if the pin is digital (True) or analog (False)
    - mode: pin mode (INPUT, OUTPUT)
    - read_value: last read value from the pin
    - written_value: last writen value to the pin
    - analog_written_value: last 'analog written' value (PWM) to the pin
    - background_task: instance of BackgroundTask, references the
        background task that is using the pin.
    - last_update: the `time.time()` value of the last update to
        the instance.

    - used_by_lib: name of the library that is using the pin
    - lib_read_value: the last values read by the library
        (a dict, since a library could read multiple values, or make
        many reads in a single call, and generate many results)

    TODO:
    - lib_written_value: the last values used to call the library
        (ie: argument values)

    Note: since the communication isn't "transactional", when some
    errors occurs, we don't know if the change was made in the Arduino.
    For example, we digitalWrite() on a PIN, but we got a timeout: we
    don't know if the write was done. This could be done having the
    'pin status' in the Arduino (maybe in some future version).
    """
    def __init__(self, pin, digital, mode=MODE_UNKNOWN, read_value=None, written_value=None,
            analog_written_value=None, background_task=None, used_by_lib=None,
            lib_read_value=None):
        self.pin = pin
        self.digital = digital
        self.mode = mode  # None == unknown
        self.read_value = read_value  # None == unknown
        self.written_value = written_value  # None == unknown
        self.analog_written_value = analog_written_value  # None == unknown
        # analog_written_value -> PWM & analogWrite()
        # background_task -> instance of BackgroundTask()
        self.background_task = background_task
        self.used_by_lib = used_by_lib
        self.lib_read_value = lib_read_value
        self.last_update = 0

    def as_dict(self):
        ret = {
            'digital': self.digital,
            'mode': self.mode,
            'read_value': self.read_value,
            'written_value': self.written_value,
            'analog_written_value': self.analog_written_value,
            'mode_is_input': self.mode == INPUT,
            'mode_is_output': self.mode == OUTPUT,
            'mode_is_unknown': self.mode not in (INPUT, OUTPUT),
            'used_by_lib': self.used_by_lib,
            'lib_read_value': self.lib_read_value,
            'last_update': self.last_update
        }

        if self.background_task:
            ret['bg_task_name'] = self.background_task.name
            ret['bg_task_status'] = self.background_task.status
            ret['bg_task_last_alive'] = \
                self.background_task.last_alive
        return ret


class StatusTracker(object):
    """Helper objecto to track status of all the pins"""
    def __init__(self):
        # self.status: (pin, digital) -> PinStatus
        # - keys are (pin, digital) tuples
        # - values are PinStatus instances
        self.status = {}
        # self.background_tasks: background_task_name -> BackgroundTask
        # - keys are 'background_task_name'
        # - values are BackgroundTask instances
        self.background_tasks = {}  # Keyed by name

    @synchronized(STATUS_TRACKER_LOCK)
    def get_pin_status_instance(self, pin, digital):
        """
        Returns the instance of `PinStatus` for the requested pin.
        """
        key = (pin, digital,)
        try:
            return self.status[key]
        except KeyError:
            # Create default status
            #  + default mode of Arduino pins is INPUT, except digital 13 (LED)
            # Anyway, we use default values of 'mode' & 'value' -> `None`
            status = PinStatus(pin, digital=digital)
            self.status[key] = status
            return status

    @synchronized(STATUS_TRACKER_LOCK)
    def set_pin_mode(self, pin, digital, mode):
        """
        Set pin mode. `mode = None` implies we don't know the pin mode
        (because an error was detected while trying to set te mode).

        This resets the value of `value`
        """
        assert mode in (INPUT, OUTPUT, MODE_UNKNOWN)
        status = self.get_pin_status_instance(pin, digital)
        status.mode = mode
        status.read_value = None
        status.written_value = None
        status.analog_written_value = None
        status.last_update = time.time()

    @synchronized(STATUS_TRACKER_LOCK)
    def set_for_library(self, pin, digital, library):
        """
        Set pin as to be used by library.
        """
        status = self.get_pin_status_instance(pin, digital)
        status.mode = MODE_UNKNOWN
        status.read_value = None
        status.written_value = None
        status.analog_written_value = None
        status.used_by_lib = library
        status.lib_read_value = None
        status.last_update = time.time()

    #    @synchronized(STATUS_TRACKER_LOCK)
    #    def set_lib_read_value(self, pin, digital, read_values_dict):
    #        """
    #        Set the last read value. `value = None` implies we don't know the value read
    #        (because an error was detected while trying to read that value to Arduino).
    #
    #        Replaces the old dict with a new one.
    #        """
    #        status = self.get_pin_status_instance(pin, digital)
    #        status.lib_read_value = read_values_dict
    #        status.last_update = time.time()

    @synchronized(STATUS_TRACKER_LOCK)
    def set_lib_read_value(self, library_name, read_values_dict):
        """
        Set the last read value. `value = None` implies we don't know the value read
        (because an error was detected while trying to read that value to Arduino).

        Replaces the old dict with a new one.
        """
        status = None
        for key in sorted(self.status.keys()):
            if self.status[key].used_by_lib == library_name:
                status = self.status[key]
                break

        if status is None:
            raise(PyArduinoException("Pin not found for library '{}'".format(library_name)))

        status.read_value = None
        status.lib_read_value = read_values_dict
        status.last_update = time.time()

    @synchronized(STATUS_TRACKER_LOCK)
    def set_pin_written_value(self, pin, digital, written_value):
        """
        Set the last value written. `value = None` implies we don't know the pin value
        (because an error was detected while trying to send that value to Arduino).
        """
        status = self.get_pin_status_instance(pin, digital)
        status.written_value = written_value
        status.analog_written_value = None  # For PWM, we should put 0 or 255 here
        status.last_update = time.time()

    @synchronized(STATUS_TRACKER_LOCK)
    def set_pin_analog_written_value(self, pin, digital, analog_written_value):
        """
        Set the last value written. `value = None` implies we don't know the pin value
        (because an error was detected while trying to send that value to Arduino).
        """
        status = self.get_pin_status_instance(pin, digital)
        status.analog_written_value = analog_written_value
        status.written_value = None  # we should put HIGH (255), LOW (0) or None here
        status.last_update = time.time()

    @synchronized(STATUS_TRACKER_LOCK)
    def set_pin_read_value(self, pin, digital, read_value):
        """
        Set the last read value. `value = None` implies we don't know the value read
        (because an error was detected while trying to read that value to Arduino).
        """
        status = self.get_pin_status_instance(pin, digital)
        status.lib_read_value = None
        status.read_value = read_value
        status.last_update = time.time()

    @synchronized(STATUS_TRACKER_LOCK)
    def reset(self):
        """
        Reset the values of status tracker.
        """
        self.status = {}
        self.background_tasks = {}

    @synchronized(STATUS_TRACKER_LOCK)
    def populate(self, arduino_type_struct):
        """
        Reset the values of status tracker and re-populates.
        """
        self.reset()
        for pin in range(0, arduino_type_struct['digital_pins']):
            self.get_pin_status_instance(pin, digital=True)
        for pin in range(0, arduino_type_struct['analog_pins']):
            self.get_pin_status_instance(pin, digital=False)

    @synchronized(STATUS_TRACKER_LOCK)
    def reserve_pins(self, pin_spec_list, background_task_name):
        """
        Mark the pins on `pin_spec_list` as reserved by background task
        identified by `background_task_name`.

        Returns True if the pin were reserved.

        For example:
            reserve_pins(((1, 'True'),), 'Led blinker @ D1')
        """
        # First check if pins are available
        for pin, digital in pin_spec_list:
            status = self.get_pin_status_instance(pin, digital)
            if status.background_task:
                logger.info("Pin %s (%s) is already reserved - Reservation for %s failed" % (
                    pin, digital, background_task_name))
                return False

        # Then reserve it
        for pin, digital in pin_spec_list:
            status = self.get_pin_status_instance(pin, digital)
            if not background_task_name in self.background_tasks:
                self.background_tasks[background_task_name] = BackgroundTask(background_task_name)
            bg_task = self.background_tasks[background_task_name]
            status.background_task = bg_task
            bg_task.pins.add(status)
            logger.info("Pin %s (%s) reserved successfully for %s" % (
                pin, digital, background_task_name))
        return True

    #    @synchronized(STATUS_TRACKER_LOCK)
    #    def update_background_task_status(self, background_task_name, status):
    #        """
    #        Returns True if the status was updated
    #        """
    #        if not background_task_name in self.background_tasks:
    #            return False
    #        self.background_tasks[background_task_name].set_status(status)

    #    @synchronized(STATUS_TRACKER_LOCK)
    #    def get_background_tasks(self):
    #        """
    #        Return list of `BackgroundTask` instances, ordered by task name
    #        """
    #        ret = []
    #        for key in sorted(self.background_tasks.keys()):
    #            ret.append(self.background_tasks[key])
    #        return ret

    @synchronized(STATUS_TRACKER_LOCK)
    def get_serializable_background_tasks(self):
        """
        Return list of serializable `BackgroundTask` instances, ordered by task name
        """
        ret = []
        ref_time = time.time()
        for key in sorted(self.background_tasks.keys()):
            bg_task = self.background_tasks[key]
            pins = []
            for pin in bg_task.pins:
                pin_info = dict(pin=pin.pin, digital=pin.digital, last_update=pin.last_update)
                pin_info['pin_name'] = 'D%d' % pin.pin if pin.digital else 'A%d' % pin.pin
                pin_info['last_update_ago'] = ref_time - pin.last_update
                pins.append(pin_info)
            ret.append({
                'name': bg_task.name,
                'last_alive': bg_task.last_alive,
                'status': bg_task.status,
                'pins': pins,
            })
        return ret

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class PyArduino(object):  # pylint: disable=R0904
    """
    Class to access the Arduino.
    """

    def __init__(self, tty=None, speed=DEFAULT_SERIAL_SPEED,
        wait_after_open=2, timeout=5, call_validate_connection=True):
        """
        Creates a PyArduino instance, BUT DOESN'T CONNECT IT.

        If call_validate_connection is true, a call to validateConnection() is done, to ensures
        the created instance could communicate to Arduino after established the serial connection.

        Parameters:
            - device name (serial port) to connect. May be None (and `connect` should be False)
            - speed: serial port speed.
            - wait_after_open: this is needed because the Arduino resets itself when
                connecting the USB.
            - timeout: default timeout (in seconds). Configure how many seconds we
                wait for a response.
            - call_validate_connection: call validateConnection() after opening the port.
            - connect: if the connection should be established
        """
        # For communicating with the computer, use one of these rates: 300, 1200, 2400, 4800,
        #    9600, 14400, 19200, 28800, 38400, 57600, or 115200.
        logger.debug("Instantiating PyArduino('%s', %d)...", tty, speed)
        self._arduino_type_struct_cache = None
        self.tty = tty
        self.speed = speed
        self.wait_after_open = wait_after_open
        self.timeout = timeout
        self.call_validate_connection = call_validate_connection

        self.serial_port = None
        self.status_tracker = StatusTracker()

    @synchronized(ARDUINO_LOCK)
    def _get_serial_port(self):
        """
        Returns a real serial port object, or a virtual serial port
        connceted to an instance of ArduinoEmulator if tty is DEVICE_FOR_EMULATOR.

        The `timeout` value is used to set read timeout and write timeout.
        """
        if self.tty == DEVICE_FOR_EMULATOR:
            return SerialConnectionArduinoEmulator()
        else:
            logger.debug("Opening serial port %s...", self.tty)
            serial_port = serial.Serial(port=self.tty, baudrate=self.speed, bytesize=8,
                parity='N', stopbits=1, timeout=self.timeout, writeTimeout=self.timeout)
            # self.serial_port.open() - The port is opened when the instance is created!
            # This has no efect on Linux, but raises an exception on other os.
            if self.wait_after_open > 0:
                logger.debug("Open OK. Now waiting for Arduino's reset")
                time.sleep(self.wait_after_open)
            return serial_port

    @synchronized(ARDUINO_LOCK)
    def connect(self, tty=None, speed=None):
        """
        Estabishes serial connection to the Arduino, and returns the PyArduino instance.
        This allow the instantiation and connection in one line:

        >>> arduino = PyArduino('/dev/ttyACM0').connect()
        """
        assert not self.is_connected()
        if tty:
            self.tty = tty
        if speed:
            self.speed = speed

        assert self.tty is not None

        logger.info("Connecting to %s", self.tty)
        self.serial_port = self._get_serial_port()

        if self.call_validate_connection:
            logger.debug("Calling validateConnection()...")
            self.validateConnection()

        logger.debug("connect() OK")

        self.status_tracker.populate(self.getArduinoTypeStruct())

        return self

    @synchronized(ARDUINO_LOCK)
    def close(self):
        """
        Closes the connection to the Arduino.
        """
        try:
            self.serial_port.close()
        except:
            logger.exception("Error detected when trying to close serial port. "
                "Continuing anyway...")
        self.serial_port = None
        self.tty = None
        self.status_tracker.reset()
        self._arduino_type_struct_cache = None

    def _assert_connected(self):
        if not self.is_connected():
            raise(NotConnected())

    def is_connected(self):
        """Return whenever the PyArduino instance is connected"""
        return bool(self.serial_port)

    def get_serial_ports(self, prefix='/dev/ttyACM'):
        ports = [x[0] for x in comports() if x[0].startswith(prefix)]
        return ports

    @synchronized(ARDUINO_LOCK)
    def autoconnect(self):
        """
        Try to connect on every available serial port.
        Returns: True if connection was posible, False otherwise.
        """
        if self.is_connected():
            raise(PyArduinoException("The instance is already connected"))

        initial_tty = self.tty
        for a_serial_port in self.get_serial_ports():
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

    @synchronized(ARDUINO_LOCK)
    def run_watchdog(self, autoconnect=False):
        """
        Check connectivity and close() in case of error.
        If not connected, does NOT check connectivity.
        """
        try:
            if self.is_connected():
                # if connected, does a ping() to validate the cx.
                self.ping()
                # If ping worked, return (no need to auto-connect)
                return
        except:
            # If ping() failed, do the close()
            logger.warn("run_watchdog(): ping failed. Will close instance.")
            try:
                self.close()
            except:
                pass

        if autoconnect:
            self.autoconnect()

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

    def _validate_analog_pin(self, pin, pin_name='pin'):  # pylint: disable=R0201
        # FIXME: validate pin value (depends on the model of Arduino)
        if not type(pin) is int:
            raise(InvalidArgument("%s must be an int" % pin_name))
        if pin < 0:
            raise(InvalidArgument("%s must be greater or equals to 0" % pin_name))

    def _validate_digital_pin(self, pin, pin_name='pin'):  # pylint: disable=R0201
        # FIXME: validate pin value (depends on the model of Arduino)
        # TODO: Remember: all analog pins works as digital pins.
        if not type(pin) is int:
            raise(InvalidArgument("%s must be an int" % pin_name))
        if pin < 0:
            raise(InvalidArgument("%s must be greater or equals to 0" % pin_name))

    def setTimeout(self, new_timeout):  # pylint: disable=C0103
        """
        Changes the timeout (in seconds).
        """
        self.timeout = new_timeout
        if self.serial_port:
            self.serial_port.timeout = new_timeout

    @synchronized(ARDUINO_LOCK)
    def get_next_response(self, timeout=None):
        """
        Note: this is a **low level** method. The only situation you may need to call this method
        is if you are creating new methods.
        
        Waits for a response from the serial connection.
        
        Parameters:
            - timeout (int): timeout in seconds to use (instead of the configured for this
                instance of PyArduino).
        
        Raises:
            - CommandTimeout if a timeout while reading is detected.
        """
        self._assert_connected()
        logger.debug("get_next_response() - waiting for response...")
        start = time.time()
        response = StringIO()
        if timeout is None:  # Use default timeout
            if self.serial_port.getTimeout() != self.timeout:
                self.serial_port.timeout = self.timeout
        else:  # Use custom timeout
            if self.serial_port.getTimeout() != timeout:
                self.serial_port.timeout = timeout

        while True:
            char = self.serial_port.read()
            if len(char) == 1:
                # Got a char
                if char in ['\n', '\r']:
                    if response.getvalue():  # response.len doesn't works for cStringIO
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

    def _check_response_for_errors(self, response, cmd):  # pylint: disable=R0201
        splitted = [item for item in response.split() if item]
        if splitted[0] == INVALID_CMD:
            if len(splitted) == 1:
                logger.warn("Received INVALID_CMD, but without error code. " + \
                    "The command was: %s", pprint.pformat(cmd))
                raise(InvalidCommand("Arduino responded with INVALID_CMD. " + \
                    "The command was: %s" % pprint.pformat(cmd)))
            else:
                raise(InvalidCommand("Arduino responded with INVALID_CMD. " + \
                    "The command was: %s. Error code: %s" % (pprint.pformat(cmd), splitted[1]),
                    error_code=splitted[1]))

        if splitted[0] == INVALID_PARAMETER:
            if len(splitted) == 1:
                logger.warn("Received INVALID_PARAMETER, but without error code. " + \
                    "The command was: %s", pprint.pformat(cmd))
                raise(InvalidParameter("Arduino responded with INVALID_PARAMETER. " + \
                    "The command was: %s" % pprint.pformat(cmd)))
            else:
                raise(InvalidParameter("Arduino responded with INVALID_PARAMETER." + \
                    "The command was: %s. The invalid parameter is %s" % (pprint.pformat(cmd),
                    splitted[1]), error_param=splitted[1]))

        if splitted[0] == UNSUPPORTED_CMD:
            raise(UnsupportedCommand("Arduino responded with UNSUPPORTED_CMD." + \
                "The unsupported command is: %s" % splitted[1], error_param=splitted[1]))

    #    def start_streaming(self, cmd, streamEndMark, timeout=None):
    #        """
    #        Note: this is a **low level** method. The only situation you may
    #        need to call this method is if you are creating new methods.
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
    #        logger.debug("start_streaming() called. cmd: %r. streamEndMark: %r",
    #            cmd, streamEndMark)
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

    @synchronized(ARDUINO_LOCK)
    def send_cmd(self, cmd, expected_response=None, timeout=None, response_transformer=None):
        """
        Note: this is a **low level** method. The only situation you may need to call this method
        is if you are creating new methods.
        
        Sends a command to the Arduino. The command is terminated with a 0x00.
        Returns the response as a string.
        
        Parameters:
            - cmd: the command to send (string)
            - expected_response: the response we expect from the Arduino. If response_transformer
                is not None, the response is first transformed, and then compared to
                'expected_response'. If expected_response is a list or tuple,
                check that the response is one of its items.
            - response_transformer: the method to call to transform. Must receive a string (the
                valuerecieved from the Arduino).
            - timeout (int): timeout in seconds to use (instead of the configured
                for this instance of PyArduino).
        
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
            response = self.get_next_response(timeout=timeout)  # Raises CommandTimeout
            if response.startswith('> '):
                logger.info("[DEBUG-TEXT-RECEIVED] %s", pprint.pformat(response))
            else:
                break

        self._check_response_for_errors(response, cmd)

        transformed_response = None
        if response_transformer is not None:  # must transform the response
            try:
                transformed_response = response_transformer(response)
            except BaseException, exception:
                raise(InvalidResponse("The response couldn't be transformed. " + \
                    "Response: %s. Exception: %s" % (pprint.pformat(exception),
                    pprint.pformat(response))))

        if expected_response is not None:  # must check the response
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

    def get_arduino_functions(self):
        """
        Returns a list of PyArduino functions.
        This is used internally to generate the sketch files.
        """
        # FIXME: this should be moved to the module (no need to be an instance method)
        all_attributes = [getattr(self, an_attribute_name) for an_attribute_name in dir(self)]
        arduino_functions = [an_attribute for an_attribute in all_attributes
            if getattr(an_attribute, 'arduino_code', False)]
        return arduino_functions

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    ## HERE STARTS PROXIED FUNCTIONS
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

    @synchronized(ARDUINO_LOCK)
    def pinMode(self, pin, mode):  # pylint: disable=C0103
        """
        Proxy function for Arduino's **pinMode()**.
        
        Configures the specified pin to behave either as an input or an output.
        
        See: http://arduino.cc/en/Reference/PinMode and
        http://arduino.cc/en/Tutorial/DigitalPins

        Note: the 'None' mode is used to inform the StatusTracker that the pin isn't used anymore

        Parameters:
            - pin (int): pin to configure
            - mode: INPUT or OUTPUT, or MODE_UNKNOWN
        """
        # TODO: The analog input pins can be used as digital pins, referred to as A0, A1, etc.
        # FIXME: validate pin and value
        # FIXME: add doc for parameters and exceptions
        self._assert_connected()
        self._validate_digital_pin(pin)
        if not mode in [INPUT, OUTPUT, MODE_UNKNOWN]:
            raise(InvalidArgument())

        if mode is MODE_UNKNOWN:
            self.status_tracker.set_pin_mode(pin, digital=True, mode=mode)
            return

        cmd = "_pMd\t%d\t%d" % (pin, mode)

        try:
            self.status_tracker.set_pin_mode(pin, digital=True, mode=mode)
            return self.send_cmd(cmd, expected_response="PM_OK")
        except:
            self.status_tracker.set_pin_mode(pin, digital=True, mode=None)
            raise
        # raises CommandTimeout,InvalidCommand,InvalidResponse

    pinMode.arduino_function_name = '_pMd'
    pinMode.arduino_code = textwrap.dedent("""
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

    @synchronized(ARDUINO_LOCK)
    def digitalWrite(self, pin, value):  # pylint: disable=C0103
        """
        Proxy function for Arduino's **digitalWrite()**.
        Write a HIGH or a LOW value to a digital pin.
        
        See: http://arduino.cc/en/Reference/DigitalWrite
        
        Parameters:
            - pin (int): pin to write
            - value (LOW or HIGH): value to write
        """
        # FIXME: validate pin and value
        # FIXME: add doc for parameters and exceptions
        self._assert_connected()
        self._validate_digital_pin(pin)
        if not value in [LOW, HIGH]:
            raise(InvalidArgument("Invalid value for 'value' parameter."))
        cmd = "_dWrt\t%d\t%d" % (pin, value)
        try:
            self.status_tracker.set_pin_written_value(pin, digital=True, written_value=value)
            return self.send_cmd(cmd, expected_response="DW_OK")
        except:
            self.status_tracker.set_pin_written_value(pin, digital=True, written_value=None)
            raise
        # raises CommandTimeout,InvalidCommand,InvalidResponse

    digitalWrite.arduino_function_name = '_dWrt'
    digitalWrite.arduino_code = textwrap.dedent("""
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

    @synchronized(ARDUINO_LOCK)
    def digitalRead(self, pin):  # pylint: disable=C0103
        """
        Proxy function for Arduino's **digitalRead()**.
        Reads the value from a specified digital pin, either HIGH or LOW.
        
        See: http://arduino.cc/en/Reference/DigitalRead
        
        Parameters:
            - pin (int): digital pin to read
        
        Returns:
            - Either HIGH or LOW
        """
        # FIXME: add doc for exceptions
        self._assert_connected()
        self._validate_digital_pin(pin)
        cmd = "_dRd\t%d" % (pin)
        try:
            response = self.send_cmd(cmd)  # raises CommandTimeout,InvalidCommand
        except:
            self.status_tracker.set_pin_read_value(pin, digital=True, read_value=None)
            raise

        try:
            int_response = int(response)
        except ValueError:
            self.status_tracker.set_pin_read_value(pin, digital=True, read_value=None)
            raise(InvalidResponse("The response couldn't be converted to int. Response: %s" % \
                pprint.pformat(response)))

        if int_response in [HIGH, LOW]:
            self.status_tracker.set_pin_read_value(pin, digital=True, read_value=int_response)
            return int_response

        self.status_tracker.set_pin_read_value(pin, digital=True, read_value=None)
        raise(InvalidResponse("The response isn't HIGH (%d) nor LOW (%d). Response: %s" % (
            HIGH, LOW, int_response)))

    digitalRead.arduino_function_name = '_dRd'
    digitalRead.arduino_code = textwrap.dedent("""
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

    @synchronized(ARDUINO_LOCK)
    def analogRead(self, pin):  # pylint: disable=C0103
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
        try:
            response = self.send_cmd(cmd, response_transformer=int)
        except:
            self.status_tracker.set_pin_read_value(pin, digital=False, read_value=None)
            raise

        if response >= 0 and response <= 1023:
            self.status_tracker.set_pin_read_value(pin, digital=False, read_value=response)
            return response

        self.status_tracker.set_pin_read_value(pin, digital=False, read_value=None)
        raise(InvalidResponse("The response isn't in the valid range of 0-1023. " + \
            "Response: %d" % response))

    analogRead.arduino_function_name = '_aRd'
    analogRead.arduino_code = textwrap.dedent("""
            void _aRd() {
                int pin = atoi(received_parameters[1]);
                int value = analogRead(pin);
                send_int_response(value);
                return;
            }
        """)

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

    @synchronized(ARDUINO_LOCK)
    def analogWrite(self, pin, value):  # pylint: disable=C0103
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
        self._validate_digital_pin(pin)  # Only for DIGITAL pins
        if not type(pin) is int or not type(value) is int or value < 0 or value > 255:
            raise(InvalidArgument())
        cmd = "_aWrt\t%d\t%d" % (pin, value)

        try:
            self.status_tracker.set_pin_analog_written_value(
                pin, digital=True, analog_written_value=value)
            return self.send_cmd(cmd, expected_response="AW_OK")
            # raises CommandTimeout,InvalidCommand,InvalidResponse
        except:
            self.status_tracker.set_pin_analog_written_value(
                pin, digital=True, analog_written_value=None)
            raise

    analogWrite.arduino_function_name = '_aWrt'
    analogWrite.arduino_code = textwrap.dedent("""
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

    @synchronized(ARDUINO_LOCK)
    def ping(self):  # pylint: disable=C0103
        """
        Sends a 'ping' to the Arduino. May be used to check if the connection is alive.
        """
        self._assert_connected()
        cmd = "_ping"
        return self.send_cmd(cmd, expected_response="PING_OK")
        # raises CommandTimeout,InvalidCommand,InvalidResponse

    ping.arduino_function_name = '_ping'
    ping.arduino_code = textwrap.dedent("""
            void _ping() {
                send_char_array_response("PING_OK");
            }
        """)

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

    @synchronized(ARDUINO_LOCK)
    def validateConnection(self):  # pylint: disable=C0103
        """
        Asserts that the current connection is valid, discarding any existing information in the
        buffer of the serial connection.
        
        This method must be called to continue using a PyArduino instance after an error, specially
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
        logger.debug("validateConnection(): will send random string %s", random_str)
        response = self.send_cmd(cmd)  # raises CommandTimeout,InvalidCommand

        while response != random_str:
            logger.warn("validateConnection(): Ignoring invalid response: %s",
                pprint.pformat(response))
            # Go for the string, or a timeout exception!
            response = self.get_next_response()

        logger.debug("validateConnection(): got valid response! Returning...")

        return response

    validateConnection.arduino_function_name = '_vCnt'
    validateConnection.arduino_code = textwrap.dedent("""
            void _vCnt() {
                send_char_array_response(received_parameters[1]);
            }
        """)

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    ## TIME RELATED FUNCTIONS
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

    @synchronized(ARDUINO_LOCK)
    def delay(self, value):  # pylint: disable=C0103
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
    delay.arduino_code = textwrap.dedent("""
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

    @synchronized(ARDUINO_LOCK)
    def delayMicroseconds(self, value):  # pylint: disable=C0103
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
    delayMicroseconds.arduino_code = textwrap.dedent("""
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

    @synchronized(ARDUINO_LOCK)
    def millis(self):  # pylint: disable=C0103
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
    millis.arduino_code = textwrap.dedent("""
            void _ms() {
                send_debug();
                Serial.print(millis());
                Serial.print("\\n");
            }
        """)

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

    @synchronized(ARDUINO_LOCK)
    def micros(self):  # pylint: disable=C0103
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
    micros.arduino_code = textwrap.dedent("""
            void _mc() {
                send_debug();
                Serial.print(micros());
                Serial.print("\\n");
            }
        """)

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    ## INTERRUPT RELATED FUNCTIONS
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

    @synchronized(ARDUINO_LOCK)
    def watchInterrupt(self, interrupt, mode):  # pylint: disable=C0103
        """
        Begin to watch if an interrupt occurs. Use :func:`getInterruptMark` to check if an
        interrupt actually occured.
        
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
        if not mode in [ATTACH_INTERRUPT_MODE_LOW,
                ATTACH_INTERRUPT_MODE_CHANGE,
                ATTACH_INTERRUPT_MODE_RISING,
                ATTACH_INTERRUPT_MODE_FALLING]:
            raise(InvalidArgument("invalid mode: %s" % str(mode)))

        return self.send_cmd("_wI\t%d\t%s" % (interrupt, mode), expected_response="WI_OK")
                                            # raises CommandTimeout,InvalidCommand,InvalidResponse

    watchInterrupt.arduino_function_name = '_wI'
    watchInterrupt.arduino_code = textwrap.dedent("""
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

    @synchronized(ARDUINO_LOCK)
    def getInterruptMark(self, interrupt):  # pylint: disable=C0103
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
    getInterruptMark.arduino_code = textwrap.dedent("""
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

    @synchronized(ARDUINO_LOCK)
    def enableDebug(self):  # pylint: disable=C0103
        """
        Enable transmision of debug messages from the Arduino.
        """
        self._assert_connected()
        return self.send_cmd("_eD", "ENA")
            # raises CommandTimeout,InvalidCommand,InvalidResponse

    enableDebug.arduino_function_name = '_eD'
    enableDebug.arduino_code = textwrap.dedent("""
            void _eD() {
                debug_enabled = 1;
                send_char_array_response("ENA");
            }
        """)

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

    @synchronized(ARDUINO_LOCK)
    def enableDebugToLcd(self):  # pylint: disable=C0103
        """
        Enable transmision of debug messages from the Arduino, and the display of some
        info in the LCD.
        """
        self._assert_connected()
        return self.send_cmd("_eDL", "ENA")
            # raises CommandTimeout,InvalidCommand,InvalidResponse

    enableDebugToLcd.arduino_function_name = '_eDL'
    enableDebugToLcd.arduino_code = textwrap.dedent("""
            void _eDL() {
                #if PY_ARDUINO_LCD_SUPPORT == 1
                    debug_enabled = 2;
                    send_char_array_response("ENA");
                #else
                    send_unsupported_cmd_response();
                #endif
            }
        """)

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

    @synchronized(ARDUINO_LOCK)
    def disableDebug(self):  # pylint: disable=C0103
        """
        Disable transmision of debug messages from the Arduino.
        """
        self._assert_connected()
        return self.send_cmd("_dD", "DIS")
            # raises CommandTimeout,InvalidCommand,InvalidResponse

    disableDebug.arduino_function_name = '_dD'
    disableDebug.arduino_code = textwrap.dedent("""
            void _dD() {
                debug_enabled = 0;
                send_char_array_response("DIS");
            }
        """)

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
    ## LCD FUNCTIONS
    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

    @synchronized(ARDUINO_LOCK)
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

    @synchronized(ARDUINO_LOCK)
    def lcdWrite(self, message, col, row, clear_lcd=False):  # pylint: disable=C0103
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
    lcdWrite.arduino_code = textwrap.dedent("""
            void _lcdW() {
                #if PY_ARDUINO_LCD_SUPPORT == 1
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

    lcdWrite.arduino_header = textwrap.dedent("""
            // If you want to disable LCD support once the sketch file is generated,
            // you can define PY_ARDUINO_LCD_SUPPORT = 0
            #define PY_ARDUINO_LCD_SUPPORT 1

            #if PY_ARDUINO_LCD_SUPPORT == 1
                #include <LiquidCrystal.h>
                #define PY_ARDUINO_LCD_SUPPORT_COLS  16
                #define PY_ARDUINO_LCD_SUPPORT_ROWS   2
                #define PY_ARDUINO_LCD_SUPPORT_rs     7
                #define PY_ARDUINO_LCD_SUPPORT_enable 6
                #define PY_ARDUINO_LCD_SUPPORT_d4     5
                #define PY_ARDUINO_LCD_SUPPORT_d5     4
                #define PY_ARDUINO_LCD_SUPPORT_d6     3
                #define PY_ARDUINO_LCD_SUPPORT_d7     2
            #endif
        """)

    lcdWrite.arduino_globals = textwrap.dedent("""
        #if PY_ARDUINO_LCD_SUPPORT == 1
            LiquidCrystal lcd = LiquidCrystal(
                PY_ARDUINO_LCD_SUPPORT_rs,
                PY_ARDUINO_LCD_SUPPORT_enable,
                PY_ARDUINO_LCD_SUPPORT_d4,
                PY_ARDUINO_LCD_SUPPORT_d5,
                PY_ARDUINO_LCD_SUPPORT_d6,
                PY_ARDUINO_LCD_SUPPORT_d7
            );
        #endif
        """)

    lcdWrite.arduino_setup = textwrap.dedent("""
        #if PY_ARDUINO_LCD_SUPPORT == 1
            lcd.begin(
                PY_ARDUINO_LCD_SUPPORT_COLS,
                PY_ARDUINO_LCD_SUPPORT_ROWS
            );
            lcd.clear();
            lcd.print("PyArduino");
            lcd.setCursor(0, 1); // column, line
            lcd.print("READY!");
        #endif
        """)

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

    @synchronized(ARDUINO_LOCK)
    def lcdClear(self):  # pylint: disable=C0103
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
    lcdClear.arduino_code = textwrap.dedent("""
            void _lcdClr() {
                #if PY_ARDUINO_LCD_SUPPORT == 1
                    lcd.clear();
                    send_char_array_response("LCLROK");
                #else
                    send_unsupported_cmd_response();
                #endif
            }
        """)

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

    @synchronized(ARDUINO_LOCK)
    def shiftOut(self, dataPin, clockPin, bitOrder, value, set_pin_mode=False):
        """
        Proxy function for Arduino's **shiftOut()**.
        Shifts out a byte of data one bit at a time.
        
        See: http://arduino.cc/en/Reference/ShiftOut and
        http://www.arduino.cc/en/Tutorial/ShiftOut
        
        Parameters:
            - dataPin (int): the pin on which to output each bit.
            - clockPin (int): the pin to toggle once the dataPin has been set to the correct value.
            - bitOrder: which order to shift out the bits; either LSBFIRST
                or MSBFIRST.
            - value (int): the data to shift out.
        """
        self._assert_connected()
        self._validate_digital_pin(dataPin, 'dataPin')
        self._validate_digital_pin(clockPin, 'clockPin')
        if not type(value) is int:
            raise(InvalidArgument("value must be an integer"))
        if value < 0 or value > 255:
            raise(InvalidArgument("value must be between 0 and 255"))
        if not bitOrder in [LSBFIRST, MSBFIRST]:
            raise(InvalidArgument("bitOrder must be LSBFIRST or " + \
                "MSBFIRST"))

        # FIXME: test detection of invalid parameters

        if set_pin_mode:
            self.pinMode(dataPin, OUTPUT)
            self.pinMode(clockPin, OUTPUT)
        return self.send_cmd("_sftO\t%d\t%d\t%d\t%d" % (dataPin,
            clockPin, bitOrder, value,), "SOOK")
            # raises CommandTimeout,InvalidCommand,InvalidResponse

    shiftOut.arduino_function_name = '_sftO'
    shiftOut.arduino_code = textwrap.dedent("""
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

    @synchronized(ARDUINO_LOCK)
    def getAvrCpuType(self):  # pylint: disable=C0103
        """
        Returns the value of _AVR_CPU_NAME_
        """
        self._assert_connected()
        return self.send_cmd("_gACT")
            # raises CommandTimeout,InvalidCommand,InvalidResponse

    getAvrCpuType.arduino_function_name = '_gACT'
    getAvrCpuType.arduino_code = textwrap.dedent("""
            void _gACT() {
                send_char_array_response(_AVR_CPU_NAME_);
            }
        """)

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

    @synchronized(ARDUINO_LOCK)
    def getArduinoTypeStruct(self):  # pylint: disable=C0103
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

        if self._arduino_type_struct_cache is not None:
            return copy.deepcopy(self._arduino_type_struct_cache)

        value = self.send_cmd("_gATS")
        splitted = [item for item in value.split() if item]

        arduino_type_struct = {
            'analog_pins': int(splitted[0]),
            'digital_pins': int(splitted[1]),
            'pwm_pins_bitmap': splitted[2],
            'eeprom_size': int(splitted[3]),  # KiB
            'flash_size': int(splitted[4]),  # KiB
            'ram_size': int(splitted[5]),  # KiB
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

        self._arduino_type_struct_cache = arduino_type_struct
        return copy.deepcopy(self._arduino_type_struct_cache)

    getArduinoTypeStruct.arduino_function_name = '_gATS'
    getArduinoTypeStruct.arduino_code = textwrap.dedent("""
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

    @synchronized(ARDUINO_LOCK)
    def enhanceArduinoTypeStruct(self, arduino_type_struct):
        """
        Returns an enhanced copy of `arduino_type_struct` with user-friendlier data.
        Adds:
            - digital_pins_items -> list
            - analog_pins_items -> list
            - digital_pins_struct -> list of dicts
                + pin (int)
                + digital (bool)
                + pwm (bool)
            - analog_pins_struct -> list of dicts
                + pin (int)
                + digital (bool)
                + pwm (bool)
        """
        arduino_type_struct = arduino_type_struct.copy()
        arduino_type_struct['digital_pins_items'] = range(0, arduino_type_struct['digital_pins'])
        arduino_type_struct['analog_pins_items'] = range(0, arduino_type_struct['analog_pins'])

        # create 'structs' for each digital pin
        digital_pins_struct = []
        for dp in arduino_type_struct['digital_pins_items']:
            digital_pins_struct.append({
                'pin': dp,
                'digital': True,
                'pwm': (dp in arduino_type_struct['pwm_pin_list']),
                'status': self.status_tracker.get_pin_status_instance(dp, digital=True).as_dict(),
            })
        arduino_type_struct['digital_pins_struct'] = digital_pins_struct
        del dp

        # create 'structs' for each analog pin
        analog_pins_struct = []
        for ap in arduino_type_struct['analog_pins_items']:
            analog_pins_struct.append({
                'pin': ap,
                'digital': False,
                'pwm': False,
                'status': self.status_tracker.get_pin_status_instance(ap, digital=False).as_dict(),
            })
        arduino_type_struct['analog_pins_struct'] = analog_pins_struct

        return arduino_type_struct

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

    @synchronized(ARDUINO_LOCK)
    def getFreeMemory(self):  # pylint: disable=C0103
        """
        Returns the available free memory.
        """
        self._assert_connected()
        return self.send_cmd("_gFM")
            # raises CommandTimeout,InvalidCommand,InvalidResponse

    getFreeMemory.arduino_function_name = '_gFM'
    getFreeMemory.arduino_code = textwrap.dedent("""
            void _gFM() {
                send_int_response(freeMemory());
            }
        """)

    ## ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

    @synchronized(ARDUINO_LOCK)
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
                response = self.get_next_response(timeout=timeout)  # Raises CommandTimeout
                if response.startswith('> '):
                    logger.info("[DEBUG-TEXT-RECEIVED] %s", pprint.pformat(response))
                else:
                    break

            self._check_response_for_errors(response, cmd)

            pending_reads -= 1

            transformed_response = None
            if response_transformer is not None:  # must transform the response
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
            response = self.get_next_response(timeout=timeout)  # Raises CommandTimeout
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

    @synchronized(ARDUINO_LOCK)
    def streamingAnalogRead(self, pin, count):  # pylint: disable=C0103
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
        return self.send_streaming_cmd("_strAR\t%d\t%d" % (pin, count,),
            count, response_transformer=int)
            # raises CommandTimeout,InvalidCommand,InvalidResponse

    streamingAnalogRead.arduino_function_name = '_strAR'
    streamingAnalogRead.arduino_code = textwrap.dedent("""
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

    @synchronized(ARDUINO_LOCK)
    def streamingDigitalRead(self, pin, count):  # pylint: disable=C0103
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
        return self.send_streaming_cmd("_strDR\t%d\t%d" % (pin, count,),
            count, response_transformer=int)
            # raises CommandTimeout,InvalidCommand,InvalidResponse

    streamingDigitalRead.arduino_function_name = '_strDR'
    streamingDigitalRead.arduino_code = textwrap.dedent("""
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

    #===============================================================================
    # DHT11 - temperature and huminity sensor
    #===============================================================================

    @synchronized(ARDUINO_LOCK)
    def dht11_read(self, pin):  # pylint: disable=C0103
        """
        Read the values of temperature and huminity of a DHT11.
        See: http://playground.arduino.cc/main/DHT11Lib
        
        Parameters:
            - pin (int): digital pin where the sensor is connected
        
        Returns:
            - tuple with temperature and humidity
        """
        # FIXME: add doc for exceptions
        self._assert_connected()
        self._validate_digital_pin(pin)
        cmd = "_dht11Rd\t%d" % (pin)

        response = self.send_cmd(cmd)  # raises CommandTimeout,InvalidCommand

        splitted_response = response.split(",")
        if splitted_response[0] == 'DHTLIB_OK':
            if len(splitted_response) == 3:
                try:
                    return int(splitted_response[1]), int(splitted_response[2])
                except ValueError:
                    raise(InvalidResponse("DHTLIB_OK received, but data "
                        "couldn't be transformed to int"))
            else:
                raise(InvalidResponse("DHTLIB_OK received, but without data"))

        raise(InvalidResponse(splitted_response[0]))

    dht11_read.arduino_function_name = '_dht11Rd'
    dht11_read.arduino_code = textwrap.dedent("""
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

    dht11_read.arduino_header = textwrap.dedent("""
            #include "dht11.h"
        """)

    #===========================================================================
    # OneWire - DS18x20
    #===========================================================================

    @synchronized(ARDUINO_LOCK)
    def ds18x20_read(self, pin):
        """
        Read the values of temperature with a DS18x20 sensor.
        See: http://playground.arduino.cc/Learning/OneWire
        
        Parameters:
            - pin (int): digital pin where the sensor is connected
        
        Returns:
            - float, temperature in celcius
        """
        # FIXME: add doc for exceptions
        self._assert_connected()
        self._validate_digital_pin(pin)
        cmd = "_ds18x20Rd\t%d" % (pin)

        response = self.send_cmd(cmd)  # raises CommandTimeout,InvalidCommand

        splitted_response = response.split(",")
        if splitted_response[0] == 'DS18X20_OK':
            if len(splitted_response) == 2:
                try:
                    temp_celcius = float(splitted_response[1]) / 16.0
                    return temp_celcius
                except ValueError:
                    raise(InvalidResponse("DS18X20_OK received, "
                        "but data couldn't be transformed to int"))
            else:
                raise(InvalidResponse("DS18X20_OK received, but without data"))

        raise(InvalidResponse(splitted_response[0]))

    ds18x20_read.arduino_function_name = '_ds18x20Rd'
    ds18x20_read.arduino_code = textwrap.dedent("""
        void _ds18x20Rd()
        {
            int pin = atoi(received_parameters[1]);
            OneWire ds(pin);
            byte i;
            byte present = 0;
            byte type_s;
            byte data[12];
            byte addr[8];
            
            if ( !ds.search(addr))
            {
                send_char_array_response("DS18X20_NO_MORE_ADDRESSES");
                return;
            }
            
            if (OneWire::crc8(addr, 7) != addr[7])
            {
                send_char_array_response("DS18X20_CRC_INVALID");
                return;
            }
            
            // the first ROM byte indicates which chip
            switch (addr[0])
            {
                case 0x10:
                    type_s = 1;
                    break;
                case 0x28:
                    type_s = 0;
                    break;
                case 0x22:
                    type_s = 0;
                    break;
                default:
                    send_char_array_response("DS18X20_DEVICE_NOT_OF_FAMILY");
                    return;
            }
            
            ds.reset();
            ds.select(addr);
            ds.write(0x44, 1); // start conversion, with parasite power on at the end
            
            delay(1000);     // maybe 750ms is enough, maybe not
            // we might do a ds.depower() here, but the reset will take care of it.
            
            present = ds.reset();
            ds.select(addr);
            ds.write(0xBE); // Read Scratchpad
            
            for ( i = 0; i < 9; i++) {           // we need 9 bytes
                data[i] = ds.read();
            }
            
            // Convert the data to actual temperature
            // because the result is a 16 bit signed integer, it should
            // be stored to an "int16_t" type, which is always 16 bits
            // even when compiled on a 32 bit processor.
            int16_t raw = (data[1] << 8) | data[0];
            if (type_s) {
                raw = raw << 3; // 9 bit resolution default
                if (data[7] == 0x10) {
                    // "count remain" gives full 12 bit resolution
                    raw = (raw & 0xFFF0) + 12 - data[6];
                }
            } else {
                byte cfg = (data[4] & 0x60);
                // at lower res, the low bits are undefined, so let's zero them
                if (cfg == 0x00) raw = raw & ~7;  // 9 bit resolution, 93.75 ms
                else if (cfg == 0x20) raw = raw & ~3; // 10 bit res, 187.5 ms
                else if (cfg == 0x40) raw = raw & ~1; // 11 bit res, 375 ms
                //// default is 12 bit resolution, 750 ms conversion time
            }
            Serial.print("DS18X20_OK,");
            Serial.print(raw);
            Serial.print("\\n");
            return;

            //celsius = (float)raw / 16.0;
            //fahrenheit = celsius * 1.8 + 32.0;
        }
        """)

    ds18x20_read.arduino_header = textwrap.dedent("""
        #include "OneWire.h"
        """)

    #===========================================================================
    # Energy Monitor
    #===========================================================================

    @synchronized(ARDUINO_LOCK)
    def energyMonitorSetup(self, v_pin, v_calibration, v_phase_shift, c_pin, c_calibration):
        """
        Setup energy monitor.
        
        Parameters:
            - v_pin (int): xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
            - v_calibration (float): xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
            - v_phase_shift (float): xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
            - c_pin (int): xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
            - c_calibration (float): xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        """
        # FIXME: add doc for exceptions
        self._assert_connected()
        self._validate_digital_pin(v_pin)
        self._validate_digital_pin(c_pin)

        cmd = "_emonStp\t%d\t%f\t%f\t%d\t%f" % (v_pin, v_calibration, v_phase_shift,
            c_pin, c_calibration)

        response = self.send_cmd(cmd)  # raises CommandTimeout,InvalidCommand

        self.status_tracker.set_for_library(v_pin, digital=False, library='EnergyMonitor/v_pin')
        self.status_tracker.set_for_library(c_pin, digital=False, library='EnergyMonitor/c_pin')

        splitted_response = response.split(",")
        if splitted_response[0] == 'EMON_S_OK':
            return splitted_response[0]

        raise(InvalidResponse(splitted_response[0]))

    energyMonitorSetup.arduino_function_name = '_emonStp'
    energyMonitorSetup.arduino_code = textwrap.dedent("""
        void _emonStp()
        {
            int v_pin = atoi(received_parameters[1]);
            float v_calibration = atof(received_parameters[2]);
            float v_phase_shift = atof(received_parameters[3]);
            int c_pin = atoi(received_parameters[4]);
            float c_calibration = atof(received_parameters[5]);

            // emon1.voltage(2, 225.00, 1.7);  // Voltage: input pin, calibration, phase_shift
            // emon1.current(1, 111.1);       // Current: input pin, calibration.

            emon.voltage(v_pin, v_calibration, v_phase_shift);
            emon.current(c_pin, c_calibration);

            Serial.print("EMON_S_OK");
            Serial.print("\\n");
            return;
        }
        """)

    energyMonitorSetup.arduino_globals = textwrap.dedent("""
        EnergyMonitor emon;
        """)

    energyMonitorSetup.arduino_header = textwrap.dedent("""
        #include "EmonLib.h"
        """)

    # --------------------

    @synchronized(ARDUINO_LOCK)
    def energyMonitorRead(self, no_wl, timeout):
        """
        Read energy monitor values.
        
        Parameters:
            - no_wl (int): first parameter for `calcVI()` function
            - timeout (int): second parameter for `calcVI()` function
        
        Returns:
            - float, realPower
            - float, apparentPower
            - float, powerFactor
            - float, Vrms
            - float, Irms
        """
        # FIXME: add doc for exceptions
        self._assert_connected()
        cmd = "_emonRd\t%d\t%d" % (int(no_wl), int(timeout))

        response = self.send_cmd(cmd)  # raises CommandTimeout,InvalidCommand

        splitted_response = response.split(",")
        if splitted_response[0] == 'EMON_R_OK':
            if len(splitted_response) == 6:
                try:
                    realPower, apparentPower, powerFactor, Vrms, Irms = (
                        float(splitted_response[1]),
                        float(splitted_response[2]),
                        float(splitted_response[3]),
                        float(splitted_response[4]),
                        float(splitted_response[5]),
                    )

                    self.status_tracker.set_lib_read_value('EnergyMonitor/v_pin', {
                        'realPower': realPower,
                        'apparentPower': apparentPower,
                        'powerFactor': powerFactor,
                        'Vrms': Vrms,
                        'Irms': Irms,
                    })

                    return (
                        realPower,
                        apparentPower,
                        powerFactor,
                        Vrms,
                        Irms,
                    )
                except ValueError:
                    self.status_tracker.set_lib_read_value(None)
                    raise(InvalidResponse("EMON_R_OK received, "
                        "but data couldn't be transformed to float"))
            else:
                self.status_tracker.set_lib_read_value(None)
                raise(InvalidResponse("EMON_R_OK received, "
                    "but without the expected number of data"))

        self.status_tracker.set_lib_read_value(None)
        raise(InvalidResponse(splitted_response[0]))

    energyMonitorRead.arduino_function_name = '_emonRd'
    energyMonitorRead.arduino_code = textwrap.dedent("""
        void _emonRd()
        {
            int no_wl = atoi(received_parameters[1]);
            int timeout = atoi(received_parameters[2]);

            emon.calcVI(no_wl, timeout);         // Calculate all. No.of wavelengths, time-out

            // emon1.serialprint();           // Print out all variables
            // float realPower = emon1.realPower;        //extract Real Power into variable
            // float apparentPower = emon1.apparentPower;    //extract Apparent Power into variable
            // float powerFActor = emon1.powerFactor;      //extract Power Factor into Variable
            // float supplyVoltage = emon1.Vrms;             //extract Vrms into Variable
            // float Irms = emon1.Irms;             //extract Irms into Variable

            Serial.print("EMON_R_OK,");
            Serial.print(emon.realPower);
            Serial.print(",");
            Serial.print(emon.apparentPower);
            Serial.print(",");
            Serial.print(emon.powerFactor);
            Serial.print(",");
            Serial.print(emon.Vrms);
            Serial.print(",");
            Serial.print(emon.Irms);
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
