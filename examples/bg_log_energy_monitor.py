import logging
import os
import time

from py_arduino_web.pyroproxy.utils import BasePyroMain


class Main(BasePyroMain):
    """
    To launch the uwsgi daemon with this running as background:

        ./bin/run_uwsgi.sh --mule=examples/bg_log_values_analog_pin.py

    """

    logger = logging.getLogger(os.path.split(__file__)[-1])

    def run(self, arduino):
        self.logger.info("Starting...")

        v_pin, v_calibration, v_phase_shift, c_pin, c_calibration = 1, 2.2, 3.3, 4, 5.5
        no_wl, timeout = 1, 2

        if not arduino.is_connected():
            self.logger.debug("Arduino is not connected...")
            while not arduino.is_connected():
                self.logger.info("Waiting until connected...")
                time.sleep(5)
            self.logger.info("Connected!")

        ## setup()

        try:
            self.logger.debug("Calling energyMonitorSetup()")
            arduino.energyMonitorSetup(v_pin, v_calibration, v_phase_shift, c_pin, c_calibration)
        except:
            self.logger.exception("Error detected when called bg_setup()")
            return

        ## loop()

        try:
            self.logger.debug("Entering loop...")
            while True:
                arduino.energyMonitorRead(no_wl, timeout)
                time.sleep(0.5)
        except:
            self.logger.exception("Error detected in loop")
            return


if __name__ == '__main__':
    Main().start()
