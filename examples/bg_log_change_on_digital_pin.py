# Licensed under the Apache License, Version 2.0
# Copyright (C) 2011-2015 - Horacio Guillermo de Oro <hgdeoro@gmail.com>

import logging
import os

from py_arduino_web.pyroproxy.mules import MuleDigitalPinMonitor


class Main(MuleDigitalPinMonitor):
    """
    To launch the uwsgi daemon with this running as background:

        ./bin/run_uwsgi.sh --mule=examples/bg_log_change_on_digital_pin.py

    """
    logger = logging.getLogger(os.path.split(__file__)[-1])
    script_on_high = "/usr/bin/logger -t py-arduino - Went HIGH on $(date)"
    script_on_low = "/usr/bin/logger -t py-arduino - Went LOW on $(date)"


if __name__ == '__main__':
    Main().start()
