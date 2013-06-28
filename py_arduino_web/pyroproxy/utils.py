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

import hmac
import logging
import time

import Pyro4
from Pyro4.errors import CommunicationError

_logger = logging.getLogger(__name__)


def get_arduino_pyro():
    """Returns a Pyro proxy of the PyArduino instance"""
    Pyro4.config.HMAC_KEY = hmac.new('this-is-py-arduino').digest()
    return Pyro4.Proxy("PYRO:py_arduino.arduino@localhost:61234")


def get_storage_pyro():
    """Returns a Pyro proxy of the Storage instance"""
    Pyro4.config.HMAC_KEY = hmac.new('this-is-py-arduino').digest()
    return Pyro4.Proxy("PYRO:py_arduino_web.storage@localhost:61234")


def wait_for_server(logger=_logger, sleep=1):
    """
    Waits until Pyro server is reachable.
    Waits for `sleep` seconds between checks.
    Logs messages using`logger`, could be `None` to disable logging.
    """
    daemon = Pyro4.Proxy("PYRO:{0}@localhost:61234".format(
        Pyro4.constants.DAEMON_NAME))
    if logger:
        logger.info("Wait to let PyRO server start up")
    while True:
        try:
            daemon.ping()
            return
        except CommunicationError:
            time.sleep(1)


def server_is_up():
    """
    Returns True if Pyro server is reachable.
    """
    daemon = Pyro4.Proxy("PYRO:{0}@localhost:61234".format(
        Pyro4.constants.DAEMON_NAME))
    try:
        daemon.ping()
        return True
    except CommunicationError:
        return False
