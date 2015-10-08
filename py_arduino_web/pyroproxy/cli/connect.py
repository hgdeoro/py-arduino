# Licensed under the Apache License, Version 2.0
# Copyright (C) 2011-2015 - Horacio Guillermo de Oro <hgdeoro@gmail.com>

import logging

from py_arduino import DEVICE_FOR_EMULATOR
from py_arduino_web.pyroproxy.utils import BasePyroMain

logger = logging.getLogger(__name__)


class Main(BasePyroMain):

    def run(self, options, args, arduino):
        if len(args) > 1:
            device = args[1]
        else:
            logger.info("No device spcified. Will connect to ARDUINO EMULATOR")
            device = DEVICE_FOR_EMULATOR

        logger.info("Calling arduino.connect() - Connecting to %s", device)
        arduino.connect(device)

        # TODO: the ping should be optional
        logger.info("Calling arduino.ping() to check the connection")
        ret = arduino.ping()
        logger.info("Ping returned: '{0}", ret)

if __name__ == '__main__':
    Main().start()
