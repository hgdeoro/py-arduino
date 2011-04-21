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

#
# To test this script, from the base directory of the project, run something like:
#
# env TTY_DEVICE=/dev/ttyACM0 ANALOG_PORT=0 src/arduino_proxy/tests/analog_read_lm35_munin.py
#
#

import os
import sys

# Setup PYTHONPATH
SRC_DIR = os.path.split(os.path.realpath(__file__))[0] # SRC_DIR/arduino_proxy/tests
SRC_DIR = os.path.split(SRC_DIR)[0] # SRC_DIR/arduino_proxy
SRC_DIR = os.path.split(SRC_DIR)[0] # SRC_DIR
sys.path.append(os.path.abspath(SRC_DIR))

from arduino_proxy import ArduinoProxy

def main():
    if len(sys.argv) == 1:
        tty_device = os.environ['TTY_DEVICE']
        analog_port = os.environ['ANALOG_PORT']
        proxy = ArduinoProxy(tty_device, 9600)
        value = proxy.analogRead(int(analog_port))
        print "temp.value %.2f" % ((5.0 * int(value) * 100.0)/1024.0)
    else:
        if sys.argv[1] == "config":
            print "graph_title Temperature"
            print "graph_args --vertical-label Temperature"
            print "graph_category arduino"
            print "temp.label Temperature"
            print "temp.type GAUGE"

if __name__ == '__main__':
    main()
