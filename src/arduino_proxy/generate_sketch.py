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
import optparse
import os
import shutil
import sys

from StringIO import StringIO

# Setup PYTHONPATH
SRC_DIR = os.path.split(os.path.realpath(__file__))[0] # SRC_DIR/arduino_proxy/tests
SRC_DIR = os.path.split(SRC_DIR)[0] # SRC_DIR/arduino_proxy
SRC_DIR = os.path.split(SRC_DIR)[0] # SRC_DIR
sys.path.append(os.path.abspath(SRC_DIR))

from arduino_proxy.proxy import ArduinoProxy, _unindent


def generate_placeholder_values(proxy, options):
    proxy_functions = proxy.get_proxy_functions()
    
    if len(proxy_functions) != len(set([function.arduino_function_name for function in
            proxy_functions])):
        raise(Exception("There are duplicates arduino function names (that's defined " + \
            "function.arduino_function_name = 'something')"))
    
    logging.info("Proxy functions:")
    for function in proxy_functions:
        logging.info(" + %s()", function.__name__)
    
    proxied_function_source = StringIO()
    proxied_function_names = StringIO()
    proxied_function_ptrs = StringIO()
    for function in proxy_functions:
        proxied_function_source.write("\n")
        proxied_function_source.write(function.arduino_code)
        proxied_function_source.write("\n")
        proxied_function_names.write('"%s", ' % function.arduino_function_name)
        proxied_function_ptrs.write('%s, ' % function.arduino_function_name)
    
    placeholder_values = {
        'proxied_function_count': len(proxy_functions),
        'proxied_function_names': proxied_function_names.getvalue(),
        'proxied_function_ptrs': proxied_function_ptrs.getvalue(),
        'proxied_function_source': proxied_function_source.getvalue(),
        'serial_speed': proxy.speed,
        'INVALID_CMD': ArduinoProxy.INVALID_CMD,
        'INVALID_PARAMETER': ArduinoProxy.INVALID_PARAMETER,
        'UNSUPPORTED_CMD': ArduinoProxy.UNSUPPORTED_CMD,
        'ATTACH_INTERRUPT_MODE_LOW': ArduinoProxy.ATTACH_INTERRUPT_MODE_LOW,
        'ATTACH_INTERRUPT_MODE_CHANGE': ArduinoProxy.ATTACH_INTERRUPT_MODE_CHANGE,
        'ATTACH_INTERRUPT_MODE_RISING': ArduinoProxy.ATTACH_INTERRUPT_MODE_RISING,
        'ATTACH_INTERRUPT_MODE_FALLING': ArduinoProxy.ATTACH_INTERRUPT_MODE_FALLING,
        'PY_ARDUINO_PROXY_LCD_SUPPORT': 0,
        'PY_ARDUINO_PROXY_DEBUG_TO_LCD': 0,
    }
    
    if options.lcd:
        placeholder_values['PY_ARDUINO_PROXY_LCD_SUPPORT'] = 1
        if not options.disable_debug_to_lcd:
            placeholder_values['PY_ARDUINO_PROXY_DEBUG_TO_LCD'] = 1
    
    return placeholder_values


def replace_placeholder_values(placeholder_values, input_lines, output):
    """
    For each elemento of 'input_lines', replace the values, and write
    the generated lines to 'output' (an StringIO instance).
    """
    output.write(_unindent(8, """
        //
        // THIS FILE WAS GENERATED AUTOMATICALLY WITH generate-pde.sh
        // WHICH IS PART OF THE PROJECT "PyArduinoProxy"
        //
    """))
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


def main(): # pylint: disable=R0914,R0912,R0915
    
    parser = optparse.OptionParser()
    parser.add_option("--lcd",
        action="store_true", dest="lcd", default=False,
        help="Generate sketch with support for LCD.")
    parser.add_option("--disable-debug-to-lcd",
        action="store_true", dest="disable_debug_to_lcd", default=False,
        help="Remove support for sending debug message to LCD. This'll shrink the sketch size.")
    parser.add_option("--output-dir",
        action="store", dest="output_dir", default="",
        help="Output directory for genereated sketch. Default: 'pde' directory.")
    
    (options, _) = parser.parse_args() # pylint: disable=W0612
    
    if options.output_dir:
        output_dir = options.output_dir
    else:
        basedir = os.environ['BASEDIR']
        output_dir = os.path.join(basedir, 'pde', 'py_arduino_proxy')
        output_dir = os.path.abspath(output_dir)
        logging.warn("Using default output directory: %s", output_dir)
    
    if not os.path.isdir(output_dir):
        raise(Exception("Output path isn't a directory! Path: %s" % output_dir))
    
    c_input_filename = os.path.join(SRC_DIR, 'src-c', 'py_arduino_proxy.c')
    h_input_filename = os.path.join(SRC_DIR, 'src-c', 'py_arduino_proxy.h')
    
    extra_source_filenames = [
        'arduino_type.h',
        'avr_cpunames.h',
        'dht11.cpp',
        'dht11.h',
    ]
    
    logging.info("Template for .ino file: %s", c_input_filename)
    logging.info("Template for .h file: %s", h_input_filename)
    for a_file in extra_source_filenames:
        logging.info("Extra source file: %s", a_file)
    
    c_file = open(c_input_filename, 'r')
    c_file_lines = [line.strip('\r\n') for line in c_file.readlines()]
    
    # Remove 'PY_ARDUINO_PROXY_DEVEL' from C file
    for i in range(0, len(c_file_lines)):
        splitted = c_file_lines[i].split()
        if len(splitted) >= 3 and \
                splitted[0] == '#define' and \
                splitted[1] == 'PY_ARDUINO_PROXY_DEVEL' and \
                splitted[2].startswith('//'):
            c_file_lines[i] = '// ' + c_file_lines[i]
            break
    
    proxy = ArduinoProxy.create_emulator()
    placeholder_values = generate_placeholder_values(proxy, options)
    proxy.close()

    output = StringIO()
    
    logging.info("Generating C/PDE file...")
    replace_placeholder_values(placeholder_values, c_file_lines, output)
    
    # Writing .C/.INO file
    output_file_c_filename = os.path.join(output_dir, 'py_arduino_proxy.ino')
    logging.info("Writing to %s", output_file_c_filename)
    output_file_c = open(output_file_c_filename, 'w')
    output_file_c.write(output.getvalue())
    output_file_c.close()
    
    # Coping .H file
    output_file_h_filename = os.path.join(output_dir, 'py_arduino_proxy.h')
    logging.info("Copying to %s", output_file_h_filename)
    shutil.copyfile(h_input_filename, output_file_h_filename)

    # Coping extra source files
    for extra_filename in extra_source_filenames:
        input_filename = os.path.join(SRC_DIR, 'src-c', extra_filename)
        output_filename = os.path.join(output_dir, extra_filename)
        logging.info("Copying to %s", output_filename)
        shutil.copyfile(input_filename, output_filename)

    logging.info("Done!")
    
if __name__ == '__main__':
    FORMAT = '[%(levelname)-7s] %(message)s'
    logging.basicConfig(level=logging.INFO, format=FORMAT)
    main()
