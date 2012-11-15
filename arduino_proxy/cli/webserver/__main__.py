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

import sys

from arduino_proxy.main_utils import default_main, \
    optional_device_arg_validator
from arduino_proxy.webui.web import start_webserver


def exit_on_error():
    sys.exit(1)


def add_options_callback(parser):
    parser.add_option("--http-port",
        action="store", dest="http_port", default="8080",
        help="TCP port to listen.")
    parser.add_option("--exit-on-validate-connection-error",
        action="store_true", dest="exit_on_validate_connection_error", default=False,
        help="Exit if validateConnection() fails")


def main():
    options, _, proxy = default_main(add_options_callback=add_options_callback,
        args_validator=optional_device_arg_validator, connect_only_if_device_specified=True)

    try:
        http_port = int(options.http_port)
    except ValueError:
        raise(Exception("Http port is not valid: {0}".format(options.http_port)))

    if options.exit_on_validate_connection_error:
        start_webserver(http_port, proxy=proxy, validate_connection_error_handler=exit_on_error)
    else:
        start_webserver(http_port, proxy=proxy)


if __name__ == '__main__':
    main()
