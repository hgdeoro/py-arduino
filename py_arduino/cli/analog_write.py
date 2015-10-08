#!/usr/bin/env python
# Licensed under the Apache License, Version 2.0
# Copyright (C) 2011-2015 - Horacio Guillermo de Oro <hgdeoro@gmail.com>


from py_arduino.main_utils import BaseMain
from py_arduino import OUTPUT

"""
#===============================================================================
# <<Writes an analog value (PWM wave) to a pin>>
#     (from http://arduino.cc/en/Reference/analogWrite)
#===============================================================================

To write 128 to pin 3:

    $ python -m py_arduino.cli.analog_write /dev/ttyACM0 3 128

#===============================================================================
# NOTE: remember to load the virtualenv before running this:
#===============================================================================

    $ . virtualenv/bin/activate

"""


class Main(BaseMain):
    optparse_usage = BaseMain.optparse_usage + " pwm_digital_pin value"
    num_args = BaseMain.num_args + 2

    def run(self, options, args, arduino):
        pwm_digital_pin = int(args[1])
        value = int(args[2])
        # TODO: check that digital pin supports PWM
        arduino.pinMode(pwm_digital_pin, OUTPUT)
        arduino.analogWrite(pwm_digital_pin, value)


if __name__ == '__main__':
    Main().start()
