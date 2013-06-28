#!/usr/bin/env python
##-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
##    py-arduino - Access your Arduino from Python
##    Copyright (C) 2011-2012 - Horacio Guillermo de Oro <hgdeoro@gmail.com>
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

from py_arduino.main_utils import default_main
from py_arduino.proxy import HIGH, LOW, INPUT


def default_callback(value, options):
    if value == HIGH:
        if options.numerical:
            print "1"
        else:
            print "HIGH"
    elif value == LOW:
        if options.numerical:
            print "0"
        else:
            print "LOW"
    else:
        raise(Exception("Invalid value for a digital read: '%s'" % str(value)))


def args_validator(parser, options, args): # pylint: disable=W0613
    if len(args) != 2:
        parser.error("must specified two argument: serial device and digital port")


def add_options_callback(parser):
    parser.add_option("--loop",
        action="store_true", dest="loop", default=False,
        help="Keep reading and printing the values.")
    parser.add_option("--numerical",
        action="store_true", dest="numerical", default=False,
        help="Prints 1 or 0 instead of 'HIGH' and 'LOW'.")


def main(callback=default_callback):
    options, args, proxy = default_main(
        optparse_usage="usage: %prog [options] serial_device digital_port",
        args_validator=args_validator,
        add_options_callback=add_options_callback)

    digital_port = int(args[1])

    try:
        proxy.pinMode(digital_port, INPUT)
        while True:
            value = proxy.digitalRead(digital_port)
            callback(value, options)
            if not options.loop:
                break
    except KeyboardInterrupt:
        print ""
    except Exception:
        raise
    finally:
        proxy.close()


if __name__ == '__main__':
    main()
