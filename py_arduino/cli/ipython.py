#!/usr/bin/env python
# Licensed under the Apache License, Version 2.0
# Copyright (C) 2011-2015 - Horacio Guillermo de Oro <hgdeoro@gmail.com>


"""
#===============================================================================
# Start an IPython interactive session.
#===============================================================================

To execute this, run:

    $ python -m py_arduino.cli.ipython --info /dev/ttyACM0

You will need ipython installed in the virtualenv. You may need to run:

    $ pip install ipython

#===============================================================================
# NOTE: remember to load the virtualenv before running this:
#===============================================================================

    $ . virtualenv/bin/activate

"""

try:
    from IPython.core.prompts import PromptManager
    from IPython.frontend.terminal.embed import InteractiveShellEmbed
except ImportError:
    print ""
    print ""
    print "ERROR: Couldn't import ipython. You may need to run somthing like:"
    print " $ pip install ipython"
    print ""
    print ""
    raise

from py_arduino.main_utils import BaseMain

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


class Main(BaseMain):

    def run(self, options, args, arduino):
        PromptManager.in_template = "PyArduino [\\#]> "
        PromptManager.out_template = "PyArduino [\\#]: "

        shell = InteractiveShellEmbed(banner2=banner)
        shell.user_ns = {}
        shell()


if __name__ == '__main__':
    Main().start()
