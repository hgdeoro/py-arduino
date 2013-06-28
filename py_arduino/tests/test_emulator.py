#!/usr/bin/env python
##-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
##    PyArduinoProxy - Access your Arduino from Python
##    Copyright (C) 2011-2012 - Horacio Guillermo de Oro <hgdeoro@gmail.com>
##
##    This file is part of PyArduinoProxy.
##
##    PyArduinoProxy is free software; you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation version 2.
##
##    PyArduinoProxy is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License version 2 for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with PyArduinoProxy; see the file LICENSE.txt.
##-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

import logging
import os
import sys
import time
import unittest
from arduino_proxy.proxy import HIGH, LOW, OUTPUT, INPUT

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
        self.proxy = ArduinoProxy.create_emulator(
            initial_input_buffer_contents="** SOME TEXT **\n" * 5)

    def test_ping(self):
        self.proxy.validateConnection()
        response = self.proxy.ping()
        self.assertEquals(response, 'PING_OK')

    def tearDown(self): # pylint: disable=C0103
        self.proxy.close()


class TestProxiedMethodsOfArduinoProxy(unittest.TestCase): # pylint: disable=R0904
    """
    Testcase for commands.
    """

    def setUp(self): # pylint: disable=C0103
        self.proxy = ArduinoProxy.create_emulator()

    def test_ping(self):
        response = self.proxy.ping()
        self.assertEquals(response, 'PING_OK')

    def test_multiping(self):
        for i in range(0, 10): # pylint: disable=W0612 @UnusedVariable
            start = time.time()
            response = self.proxy.ping()
            end = time.time()
            self.assertEquals(response, 'PING_OK')
            logging.info("PING took %.2f ms", ((end - start) * 1000))

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
        self.assertTrue(response in [HIGH, LOW])

        # test with invalid arguments
        for an_arg in (None, 'something', Exception(), 1.1):
            self.assertRaises(InvalidArgument, self.proxy.digitalRead, an_arg)

    def test_digital_write(self):
        self.proxy.digitalWrite(99, HIGH)
        self.proxy.digitalWrite(99, LOW)

        # test with invalid arguments
        for an_arg in (None, 'something', Exception(), 1.1):
            self.assertRaises(InvalidArgument, self.proxy.digitalWrite, 99, an_arg)
            self.assertRaises(InvalidArgument, self.proxy.digitalWrite, an_arg, HIGH)
            self.assertRaises(InvalidArgument, self.proxy.digitalWrite, an_arg, LOW)

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
        self.proxy.pinMode(99, OUTPUT)
        self.proxy.pinMode(99, INPUT)

        # test with invalid arguments
        for an_arg in (None, 'something', Exception(), 1.1):
            self.assertRaises(InvalidArgument, self.proxy.pinMode, 99, an_arg)
            self.assertRaises(InvalidArgument, self.proxy.pinMode, an_arg, OUTPUT)
            self.assertRaises(InvalidArgument, self.proxy.pinMode, an_arg, INPUT)

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

    def test_disableDebug(self):
        self.proxy.disableDebug()

    def test_enableDebug(self):
        self.proxy.enableDebug()

    def test_getArduinoTypeStruct(self):
        ard_type_st = self.proxy.getArduinoTypeStruct()
        self.assertTrue(ard_type_st['analog_pins'])
        self.assertTrue(ard_type_st['digital_pins'])
        self.assertTrue(ard_type_st['pwm_pins_bitmap'])
        self.assertTrue(ard_type_st['eeprom_size'])
        self.assertTrue(ard_type_st['flash_size'])
        self.assertTrue(ard_type_st['ram_size'])
        self.assertTrue(ard_type_st['pwm_pin_list'])
        self.assertTrue(ard_type_st['eeprom_size_bytes'])
        self.assertTrue(ard_type_st['flash_size_bytes'])
        self.assertTrue(ard_type_st['ram_size_bytes'])

        enhanced = self.proxy.enhanceArduinoTypeStruct(ard_type_st)
        self.assertTrue(enhanced['digital_pins_items'])
        self.assertTrue(enhanced['analog_pins_items'])
        self.assertTrue(enhanced['digital_pins_struct'])
        for item in enhanced['digital_pins_struct']:
            self.assertTrue('pin' in item)
            self.assertTrue('digital' in item)
            self.assertTrue('pwm' in item)
            self.assertTrue('label' in item)
        self.assertTrue(enhanced['analog_pins_struct'])

    def test_getAvrCpuType(self):
        self.proxy.getAvrCpuType()

    def tearDown(self): # pylint: disable=C0103
        self.proxy.close()


## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestInternalsOfArduinoProxy(unittest.TestCase): # pylint: disable=R0904

    def setUp(self): # pylint: disable=C0103
        self.proxy = ArduinoProxy.create_emulator()

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
