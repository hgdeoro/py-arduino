# Licensed under the Apache License, Version 2.0
# Copyright (C) 2011-2015 - Horacio Guillermo de Oro <hgdeoro@gmail.com>

import hmac
import logging
import optparse
import sys
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


def get_status_tracker():
    """Returns a Pyro proxy of the Status Tracker instance"""
    Pyro4.config.HMAC_KEY = hmac.new('this-is-py-arduino').digest()
    return Pyro4.Proxy("PYRO:py_arduino.status_tracker@localhost:61234")


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
        self.options = None
        self.args = None

    def add_options(self):
        self.parser.add_option("--debug",
            action="store_true", dest="debug", default=False,
            help="Configure logging to show debug messages.")
        self.parser.add_option("--info",
            action="store_true", dest="info", default=False,
            help="Configure logging to show info messages.")
        self.parser.add_option("--dont-check-pyro-server",
            action="store_true", dest="dont_check_pyro_server", default=False,
            help="Don't check if PyRO server is reachable (by default, "
            "a check is done and we exit if the server isn't reachable.)")
        self.parser.add_option("--wait-until-connected",
            action="store_true", dest="wait_until_pyro_server_is_up", default=False,
            help="Wait until the PyRO server is up")

    def run(self, arduino):
        """
        To be overriden in subclass.
        Do not call this method directly! You must call `start()`.
        """
        raise(NotImplementedError())

    def start(self):
        self.options, self.args = self.parser.parse_args()

        _debug = False
        _info = False

        # setup logging
        if self.options.debug:
            _debug = True
        elif self.options.info:
            _info = True

        _dont_check_pyro_server = self.options.dont_check_pyro_server
        _wait_until_pyro_server_is_up = self.options.wait_until_pyro_server_is_up

        # TODO: add support 'wait_until_connected'
        self._start(_debug, _info, _dont_check_pyro_server, _wait_until_pyro_server_is_up)

    def _start(self, debug=False, info=False, dont_check_pyro_server=False,
        wait_until_pyro_server_is_up=False, wait_until_connected=False):
        """
        Internal functions that really launch the process.
        This is needed becaus for mules, it's not posible to pass command line arguments.
        """
        # setup logging
        if debug:
            logging.basicConfig(level=logging.DEBUG)
        elif info:
            logging.basicConfig(level=logging.INFO)
        else:
            logging.basicConfig(level=logging.ERROR)

        if not dont_check_pyro_server:
            if not server_is_up():
                print "ERROR: PyRO server isn't reachable"
                sys.exit(1)

        if wait_until_pyro_server_is_up:
            wait_for_server()

        arduino = get_arduino_pyro()

        if wait_until_connected:
            reported = False
            while not arduino.is_connected():
                if not reported:
                    BasePyroMain.logger.info("Arduino not connected... will wait until connected")
                reported = True
                time.sleep(3)
            BasePyroMain.logger.info("Connection detected! Will continue with execution")

        try:
            return self.run(arduino)
        except KeyboardInterrupt:
            print ""
            return None
        except Exception:
            raise
