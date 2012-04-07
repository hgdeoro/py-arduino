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
SRC_DIR = os.path.split(os.path.realpath(__file__))[0] # SRC_DIR/arduino_proxy/tests
SRC_DIR = os.path.split(SRC_DIR)[0] # SRC_DIR/arduino_proxy
SRC_DIR = os.path.split(SRC_DIR)[0] # SRC_DIR
sys.path.append(os.path.abspath(SRC_DIR))

from arduino_proxy import ArduinoProxy, InvalidCommand, CommandTimeout, InvalidResponse
from arduino_proxy.main_utils import default_main


def main(): # pylint: disable=R0915
    _, _, proxy = default_main() # pylint: disable=W0612
    try:
        print "getFreeMemory() -> %s" % str(proxy.getFreeMemory())
        print "enableDebug() -> %s" % str(proxy.enableDebug())
        print "disableDebug() -> %s" % str(proxy.disableDebug())
        print "validateConnection() -> %s" % str(proxy.validateConnection())
        print "ping() -> %s" % str(proxy.ping())
        print "pinMode() -> %s" % str(proxy.pinMode(13, ArduinoProxy.OUTPUT))
        print "analogRead() -> %s" % str(proxy.analogRead(0))
        print "analogWrite() -> %s" % str(proxy.analogWrite(0, 128))
        print "digitalRead() -> %s" % str(proxy.digitalRead(0))
        print "digitalWrite() -> %s" % str(proxy.digitalWrite(0, ArduinoProxy.HIGH))
        print "digitalRead() -> %s" % str(proxy.digitalRead(0))
        print "delay() -> %s" % str(proxy.delay(1))
        print "delayMicroseconds() -> %s" % str(proxy.delayMicroseconds(1))
        print "millis() -> %s " % str(proxy.millis())
        print "micros() -> %s" % str(proxy.micros())
        print "shiftOut() -> %s" % str(proxy.shiftOut(10, 11, ArduinoProxy.LSBFIRST, 255,
            set_pin_mode=True))
        
        #define RETURN_OK 0
        #define READ_ONE_PARAM_NEW_LINE_FOUND 7
        #define READ_ONE_PARAM_EMPTY_RESPONSE 1
        #define READ_ONE_PARAM_ERROR_PARAMETER_TOO_LARGE 2
        #define READ_PARAMETERS_ERROR_TOO_MANY_PARAMETERS 3
        #define UNEXPECTED_RESPONSE_FROM_READ_ONE_PARAM 4
        #define UNEXPECTED_RESPONSE_FROM_READ_PARAMETERS 5
        #define FUNCTION_NOT_FOUND 6
        
        try:
            print "Check for READ_ONE_PARAM_ERROR_PARAMETER_TOO_LARGE"
            proxy.send_cmd("laaaarge_meeeethod_" * 10)
            assert False, "The previous line should raise an exception!"
        except InvalidCommand, exception:
            # READ_ONE_PARAM_ERROR_PARAMETER_TOO_LARGE == 2
            print " +", exception
            assert exception.error_code == "2"

        try:
            print "Check for FUNCTION_NOT_FOUND"
            proxy.send_cmd("_nonexisting\tp1\tp2\tp3\tp4\tp5\tp6\tp7\tp8\tp9")
            assert False, "The previous line should raise an exception!"
        except InvalidCommand, exception:
            # FUNCTION_NOT_FOUND == 6
            print " +", exception
            assert exception.error_code == "6"
        
        try:
            print "Check for READ_PARAMETERS_ERROR_TOO_MANY_PARAMETERS"
            proxy.send_cmd("cmd\tp1\tp2\tp3\tp4\tp5\tp6\tp7\tp8\tp9\tp10")
            assert False, "The previous line should raise an exception!"
        except InvalidCommand, exception:
            # READ_PARAMETERS_ERROR_TOO_MANY_PARAMETERS == 3
            print " +", exception
            assert exception.error_code == "3"
        
        proxy.setTimeout(1)
        print "delay(500)"
        proxy.delay(500)
        
        print "delay(2000)"
        proxy.delay(2000)
        
        print "low level delay(500)"
        ret = proxy.send_cmd("%s\t500" % (proxy.delay.arduino_function_name))
        assert ret == "D_OK"
        
        print "low level delay(1500)"
        try:
            proxy.send_cmd("%s\t1500" % (proxy.delay.arduino_function_name))
            assert False, "The previous line should raise an exception!"
        except CommandTimeout, exception:
            print " +", exception.__class__
        
        try:
            # The INPUT buffer has the response from the timed-out delay()
            # Anything before a validateConnection() should fail.
            print "ping() -> %s" % str(proxy.ping())
            assert False, "The previous line should raise an exception!"
        except InvalidResponse, exception:
            pass
        
        print "Re-connecting after timeout. validateConnection() -> %s" % \
            str(proxy.validateConnection())
        
        # Now, the connection is valid again, ping() should work...
        print "ping() -> %s" % str(proxy.ping())
        
        print "getFreeMemory() -> %s" % str(proxy.getFreeMemory())
        
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Test streaming
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        # Test streaming of analog values
        for val in proxy.streamingAnalogRead(0, 10):
            print "streamingAnalogRead() -> %s" % str(val)
        
        # Test streaming of analog values
        for val in proxy.streamingDigitalRead(0, 10):
            print "streamingDigitalRead() -> %s" % str(val)
        
        print "validateConnection() -> %s" % str(proxy.validateConnection())
        print "millis() -> %s " % str(proxy.millis())
        # Finished!
        
    except KeyboardInterrupt:
        print ""
    except Exception:
        raise
    finally:
        proxy.close()

if __name__ == '__main__':
    main()
