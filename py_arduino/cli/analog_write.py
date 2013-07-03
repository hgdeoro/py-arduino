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
