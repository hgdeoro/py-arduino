import time
import logging
import subprocess
import os

from py_arduino import HIGH, INPUT
from py_arduino_web.pyroproxy.utils import BasePyroMain

logger = logging.getLogger(__name__)

PIN_ALARMA_PATIO = 12
SCRIPT_DISPARO_ALARMA = "/home/scripts/alarma/alarma.txt"
SCRIPT_FIN_DISPARO_ALARMA = "/home/scripts/alarma/fin_alarma.txt"
ESPERA_LUEGO_DE_CAMBIO_EN_VALOR = 0.1

# TODO: evitar 'falsos positivos' cuando se activa/desactiva la alarma


class Main(BasePyroMain):

    def run(self, arduino):
        logger.info("Iniciando - PIN_ALARMA_PATIO: %s",
            PIN_ALARMA_PATIO)
        try:
            arduino.pinMode(PIN_ALARMA_PATIO, INPUT)
            arduino.digitalWrite(PIN_ALARMA_PATIO, HIGH)

            #ultimo_valor = HIGH
            ultimo_valor = arduino.digitalRead(PIN_ALARMA_PATIO)
            while True:
                value = arduino.digitalRead(PIN_ALARMA_PATIO)
                if value != ultimo_valor:
                    logger.info("ALARMA PATIO: el valor ha cambiado. Nuevo valor: %s", value)
                    ultimo_valor = value
                    if value == HIGH:
                        subprocess.call(SCRIPT_DISPARO_ALARMA, shell=True)
                    else:
                        subprocess.call(SCRIPT_FIN_DISPARO_ALARMA, shell=True)
                    time.sleep(ESPERA_LUEGO_DE_CAMBIO_EN_VALOR)
        except:
            logger.exception("ERROR in check_disparo_de_alarma()... "
                "Haremos 'os._exit(1)' para forzar el reinicio del servidor y de Arduino")
            os._exit(1)

if __name__ == '__main__':
    Main()._start(info=True, dont_check_pyro_server=True, wait_until_pyro_server_is_up=True)
