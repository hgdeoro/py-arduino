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
import time

# Setup PYTHONPATH
SRC_DIR = os.path.split(os.path.realpath(__file__))[0] # SRC_DIR/arduino_proxy/tests
SRC_DIR = os.path.split(SRC_DIR)[0] # SRC_DIR/arduino_proxy
SRC_DIR = os.path.split(SRC_DIR)[0] # SRC_DIR
sys.path.append(os.path.abspath(SRC_DIR))

from arduino_proxy import ArduinoProxy
from arduino_proxy.tests import default_main

def args_validator(parser, options, args): # pylint: disable=W0613
    if len(args) != 2:
        parser.error("must specified two argument: serial device and digital port")

def main():
    options, args, proxy = default_main(optparse_usage=\
        "usage: %prog [options] serial_device digital_port", args_validator=args_validator)
    
    digital_port = int(args[1])
    
    try:
        proxy.pinMode(digital_port, ArduinoProxy.OUTPUT)
        while True:
            proxy.digitalWrite(digital_port, ArduinoProxy.HIGH)
            time.sleep(0.5)
            proxy.digitalWrite(digital_port, ArduinoProxy.LOW)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print ""
    except Exception:
        raise
    finally:
        proxy.close()

if __name__ == '__main__':
    main()
