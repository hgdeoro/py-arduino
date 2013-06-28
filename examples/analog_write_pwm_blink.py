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

#
# Run with:
#
# $ python -m examples.analog_write_pwm_blink --info /dev/ttyACM0 13
#

from py_arduino import OUTPUT
from py_arduino.main_utils import default_main


def args_validator(parser, options, args):  # pylint: disable=W0613
    if len(args) != 2:
        parser.error("must specified three argument: serial device, PWM digital port")


def main():
    USAGE = "usage: %prog [options] serial_device pwm_digital_port"
    _, args, arduino = default_main(optparse_usage=USAGE,
        args_validator=args_validator)

    pwm_digital_port = int(args[1])

    try:
        arduino.pinMode(pwm_digital_port, OUTPUT)
        while True:
            print "Going from 0 to 255..."
            for value in range(0, 256, 5):
                arduino.analogWrite(pwm_digital_port, value)
            print "Going from 255 to 0..."
            for value in range(255, -1, -5):
                arduino.analogWrite(pwm_digital_port, value)
    except KeyboardInterrupt:
        print ""
    except Exception:
        raise
    finally:
        arduino.close()

if __name__ == '__main__':
    main()
