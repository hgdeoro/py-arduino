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

from datetime import datetime

from . import setup_pythonpath

setup_pythonpath()

from py_arduino.main_utils import default_main


def main(): # pylint: disable=R0915
    _, _, arduino = default_main() # pylint: disable=W0612
    analog_reads = (400, 1000,)
    try:
        #
        # streamingAnalogRead()
        #
        print "Initiating %d reads using analogRead()" % analog_reads[0]
        start_analogRead = datetime.now()
        for i in xrange(0, analog_reads[0]): #@UnusedVariable
            arduino.analogRead(0)
        end_analogRead = datetime.now()
        analogRead_time = end_analogRead - start_analogRead

        print "Initiating %d reads using streamingAnalogRead()" % analog_reads[1]
        start_streamingAnalogRead = datetime.now()
        for i in arduino.streamingAnalogRead(0, analog_reads[1]): #@UnusedVariable
            pass
        end_streamingAnalogRead = datetime.now()
        streamingAnalogRead_time = end_streamingAnalogRead - start_streamingAnalogRead

        non_streaming = float(analog_reads[0]) / analogRead_time.total_seconds()
        streaming = float(1000.0) / streamingAnalogRead_time.total_seconds()
        print "analogRead() -> %f reads per second" % non_streaming
        print "streamingAnalogRead() ->  %f reads per second" % streaming
        print "speedup: X%0.2f" % (streaming / non_streaming)

        #
        # streamingDigitalRead()
        #
        print "Initiating %d reads using digitalRead()" % analog_reads[0]
        start_digitalRead = datetime.now()
        for i in xrange(0, analog_reads[0]): #@UnusedVariable
            arduino.digitalRead(0)
        end_digitalRead = datetime.now()
        digitalRead_time = end_digitalRead - start_digitalRead

        print "Initiating %d reads using streamingDigitalRead()" % analog_reads[1]
        start_streamingDigitalRead = datetime.now()
        for i in arduino.streamingDigitalRead(0, analog_reads[1]): #@UnusedVariable
            pass
        end_streamingDigitalRead = datetime.now()
        streamingDigitalRead_time = end_streamingDigitalRead - start_streamingDigitalRead

        non_streaming = float(analog_reads[0]) / digitalRead_time.total_seconds()
        streaming = float(1000.0) / streamingDigitalRead_time.total_seconds()
        print "digitalRead() -> %f reads per second" % non_streaming
        print "streamingDigitalRead() ->  %f reads per second" % streaming
        print "speedup: X%0.2f" % (streaming / non_streaming)

    except KeyboardInterrupt:
        print ""
    except Exception:
        raise
    finally:
        arduino.close()

if __name__ == '__main__':
    main()
