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

import logging
import hmac
import os
import Pyro4

from py_arduino.arduino import PyArduino
from py_arduino_web.storage import Storage


def main():
    """
    Expose object using PyRO
    """
    if "ENABLE_LOGGING" in os.environ:
        logging.basicConfig(level=logging.DEBUG)
    Pyro4.config.HMAC_KEY = hmac.new('this-is-py-arduino').digest()
    Pyro4.config.SOCK_REUSE = True
    arduino = PyArduino()
    try:
        from py_arduino_web.dj.models import DjStorage
        storage = DjStorage()
    except:
        logging.error("-" * 80)
        logging.exception("Couldn't import DjStorage")
        logging.error("-" * 80)
        storage = Storage()

    Pyro4.Daemon.serveSimple(
        {
            arduino: "py_arduino.arduino",
            storage: "py_arduino_web.storage",
        },
        host="localhost", port=61234, ns=False)
    # FORMA DE URI -> uri_string = "PYRO:py_arduino.PyArduino@localhost:61234"

if __name__ == '__main__':
    main()
