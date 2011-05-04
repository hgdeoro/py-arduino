#!/usr/bin/env python

import logging
import os
import re
import sys
import traceback

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from PyQt4 import QtCore, QtGui

# Setup PYTHONPATH
SRC_DIR = os.path.split(os.path.realpath(__file__))[0] # SRC_DIR/arduino_proxy/tests
SRC_DIR = os.path.split(SRC_DIR)[0] # SRC_DIR/arduino_proxy
SRC_DIR = os.path.split(SRC_DIR)[0] # SRC_DIR
sys.path.append(os.path.abspath(SRC_DIR))

from arduino_proxy import ArduinoProxy
from arduino_proxy.ui.main_ui import *
from arduino_proxy.tests import default_main

logger = logging.getLogger(__name__) # pylint: disable=C0103

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

RE_PINMODE_BUTTON = re.compile(r'^pinMode(\d{1,2})$')
RE_PIN_ENABLE_CHECKBOX = re.compile(r'^pinEnabled(\d{1,2})$')

RE_DIGITAL_WRITE_LOW_BUTTON = re.compile(r'^dw(\d{1,2})_l$')
RE_DIGITAL_WRITE_HIGH_BUTTON = re.compile(r'^dw(\d{1,2})_h$')

RE_ANALOG_WRITE_SLIDER = re.compile(r'^pinValue(\d{1,2})$')

class ArduinoProxyMainWindow(Ui_MainWindow):
    
    LED_ON_PIXMAP = None
    LED_OFF_PIXMAP = None

    def __init__(self, q_main_window, options, args, proxy):
        self.q_main_window = q_main_window
        self.options = options
        self.args = args
        self.proxy = proxy
        self.update_timer = QtCore.QTimer()
        
        Ui_MainWindow.setupUi(self, self.q_main_window)
        
        # -> update_arduino_values()
        self.q_main_window.connect(self.pushButtonUpdate, QtCore.SIGNAL('clicked()'),
            self.update_arduino_values)
        self.q_main_window.connect(self.update_timer, QtCore.SIGNAL('timeout()'),
            self.update_arduino_values)
        
        # -> checkbox_auto_update_toggle()
        self.q_main_window.connect(self.checkboxAutoUpdate, QtCore.SIGNAL('stateChanged(int)'),
            self.checkbox_auto_update_toggle)
        
        # -> pinModeClicked()
        self._easy_connect(RE_PINMODE_BUTTON, 'clicked()', self.pinModeClicked)

        # -> pinEnabledDisabled()
        self._easy_connect(RE_PIN_ENABLE_CHECKBOX, 'stateChanged(int)', self.pinEnabledDisabled)
        
        # -> digitalWriteLow()
        self._easy_connect(RE_DIGITAL_WRITE_LOW_BUTTON, 'clicked()', self.digitalWriteLow)
        
        # -> digitalWriteHigh()
        self._easy_connect(RE_DIGITAL_WRITE_HIGH_BUTTON, 'clicked()', self.digitalWriteHigh)
        
        # -> analogWriteValueChanged()
        self._easy_connect(RE_ANALOG_WRITE_SLIDER, 'valueChanged(int)',
            self.analogWriteValueChanged)
        
        ArduinoProxyMainWindow.LED_ON_PIXMAP = QtGui.QPixmap(":/images/led-on.png")
        ArduinoProxyMainWindow.LED_OFF_PIXMAP = QtGui.QPixmap(":/images/led-off.png")
    
    def _get_attributes(self, pattern):
        """Get a list of attributes that matches the pattern"""
        return [ getattr(self, x) for x in dir(self) if pattern.match(x) ]
    
    def _easy_connect(self, pattern, signal_str, receiver_function):
        """
        Connect attributes of 'self' that match the given pattern to the 'receiver_function'.
        """
        attr_list = self._get_attributes(pattern)
        if not attr_list:
            logger.warn("No attribute found! pattern: %s - SIGNAL('%s') -> %s()",
                pattern, signal_str, receiver_function.__name__)
        for an_attr in attr_list:
            logger.info("connect SIGNAL('%s') %s -> %s()", signal_str, an_attr.objectName(),
                receiver_function.__name__)
            self.q_main_window.connect(an_attr,
                QtCore.SIGNAL(signal_str), receiver_function)
    
    def _get_pin(self, patter, sender):
        """Returns the pin at which the 'sender' is associated."""
        m = patter.match(sender.objectName())
        assert m is not None
        return int(m.group(1))
    
    def pinModeClicked(self):
        sender = self.q_main_window.sender()
        pin = self._get_pin(RE_PINMODE_BUTTON, sender)
        logger.info("[%02d] pinModeClicked() - sender: %s", pin, sender.objectName())
        if sender.text() == 'I':
            try:
                self.proxy.pinMode(pin, ArduinoProxy.OUTPUT)
                sender.setText('O')
            except:
                # FIXME: log and show error
                pass
        else:
            try:
                sender.setText('I')
                self.proxy.pinMode(pin, ArduinoProxy.INPUT)
            except:
                # FIXME: log and show error
                pass
    
    def pinEnabledDisabled(self):
        sender = self.q_main_window.sender()
        pin = self._get_pin(RE_PIN_ENABLE_CHECKBOX, sender)
        logger.info("[%02d] pinEnabledDisabled() - sender: %s - state: %s", pin,
            sender.objectName(), str(bool(sender.checkState())))
        
        attr = getattr(self, 'pinValue%d' % pin, None)
        if bool(sender.checkState()):
            # ENABLED
            getattr(self, 'pinMode%d' % pin).setEnabled(False)
            if getattr(self, 'pinMode%d' % pin).text() == 'O': # >>> OUTPUT
                # Send HIGH/LOW
                getattr(self, 'dw%d_l' % pin).setEnabled(True)
                getattr(self, 'dw%d_h' % pin).setEnabled(True)
                if attr:
                    attr.setEnabled(True)
            else: # >>> INPUT
                # Enable/disable pullup resistor
                getattr(self, 'dw%d_l' % pin).setEnabled(True)
                getattr(self, 'dw%d_h' % pin).setEnabled(True)
                if attr:
                    attr.setEnabled(False)
        else:
            # DISABLED
            getattr(self, 'pinMode%d' % pin).setEnabled(True)
            getattr(self, 'dw%d_l' % pin).setEnabled(True)
            getattr(self, 'dw%d_h' % pin).setEnabled(True)
            if attr:
                attr.setEnabled(True)
    
    def digitalWriteLow(self):
        sender = self.q_main_window.sender()
        pin = self._get_pin(RE_DIGITAL_WRITE_LOW_BUTTON, sender)
        logger.info("[%02d] digitalWriteLow() - sender: %s", pin, sender.objectName())
        try:
            self.proxy.digitalWrite(pin, ArduinoProxy.LOW)
            self._led_off(pin)
        except:
            # FIXME: log and show error
            pass
    
    def digitalWriteHigh(self):
        sender = self.q_main_window.sender()
        pin = self._get_pin(RE_DIGITAL_WRITE_HIGH_BUTTON, sender)
        logger.info("[%02d] digitalWriteHigh() - sender: %s", pin, sender.objectName())
        try:
            self.proxy.digitalWrite(pin, ArduinoProxy.HIGH)
            self._led_on(pin)
        except:
            # FIXME: log and show error
            pass
    
    def analogWriteValueChanged(self):
        sender = self.q_main_window.sender()
        pin = self._get_pin(RE_ANALOG_WRITE_SLIDER, sender)
        logger.info("[%02d] analogWriteValueChanged() - sender: %s - value: %s", pin,
            sender.objectName(), str(sender.value()))
        # FIXME: implement!
    
    def _led_on(self, pin):
        getattr(self, "led%d" % pin).setPixmap(ArduinoProxyMainWindow.LED_ON_PIXMAP)
    
    def _led_off(self, pin):
        getattr(self, "led%d" % pin).setPixmap(ArduinoProxyMainWindow.LED_OFF_PIXMAP)
    
    def _get_enabled_pins(self):
        """
        Return a list enabled pins.
        Each element is an integer.
        """
        return [ self._get_pin(RE_PIN_ENABLE_CHECKBOX, an_attr)
            for an_attr in self._get_attributes(RE_PIN_ENABLE_CHECKBOX)
                if bool(an_attr.checkState()) ]
    
    def _update_one_pin(self, pin, log):
        # TODO: double check: if this pin is enabled
        if getattr(self, 'pinMode%d' % pin).text() == 'I': # >>> INPUT
            value = self.proxy.digitalRead(pin)
            assert value in [ArduinoProxy.HIGH, ArduinoProxy.LOW]
            ## self._set_led_from_value(pin, value)
            log.write(" - pin[%d] -> %s" % (pin, str(value)))
            if value == ArduinoProxy.HIGH:
                self._led_on(pin)
            else:
                self._led_off(pin)
    
    def update_arduino_values(self):
        log = StringIO()
        try:
            ret = self.proxy.connect()
            log.write("connect(): %s" % ret)
            for pin in self._get_enabled_pins():
                self._update_one_pin(pin, log)
            self.statusbar.showMessage(log.getvalue())
        except:
            traceback.print_exc()
            self.statusbar.showMessage("EXCEPTION DETECTED. More info: %s" % log.getvalue())
    
    def checkbox_auto_update_toggle(self):
        """Toggle auto-update."""
        enabled = bool(self.checkboxAutoUpdate.checkState())
        if enabled:
            self.pushButtonUpdate.setEnabled(False)
            self.update_timer.start(50)
        else:
            self.update_timer.stop()
            self.pushButtonUpdate.setEnabled(True)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def default_args_validator(parser, options, args): # pylint: disable=W0613
    if len(args) <1:
        parser.error("You should specify the serial device.")

def main():
    options, args, proxy = default_main(args_validator=default_args_validator)
    app = QtGui.QApplication(args[1:])
    q_main_window = QtGui.QMainWindow()
    window = ArduinoProxyMainWindow(q_main_window, options, args, proxy) # pylint: disable=W0612
    q_main_window.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
