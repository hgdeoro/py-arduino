import logging
import sys
import time

from arduino_proxy import ArduinoProxy

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    proxy = ArduinoProxy(sys.argv[1], 9600)
    print "Esperando reinicio de Arduino..."
    time.sleep(2)
    try:
        while True:
            print "Enviando ping..."
            proxy.ping()
            print " + Respuesta recibida!"
    except KeyboardInterrupt:
        proxy.close()
        raise
