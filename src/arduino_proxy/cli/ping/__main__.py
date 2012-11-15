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

import sys
import time

from arduino_proxy.main_utils import default_main
from arduino_proxy.proxy import CommandTimeout


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
