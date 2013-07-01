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
# EXAMPLE - Reads the temperature using a LM35 on analog pin 0
#===============================================================================

To run this example:

    $ python -m examples.read_lm35 /dev/ttyACM0

or, if you want to see what's going on:

    $ python -m examples.read_lm35 --info /dev/ttyACM0

or, if you want to see LOT of debug messages:

    $ python -m examples.read_lm35 --debug /dev/ttyACM0

#===============================================================================
# NOTE: remember to load the virtualenv before running this:
#===============================================================================

    $ . virtualenv/bin/activate

"""

import logging

from py_arduino import PyArduino
from py_arduino.main_utils import BaseMain

PIN = 0

logger = logging.getLogger(__name__)


class Main(BaseMain):

    def run(self, options, args, arduino):
        assert isinstance(arduino, PyArduino)
        while True:
            # Load 11 values
            values = [arduino.analogRead(PIN) for _ in range(0, 11)]
            # Use the MEDIAN
            value = values[(len(values) / 2)]
            # Do the math
            temp = (5.0 * value * 100.0) / 1024.0
            # Print
            print("PIN {0} -> analog read: {1:4} -> Temp: {2:3.2f} C".format(PIN, value, temp))

if __name__ == '__main__':
    Main().start()
