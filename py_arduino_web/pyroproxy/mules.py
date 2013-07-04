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

import time
import subprocess

from py_arduino import HIGH, INPUT, LOW
from py_arduino_web.pyroproxy.utils import BasePyroMain


"""
#===============================================================================
# Example - How to use MuleDigitalPinMonitor
#===============================================================================

See `examples/bg_log_change_on_digital_pin_a.py`

"""


class MuleDigitalPinMonitor(BasePyroMain):

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
        if new_value == HIGH:
            if self.script_on_high:
                subprocess.call(self.script_on_high, shell=True)
        if new_value == LOW:
            if self.script_on_low:
                subprocess.call(self.script_on_low, shell=True)

    def bg_setup(self, options, args, arduino):
        arduino.pinMode(self.pin, INPUT)
        arduino.digitalWrite(self.pin, HIGH)

    def bg_loop(self, options, args, arduino):
        last_value = arduino.digitalRead(self.pin)
        while True:
            value = arduino.digitalRead(self.pin)
            if value != last_value:
                # Value changed
                last_value = value
                self.value_changed(value)
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
            while not arduino.is_connected():
                self.logger.info("Waiting until connected...")
                time.sleep(5)
            self.logger.info("Connected!")

        ## setup()

        try:
            self.bg_setup(options, args, arduino)
        except:
            self.logger.exception("Error detected when called bg_setup()")
            return

        ## loop()

        try:
            self.bg_loop(options, args, arduino)
        except:
            self.logger.exception("Error detected in loop")
            return
