##-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
##    PyArduinoProxy - Access your Arduino from Python
##    Copyright (C) 2011-2013 - Horacio Guillermo de Oro <hgdeoro@gmail.com>
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

import Pyro4
import hmac
import sys

from arduino_proxy.proxy import DEVICE_FOR_EMULATOR


def main():
    Pyro4.config.HMAC_KEY = hmac.new('this-is-PyArduinoProxy').digest()
    arduino_proxy = Pyro4.Proxy("PYRO:arduino_proxy.Proxy@localhost:61234")
    if len(sys.argv) > 1:
        device = sys.argv[1]
    else:
        device = DEVICE_FOR_EMULATOR
    print "Calling proxy.connect() - Connecting to {0}".format(device)
    arduino_proxy.connect(device)
    print "Calling proxy.ping() to check the connection"
    ret = arduino_proxy.ping()
    print "Ping returned: '{0}'. End.".format(ret)

if __name__ == '__main__':
    main()
