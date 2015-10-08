#!/usr/bin/env python
# Licensed under the Apache License, Version 2.0
# Copyright (C) 2011-2015 - Horacio Guillermo de Oro <hgdeoro@gmail.com>

"""
#===============================================================================
# EXAMPLE - Reads the temperature using a LM35 connected to analog pin 0
#===============================================================================

To run this example:

    $ python -m examples.read_lm35_basic /dev/ttyACM0


#===============================================================================
# NOTE: remember to load the virtualenv before running this:
#===============================================================================

    $ . virtualenv/bin/activate

"""

from py_arduino.main_utils import BaseMain

PIN = 0


class Main(BaseMain):

    def run(self, options, args, arduino):
        value = arduino.analogRead(PIN)
        temp = (5.0 * value * 100.0) / 1024.0
        print("Temperature: {0:3.2f} C").format(temp)

if __name__ == '__main__':
    Main().start()
