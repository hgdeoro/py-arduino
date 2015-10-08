#!/usr/bin/env python
# Licensed under the Apache License, Version 2.0
# Copyright (C) 2011-2015 - Horacio Guillermo de Oro <hgdeoro@gmail.com>

import os
import sys

try:
    from py_arduino.main_utils import default_main
except ImportError:
    # Setup PYTHONPATH
    SRC_DIR = os.path.split(os.path.realpath(__file__))[0]  # SRC_DIR=BIN_DIR
    SRC_DIR = os.path.split(SRC_DIR)[0]  # SRC_DIR=SRC_DIR/../
    sys.path.append(os.path.abspath(SRC_DIR))
    from py_arduino.main_utils import default_main


def default_callback(value):
    print value


def args_validator(parser, options, args):  # pylint: disable=W0613
    if len(args) != 2:
        parser.error("must specified two argument: serial device and digital port")


def add_options_callback(parser):
    parser.add_option("--loop",
        action="store_true", dest="loop", default=False,
        help="Keep reading and printing the values.")


def main(callback):
    options, args, arduino = default_main(
        optparse_usage="usage: %prog [options] serial_device digital_port",
        args_validator=args_validator,
        add_options_callback=add_options_callback)

    digital_port = int(args[1])

    try:
        while True:
            value = arduino.ds18x20_read(digital_port)
            callback(value)
            if not options.loop:
                break
    except KeyboardInterrupt:
        print ""
    except Exception:
        raise
    finally:
        arduino.close()

if __name__ == '__main__':
    main(default_callback)
