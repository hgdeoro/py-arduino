'''
Created on May 22, 2013

@author: Horacio G. de Oro
'''
import time
import logging

from py_arduino.proxy import OUTPUT, HIGH, LOW
from py_arduino.pyroproxy.utils import get_arduino_proxy_proxy,\
    wait_for_server

logger = logging.getLogger(__name__)


def main():
     = get_arduino_proxy_proxy()
    wait_for_server(logger)

    logger.info("Wait until Arduino is connected...")
    while not .is_connected():
        time.sleep(1)

    logger.info("Connected! :-D")

    logger.info("Starting to blink")
    .pinMode(13, OUTPUT)
    while True:
        .digitalWrite(13, HIGH)
        time.sleep(1)
        .digitalWrite(13, LOW)
        time.sleep(1)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
