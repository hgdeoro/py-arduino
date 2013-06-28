'''
Created on May 22, 2013

@author: Horacio G. de Oro
'''
import time
import logging

from py_arduino import LOW, HIGH, OUTPUT
from py_arduino_web.pyroproxy.utils import get_arduino_pyro, \
    wait_for_server, get_storage_pyro

logger = logging.getLogger(__name__)


PIN_ID = 'integrated-arduino-led'


def main():
    arduino = get_arduino_pyro()
    storage = get_storage_pyro()
    wait_for_server(logger)

    pin = None
    while pin == None:
        logger.info("Getting pin number by ID")
        pin = storage.get_pin_by_id(PIN_ID)
        logger.info(" + Got pin: %s", pin)
        if pin is None:
            logger.warn(" + The pin with ID '%s' was not found... Will retry in 5 secs", PIN_ID)
            time.sleep(5)
            continue

    logger.info("Wait until Arduino is connected...")
    while not arduino.is_connected():
        time.sleep(1)

    logger.info("Connected! :-D")

    logger.info("Starting to blink")
    arduino.pinMode(pin.pin, OUTPUT)
    while True:
        arduino.digitalWrite(pin.pin, HIGH)
        time.sleep(1)
        arduino.digitalWrite(pin.pin, LOW)
        time.sleep(1)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
