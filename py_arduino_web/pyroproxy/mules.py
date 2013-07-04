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

import datetime
import time
import subprocess

from py_arduino import HIGH, INPUT, LOW
from py_arduino_web.pyroproxy.utils import BasePyroMain


class MuleDigitalPinMonitor(BasePyroMain):
    """
    TODO: add documentation

    Example: See `examples/bg_log_change_on_digital_pin.py`
    """

    pin = None
    script_on_high = None
    script_on_low = None
    wait_after_change = 0.1
    wait_if_nothing_changed = 0.5

    def add_options(self):
        super(MuleDigitalPinMonitor, self).add_options()
        self.parser.set_defaults(info=True, dont_check_pyro_server=True,
            wait_until_pyro_server_is_up=True)

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

    def bg_setup(self, options, args, arduino):
        self.logger.debug("Setting pinMode() on %s", self.pin)
        arduino.pinMode(self.pin, INPUT)
        arduino.digitalWrite(self.pin, HIGH)

    def bg_loop(self, options, args, arduino):
        last_value = arduino.digitalRead(self.pin)
        self.logger.debug("Initial value: %s", last_value)
        while True:
            new_value = arduino.digitalRead(self.pin)
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

    def run(self, options, args, arduino):
        self.logger.info("Starting on pin: %s", self.pin)
        if self.pin is None:
            self.logger.error("You must set the PIN to a valid integer...")
            self.logger.error("(will halt this mule for an hour)")
            time.sleep(60 * 60)

        if not arduino.is_connected():
            self.logger.debug("Arduino is not connected...")
            while not arduino.is_connected():
                self.logger.info("Waiting until connected...")
                time.sleep(5)
            self.logger.info("Connected!")

        ## setup()

        try:
            self.logger.debug("Calling self.bg_setup()")
            self.bg_setup(options, args, arduino)
        except:
            self.logger.exception("Error detected when called bg_setup()")
            return

        ## loop()

        try:
            self.logger.debug("Calling self.bg_loop()")
            self.bg_loop(options, args, arduino)
        except:
            self.logger.exception("Error detected in loop")
            return


class MuleDigitalPinMonitorWithBounceControl(MuleDigitalPinMonitor):
    """
    TODO: add documentation

    Example: See `examples/bg_log_change_on_digital_pin_with_bounce_control.py`
    """

    bounce_control_time = 2.0  # in seconds

    def bg_loop(self, options, args, arduino):
        bounce_control_start = None
        last_value = arduino.digitalRead(self.pin)
        self.logger.debug("Initial value: %s", last_value)

        while True:
            new_value = arduino.digitalRead(self.pin)
            self.logger.debug("Read value: %s", new_value)

            if new_value != last_value:
                #===============================================================
                # Value changed
                #===============================================================
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
                #===============================================================
                # Value hasn't changed
                #===============================================================
                if bounce_control_start is not None:
                    self.logger.debug("Ignored change in value (bounce control)")
                    bounce_control_start = None  # reset bounce control
                if self.wait_if_nothing_changed:
                    time.sleep(self.wait_if_nothing_changed)
