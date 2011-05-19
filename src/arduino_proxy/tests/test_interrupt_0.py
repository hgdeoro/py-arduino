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
import traceback

# Setup PYTHONPATH
SRC_DIR = os.path.split(os.path.realpath(__file__))[0] # SRC_DIR/arduino_proxy/tests
SRC_DIR = os.path.split(SRC_DIR)[0] # SRC_DIR/arduino_proxy
SRC_DIR = os.path.split(SRC_DIR)[0] # SRC_DIR
sys.path.append(os.path.abspath(SRC_DIR))

from arduino_proxy import ArduinoProxy, InvalidCommand, CommandTimeout, ArduinoProxyException
from arduino_proxy.main_utils import default_main

def main():
    options, args, proxy = default_main()
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
        proxy.pinMode(2, ArduinoProxy.INPUT) # INT_0
        proxy.delay(200)
        
        print "proxy.digitalWrite(2,HIGH) -> pullup resistor"
        proxy.digitalWrite(2, ArduinoProxy.HIGH) # INT_0 -> pullup resistor
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
                print "validate_connection() -> %s" % str(proxy.validate_connection())
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
