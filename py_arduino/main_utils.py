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

from py_arduino import PyArduino

#
# Example for "add_options_callback" parameter of "default_main()":
#
#    def add_options_callback_example(parser):
#        parser.add_option("--initial-wait",
#            action="store", dest="initial_wait", default=None,
#            help="How many seconds wait before conect " +\
#                "(workaround for auto-reset on connect bug).")
#


def default_args_validator(parser, options, args): # pylint: disable=W0613
    if len(args) > 1:
        parser.error("you specified more than one argument, and only one is spected")


def optional_device_arg_validator(parser, options, args): # pylint: disable=W0613
    # len(args) should be 0 or 1
    if len(args) > 1:
        parser.error("you specified more than one argument, and none or one is spected")


def default_main(optparse_usage="usage: %prog [options] serial_device",
        add_options_callback=None, args_validator=default_args_validator,
        connect_only_if_device_specified=False):
    """
    Utility method to help creation of programs around PyArduino. This method configures logging
    and initial wait, and creates the PyArduino instance.
    
    Parameters:
        - add_options_callback: callback method to let the user of 'main_utils()' add options.
            This method is called, and the 'parser' instance is passed as parameter.
        - args_validator: method that validates the args.
    
    Returns:
        - options, args, arduino
    """
    parser = optparse.OptionParser(usage=optparse_usage)
    parser.add_option("--debug",
        action="store_true", dest="debug", default=False,
        help="Configure logging to show debug messages.")
    parser.add_option("--arduino-debug",
        action="store_true", dest="arduino_debug", default=False,
        help="Configure the PyArduino instance to debug all the " +
            "comunication with Arduino (implies --info).")
    parser.add_option("--info",
        action="store_true", dest="info", default=False,
        help="Configure logging to show info messages.")
    parser.add_option("--initial-wait",
        action="store", dest="initial_wait", default=None,
        help="How many seconds wait before conect (workaround for auto-reset on connect).")
    parser.add_option("--dont-call-validate-connection",
        action="store_true", dest="dont_call_validate_connection", default=False,
        help="Don't call validateConnection() on startup (the default is " + \
            "to call validateConnection() automatically at startup).")

    if not add_options_callback is None:
        add_options_callback(parser)

    (options, args) = parser.parse_args()

    if len(args) == 0 and not connect_only_if_device_specified:
        parser.error("must specify the serial device (like /dev/ttyACM0). " + \
            "Serial devices that looks like Arduinos: %s." % ', '.join(glob.glob('/dev/ttyACM*')))

    if args_validator:
        args_validator(parser, options, args)

    if options.debug:
        logging.basicConfig(level=logging.DEBUG)
    elif options.info or options.arduino_debug:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.ERROR)

    if connect_only_if_device_specified and len(args) == 0:
        return options, args, None
    else:
        if options.initial_wait == 0:
            arduino = PyArduino(args[0], 9600, wait_after_open=0,
                call_validate_connection=not(options.dont_call_validate_connection)).connect()
        else:
            if options.initial_wait is None:
                logging.info("Waiting some seconds to let the Arduino reset...")
                arduino = PyArduino(args[0], 9600,
                    call_validate_connection=not(options.dont_call_validate_connection)).connect()
            else:
                initial_wait = int(options.initial_wait)
                if initial_wait > 0:
                    logging.info("Waiting %d seconds to let the Arduino reset...", initial_wait)
                arduino = PyArduino(args[0], 9600, wait_after_open=initial_wait,
                    call_validate_connection=not(options.dont_call_validate_connection)).connect()
    
        if options.arduino_debug:
            arduino.enableDebug()
    
        return options, args, arduino
