# Licensed under the Apache License, Version 2.0
# Copyright (C) 2011-2015 - Horacio Guillermo de Oro <hgdeoro@gmail.com>

import datetime
import time
import subprocess

from py_arduino import HIGH, INPUT, LOW
from py_arduino_web.pyroproxy.utils import BasePyroMain, get_status_tracker


class MulePinReader(BasePyroMain):
    """Base class for background tasks"""

    def add_options(self):
        super(MulePinReader, self).add_options()
        self.parser.add_option("--pin",
                               dest="pin",
                               help="Pin to monitor.")
        self.parser.add_option("--description",
                               dest="description",
                               help="Description to use for background task.")
        self.parser.set_defaults(info=True,
                                 dont_check_pyro_server=True,
                                 wait_until_pyro_server_is_up=True)

    def bg_setup(self, arduino):
        raise (NotImplemented())

    def bg_loop(self, arduino):
        raise (NotImplemented())

    def run(self, arduino):
        pin = int(self.options.pin)
        self.logger.info("Starting on pin: %s", pin)

        if not arduino.is_connected():
            self.logger.debug("Arduino is not connected...")
            while not arduino.is_connected():
                self.logger.info("Waiting until connected...")
                time.sleep(5)
            self.logger.info("Connected!")

        # setup()

        try:
            self.logger.debug("Calling self.bg_setup()")
            self.bg_setup(arduino)
        except:
            self.logger.exception("Error detected when called bg_setup()")
            return

        # loop()

        try:
            self.logger.debug("Calling self.bg_loop()")
            self.bg_loop(arduino)
        except:
            self.logger.exception("Error detected in loop")
            return


class MuleAnalogPinLogger(MulePinReader):
    """
    Simple background task that reads a analog pin and log its value
    """

    wait_between_reads = 1.0

    def bg_setup(self, arduino):
        pin = int(self.options.pin)
        self.logger.debug("Setting pinMode() on %s", pin)
        status_tracker = get_status_tracker()
        reserved_ok = status_tracker.reserve_pins([[pin, False]],
                                                  self.options.description or "MuleAnalogPinLogger on pin {}".format(
                                                      pin))
        assert reserved_ok, "Couldn't reserve pin"

    def bg_loop(self, arduino):
        pin = int(self.options.pin)
        while True:
            self.logger.debug("Read value: %s", arduino.analogRead(pin))
            time.sleep(self.wait_between_reads)


class MuleDigitalPinMonitor(MulePinReader):
    """
    TODO: add documentation

    Example: See `examples/bg_log_change_on_digital_pin.py`
    """

    script_on_high = None
    script_on_low = None
    wait_after_change = 0.1
    wait_if_nothing_changed = 0.5

    def value_changed(self, new_value):
        self.logger.debug("Value changed: %s", new_value)
        if new_value == HIGH:
            if self.script_on_high:
                self.logger.debug("Calling script: %s", self.script_on_high)
                subprocess.call(self.script_on_high, shell=True)
        if new_value == LOW:
            if self.script_on_low:
                self.logger.debug("Calling script: %s", self.script_on_low)
                subprocess.call(self.script_on_low, shell=True)

    def bg_setup(self, arduino):
        pin = int(self.options.pin)
        self.logger.debug("Setting pinMode() on %s", pin)
        status_tracker = get_status_tracker()
        reserved_ok = status_tracker.reserve_pins([[pin, True]],
                                                  self.options.description or "MuleDigitalPinMonitor on pin {}".format(
                                                      pin))
        assert reserved_ok, "Couldn't reserve pin"
        arduino.pinMode(pin, INPUT)
        arduino.digitalWrite(pin, HIGH)

    def bg_loop(self, arduino):
        pin = int(self.options.pin)
        last_value = arduino.digitalRead(pin)
        self.logger.debug("Initial value: %s", last_value)
        while True:
            new_value = arduino.digitalRead(pin)
            self.logger.debug("Read value: %s", new_value)
            if new_value != last_value:
                # Value changed
                last_value = new_value
                self.value_changed(new_value)
                time.sleep(self.wait_after_change)
            else:
                # Value hasn't changed
                if self.wait_if_nothing_changed:
                    time.sleep(self.wait_if_nothing_changed)


class MuleDigitalPinMonitorWithBounceControl(MuleDigitalPinMonitor):
    """
    TODO: add documentation

    Example: See `examples/bg_log_change_on_digital_pin_with_bounce_control.py`
    """

    bounce_control_time = 2.0  # in seconds

    def bg_loop(self, arduino):
        bounce_control_start = None
        last_value = arduino.digitalRead(self.pin)
        self.logger.debug("Initial value: %s", last_value)

        while True:
            new_value = arduino.digitalRead(self.pin)
            self.logger.debug("Read value: %s", new_value)

            if new_value != last_value:
                # ===============================================================
                # Value changed
                # ===============================================================
                if bounce_control_start is None:
                    bounce_control_start = datetime.datetime.now()
                    self.logger.debug("Starting bounce control: %s -> %s", last_value, new_value)

                time_diff = (datetime.datetime.now() - bounce_control_start).total_seconds()
                if time_diff > self.bounce_control_time:
                    # We must 'commit' the change
                    self.logger.debug("New value wasn't a bouce! It's the same after %s secs. "
                                      "Taking new value: %s", time_diff, new_value)
                    last_value = new_value
                    self.value_changed(new_value)
                    bounce_control_start = None  # reset bounce control

                time.sleep(self.wait_after_change)

            else:
                # ===============================================================
                # Value hasn't changed
                # ===============================================================
                if bounce_control_start is not None:
                    self.logger.debug("Ignored change in value (bounce control)")
                    bounce_control_start = None  # reset bounce control
                if self.wait_if_nothing_changed:
                    time.sleep(self.wait_if_nothing_changed)
