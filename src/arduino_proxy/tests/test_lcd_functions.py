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

from arduino_proxy.main_utils import default_main

def main():
    options, args, proxy = default_main() # pylint: disable=W0612
    try:
        print "Clearing LCD", proxy.lcdClear()
        raw_input("Press any key to continue...")
        
        print "'Hello, world!' on row 0", proxy.lcdMessage("Hello, world!")
        raw_input("Press any key to continue...")

        print "'Hello, world!' on row 0", proxy.lcdMessage(["Hello, world!"])
        raw_input("Press any key to continue...")

        print "'Hello, world!' on row 0, 'bye bye world' on line 1", \
            proxy.lcdMessage(["Hello, world!", "bye bye world"])
        raw_input("Press any key to continue...")
        
        print "Filling screen with letters and numbers"
        for a_char in ['a', 'b', 'c', 'x', 'y', 'z']:
            proxy.lcdMessage([a_char*16, a_char*16])
            time.sleep(0.1)
        raw_input("Press any key to continue...")

        print "Moving an @"
        for i in range(0, 32):
            proxy.lcdWrite("@", i%16, i/16, clear_lcd=True) # msg, col, row
            time.sleep(0.2)
        raw_input("Press any key to continue...")

    except KeyboardInterrupt:
        print ""
    finally:
        proxy.close()

if __name__ == '__main__':
    main()
