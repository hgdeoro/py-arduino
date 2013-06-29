#!/usr/bin/env python
##-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
##    py-arduino - Access your Arduino from Python
##    Copyright (C) 2011-2013 - Horacio Guillermo de Oro <hgdeoro@gmail.com>
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

"""
#===============================================================================
# EXAMPLE - Blinks the led on PIN 13
#===============================================================================

To run this example:

    $ python -m examples.blink_pin13 /dev/ttyACM0

or, if you want to see what's going on:

    $ python -m examples.blink_pin13 --info /dev/ttyACM0

or, if you want to see LOT of debug messages:

    $ python -m examples.blink_pin13 --debug /dev/ttyACM0

#===============================================================================
# NOTE 1: remember to load the virtualenv:
#===============================================================================

    $ . virtualenv/bin/activate

#===============================================================================
# NOTE 2: you can change the PIN setting the environment variable 'PIN':
#===============================================================================

    $ env PY_ARDUINO_PIN=5 python -m examples.blink_pin13 /dev/ARDUINO_EMULATOR

"""

import logging
import os
import time

from py_arduino import OUTPUT
from py_arduino.main_utils import default_main
from py_arduino.arduino import PyArduino, HIGH, LOW

PIN = int(os.environ.get('PY_ARDUINO_PIN', '13'))

logger = logging.getLogger(__name__)


def main():
    USAGE = "usage: %prog [options] serial_device"
    _, _, arduino = default_main(optparse_usage=USAGE)
    assert isinstance(arduino, PyArduino)

    try:
        arduino.pinMode(PIN, OUTPUT)
        while True:
            print("PIN {0} -> HIGH".format(PIN))
            arduino.digitalWrite(PIN, HIGH)
            time.sleep(0.5)
            print("PIN {0} -> LOW".format(PIN))
            arduino.digitalWrite(PIN, LOW)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print ""
    except Exception:
        raise
    finally:
        arduino.close()

if __name__ == '__main__':
    main()
