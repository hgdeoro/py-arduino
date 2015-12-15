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

import sys
import time

from py_arduino import LOW, HIGH, OUTPUT
from py_arduino_web.pyroproxy.utils import BasePyroMain


def print_help():
    print ""
    print "Forma de uso:"
    print "    digital_write.py <PIN_DIGIAL> <0|1>"
    print ""
    
class Main(BasePyroMain):

    def run(self, arduino):
        
        try:
            pin_number = int(sys.argv[1])
        except IndexError:
            print "ERROR: no se ha especificado el 1er argumento (PIN DIGITAL)"
            print_help()
            sys.exit(1)
        except ValueError:
            print "ERROR: el primer argumento (PIN DIGITAL) no es un entero valido"
            print_help()
            sys.exit(1)

        try:        
            value = int(sys.argv[2])
        except IndexError:
            print "ERROR: no se ha especificado el 2do argumento (0 -> LOW, 1 -> HIGH)"
            print_help()
            sys.exit(1)
        except ValueError:
            print "ERROR: el 2do argumento (valor a escribir) no es un entero valido"
            print_help()
            sys.exit(1)
        
        if value not in [LOW, HIGH]:
            print "ERROR: el valor para el 2do argumento no es valido"
            print "  Valores validos: 0 y 1 (0 -> LOW, 1 -> HIGH)"
            print_help()
            sys.exit(1)
        
        assert value in [LOW, HIGH]
        
        print "Setting pin {} to OUTPUT".format(pin_number)
        arduino.pinMode(pin_number, OUTPUT)

        print "Writing {} on pin {}".format(value, pin_number)
        arduino.digitalWrite(pin_number, value)

if __name__ == '__main__':
    Main().start()
