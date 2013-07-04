import logging
import os

from py_arduino_web.pyroproxy.mules import MuleDigitalPinMonitor


class Main(MuleDigitalPinMonitor):
    logger = logging.getLogger(os.path.split(__file__)[-1])
    pin = 13
    script_on_high = "/usr/bin/logger -t py-arduino - Went HIGH on $(date)"
    script_on_low = "/usr/bin/logger -t py-arduino - Went LOW on $(date)"

if __name__ == '__main__':
    Main().start()
