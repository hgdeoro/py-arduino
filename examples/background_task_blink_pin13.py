'''
Created on May 22, 2013

@author: Horacio G. de Oro
'''
import time
import logging

from py_arduino import OUTPUT, HIGH, LOW
from py_arduino_web.pyroproxy.utils import get_arduino_pyro, \
    wait_for_server

logger = logging.getLogger(__name__)


def main():
    arduino = get_arduino_pyro()
    wait_for_server(logger)

    logger.info("Wait until Arduino is connected...")
    while not arduino.is_connected():
        time.sleep(1)

    logger.info("Connected! :-D")

    logger.info("Starting to blink")
    arduino.pinMode(13, OUTPUT)
    while True:
        arduino.digitalWrite(13, HIGH)
        time.sleep(1)
        arduino.digitalWrite(13, LOW)
        time.sleep(1)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
