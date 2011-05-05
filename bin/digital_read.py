#!/usr/bin/env python
##-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
##    Py-Arduino-Proxy - Access your Arduino from Python
##    Copyright (C) 2011 - Horacio Guillermo de Oro <hgdeoro@gmail.com>
##
##    This file is part of Py-Arduino-Proxy.
##
##    Py-Arduino-Proxy is free software; you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation version 2.
##
##    Py-Arduino-Proxy is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License version 2 for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with Py-Arduino-Proxy; see the file LICENSE.txt.
##-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

import os
import sys

# Setup PYTHONPATH
SRC_DIR = os.path.split(os.path.realpath(__file__))[0] # SRC_DIR=BIN_DIR
SRC_DIR = os.path.split(SRC_DIR)[0] # SRC_DIR=SRC_DIR/../
SRC_DIR = os.path.join(SRC_DIR, 'src') # SRC_DIR
sys.path.append(os.path.abspath(SRC_DIR))

from arduino_proxy.main_utils import default_main
from arduino_proxy import ArduinoProxy

def default_callback(value, options):
    if value == ArduinoProxy.HIGH:
        if options.numerical:
            print "1"
        else:
            print "HIGH"
    elif value == ArduinoProxy.LOW:
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

def main(callback):
    options, args, proxy = default_main(optparse_usage=\
        "usage: %prog [options] serial_device digital_port", args_validator=args_validator,
        add_options_callback=add_options_callback)
    
    digital_port = int(args[1])
    
    try:
        proxy.pinMode(digital_port, ArduinoProxy.INPUT)
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
    main(default_callback)
