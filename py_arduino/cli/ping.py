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

import sys
import time

from py_arduino import CommandTimeout
from py_arduino.main_utils import BaseMain

"""
#===============================================================================
# Ping to the Arduino until Ctrl+C is pressed.
#===============================================================================

To execute this, run:

    $ python -m py_arduino.cli.ping --info /dev/ttyACM0

#===============================================================================
# NOTE: remember to load the virtualenv before running this:
#===============================================================================

    $ . virtualenv/bin/activate

"""


class Main(BaseMain):

    def run(self, options, args, arduino):
        while True:
            sys.stdout.write("Ping sent...")
            sys.stdout.flush()
            try:
                start = time.time()
                arduino.ping()
                end = time.time()
                sys.stdout.write(" OK - Time={0:.3f} ms\n".format((end - start) * 1000))
                sys.stdout.flush()
                time.sleep(1)
            except CommandTimeout:
                sys.stdout.write(" timeout\n")
                sys.stdout.flush()

if __name__ == '__main__':
    Main().start()
