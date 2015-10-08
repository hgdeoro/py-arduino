#!/usr/bin/env python
# Licensed under the Apache License, Version 2.0
# Copyright (C) 2011-2015 - Horacio Guillermo de Oro <hgdeoro@gmail.com>

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
