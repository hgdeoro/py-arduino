#!/usr/bin/env python
# Licensed under the Apache License, Version 2.0
# Copyright (C) 2011-2015 - Horacio Guillermo de Oro <hgdeoro@gmail.com>

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
