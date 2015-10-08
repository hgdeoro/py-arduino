#!/usr/bin/env python
# Licensed under the Apache License, Version 2.0
# Copyright (C) 2011-2015 - Horacio Guillermo de Oro <hgdeoro@gmail.com>

import logging
import unittest

from py_arduino.arduino import PyArduino


class AutoConnectTest(unittest.TestCase):
    """
    Just call autoconnect(). This test WILL FAILL if you don't have an Arduino connected!
    """

    def test_autoconnect(self):
        logging.basicConfig(level=logging.DEBUG)
        arduino = PyArduino()
        arduino.autoconnect()
        arduino.ping()
        arduino.close()


if __name__ == '__main__':
    unittest.main()
