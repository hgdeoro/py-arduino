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

from IPython.Shell import IPShellEmbed

# Setup PYTHONPATH
SRC_DIR = os.path.split(os.path.realpath(__file__))[0] # SRC_DIR=BIN_DIR
SRC_DIR = os.path.split(SRC_DIR)[0] # SRC_DIR=SRC_DIR/../
SRC_DIR = os.path.join(SRC_DIR, 'src') # SRC_DIR
sys.path.append(os.path.abspath(SRC_DIR))

from arduino_proxy.main_utils import default_main
from arduino_proxy.proxy import CommandTimeout

def main():
    
    options, args, proxy = default_main() # pylint: disable=W0612
    ipshell = IPShellEmbed()
    ipshell.set_banner("""

Launching IPython shell...

Available variables:
 - proxy: the ArduinoProxy instance.
 - options, args: parsed argument options.

To import ArduinoProxy class:
>>> from arduino_proxy import ArduinoProxy

Enter 'quit()' to exit.
 
    """)
    ipshell()

if __name__ == '__main__':
    main()
