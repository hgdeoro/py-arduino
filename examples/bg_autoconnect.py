import logging
import time

from py_arduino_web.pyroproxy.utils import BasePyroMain


class MuleAutoconnect(BasePyroMain):

    def __init__(self, *args, **kwargs):
        super(MuleAutoconnect, self).__init__(*args, **kwargs)

    def add_options(self):
        super(MuleAutoconnect, self).add_options()
        self.parser.add_option("--delay", default="5",
            dest="delay", help="Seconds to wait between checks")

    def _run(self, arduino):
        """This method implements the real check"""
        arduino.run_watchdog(autoconnect=True)

    def run(self, arduino):
        self.logger.info("Waiting 2 seconds to start...")
        time.sleep(2)
        self.logger.info("Starting MuleAutoconnect")
        delay = int(self.options.delay)
        self.logger.info("Using delay of %s seconds", delay)

        while True:
            try:
                self._run(arduino)
            except:
                self.logger.exception("Error detected")
            time.sleep(delay)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    MuleAutoconnect().start()
