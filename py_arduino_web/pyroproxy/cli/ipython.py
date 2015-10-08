# Licensed under the Apache License, Version 2.0
# Copyright (C) 2011-2015 - Horacio Guillermo de Oro <hgdeoro@gmail.com>

from IPython.frontend.terminal.embed import InteractiveShellEmbed
from IPython.core.prompts import PromptManager

from py_arduino_web.pyroproxy.utils import BasePyroMain


banner = """

----------------------------------------------------------------------
py-arduino
----------------------------------------------------------------------

Launching IPython shell... Enter 'quit()' to exit.

Available variables:
    - arduino: the PyArduino instance.

Example:
    >>> arduino.ping()
    'PING_OK'
 
"""


class Main(BasePyroMain):

    def run(self, options, args, arduino):
        try:
            arduino.ping()
        except:
            pass

        PromptManager.in_template = "PyArduino [\\#]> "
        PromptManager.out_template = "PyArduino [\\#]: "

        shell = InteractiveShellEmbed(banner2=banner)
        shell.user_ns = {}
        shell()

if __name__ == '__main__':
    Main().start()
