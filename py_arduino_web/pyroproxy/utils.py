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

import hmac
import logging
import optparse
import time

import Pyro4
from Pyro4.errors import CommunicationError
import sys

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
    Pyro4.config.HMAC_KEY = hmac.new('this-is-py-arduino').digest()
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
    Pyro4.config.HMAC_KEY = hmac.new('this-is-py-arduino').digest()
    daemon = Pyro4.Proxy("PYRO:{0}@localhost:61234".format(
        Pyro4.constants.DAEMON_NAME))
    try:
        daemon.ping()
        return True
    except CommunicationError:
        return False


#===============================================================================
# PyroMain
#===============================================================================

class BasePyroMain(object):
    """
    Base class to create scrpits from `pyroproxy.cli.*`
    """

    logger = logging.getLogger('BasePyroMain')

    def __init__(self):
        self.parser = optparse.OptionParser()
        self.add_options()

    def add_options(self):
        self.parser.add_option("--debug",
            action="store_true", dest="debug", default=False,
            help="Configure logging to show debug messages.")
        self.parser.add_option("--info",
            action="store_true", dest="info", default=False,
            help="Configure logging to show info messages.")
        self.parser.add_option("--check-pyro-server",
            action="store_true", dest="check_pyro_server", default=False,
            help="Check if PyRO server is reachable, exit if it isn't reachable.")

    def run(self, options, args, arduino):
        """
        To be overriden in subclass.
        Do not call this method directly! You must call `start()`.
        """
        raise(NotImplementedError())

    def start(self):
        (options, args) = self.parser.parse_args()

        # setup logging
        if options.debug:
            logging.basicConfig(level=logging.DEBUG)
        elif options.info:
            logging.basicConfig(level=logging.INFO)
        else:
            logging.basicConfig(level=logging.ERROR)

        if options.check_pyro_server:
            if not server_is_up():
                print "ERROR: PyRO server isn't reachable"
                sys.exit(1)

        arduino = get_arduino_pyro()
        try:
            return self.run(options, args, arduino)
        except KeyboardInterrupt:
            print ""
            return None
        except Exception:
            raise
