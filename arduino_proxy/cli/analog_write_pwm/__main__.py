#!/usr/bin/env python
##-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
##    PyArduinoProxy - Access your Arduino from Python
##    Copyright (C) 2011-2012 - Horacio Guillermo de Oro <hgdeoro@gmail.com>
##
##    This file is part of PyArduinoProxy.
##
##    PyArduinoProxy is free software; you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation version 2.
##
##    PyArduinoProxy is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License version 2 for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with PyArduinoProxy; see the file LICENSE.txt.
##-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

from arduino_proxy.main_utils import default_main
from arduino_proxy.proxy import ArduinoProxy


def args_validator(parser, options, args): # pylint: disable=W0613
    if len(args) != 3:
        parser.error("must specified three argument: serial device, "
            "PWM digital port and value")


def main():
    _, args, proxy = default_main(
        optparse_usage="usage: %prog [options] serial_device pwm_digital_port value",
        args_validator=args_validator)

    pwm_digital_port = int(args[1])
    value = int(args[2])

    try:
        proxy.pinMode(pwm_digital_port, ArduinoProxy.OUTPUT)
        proxy.analogWrite(pwm_digital_port, value)
    except KeyboardInterrupt:
        print ""
    except Exception:
        raise
    finally:
        proxy.close()


if __name__ == '__main__':
    main()
