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

import Pyro4
import hmac
import sys


def main():
    Pyro4.config.HMAC_KEY = hmac.new('this-is-PyArduinoProxy').digest()
    arduino_proxy = Pyro4.Proxy("PYRO:arduino_proxy.Proxy@localhost:61234")
    print "Check connection status..."
    connected = arduino_proxy.is_connected()
    if not connected:
        print "ERROR: ArduinoProxy isn't connected to an Arduino or to the emulator. "
        print "See the 'connect' script."
        sys.exit(1)
    print "Calling proxy.ping()"
    ret = arduino_proxy.ping()
    print "Ping returned: '{0}'. End.".format(ret)

if __name__ == '__main__':
    main()
