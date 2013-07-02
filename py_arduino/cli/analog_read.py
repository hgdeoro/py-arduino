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

from py_arduino.main_utils import BaseMain

"""
#===============================================================================
# <<Reads the value from the specified analog pin>>
#     (from http://arduino.cc/en/Reference/AnalogRead)
#===============================================================================

To read the value of analog pin 3 one time:

    $ python -m py_arduino.cli.analog_read /dev/ttyACM0 3

To read the value of analog pni 3 for ever (ie: until Ctrl+C):

    $ python -m py_arduino.cli.analog_read --loop /dev/ttyACM0 3

#===============================================================================
# NOTE: remember to load the virtualenv before running this:
#===============================================================================

    $ . virtualenv/bin/activate

"""


class Main(BaseMain):
    optparse_usage = BaseMain.optparse_usage + " analog_pin"
    num_args = BaseMain.num_args + 1

    def add_options(self):
        super(Main, self).add_options()
        self.parser.add_option("--loop",
            action="store_true", dest="loop", default=False,
            help="Keep reading and printing the values.")

    def run(self, options, args, arduino):
        analog_pin = int(args[1])

        while True:
            value = arduino.analogRead(analog_pin)
            print value
            if not options.loop:
                break

if __name__ == '__main__':
    Main().start()
