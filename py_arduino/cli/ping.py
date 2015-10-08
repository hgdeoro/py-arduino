#!/usr/bin/env python
# Licensed under the Apache License, Version 2.0
# Copyright (C) 2011-2015 - Horacio Guillermo de Oro <hgdeoro@gmail.com>

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

import sys
import time

from py_arduino import CommandTimeout
from py_arduino.main_utils import BaseMain


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
