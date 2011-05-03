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

import glob
import logging
import optparse

from arduino_proxy import ArduinoProxy

#
# Example for "add_options_callback" parameter of "default_main()":
#
#    def add_options_callback_example(parser):
#        parser.add_option("--initial-wait",
#            action="store", dest="initial_wait", default=None,
#            help="How many seconds wait before conect (workaround for auto-reset on connect bug).")
#

def default_args_validator(parser, options, args): # pylint: disable=W0613
    if len(args) > 1:
        parser.error("you specified more than one argument, and only one is spected")

def default_main(optparse_usage="usage: %prog [options] serial_device", 
        add_options_callback=None, args_validator=default_args_validator, quiet=False):
    """
    Utility method to help creation of programs around ArduinoProxy. This method configures logging
    and initial wait, and creates the ArduinoProxy instance.
    
    Parameters:
        - add_options_callback: callback method to let the user of 'main_utils()' add options.
            This method is called, and the 'parser' instance is passed as parameter.
        - args_validator: method that validates the args.
        - quiet: try to be quiet. If True, doesn't show the "let the Arduino reset" message. This
            is also setted as True if --quiet is specified.
    
    Returns:
        - options, args, proxy
    """
    parser = optparse.OptionParser(usage=optparse_usage)
    parser.add_option("--debug",
        action="store_true", dest="debug", default=False,
        help="Configure logging to show debug messages.")
    parser.add_option("--info",
        action="store_true", dest="info", default=False,
        help="Configure logging to show info messages.")
    parser.add_option("--quiet",
        action="store_true", dest="quiet", default=False,
        help="Try to be quiet.")
    parser.add_option("--initial-wait",
        action="store", dest="initial_wait", default=None,
        help="How many seconds wait before conect (workaround for auto-reset on connect bug).")
    parser.add_option("--dont-call-connect",
        action="store_true", dest="dont_call_connect", default=False,
        help="Don't call connect on startup (the default is " + \
            "to call connect automatically at startup).")
    
    if not add_options_callback is None:
        add_options_callback(parser)
    
    (options, args) = parser.parse_args()
    
    if len(args) == 0:
        parser.error("must specify the serial device (like /dev/ttyACM0). " + \
            "Serial devices that looks like Arduinos: %s." % ', '.join(glob.glob('/dev/ttyACM*')))
    
    if args_validator:
        args_validator(parser, options, args)
    
    quiet = (quiet or options.quiet)
    
    if options.debug:
        logging.basicConfig(level=logging.DEBUG)
    elif options.info:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.ERROR)
    
    if options.initial_wait == 0:
        proxy = ArduinoProxy(args[0], 9600, wait_after_open=0,
            call_connect=not(options.dont_call_connect))
    else:
        if options.initial_wait is None:
            if not quiet:
                print "Warning: waiting some seconds to let the Arduino reset..."
            proxy = ArduinoProxy(args[0], 9600, call_connect=not(options.dont_call_connect))
        else:
            if not quiet:
                print "Warning: waiting %d seconds to let the Arduino reset..." % \
                    int(options.initial_wait)
            proxy = ArduinoProxy(args[0], 9600, wait_after_open=int(options.initial_wait),
                call_connect=not(options.dont_call_connect))

    return options, args, proxy
