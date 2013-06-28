##-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
##    py-arduino - Access your Arduino from Python
##    Copyright (C) 2011-2012 - Horacio Guillermo de Oro <hgdeoro@gmail.com>
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


def setup_pythonpath():
    try:
        from py_arduino import PyArduino
    except ImportError:
        import os
        import sys
        PROJECT_DIR = os.path.split(os.path.realpath(__file__))[0]  # PROJECT_DIR/py_arduino/tests
        PROJECT_DIR = os.path.split(PROJECT_DIR)[0]  # PROJECT_DIR/py_arduino
        PROJECT_DIR = os.path.split(PROJECT_DIR)[0]  # PROJECT_DIR
        sys.path.append(os.path.abspath(PROJECT_DIR))
        from py_arduino import PyArduino  # to force check
