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

import os
import sys
import traceback
from arduino_proxy.proxy import INPUT, HIGH

# Setup PYTHONPATH
SRC_DIR = os.path.split(os.path.realpath(__file__))[0] # SRC_DIR/arduino_proxy/tests
SRC_DIR = os.path.split(SRC_DIR)[0] # SRC_DIR/arduino_proxy
SRC_DIR = os.path.split(SRC_DIR)[0] # SRC_DIR
sys.path.append(os.path.abspath(SRC_DIR))

from arduino_proxy import ArduinoProxy, InvalidCommand, ArduinoProxyException
from arduino_proxy.main_utils import default_main


def main():
    options, _, proxy = default_main() # pylint: disable=W0612
    try:
        if options.debug:
            proxy.enableDebug()
        
        #    LOW to trigger the interrupt whenever the pin is low,
        #    CHANGE to trigger the interrupt whenever the pin changes value
        #    RISING to trigger when the pin goes from low to high,
        #    FALLING for when the pin goes from high to low.
        #
        #    ATTACH_INTERRUPT_MODE_LOW = 'L'
        #    ATTACH_INTERRUPT_MODE_CHANGE = 'C'
        #    ATTACH_INTERRUPT_MODE_RISING = 'R'
        #    ATTACH_INTERRUPT_MODE_FALLING = 'F'
        
        print "proxy.pinMode()"
        proxy.pinMode(2, INPUT) # INT_0
        proxy.delay(200)
        
        print "proxy.digitalWrite(2,HIGH) -> pullup resistor"
        proxy.digitalWrite(2, HIGH) # INT_0 -> pullup resistor
        proxy.delay(200)
        
        print "proxy.watchInterrupt(0) -> interrupt occurs when pin 2 become LOW."
        print " +", proxy.watchInterrupt(0, ArduinoProxy.ATTACH_INTERRUPT_MODE_LOW)
        
        while True:
            try:
                if proxy.getInterruptMark(0):
                    print " + INTERRUPT 0 has ocurred"
            except InvalidCommand:
                print " + Ignoring InvalidCommand! This is normal when working with interrupts."
            except ArduinoProxyException:
                traceback.print_exc()
                print "##"
                print "## ERROR DETECTED!"
                print "##"
                print "validateConnection() -> %s" % str(proxy.validateConnection())
                print "enableDebug() -> %s" % str(proxy.enableDebug())
                print "ping() -> %s" % str(proxy.ping())
                print ""
                print "Continuing..."
                print ""
                
    except KeyboardInterrupt:
        print ""
    finally:
        proxy.close()

if __name__ == '__main__':
    main()
