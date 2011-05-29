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
import os
import pprint
import random
import sys
import time
import unittest
import weakref

# Setup PYTHONPATH
SRC_DIR = os.path.split(os.path.realpath(__file__))[0] # SRC_DIR/arduino_proxy/tests
SRC_DIR = os.path.split(SRC_DIR)[0] # SRC_DIR/arduino_proxy
SRC_DIR = os.path.split(SRC_DIR)[0] # SRC_DIR
sys.path.append(os.path.abspath(SRC_DIR))

from arduino_proxy import ArduinoProxy, InvalidArgument, InvalidResponse, InvalidCommand

logger = logging.getLogger(__name__) # pylint: disable=C0103

class TestArduinoProxyWithInitialContentInSerialBuffer(unittest.TestCase): # pylint: disable=R0904
    """
    Testcase for commands.
    """
    def setUp(self): # pylint: disable=C0103
        self.proxy = ArduinoProxy(tty='')
        self.proxy.serial_port = SerialConnectionMock( \
            initial_in_buffer_contents="** SOME TEXT **\n" * 5)
        self.emulator = ArduinoEmulator(self.proxy.serial_port.get_other_side())
        self.emulator.start()

    def test_ping(self):
        self.proxy.validate_connection()
        response = self.proxy.ping()
        self.assertEquals(response, 'PING_OK')

    def tearDown(self): # pylint: disable=C0103
        self.proxy.close()
        self.emulator.stop_running()
        logger.info("tearDown(): emulator.join()")
        self.emulator.join()
        logger.debug("tearDown(): %s", str(self.proxy.serial_port))

class TestProxiedMethodsOfArduinoProxy(unittest.TestCase): # pylint: disable=R0904
    """
    Testcase for commands.
    """
    
    def setUp(self): # pylint: disable=C0103
        self.proxy = ArduinoProxy(tty='')
        self.proxy.serial_port = SerialConnectionMock()
        self.emulator = ArduinoEmulator(self.proxy.serial_port.get_other_side())
        self.emulator.start()
    
    def test_ping(self):
        response = self.proxy.ping()
        self.assertEquals(response, 'PING_OK')
    
    def test_multiping(self):
        for i in range(0, 10): # pylint: disable=W0612
            start = time.time()
            response = self.proxy.ping()
            end = time.time()
            self.assertEquals(response, 'PING_OK')
            logging.info("PING took %.2f ms", ((end-start)*1000))
    
    def test_analog_read(self):
        response = self.proxy.analogRead(5)
        self.assertTrue(type(response) is int)
        if response < 0 or response > 1023:
            self.fail("analogRead() returned invalid value: %d" % response)
        
        # test with invalid arguments
        for an_arg in (None, 'something', Exception(), 1.1):
            self.assertRaises(InvalidArgument, self.proxy.analogRead, an_arg)

    def test_digital_read(self):
        response = self.proxy.digitalRead(99)
        self.assertTrue(response in [ArduinoProxy.HIGH, ArduinoProxy.LOW])
        
        # test with invalid arguments
        for an_arg in (None, 'something', Exception(), 1.1):
            self.assertRaises(InvalidArgument, self.proxy.digitalRead, an_arg)
    
    def test_digital_write(self):
        self.proxy.digitalWrite(99, ArduinoProxy.HIGH)
        self.proxy.digitalWrite(99, ArduinoProxy.LOW)

        # test with invalid arguments
        for an_arg in (None, 'something', Exception(), 1.1):
            self.assertRaises(InvalidArgument, self.proxy.digitalWrite, 99, an_arg)
            self.assertRaises(InvalidArgument, self.proxy.digitalWrite, an_arg, ArduinoProxy.HIGH)
            self.assertRaises(InvalidArgument, self.proxy.digitalWrite, an_arg, ArduinoProxy.LOW)

    def test_analog_write(self):
        for value in range(0, 256):
            self.proxy.analogWrite(99, value)

        # test with invalid arguments
        self.assertRaises(InvalidArgument, self.proxy.analogWrite, 99, -1)
        self.assertRaises(InvalidArgument, self.proxy.analogWrite, 99, 256)
        self.assertRaises(InvalidArgument, self.proxy.analogWrite, 99, 1000)
        
        for an_arg in (None, 'something', Exception(), 1.1):
            self.assertRaises(InvalidArgument, self.proxy.analogWrite, 99, an_arg)
            self.assertRaises(InvalidArgument, self.proxy.analogWrite, an_arg, 0)
            self.assertRaises(InvalidArgument, self.proxy.analogWrite, an_arg, 1)
            self.assertRaises(InvalidArgument, self.proxy.analogWrite, an_arg, 100)
            self.assertRaises(InvalidArgument, self.proxy.analogWrite, an_arg, 255)

    def test_pin_mode(self):
        self.proxy.pinMode(99, ArduinoProxy.OUTPUT)
        self.proxy.pinMode(99, ArduinoProxy.INPUT)

        # test with invalid arguments
        for an_arg in (None, 'something', Exception(), 1.1):
            self.assertRaises(InvalidArgument, self.proxy.pinMode, 99, an_arg)
            self.assertRaises(InvalidArgument, self.proxy.pinMode, an_arg, ArduinoProxy.OUTPUT)
            self.assertRaises(InvalidArgument, self.proxy.pinMode, an_arg, ArduinoProxy.INPUT)

    def test_delay(self):
        self.proxy.delay(0)
        self.proxy.delay(99)
        self.proxy.delayMicroseconds(0)
        self.proxy.delayMicroseconds(99)

        # test with invalid arguments
        for an_arg in (None, 'something', Exception(), -1):
            self.assertRaises(InvalidArgument, self.proxy.delay, an_arg)
            self.assertRaises(InvalidArgument, self.proxy.delayMicroseconds, an_arg)
    
    def test_millis_micros(self):
        self.assertTrue(self.proxy.millis() >= 0)
        self.assertTrue(self.proxy.micros() >= 0)
    
    def tearDown(self): # pylint: disable=C0103
        self.proxy.close()
        self.emulator.stop_running()
        logger.info("tearDown(): emulator.join()")
        self.emulator.join()
        logger.debug("tearDown(): %s", str(self.proxy.serial_port))

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestInternalsOfArduinoProxy(unittest.TestCase): # pylint: disable=R0904
    
    def setUp(self): # pylint: disable=C0103
        self.proxy = ArduinoProxy(tty='')
        self.proxy.serial_port = SerialConnectionMock()
        self.emulator = ArduinoEmulator(self.proxy.serial_port.get_other_side())
        self.emulator.start()
    
    def test_send_cmd(self):
        
        def valid_transformer1(arg1):
            return arg1

        def valid_transformer2(arg1): # pylint: disable=W0613
            return "RESPONSE_FROM_TRANSFORMER"
        
        def invalid_transformer1():
            pass
        
        def invalid_transformer2(arg1, arg2): # pylint: disable=W0613
            pass
        
        def invalid_transformer3(arg1): # pylint: disable=W0613
            raise(Exception("Exception while transforming"))
        
        # send_cmd(self, cmd, expected_response=None, timeout=None, response_transformer=None):
        self.proxy.send_cmd("_ms", response_transformer=int)
        self.proxy.send_cmd("_ms", response_transformer=valid_transformer1)
        self.proxy.send_cmd("_ms", response_transformer=valid_transformer2,
            expected_response="RESPONSE_FROM_TRANSFORMER")
        
        self.assertRaises(InvalidResponse, self.proxy.send_cmd, "_ms",
            response_transformer=invalid_transformer1)
        self.assertRaises(InvalidResponse, self.proxy.send_cmd, "_ms", 
            response_transformer=invalid_transformer2)
        self.assertRaises(InvalidResponse, self.proxy.send_cmd, "_ms", 
            response_transformer=invalid_transformer3)
        
        self.assertRaises(InvalidResponse, self.proxy.send_cmd, "_ms", expected_response="X")
        
        self.assertRaises(InvalidCommand, self.proxy.send_cmd, "_INEXISTING_CMD")
    
    def tearDown(self): # pylint: disable=C0103
        self.proxy.close()
        self.emulator.stop_running()
        logger.info("tearDown(): emulator.join()")
        self.emulator.join()
        logger.debug("tearDown(): %s", str(self.proxy.serial_port))

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    ARGS = list(sys.argv)
    if '--debug' in ARGS:
        logging.basicConfig(level=logging.DEBUG)
        ARGS.remove('--debug')
    elif '--info' in ARGS:
        logging.basicConfig(level=logging.INFO)
        ARGS.remove('--info')
    else:
        logging.basicConfig(level=logging.WARN)
    
    unittest.main(argv=ARGS)
