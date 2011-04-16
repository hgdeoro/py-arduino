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

import logging
import sys

from arduino_proxy import ArduinoProxy

def default_callback(value):
    print value

def main(callback):
    argv = list(sys.argv)
    if "--debug" in argv:
        logging.basicConfig(level=logging.DEBUG)
        argv.remove("--debug")
    else:
        logging.basicConfig(level=logging.ERROR)
    
    if "--loop" in argv:
        do_loop = True
        argv.remove("--loop")
    else:
        do_loop = False
    
    try:
        serial = argv[1]
        analog_port = int(argv[2])
    except (IndexError, ValueError, ):
        print "Use: %s <SERIAL_PORT> <ANALOG_PORT_OF_ARDUINO>" % argv[0]
        sys.exit(1)
    
    proxy = ArduinoProxy(serial, 9600)
    try:
        while True:
            value = proxy.analogRead(analog_port)
            callback(value)
            if not do_loop:
                break
    finally:
        proxy.close()

if __name__ == '__main__':
    main(default_callback)
