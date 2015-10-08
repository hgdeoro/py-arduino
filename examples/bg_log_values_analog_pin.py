# Licensed under the Apache License, Version 2.0
# Copyright (C) 2011-2015 - Horacio Guillermo de Oro <hgdeoro@gmail.com>

import logging
import os

from py_arduino_web.pyroproxy.mules import MuleAnalogPinLogger


class Main(MuleAnalogPinLogger):
    """
    To launch the uwsgi daemon with this running as background:

        ./bin/run_uwsgi.sh --mule=examples/bg_log_values_analog_pin.py

    """
    logger = logging.getLogger(os.path.split(__file__)[-1])


if __name__ == '__main__':
    Main().start()
