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

from datetime import datetime

# Setup PYTHONPATH
SRC_DIR = os.path.split(os.path.realpath(__file__))[0] # SRC_DIR/arduino_proxy/tests
SRC_DIR = os.path.split(SRC_DIR)[0] # SRC_DIR/arduino_proxy
SRC_DIR = os.path.split(SRC_DIR)[0] # SRC_DIR
sys.path.append(os.path.abspath(SRC_DIR))

from arduino_proxy import ArduinoProxy, InvalidCommand, CommandTimeout, InvalidResponse
from arduino_proxy.main_utils import default_main

def main(): # pylint: disable=R0915
    options, args, proxy = default_main() # pylint: disable=W0612
    analog_reads = (400, 1000, )
    try:
        #
        # streamingAnalogRead()
        #
        print "Initiating %d reads using analogRead()" % analog_reads[0]
        start_analogRead = datetime.now()
        for i in xrange(0, analog_reads[0]):
            proxy.analogRead(0)
        end_analogRead = datetime.now()
        
        print "Initiating %d reads using streamingAnalogRead()" % analog_reads[1]
        start_streamingAnalogRead = datetime.now()
        for i in proxy.streamingAnalogRead(0, analog_reads[1]):
            pass
        end_streamingAnalogRead = datetime.now()
        
        non_streaming = float(analog_reads[0])/(end_analogRead-start_analogRead).total_seconds()
        streaming = float(1000.0)/(end_streamingAnalogRead-start_streamingAnalogRead).total_seconds()
        print "analogRead() -> %f reads per second" % non_streaming
        print "streamingAnalogRead() ->  %f reads per second" % streaming
        print "speedup: X%0.2f" % (int(streaming/non_streaming))
        
        #
        # streamingDigitalRead()
        #
        print "Initiating %d reads using digitalRead()" % analog_reads[0]
        start_digitalRead = datetime.now()
        for i in xrange(0, analog_reads[0]):
            proxy.digitalRead(0)
        end_digitalRead = datetime.now()
        
        print "Initiating %d reads using streamingDigitalRead()" % analog_reads[1]
        start_streamingDigitalRead = datetime.now()
        for i in proxy.streamingDigitalRead(0, analog_reads[1]):
            pass
        end_streamingDigitalRead = datetime.now()
        
        non_streaming = float(analog_reads[0])/(end_digitalRead-start_digitalRead).total_seconds()
        streaming = float(1000.0)/(end_streamingDigitalRead-start_streamingDigitalRead).total_seconds()
        print "digitalRead() -> %f reads per second" % non_streaming
        print "streamingDigitalRead() ->  %f reads per second" % streaming
        print "speedup: X%0.2f" % (int(streaming/non_streaming))
        
    except KeyboardInterrupt:
        print ""
    except Exception:
        raise
    finally:
        proxy.close()

if __name__ == '__main__':
    main()
