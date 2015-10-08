##-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
##    py-arduino - Access your Arduino from Python
##    Copyright (C) 2011-2015 - Horacio Guillermo de Oro <hgdeoro@gmail.com>
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
import optparse

from py_arduino.arduino import PyArduino
from py_arduino_web.storage import Storage
from py_arduino import DEVICE_FOR_EMULATOR


def main():
    """
    Expose object using PyRO
    """
    parser = optparse.OptionParser()
    parser.add_option("--debug",
        action="store_true", dest="debug", default=False,
        help="Configure logging to show debug messages.")
    parser.add_option("--info",
        action="store_true", dest="info", default=False,
        help="Configure logging to show info messages.")
    parser.add_option("--emulator",
        action="store_true", dest="emulator", default=False,
        help="Automatically connect to emulator.")

    (options, _) = parser.parse_args()

    if options.debug:
        logging.basicConfig(level=logging.DEBUG)
    elif options.info:
        logging.basicConfig(level=logging.INFO)

    import Pyro4

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

    status_tracker = arduino.status_tracker

    if options.emulator:
        arduino.connect(DEVICE_FOR_EMULATOR)

    Pyro4.Daemon.serveSimple(
        {
            arduino: "py_arduino.arduino",
            storage: "py_arduino_web.storage",
            status_tracker: "py_arduino.status_tracker",
        },
        host="localhost", port=61234, ns=False)
    # FORMA DE URI -> uri_string = "PYRO:py_arduino.PyArduino@localhost:61234"

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
