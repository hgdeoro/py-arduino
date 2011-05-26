#!/usr/bin/env python
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
import optparse
import os
import sys
import time

# Setup PYTHONPATH
BASE_DIR = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(os.path.abspath(os.path.join(BASE_DIR, 'src')))
sys.path.append(os.path.abspath(os.path.join(BASE_DIR, 'lib')))

import cherrypy

from arduino_proxy.main_utils import default_main
from arduino_proxy.web import start_webserver

def main():
    parser = optparse.OptionParser()
    
    parser.add_option("--debug",
        action="store_true", dest="debug", default=False,
        help="Configure logging to show debug messages.")
    
    parser.add_option("--info",
        action="store_true", dest="info", default=False,
        help="Configure logging to show info messages.")
    
    parser.add_option("--access",
        action="store_true", dest="access", default=False,
        help="Configure logging to show request processed by the web server.")
    
    parser.add_option("--initial-wait",
        action="store", dest="initial_wait", default=None,
        help="How many seconds wait before conect (workaround for auto-reset on connect).")
    
    (options, args) = parser.parse_args()

    if options.debug:
        logging.basicConfig(level=logging.DEBUG)
    elif options.info:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.ERROR)
    
    if options.access:
        logging.getLogger('cherrypy.access').setLevel(logging.INFO)
    else:
        logging.getLogger('cherrypy.access').setLevel(logging.ERROR)
    
    start_webserver(BASE_DIR)

if __name__ == '__main__':
    main()
