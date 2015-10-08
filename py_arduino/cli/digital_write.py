#!/usr/bin/env python
# Licensed under the Apache License, Version 2.0
# Copyright (C) 2011-2015 - Horacio Guillermo de Oro <hgdeoro@gmail.com>

"""
#===============================================================================
# <<Write a HIGH or a LOW value to a digital pin.>>
#     (http://arduino.cc/en/Reference/DigitalWrite)
#===============================================================================

To write HIGH to digital pin 3:

    $ python -m py_arduino.cli.digital_write /dev/ttyACM0 3 1

To write LOW to digital pin 8:

    $ python -m py_arduino.cli.digital_write /dev/ttyACM0 8 0

#===============================================================================
# NOTE: remember to load the virtualenv before running this:
#===============================================================================

    $ . virtualenv/bin/activate

"""

from py_arduino.main_utils import BaseMain
from py_arduino import HIGH, LOW, OUTPUT


class Main(BaseMain):
    optparse_usage = BaseMain.optparse_usage + " digital_pin value"
    num_args = BaseMain.num_args + 2

    def validate(self, options, args):
        super(Main, self).validate(options, args)
        value = int(args[2])
        if value not in (0, 1):
            self.parser.error("value must be 0 or 1")

    def run(self, options, args, arduino):
        digital_pin = int(args[1])
        value = int(args[2])
        assert value in (0, 1)

        arduino.pinMode(digital_pin, OUTPUT)
        if value == 0:
            arduino.digitalWrite(digital_pin, LOW)
        else:
            arduino.digitalWrite(digital_pin, HIGH)


if __name__ == '__main__':
    Main().start()
