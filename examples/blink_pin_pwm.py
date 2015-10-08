#!/usr/bin/env python
# Licensed under the Apache License, Version 2.0
# Copyright (C) 2011-2015 - Horacio Guillermo de Oro <hgdeoro@gmail.com>

"""
#===============================================================================
# EXAMPLE - Blinks a led using PWM
#===============================================================================

To run this example:

    $ python -m examples.blink_pin_pwm /dev/ttyACM0 13

or, if you want to see what's going on:

    $ python -m examples.blink_pin_pwm --info /dev/ttyACM0 13

or, if you want to see LOT of debug messages:

    $ python -m examples.blink_pin_pwm --debug /dev/ttyACM0 13

#===============================================================================
# NOTE 1: remember to load the virtualenv before running this:
#===============================================================================

    $ . virtualenv/bin/activate

"""

from py_arduino import OUTPUT
from py_arduino.main_utils import BaseMain


class Main(BaseMain):
    optparse_usage = BaseMain.optparse_usage + " pwm_digital_pin"
    num_args = BaseMain.num_args + 1

    def run(self, options, args, arduino):
        pwm_digital_pin = int(args[1])  # args[0] -> serial port

        arduino.pinMode(pwm_digital_pin, OUTPUT)
        while True:
            print "Going from 0 to 255..."
            for value in range(0, 256, 5):
                arduino.analogWrite(pwm_digital_pin, value)
            print "Going from 255 to 0..."
            for value in range(255, -1, -5):
                arduino.analogWrite(pwm_digital_pin, value)

if __name__ == '__main__':
    Main().start()
