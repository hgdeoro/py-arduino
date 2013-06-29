#!/usr/bin/env python
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
from IPython.core.prompts import PromptManager

try:
    from IPython.frontend.terminal.embed import InteractiveShellEmbed
except ImportError:
    print ""
    print ""
    print "ERROR: Couldn't import ipython. You may need to run somthing like:"
    print " $ pip install ipython"
    print ""
    print ""
    raise

from py_arduino.main_utils import default_main


banner = """

----------------------------------------------------------------------
py-arduino
----------------------------------------------------------------------

Launching IPython shell... Enter 'quit()' to exit.

Available variables:
    - arduino: the PyArduino instance.
    - options, args: parsed argument options.

Example:
    >>> arduino.ping()
    'PING_OK'
 
"""


def main():

    options, args, arduino = default_main()  # pylint: disable=W0612 @UnusedVariable
    PromptManager.in_template = "PyArduino [\\#]> "
    PromptManager.out_template = "PyArduino [\\#]: "

    shell = InteractiveShellEmbed(banner2=banner)
    shell.user_ns = {}
    shell()


if __name__ == '__main__':
    main()
