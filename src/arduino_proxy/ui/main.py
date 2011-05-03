#!/usr/bin/env python

import os
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

class Subclass(Ui_MainWindow):
	
	def __init__(self, qMainWindow, options, args, proxy):
		self.qMainWindow = qMainWindow
		self.options = options
		self.args = args
		self.proxy = proxy
		Ui_MainWindow.setupUi(self, self.qMainWindow)
		
		for pin_mode_attr in [ self.pinMode13, self.pinMode12,
				self.pinMode11, self.pinMode10, self.pinMode9,
				self.pinMode8]:
			self.qMainWindow.connect(pin_mode_attr,
				QtCore.SIGNAL('clicked()'), self.pinModeClicked)
		
		#self.led13.setPixmap(QtGui.QPixmap(":/images/led-off.png"))
		#self.qMainWindow.connect(self.led13,
		#	QtCore.SIGNAL('clicked()'), self.setPixmap123)
	
	#def setPixmap123(self):
	#	self.led13.setPixmap(QtGui.QPixmap(":/images/led-on.png"))
	
	def pinModeClicked(self):
		sender = self.qMainWindow.sender()
		if sender.text() == 'I':
			sender.setText('O')
		else:
			sender.setText('I')

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
