'''
Created on May 22, 2013

@author: Horacio G. de Oro
'''
import time
import logging

from arduino_proxy.proxy import LOW, HIGH, OUTPUT
from arduino_proxy.pyroproxy.utils import get_arduino_proxy_proxy, \
    wait_for_server, get_arduino_storage_proxy

logger = logging.getLogger(__name__)


PIN_ID = 'integrated-arduino-led'


def main():
    arduino_proxy = get_arduino_proxy_proxy()
    storage = get_arduino_storage_proxy()
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
    while not arduino_proxy.is_connected():
        time.sleep(1)

    logger.info("Connected! :-D")

    logger.info("Starting to blink")
    arduino_proxy.pinMode(pin.pin, OUTPUT)
    while True:
        arduino_proxy.digitalWrite(pin.pin, HIGH)
        time.sleep(1)
        arduino_proxy.digitalWrite(pin.pin, LOW)
        time.sleep(1)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
