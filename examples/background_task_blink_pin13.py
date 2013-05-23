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


def main():
    Pyro4.config.HMAC_KEY = hmac.new('this-is-PyArduinoProxy').digest()
    daemon = Pyro4.Proxy("PYRO:{0}@localhost:61234".format(
        Pyro4.constants.DAEMON_NAME))
    arduino_proxy = Pyro4.Proxy("PYRO:arduino_proxy.Proxy@localhost:61234")

    logger.info("Wait to let PyRO server start up")
    while True:
        try:
            daemon.ping()
            break
        except CommunicationError:
            time.sleep(1)

    logger.info("Wait until Arduino is connected...")
    while not arduino_proxy.is_connected():
        time.sleep(1)

    logger.info("Connected! :-D")

    logger.info("Starting to blink")
    arduino_proxy.pinMode(13, ArduinoProxy.OUTPUT)
    while True:
        arduino_proxy.digitalWrite(13, ArduinoProxy.HIGH)
        time.sleep(1)
        arduino_proxy.digitalWrite(13, ArduinoProxy.LOW)
        time.sleep(1)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
