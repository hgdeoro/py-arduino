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
from py_arduino.arduino import PyArduino

"""
#===============================================================================
# EXAMPLE - Reads the temperature using a LM35 connected to analog pin 0
#===============================================================================

To run this example:

    $ python -m examples.read_ir --pin 3 /dev/ttyACM0


#===============================================================================
# NOTE: remember to load the virtualenv before running this:
#===============================================================================

    $ . virtualenv/bin/activate

"""

from py_arduino.main_utils import BaseMain


class Main(BaseMain):

    def add_options(self):
        super(Main, self).add_options()
        self.parser.add_option("--pin",
            action="store", dest="pin", default=0, type="int",
            help="Analog pin to read.")
        self.parser.add_option("--timeout",
            action="store", dest="timeout", default=2000, type="int",
            help="Timeout in milliseconds.")
        self.parser.add_option("--loop",
            action="store_true", dest="loop", default=False,
            help="Keep reading and printing the values.")

    def run(self, options, args, arduino):
        assert isinstance(arduino, PyArduino)
        while True:
            value = arduino.irRead(options.pin, options.timeout)
            print("IR: {0}").format(value)

            # Break the loop if --loop was not specified
            if not options.loop:
                break

if __name__ == '__main__':
    Main().start()
