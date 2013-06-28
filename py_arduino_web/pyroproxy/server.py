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

import os
import hmac
import Pyro4

from arduino_proxy.proxy import ArduinoProxy


def main():
    """
    Expose object using PyRO
    """
    if "ENABLE_LOGGING" in os.environ:
        import logging
        logging.basicConfig(level=logging.DEBUG)
    Pyro4.config.HMAC_KEY = hmac.new('this-is-py-arduino').digest()
    Pyro4.config.SOCK_REUSE = True
    proxy = ArduinoProxy()
    Pyro4.Daemon.serveSimple(
        {
            proxy: "arduino_proxy.Proxy",
            proxy.storage: "arduino_proxy.Storage",
        },
        host="localhost", port=61234, ns=False)
    # FORMA DE URI -> uri_string = "PYRO:arduino_proxy.Proxy@localhost:61234"

if __name__ == '__main__':
    main()
