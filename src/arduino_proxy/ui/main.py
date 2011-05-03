#!/usr/bin/env python

import logging
import os
import re
import sys

from PyQt4 import QtCore, QtGui

# Setup PYTHONPATH
SRC_DIR = os.path.split(os.path.realpath(__file__))[0] # SRC_DIR/arduino_proxy/tests
SRC_DIR = os.path.split(SRC_DIR)[0] # SRC_DIR/arduino_proxy
SRC_DIR = os.path.split(SRC_DIR)[0] # SRC_DIR
sys.path.append(os.path.abspath(SRC_DIR))

from arduino_proxy import ArduinoProxy
from arduino_proxy.ui.main_ui import *
from arduino_proxy.tests import default_main

RE_PINMODE_BUTTON = re.compile(r'^pinMode(\d{1,2})$')
RE_PIN_ENABLE_CHECKBOX = re.compile(r'^pinEnabled(\d{1,2})$')

logger = logging.getLogger(__name__)

class Subclass(Ui_MainWindow):
    
    def _easy_connect(self, pattern, signal_str, receiver_function):
        """
        Connect attributes of 'self' that match the given pattern to the 'receiver_function'.
        """
        for an_attr in [ getattr(self, x) for x in dir(self) if pattern.match(x) ]:
            logger.info("connect SIGNAL('%s') %s -> %s()", signal_str, an_attr.objectName(),
                receiver_function.__name__)
            logger.info("connect SIGNAL('clicked()') %s -> pinModeClicked()", an_attr.objectName())
            self.qMainWindow.connect(an_attr,
                QtCore.SIGNAL('clicked()'), self.pinModeClicked)
    
    def __init__(self, qMainWindow, options, args, proxy):
        self.qMainWindow = qMainWindow
        self.options = options
        self.args = args
        self.proxy = proxy
        Ui_MainWindow.setupUi(self, self.qMainWindow)
        
        # -> pinModeClicked()
        self._easy_connect(RE_PINMODE_BUTTON, 'clicked()', self.pinModeClicked)

        # -> pinEnabledDisabled()
        self._easy_connect(RE_PIN_ENABLE_CHECKBOX, 'stateChanged(int)',
            self.pinEnabledDisabled)
        
        #self.led13.setPixmap(QtGui.QPixmap(":/images/led-off.png"))
        #self.qMainWindow.connect(self.led13,
        #    QtCore.SIGNAL('clicked()'), self.setPixmap123)
    
    #def setPixmap123(self):
    #    self.led13.setPixmap(QtGui.QPixmap(":/images/led-on.png"))
    
    def pinModeClicked(self):
        sender = self.qMainWindow.sender()
        logger.info("pinModeClicked() - sender: %s", sender.objectName())
        if sender.text() == 'I':
            sender.setText('O')
        else:
            sender.setText('I')
    
    def pinEnabledDisabled(self):
        sender = self.qMainWindow.sender()
        logger.info("pinEnabledDisabled() - sender: %s - state: %s", sender.objectName(),
            str(sender.checkState()))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def default_args_validator(parser, options, args): # pylint: disable=W0613
    if len(args) <1:
        parser.error("You should specify the serial device.")

def main():
    options, args, proxy = default_main(args_validator=default_args_validator)
    app = QtGui.QApplication(args[1:])
    MainWindow = QtGui.QMainWindow()
    ui = Subclass(MainWindow, options, args, proxy)
    MainWindow.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
