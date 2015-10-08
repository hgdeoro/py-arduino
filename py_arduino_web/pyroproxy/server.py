# Licensed under the Apache License, Version 2.0
# Copyright (C) 2011-2015 - Horacio Guillermo de Oro <hgdeoro@gmail.com>

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
                      action="store_true",
                      dest="debug",
                      default=False,
                      help="Configure logging to show debug messages.")
    parser.add_option("--info",
                      action="store_true",
                      dest="info",
                      default=False,
                      help="Configure logging to show info messages.")
    parser.add_option("--emulator",
                      action="store_true",
                      dest="emulator",
                      default=False,
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
    # URI FORMAT -> uri_string = "PYRO:py_arduino.PyArduino@localhost:61234"


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
