#!/usr/bin/env python
# Licensed under the Apache License, Version 2.0
# Copyright (C) 2011-2015 - Horacio Guillermo de Oro <hgdeoro@gmail.com>

from datetime import datetime

from py_arduino.main_utils import BaseMain

NON_STREAMING_READS = 400
STREAMING_READS = 1000


def nsar(arduino):
    start_analogRead = datetime.now()
    for i in xrange(0, NON_STREAMING_READS):  # @UnusedVariable
        arduino.analogRead(0)
    end_analogRead = datetime.now()
    analogRead_time = end_analogRead - start_analogRead
    return analogRead_time


def sar(arduino):
    start_streamingAnalogRead = datetime.now()
    for i in arduino.streamingAnalogRead(0, STREAMING_READS):  # @UnusedVariable
        pass
    end_streamingAnalogRead = datetime.now()
    streamingAnalogRead_time = end_streamingAnalogRead - start_streamingAnalogRead
    return streamingAnalogRead_time


def nsdr(arduino):
    start_digitalRead = datetime.now()
    for i in xrange(0, NON_STREAMING_READS):  # @UnusedVariable
        arduino.digitalRead(0)
    end_digitalRead = datetime.now()
    digitalRead_time = end_digitalRead - start_digitalRead
    return digitalRead_time


def sdr(arduino):
    start_streamingDigitalRead = datetime.now()
    for i in arduino.streamingDigitalRead(0, STREAMING_READS):  # @UnusedVariable
        pass
    end_streamingDigitalRead = datetime.now()
    streamingDigitalRead_time = end_streamingDigitalRead - start_streamingDigitalRead
    return streamingDigitalRead_time


class Main(BaseMain):

    def run(self, options, args, arduino):
        #=======================================================================
        # arduino.analogRead
        #=======================================================================
        print " + read %d values using arduino.analogRead()..." % NON_STREAMING_READS
        analogRead_time = nsar(arduino)

        #=======================================================================
        # arduino.streamingAnalogRead()
        #=======================================================================
        print " + read %d values using arduino.streamingAnalogRead()" % STREAMING_READS
        streamingAnalogRead_time = sar(arduino)

        #=======================================================================
        # Stats
        #=======================================================================
        non_streaming = float(NON_STREAMING_READS) / analogRead_time.total_seconds()
        streaming = float(1000.0) / streamingAnalogRead_time.total_seconds()
        print " - arduino.analogRead() -> %f reads per second" % non_streaming
        print " - arduino.streamingAnalogRead() ->  %f reads per second" % streaming
        print "     +-> speedup: X%0.2f" % (streaming / non_streaming)

        #=======================================================================
        # arduino.digitalRead()
        #=======================================================================
        print " + read %d values using arduino.digitalRead()" % NON_STREAMING_READS
        digitalRead_time = nsdr(arduino)

        #=======================================================================
        # arduino.streamingDigitalRead
        #=======================================================================
        print " + read %d values using arduino.streamingDigitalRead()" % STREAMING_READS
        streamingDigitalRead_time = sdr(arduino)

        #=======================================================================
        # Stats
        #=======================================================================
        non_streaming = float(NON_STREAMING_READS) / digitalRead_time.total_seconds()
        streaming = float(1000.0) / streamingDigitalRead_time.total_seconds()
        print " - arduino.digitalRead() -> %f reads per second" % non_streaming
        print " - arduino.streamingDigitalRead() ->  %f reads per second" % streaming
        print "     +-> speedup: X%0.2f" % (streaming / non_streaming)

if __name__ == '__main__':
    Main().start()
