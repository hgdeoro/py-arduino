#!/usr/bin/env python

import sys

from PyQt4 import QtCore, QtGui

from main_ui import *

class Subclass(Ui_MainWindow):
	
	def __init__(self, qMainWindow):
		self.qMainWindow = qMainWindow
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

def main():
	app = QtGui.QApplication(sys.argv)
	MainWindow = QtGui.QMainWindow()
	ui = Subclass(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
