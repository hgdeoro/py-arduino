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

import os
import sys
import time

# Setup PYTHONPATH
BASE_DIR = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(os.path.abspath(os.path.join(BASE_DIR, 'src')))
sys.path.append(os.path.abspath(os.path.join(BASE_DIR, 'lib')))

from arduino_proxy.main_utils import default_main
from arduino_proxy.web import start_webserver

def main():
    options, args, proxy = default_main() # pylint: disable=W0612
    start_webserver(BASE_DIR, options, args, proxy)

if __name__ == '__main__':
    main()
