#!/usr/bin/env python
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

import datetime
import logging
import optparse
import os
import shutil
import sys
import textwrap

from StringIO import StringIO

BASE_DIR = os.path.split(os.path.realpath(__file__))[0]  # BASE_DIR = XXX/sketches
BASE_DIR = os.path.split(BASE_DIR)[0]  # BASE_DIR = XXX

try:
    from py_arduino.arduino import PyArduino as tmp  # @UnusedImport
except ImportError:
    sys.path.append(os.path.abspath(BASE_DIR))

from py_arduino import ATTACH_INTERRUPT_MODE_LOW, \
    ATTACH_INTERRUPT_MODE_CHANGE, ATTACH_INTERRUPT_MODE_RISING, \
    ATTACH_INTERRUPT_MODE_FALLING, INVALID_CMD, INVALID_PARAMETER,\
    UNSUPPORTED_CMD
from py_arduino.arduino import PyArduino


def generate_placeholder_values(arduino, options):
    arduino_functions = arduino.get_arduino_functions()

    if len(arduino_functions) != len(set([function.arduino_function_name for function in
            arduino_functions])):
        raise(Exception("There are duplicates arduino function names (that's defined " + \
            "function.arduino_function_name = 'something')"))

    proxied_function_source = StringIO() # Arduino function's sources
    proxied_function_headers = StringIO() # To add in the header (#includes, etc.)
    proxied_function_globals = StringIO() # Global variables
    proxied_function_setup = StringIO() # To run in Arduino's setup()
    proxied_function_names = StringIO()
    proxied_function_ptrs = StringIO()

    logging.info("Generating functions:")
    for function in arduino_functions:
        logging.info(" + %s()", function.__name__)
        proxied_function_source.write("\n")
        proxied_function_source.write("// sources for {0}()\n".format(function.__name__))
        proxied_function_source.write(function.arduino_code)
        proxied_function_source.write("\n")
        if hasattr(function, 'arduino_header'):
            logging.info("     - arduino_header")
            proxied_function_headers.write("\n")
            proxied_function_headers.write("// headers for {0}()\n".format(function.__name__))
            proxied_function_headers.write(function.arduino_header)
            proxied_function_headers.write("\n")
        if hasattr(function, 'arduino_globals'):
            logging.info("     - arduino_globals")
            proxied_function_globals.write("\n")
            proxied_function_globals.write("// globals for {0}()\n".format(function.__name__))
            proxied_function_globals.write(function.arduino_globals)
            proxied_function_globals.write("\n")
        if hasattr(function, 'arduino_setup'):
            logging.info("     - arduino_setup")
            proxied_function_setup.write("\n")
            proxied_function_setup.write("// setup code for {0}()\n".format(function.__name__))
            proxied_function_setup.write(function.arduino_setup)
            proxied_function_setup.write("\n")
        proxied_function_names.write('"%s", ' % function.arduino_function_name)
        proxied_function_ptrs.write('%s, ' % function.arduino_function_name)

    placeholder_values = {
        'proxied_function_count': len(arduino_functions),
        'proxied_function_names': proxied_function_names.getvalue(),
        'proxied_function_ptrs': proxied_function_ptrs.getvalue(),
        'proxied_function_source': proxied_function_source.getvalue(),
        'proxied_function_headers': proxied_function_headers.getvalue(),
        'proxied_function_globals': proxied_function_globals.getvalue(),
        'proxied_function_setup': proxied_function_setup.getvalue(),
        'serial_speed': arduino.speed,
        'INVALID_CMD': INVALID_CMD,
        'INVALID_PARAMETER': INVALID_PARAMETER,
        'UNSUPPORTED_CMD': UNSUPPORTED_CMD,
        'ATTACH_INTERRUPT_MODE_LOW': ATTACH_INTERRUPT_MODE_LOW,
        'ATTACH_INTERRUPT_MODE_CHANGE': ATTACH_INTERRUPT_MODE_CHANGE,
        'ATTACH_INTERRUPT_MODE_RISING': ATTACH_INTERRUPT_MODE_RISING,
        'ATTACH_INTERRUPT_MODE_FALLING': ATTACH_INTERRUPT_MODE_FALLING,
    }

    return placeholder_values


def replace_placeholder_values(placeholder_values, input_lines, output):
    """
    For each elemento of 'input_lines', replace the values, and write
    the generated lines to 'output' (an StringIO instance).
    """
    output.write(textwrap.dedent("""
        //
        // THIS FILE WAS GENERATED AUTOMATICALLY on {0}
        // WITH 'sketches/generate_sketch.py'
        // WHICH IS PART OF THE PROJECT "py-arduino"
        //
    """.format(str(datetime.datetime.now()))))

    output.write("\n\n")
    for line in input_lines:
        splitted = line.split()
        if len(splitted) > 2 and \
                splitted[-2] == '//' and \
                splitted[-1] == '{***PLACEHOLDER***}':
            output.write('// >>>>>>>>>>>>>>>>>>>> PLACEHOLDER <<<<<<<<<<<<<<<<<<<<\n')
            try:
                modified_line = line % placeholder_values
                output.write(modified_line)
                logging.info(" + PLACEHOLDER found. Line: %s", line)
                if modified_line == line:
                    logging.error(" + PLACEHOLDER found, but no change was found in the line.")
                    logging.error("    - Original line: %s", line)
                    logging.error("    - Modified line: %s", modified_line)
                    assert False
            except TypeError:
                print "> "
                print "> Error while trying to replace values in line with PLACEHOLDER"
                print "> Line: %s" % line
                print "> "
                raise
        else:
            output.write(line)
        output.write('\n')


def main():  # pylint: disable=R0914,R0912,R0915

    parser = optparse.OptionParser()
    (options, args) = parser.parse_args()  # pylint: disable=W0612

    if len(args) != 1:
        parser.error("Must specify the output directory")

    output_dir = args[0]
    if not os.path.isdir(output_dir):
        parser.error("The specified output directory isn't a directory! Path: {0}".format(
            output_dir))

    c_input_filename = os.path.join(BASE_DIR, 'src-c', 'py_arduino.c')
    h_input_filename = os.path.join(BASE_DIR, 'src-c', 'py_arduino.h')

    extra_source_filenames = [
        'arduino_type.h',
        'avr_cpunames.h',
        'dht11.cpp',
        'dht11.h',
        'OneWire.cpp',
        'OneWire.h',
    ]

    logging.info("Template for .ino file: %s", c_input_filename)
    logging.info("Template for .h file: %s", h_input_filename)
    for a_file in extra_source_filenames:
        logging.info("Extra source file: %s", a_file)

    c_file = open(c_input_filename, 'r')
    c_file_lines = [line.strip('\r\n') for line in c_file.readlines()]

    arduino = PyArduino()
    placeholder_values = generate_placeholder_values(arduino, options)

    output = StringIO()

    logging.info("Generating C/PDE file...")
    replace_placeholder_values(placeholder_values, c_file_lines, output)

    # Writing .C/.INO file
    output_file_c_filename = os.path.join(output_dir, 'py_arduino.ino')
    logging.info("Writing to %s", output_file_c_filename)
    output_file_c = open(output_file_c_filename, 'w')
    output_file_c.write(output.getvalue())
    output_file_c.close()

    # Coping .H file
    output_file_h_filename = os.path.join(output_dir, 'py_arduino.h')
    logging.info("Copying to %s", output_file_h_filename)
    shutil.copyfile(h_input_filename, output_file_h_filename)

    # Coping extra source files
    for extra_filename in extra_source_filenames:
        input_filename = os.path.join(BASE_DIR, 'src-c', extra_filename)
        output_filename = os.path.join(output_dir, extra_filename)
        logging.info("Copying to %s", output_filename)
        shutil.copyfile(input_filename, output_filename)

    logging.info("Done!")

if __name__ == '__main__':
    FORMAT = '[%(levelname)-7s] %(message)s'
    logging.basicConfig(level=logging.INFO, format=FORMAT)
    main()
