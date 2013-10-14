##-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
##    py-arduino - Access your Arduino from Python
##    Copyright (C) 2011-2013 - Horacio Guillermo de Oro <hgdeoro@gmail.com>
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

#===============================================================================
# CONSTANTS - Values to write to pins, and read from pins
#===============================================================================
HIGH = 0x01  # define HIGH 0x1
LOW = 0x00  # define LOW  0x0

#===============================================================================
# CONSTANTS - Pin modes
#===============================================================================
INPUT = 0x00  # define INPUT 0x0
OUTPUT = 0x01  # define OUTPUT 0x1

# This mode doesn't exists in Arduino.
# We use internally it to track the mode of a pin
MODE_UNKNOWN = None

#===============================================================================
# CONSTANTS - Bit
#===============================================================================
LSBFIRST = 0x00  # define LSBFIRST 0
MSBFIRST = 0x01  # define MSBFIRST 1

#===============================================================================
# CONSTANTS - Interrupt
#===============================================================================
ATTACH_INTERRUPT_MODE_LOW = 'L'
ATTACH_INTERRUPT_MODE_CHANGE = 'C'
ATTACH_INTERRUPT_MODE_RISING = 'R'
ATTACH_INTERRUPT_MODE_FALLING = 'F'

#===============================================================================
# CONSTANTS - Other
#===============================================================================

# Default serial speed
DEFAULT_SERIAL_SPEED = 9600

# Device to use to launch an emulator instad of connecting to a real Arduino
DEVICE_FOR_EMULATOR = '/dev/ARDUINO_EMULATOR'

#===============================================================================
# CONSTANTS - serial
#===============================================================================

INVALID_CMD = "INVALID_CMD"
INVALID_PARAMETER = "INVALID_PARAMETER"
UNSUPPORTED_CMD = "UNSUPPORTED_CMD"


#===============================================================================
# Exceptions
#===============================================================================

class PyArduinoException(Exception):
    """Base class for all the exception raised in the project."""


class InvalidCommand(PyArduinoException):
    """
    Raised when the Arduino reported an error in the command.
    """

    def __init__(self, msg, error_code=None):
        PyArduinoException.__init__(self, msg)
        self.error_code = error_code


class InvalidParameter(PyArduinoException):
    """
    Raised when the Arduino reported an invalid parameter.
    """

    def __init__(self, msg, error_param=None):
        PyArduinoException.__init__(self, msg)
        self.error_param = error_param


class InvalidResponse(PyArduinoException):
    """
    Raised when the response from the Arduino wasn't valid.
    """


class EmptyResponse(PyArduinoException):
    """
    Raised when the response from the Arduino was empty.
    """


class CommandTimeout(PyArduinoException):
    """
    Raised when a timeout occurs while waiting for Arduino's response.
    """


class InvalidArgument(PyArduinoException):
    """
    Raised when a method was called with invalid argument type or values.
    This is detected in Python, and thus no data was sent to the Arduino.
    """


class UnsupportedCommand(PyArduinoException):
    """
    Raised when there is no support for the given command in the Arduino.
    
    Raised when lcdWrite() is used, but the uploaded program to the Arduino wans't generated with
    support for LCD. This means that the command is valid, but the program in the Arduino lacks
    the functionality to run it.
    """

    def __init__(self, msg, error_param=None):
        PyArduinoException.__init__(self, msg)
        self.error_param = error_param


class NotConnected(PyArduinoException):
    """
    Raised when a method that required a connection was called, but the
    instance wasn't connected.
    """
