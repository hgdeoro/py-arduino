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
import os.path
import shutil
import sys

from StringIO import StringIO

# Setup PYTHONPATH
SRC_DIR = os.path.split(os.path.realpath(__file__))[0] # SRC_DIR/arduino_proxy/tests
SRC_DIR = os.path.split(SRC_DIR)[0] # SRC_DIR/arduino_proxy
SRC_DIR = os.path.split(SRC_DIR)[0] # SRC_DIR
sys.path.append(os.path.abspath(SRC_DIR))

from arduino_proxy.proxy import ArduinoProxy, _unindent

def main():
    
    if len(sys.argv) != 2:
        raise(Exception("Must specify output directory!"))
    
    output_dir = sys.argv[1]
    if not os.path.isdir(output_dir):
        raise(Exception("Output path isn't a directory! Path: %s" % output_dir))
    
    c_input_filename = os.path.join(SRC_DIR, 'src-c', 'arduino.c')
    h_input_filename = os.path.join(SRC_DIR, 'src-c', 'py_arduino_proxy.h')
    
    logging.info("Template for .c/.pde file: %s", c_input_filename)
    logging.info("Template for .h file: %s", h_input_filename)
    
    c_file = open(c_input_filename, 'r')
    c_file_lines = [line.strip('\r\n') for line in c_file.readlines()]
    for i in range(0, len(c_file_lines)):
        splitted = c_file_lines[i].split()
        if len(splitted) >= 3 and \
                splitted[0] == '#define' and \
                splitted[1] == 'PY_ARDUINO_PROXY_DEVEL' and \
                splitted[2].startswith('//'):
            c_file_lines[i] = '// ' + c_file_lines[i]
            break
    
    output = StringIO()
    output.write(_unindent(8, """
        //
        // THIS FILE IS GENERATED AUTOMATICALLI WITH generate-pde.sh
        // WHICH IS PART OF THE PROJECT "PyArduinoProxy"
        //
    """))
    output.write("\n\n")
    
    proxy = ArduinoProxy('')
    proxy_functions = proxy.get_proxy_functions()
    
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
        proxied_function_names.write('"_%s", ' % function.__name__)
        proxied_function_ptrs.write('_%s, ' % function.__name__)

    placeholder_values = {
        'proxied_function_count': len(proxy_functions), 
        'proxied_function_names': proxied_function_names.getvalue(), 
        'proxied_function_ptrs': proxied_function_ptrs.getvalue(), 
        'proxied_function_source': proxied_function_source.getvalue(), 
        'serial_speed': proxy.speed, 
        'INVALID_CMD': ArduinoProxy.INVALID_CMD, 
        'INVALID_PARAMETER': ArduinoProxy.INVALID_PARAMETER,
    }
    
    logging.info("Generating C/PDE file...")
    for line in c_file_lines:
        splitted = line.split()
        if len(splitted) > 2 and \
                splitted[-2] == '//' and \
                splitted[-1] == '{***PLACEHOLDER***}':
            output.write('// >>>>>>>>>>>>>>>>>>>> PLACEHOLDER <<<<<<<<<<<<<<<<<<<<\n')
            try:
                output.write(line % placeholder_values)
                logging.info(" + PLACEHOLDER found. Line: %s", line)
            except TypeError:
                print "> "
                print "> Error while trying to replace values in line with PLACEHOLDER"
                print "> Line: %s" % line
                print "> "
                raise
        else:
            output.write(line)
        output.write('\n')
    
    # Writing .C/.PDE file
    output_file_c_filename = os.path.join(output_dir, 'py_arduino_proxy.pde')
    logging.info("Writing to %s", output_file_c_filename)
    output_file_c = open(output_file_c_filename, 'w')
    output_file_c.write(output.getvalue())
    output_file_c.close()
    
    # Coping .H file
    output_file_h_filename = os.path.join(output_dir, 'py_arduino_proxy.h')
    logging.info("Copying to %s", output_file_h_filename)
    shutil.copyfile(h_input_filename, output_file_h_filename)
    
    logging.info("Done!")
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
