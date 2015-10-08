import time
import logging
import subprocess
import os

from py_arduino import HIGH, INPUT
from py_arduino_web.pyroproxy.utils import BasePyroMain

logger = logging.getLogger(__name__)

PIN_TIMBRE = 7
SCRIPT_TIMBRE = '/home/scripts/alarma/alarma_activada.txt'
ESPERA_LUEGO_DE_ACTIVACION_DE_TIMBRE = 20.0


class Main(BasePyroMain):

    def run(self, arduino):
        logger.info("Iniciando mule_check_activacion_timbre.py() - PIN_TIMBRE: %s", PIN_TIMBRE)

        try:
            arduino.pinMode(PIN_TIMBRE, INPUT)
            arduino.digitalWrite(PIN_TIMBRE, HIGH)

            while True:
                value = arduino.digitalRead(PIN_TIMBRE)
                if value == HIGH:
                    logger.info("Tiembre ha sido activado")
                    subprocess.call(SCRIPT_TIMBRE, shell=True)
                time.sleep(ESPERA_LUEGO_DE_ACTIVACION_DE_TIMBRE)
        except:
            logger.exception("ERROR in mule_check_activacion_timbre()... "
                "Haremos 'os._exit(1)' para forzar el reinicio del servidor y de Arduino")
            # FIXME: estoy ya no es cierto en uWSGI
            os._exit(1)

if __name__ == '__main__':
    Main()._start(info=True, dont_check_pyro_server=True, wait_until_pyro_server_is_up=True, wait_until_connected=True)
