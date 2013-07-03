#!/usr/bin/env python
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

"""
#===============================================================================
# EXAMPLE - Blinks the led on PIN 13
#===============================================================================

To run this example:

    $ python -m examples.blink_pin13 /dev/ttyACM0

or, if you want to see what's going on:

    $ python -m examples.blink_pin13 --info /dev/ttyACM0

or, if you want to see LOT of debug messages:

    $ python -m examples.blink_pin13 --debug /dev/ttyACM0

#===============================================================================
# NOTE 1: remember to load the virtualenv before running this:
#===============================================================================

    $ . virtualenv/bin/activate

"""

import time

from py_arduino import OUTPUT
from py_arduino.main_utils import BaseMain
from py_arduino.arduino import PyArduino, HIGH, LOW

PIN = 13


class Main(BaseMain):

    def run(self, options, args, arduino):
        assert isinstance(arduino, PyArduino)
        arduino.pinMode(PIN, OUTPUT)
        while True:
            print("PIN {0} -> HIGH".format(PIN))
            arduino.digitalWrite(PIN, HIGH)
            time.sleep(0.5)
            print("PIN {0} -> LOW".format(PIN))
            arduino.digitalWrite(PIN, LOW)
            time.sleep(0.5)

if __name__ == '__main__':
    Main().start()
