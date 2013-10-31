import datetime
import logging
import time

from py_arduino_web.pyroproxy.utils import BasePyroMain
from py_arduino import InvalidResponse

logger = logging.getLogger(__name__)

PIN_TEMPERATURA = 9
ARCHIVO = '/tmp/temperatura-pileta.txt'


class Main(BasePyroMain):

    def run(self, arduino):
        
        while True:
            logger.info("Iniciando - PIN_TEMPERATURA: %s - ARCHIVO: %s",
                PIN_TEMPERATURA, ARCHIVO)
            try:
                # arduino.pinMode(PIN_TEMPERATURA, ArduinoProxy.INPUT)
                value = arduino.ds18x20_read(PIN_TEMPERATURA)
                hora = datetime.datetime.now()
                with open(ARCHIVO, 'a') as f:
                    f.write("{:0.1f}".format(value))
                    f.write("  -->> ")
                    f.write(hora.strftime("%H:%M:%S %Y-%m-%d"))
                    f.write("\n")
            except InvalidResponse, e:
                if e.message == 'DS18X20_NO_MORE_ADDRESSES':
                    logger.warn("Se detecto DS18X20_NO_MORE_ADDRESSES. "
                        "Esperando y reintentando...")
                    time.sleep(10)
                else:
                    raise

if __name__ == '__main__':
    Main()._start(info=True, dont_check_pyro_server=True, wait_until_pyro_server_is_up=True,
        wait_until_connected=True)
