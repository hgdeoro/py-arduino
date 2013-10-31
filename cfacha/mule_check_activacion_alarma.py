import time
import logging
import subprocess
import os

from py_arduino import HIGH, INPUT
from py_arduino_web.pyroproxy.utils import BasePyroMain

logger = logging.getLogger(__name__)

PIN_ALARMA_PATIO = 11
SCRIPT_ACTIVACION_ALARMA = '/home/scripts/alarma/alarma_activada.txt'
SCRIPT_DESACTIVACION_ALARMA = '/home/scripts/alarma/alarma_desactivada.txt'
ESPERA_LUEGO_DE_CAMBIO_EN_VALOR = 0.1


class Main(BasePyroMain):

    def run(self, arduino):
        logger.info("Iniciando check_activacion_alarma() - PIN_ALARMA_PATIO: %s",
            PIN_ALARMA_PATIO)

        try:
            arduino.pinMode(PIN_ALARMA_PATIO, INPUT)
            arduino.digitalWrite(PIN_ALARMA_PATIO, HIGH)

            # ultimo_valor = HIGH
            ultimo_valor = arduino.digitalRead(PIN_ALARMA_PATIO)
            while True:
                value = arduino.digitalRead(PIN_ALARMA_PATIO)
                if value != ultimo_valor:
                    ultimo_valor = value
                    if value == HIGH:
                        logger.info("Alarma CONECTADA. Nuevo valor: %s", value)
                        subprocess.call(SCRIPT_DESACTIVACION_ALARMA, shell=True)
                    else:
                        logger.info("Alarma DESCONECTADA. Nuevo valor: %s", value)
                        subprocess.call(SCRIPT_ACTIVACION_ALARMA, shell=True)
                    time.sleep(ESPERA_LUEGO_DE_CAMBIO_EN_VALOR)
        except:
            logger.exception("ERROR in check_activacion_alarma()... "
                "Haremos 'os._exit(1)' para forzar el reinicio del servidor y de Arduino")
            # FIXME: estoy ya no es cierto en uWSGI
            os._exit(1)

if __name__ == '__main__':
    Main()._start(info=True, dont_check_pyro_server=True, wait_until_pyro_server_is_up=True,
        wait_until_connected=True)
