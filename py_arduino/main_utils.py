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

import glob
import logging
import optparse

from py_arduino.arduino import PyArduino


class BaseMain(object):
    """
    Utility class to easilly extend and do stuff with PyArduino.

    Inspired in the 'custom management commands' of Django and threading.

    Example:

    #===============================================================================
    #     class ReadDigitalPort(BaseMain):
    #         optparse_usage = BaseMain.optparse_usage + " digital_port"
    #         num_args = 2
    #
    #         def run(self, options, args, arduino):
    #             digital_port = int(args[1])
    #             arduino.pinMode(digital_port, INPUT)
    #             print arduino.digitalRead(digital_port)
    #
    #     if __name__ == '__main__':
    #         MyMain().start()
    #===============================================================================
    """

    """
    - optparse_usage
        Usage text. Subclass could append text to it.
    """
    optparse_usage = "usage: %prog [options] serial_device"

    """
    - num_args
        Number of arguments. Used to do a simple automatic check.
        If you need a more fine-grained way to check the arguments,
        add a validator to `args_validator`
    """
    num_args = 1

    """
    - auto_close
        Automatically close the PyArduino (also ignores KeyboardInterrupt)
    """
    auto_close = True

    def __init__(self):
        self.parser = optparse.OptionParser(usage=self.optparse_usage)
        self.add_options()

    def add_options(self):
        self.parser.add_option("--debug",
            action="store_true", dest="debug", default=False,
            help="Configure logging to show debug messages.")
        self.parser.add_option("--arduino-debug",
            action="store_true", dest="arduino_debug", default=False,
            help="Configure the PyArduino instance to debug all the " +
                "comunication with Arduino (implies --info).")
        self.parser.add_option("--info",
            action="store_true", dest="info", default=False,
            help="Configure logging to show info messages.")
        self.parser.add_option("--initial-wait",
            action="store", dest="initial_wait", default=None,
            help="How many seconds wait before conect (workaround for auto-reset on connect).")
        self.parser.add_option("--dont-call-validate-connection",
            action="store_true", dest="dont_call_validate_connection", default=False,
            help="Don't call validateConnection() on startup (the default is " + \
                "to call validateConnection() automatically at startup).")

    def run(self, options, args, arduino):
        """
        To be overriden in subclass.
        Do not call this method directly! You must call `start()`.
        """
        raise(NotImplementedError())

    def get_device(self, options, args):
        """
        Returns the device to use. By default, return the first argument.
        """
        return args[0]

    def validate(self, options, args):
        """
        Additional validations could be added to subclass, but
        remember to call this first.
        You can use `self.parser.error()` to raise errors.

        #===============================================================================
        # Example:
        #===============================================================================
        #    class MyMain(BaseMain):
        #
        #        def validate(self, options, args):
        #            super(MyMain, self).validate(options, args)
        #            MORE VALIDATIONS HERE
        #            MORE VALIDATIONS HERE
        #            MORE VALIDATIONS HERE
        #===============================================================================

        """
        if len(args) < self.num_args:
            self.parser.error("must specify the serial device (like /dev/ttyACM0). "
                "Serial devices that looks like "
                "Arduinos: %s." % ', '.join(glob.glob('/dev/ttyACM*')))

    def start(self):
        (options, args) = self.parser.parse_args()
        self.validate(options, args)

        # setup logging
        if options.debug:
            logging.basicConfig(level=logging.DEBUG)
        elif options.info or options.arduino_debug:
            logging.basicConfig(level=logging.INFO)
        else:
            logging.basicConfig(level=logging.ERROR)

        serial_device = self.get_device(options, args)
        logging.info("Creating PyArduino instance - serial: %s - speed: %s", serial_device, 9600)
        if options.initial_wait == 0:
            arduino = PyArduino(serial_device, 9600, wait_after_open=0,
                call_validate_connection=not(options.dont_call_validate_connection)).connect()
        elif options.initial_wait is None:
            # TODO: move this logging to PyArduino
            logging.info("Waiting some seconds to let the Arduino reset...")
            arduino = PyArduino(serial_device, 9600,
                call_validate_connection=not(options.dont_call_validate_connection)).connect()
        else:
            initial_wait = int(options.initial_wait)
            if initial_wait > 0:
                # TODO: move this logging to PyArduino
                logging.info("Waiting %d seconds to let the Arduino reset...", initial_wait)
            arduino = PyArduino(serial_device, 9600, wait_after_open=initial_wait,
                call_validate_connection=not(options.dont_call_validate_connection)).connect()

        # enable debugging if required
        if options.arduino_debug:
            arduino.enableDebug()

        if self.auto_close:
            try:
                return self.run(options, args, arduino)
            except KeyboardInterrupt:
                print ""
                return None
            except Exception:
                raise
            finally:
                if self.auto_close:
                    # While `run()` is executed, `self.auto_close` can become False
                    arduino.close()
        else:
            return self.run(options, args, arduino)
