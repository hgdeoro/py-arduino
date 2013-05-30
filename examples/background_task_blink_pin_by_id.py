'''
Created on May 22, 2013

@author: Horacio G. de Oro
'''
import Pyro4
import hmac
import time
import logging

from arduino_proxy.proxy import ArduinoProxy
from Pyro4.errors import CommunicationError

logger = logging.getLogger(__name__)


PIN_ID = 'integrated-arduino-led'


def main():
    Pyro4.config.HMAC_KEY = hmac.new('this-is-PyArduinoProxy').digest()
    daemon = Pyro4.Proxy("PYRO:{0}@localhost:61234".format(
        Pyro4.constants.DAEMON_NAME))
    arduino_proxy = Pyro4.Proxy("PYRO:arduino_proxy.Proxy@localhost:61234")
    storage = Pyro4.Proxy("PYRO:arduino_proxy.Storage@localhost:61234")

    logger.info("Wait to let PyRO server start up")
    while True:
        try:
            daemon.ping()
            break
        except CommunicationError:
            time.sleep(1)

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
    arduino_proxy.pinMode(pin.pin, ArduinoProxy.OUTPUT)
    while True:
        arduino_proxy.digitalWrite(pin.pin, ArduinoProxy.HIGH)
        time.sleep(1)
        arduino_proxy.digitalWrite(pin.pin, ArduinoProxy.LOW)
        time.sleep(1)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
