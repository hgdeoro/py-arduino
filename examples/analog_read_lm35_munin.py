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

#
# To test this script, from the base directory of the project, run something like:
#
# env TTY_DEVICE=/dev/ttyACM0 ANALOG_PORT=0 examples/analog_read_lm35_munin.py
#
#

import os
import sys

# Setup PYTHONPATH
SRC_DIR = os.path.split(os.path.realpath(__file__))[0] # SRC_DIR=EXAMPLE_DIR
SRC_DIR = os.path.split(SRC_DIR)[0] # SRC_DIR=SRC_DIR/../
SRC_DIR = os.path.join(SRC_DIR, 'src') # SRC_DIR
sys.path.append(os.path.abspath(SRC_DIR))

from arduino_proxy import ArduinoProxy

COUNT = 10

def main():
    if len(sys.argv) == 1:
        tty_device = os.environ['TTY_DEVICE']
        analog_port = os.environ['ANALOG_PORT']
        proxy = ArduinoProxy(tty_device, 9600)
        sum = 0.0
        for i in range(0, COUNT):
            value = proxy.analogRead(int(analog_port))
            value = ((5.0 * value * 100.0)/1024.0)
            sum = sum + value
        value = sum/float(COUNT)
        print "temp.value %.2f" % value
    else:
        if sys.argv[1] == "config":
            print "graph_title Temperature"
            print "graph_args --vertical-label Temperature"
            print "graph_category arduino"
            print "temp.label Temperature"
            print "temp.type GAUGE"

if __name__ == '__main__':
    main()
