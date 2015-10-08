#!/usr/bin/env python
# Licensed under the Apache License, Version 2.0
# Copyright (C) 2011-2015 - Horacio Guillermo de Oro <hgdeoro@gmail.com>

"""
#===============================================================================
# EXAMPLE - Reads the temperature using a LM35 (on analog pin 0 by default)
#  The pin can be specified using --pin
#===============================================================================

To run this example:

    $ python -m examples.read_lm35_advanced /dev/ttyACM0

or, if you connected the LM35 in other pin:

    $ python -m examples.read_lm35_advanced --pin 3 /dev/ttyACM0

or, if you want to see what's going on:

    $ python -m examples.read_lm35_advanced --info /dev/ttyACM0

or, if you want to see LOT of debug messages:

    $ python -m examples.read_lm35_advanced --debug /dev/ttyACM0

#===============================================================================
# NOTE: remember to load the virtualenv before running this:
#===============================================================================

    $ . virtualenv/bin/activate

"""

from py_arduino.arduino import PyArduino
from py_arduino.main_utils import BaseMain


class Main(BaseMain):

    def add_options(self):
        super(Main, self).add_options()
        self.parser.add_option("--pin",
            action="store", dest="pin", default=0, type="int",
            help="Analog pin to read.")
        self.parser.add_option("--loop",
            action="store_true", dest="loop", default=False,
            help="Keep reading and printing the values.")
        self.parser.add_option("--csv",
            action="store_true", dest="csv", default=False,
            help="Print values in CSV format.")

    def run(self, options, args, arduino):
        assert isinstance(arduino, PyArduino)
        if options.csv:
            # If CSV, print header
            print "pin,analog_read,temperature_celcius"

        while True:
            # Load 11 values
            values = [arduino.analogRead(options.pin) for _ in range(0, 11)]
            # Use the MEDIAN
            value = values[(len(values) / 2)]
            # Do the math
            temp = (5.0 * value * 100.0) / 1024.0

            # Print
            if options.csv:
                print("{0},{1},{2:3.2f}".format(options.pin, value, temp))
            else:
                print("PIN {0} -> analog read: {1:4} -> Temp: {2:3.2f} C".format(
                    options.pin, value, temp))

            # Break the loop if --loop was not specified
            if not options.loop:
                break

if __name__ == '__main__':
    Main().start()
