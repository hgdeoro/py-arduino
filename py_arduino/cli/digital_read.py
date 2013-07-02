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
from py_arduino import HIGH, LOW, INPUT

"""
#===============================================================================
# <<Reads the value from a specified digital pin, either HIGH or LOW>>
#     (http://arduino.cc/en/Reference/DigitalRead)
#===============================================================================

To read the value of digital pin 5 one time:

    $ python -m py_arduino.cli.digital_read /dev/ttyACM0 5

To print 0 or 1 instead of LOW or HIGH:

    $ python -m py_arduino.cli.digital_read --numerical /dev/ttyACM0 5

#===============================================================================
# NOTE: remember to load the virtualenv before running this:
#===============================================================================

    $ . virtualenv/bin/activate

"""


class Main(BaseMain):
    optparse_usage = BaseMain.optparse_usage + " digital_port"
    num_args = BaseMain.num_args + 1

    def add_options(self):
        super(Main, self).add_options()
        self.parser.add_option("--loop",
            action="store_true", dest="loop", default=False,
            help="Keep reading and printing the values.")
        self.parser.add_option("--numerical",
            action="store_true", dest="numerical", default=False,
            help="Prints 1 or 0 instead of 'HIGH' and 'LOW'.")

    def run(self, options, args, arduino):
        digital_pin = int(args[1])
        arduino.pinMode(digital_pin, INPUT)
        while True:
            value = arduino.digitalRead(digital_pin)
            if value == HIGH:
                if options.numerical:
                    print "1"
                else:
                    print "HIGH"
            elif value == LOW:
                if options.numerical:
                    print "0"
                else:
                    print "LOW"
            else:
                raise(Exception("Invalid value for a digital read: '%s'" % str(value)))
            if not options.loop:
                break

if __name__ == '__main__':
    Main().start()
