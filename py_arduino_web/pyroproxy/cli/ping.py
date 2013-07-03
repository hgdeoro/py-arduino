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

from py_arduino_web.pyroproxy.utils import BasePyroMain


class Main(BasePyroMain):

    def run(self, options, args, arduino):
        while True:
            sys.stdout.write("Ping sent...")
            sys.stdout.flush()
            start = time.time()
            try:
                arduino.ping()
                end = time.time()
                sys.stdout.write(" OK - Time={0:.3f} ms\n".format((end - start) * 1000))
                sys.stdout.flush()
                time.sleep(1)
            except KeyboardInterrupt:
                raise
            except:  # CommandTimeout
                # TODO: check with PYRO if original exceptoin was CommandTimeout
                sys.stdout.write(" error\n")
                sys.stdout.flush()
                end = time.time()
                if (end - start) < 0.5:
                    time.sleep(0.5)

if __name__ == '__main__':
    Main().start()
