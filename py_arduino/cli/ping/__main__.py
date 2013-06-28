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

import sys
import time

from py_arduino.main_utils import default_main
from py_arduino.proxy import CommandTimeout


def main():

    _, _, proxy = default_main() # pylint: disable=W0612
    try:
        while True:
            sys.stdout.write("Ping sent...")
            sys.stdout.flush()
            start = time.time()
            try:
                proxy.ping()
                end = time.time()
                sys.stdout.write(" OK - Time=%.3f ms\n" % ((end - start) * 1000))
                sys.stdout.flush()
                time.sleep(1)
            except CommandTimeout:
                sys.stdout.write(" timeout\n")
                sys.stdout.flush()
    except KeyboardInterrupt:
        print ""
        proxy.close()


if __name__ == '__main__':
    main()
