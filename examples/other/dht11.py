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

import os
import sys

# Setup PYTHONPATH
SRC_DIR = os.path.split(os.path.realpath(__file__))[0]  # SRC_DIR=EXAMPLE_DIR
SRC_DIR = os.path.split(SRC_DIR)[0]  # SRC_DIR=SRC_DIR/../
SRC_DIR = os.path.join(SRC_DIR, 'src')  # SRC_DIR
sys.path.append(os.path.abspath(SRC_DIR))

from py_arduino.main_utils import default_main


def args_validator(parser, options, args):  # pylint: disable=W0613
    if len(args) != 2:
        parser.error("must specified two argument: serial device and digital port")


def add_options_callback(parser):
    parser.add_option("--loop",
        action="store_true", dest="loop", default=False,
        help="Keep reading and printing the values.")


def main():
    options, args, arduino = default_main(
        optparse_usage="usage: %prog [options] serial_device digital_port",
        args_validator=args_validator,
        add_options_callback=add_options_callback)

    digital_port = int(args[1])

    try:
        while True:
            temp, hum = arduino.dht11_read(digital_port)
            print "Temp: {0}C - Hum: {1}%".format(
                temp, hum)
            if options.loop:
                arduino.delay(500)
            else:
                break
    except KeyboardInterrupt:
        print ""
    except Exception:
        raise
    finally:
        arduino.close()

if __name__ == '__main__':
    main()
