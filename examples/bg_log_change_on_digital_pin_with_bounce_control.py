import logging
import os

from py_arduino_web.pyroproxy.mules import MuleDigitalPinMonitorWithBounceControl


class Main(MuleDigitalPinMonitorWithBounceControl):
    """
    To launch the uwsgi daemon with this running as background:

        ./bin/run_uwsgi.sh --mule=examples/bg_log_change_on_digital_pin_with_bounce_control.py

    """
    logger = logging.getLogger(os.path.split(__file__)[-1])
    pin = 13
    script_on_high = "/usr/bin/logger -t py-arduino - Went HIGH on $(date)"
    script_on_low = "/usr/bin/logger -t py-arduino - Went LOW on $(date)"
    bounce_control_time = 3


if __name__ == '__main__':
    Main().start()
