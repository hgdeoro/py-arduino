#!/usr/bin/env python
# Licensed under the Apache License, Version 2.0
# Copyright (C) 2011-2015 - Horacio Guillermo de Oro <hgdeoro@gmail.com>

import traceback

from py_arduino import InvalidCommand, PyArduinoException, \
    INPUT, HIGH, ATTACH_INTERRUPT_MODE_LOW
from py_arduino.main_utils import BaseMain


class Main(BaseMain):
    def run(self, options, args, arduino):

        #    LOW to trigger the interrupt whenever the pin is low,
        #    CHANGE to trigger the interrupt whenever the pin changes value
        #    RISING to trigger when the pin goes from low to high,
        #    FALLING for when the pin goes from high to low.
        #
        #    ATTACH_INTERRUPT_MODE_LOW = 'L'
        #    ATTACH_INTERRUPT_MODE_CHANGE = 'C'
        #    ATTACH_INTERRUPT_MODE_RISING = 'R'
        #    ATTACH_INTERRUPT_MODE_FALLING = 'F'

        print "arduino.pinMode()"
        arduino.pinMode(2, INPUT)  # INT_0
        arduino.delay(200)

        print "arduino.digitalWrite(2,HIGH) -> pullup resistor"
        arduino.digitalWrite(2, HIGH)  # INT_0 -> pullup resistor
        arduino.delay(200)

        print "arduino.watchInterrupt(0) -> interrupt occurs when pin 2 become LOW."
        print " +", arduino.watchInterrupt(0, ATTACH_INTERRUPT_MODE_LOW)

        while True:
            try:
                if arduino.getInterruptMark(0):
                    print " + INTERRUPT 0 has ocurred"
            except InvalidCommand:
                print " + Ignoring InvalidCommand! This is normal when working with interrupts."
            except PyArduinoException:
                traceback.print_exc()
                print "##"
                print "## ERROR DETECTED!"
                print "##"
                print "validateConnection() -> %s" % str(arduino.validateConnection())
                print "enableDebug() -> %s" % str(arduino.enableDebug())
                print "ping() -> %s" % str(arduino.ping())
                print ""
                print "Continuing..."
                print ""


if __name__ == '__main__':
    Main().start()
