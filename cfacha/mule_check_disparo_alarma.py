# -*- coding: utf-8 -*-

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

"""
ESPERA_ENTRE_LECTURAS: cuanto esperar entre sucesivas
lecturas. Si lo que importa es detectar el disparo de la alarma
(y no la ACTIVACIÓN/DESACTIVACIÓN), no hace falta leer continuamente.
"""
ESPERA_ENTRE_LECTURAS = 0.5

"""
ESPERA_PARA_RELEER: luego de detectar un HIGH, cuánto esperar
para re-leer (si esta nueva lectura es HIGH, significa que la alarma se
ha disparado, sino, significa que el primer HIGH fue por (des)activación.
"""
ESPERA_PARA_RE_LEER = 3.0


class Main(BasePyroMain):

    def run(self, arduino):
        logger.info("Iniciando - PIN_ALARMA_PATIO: %s",
            PIN_ALARMA_PATIO)
        try:
            arduino.pinMode(PIN_ALARMA_PATIO, INPUT)
            arduino.digitalWrite(PIN_ALARMA_PATIO, HIGH)

            # FIXME: el valor inicial de `ultimo_valor` deberia ser algo inválido
            # para que, si el script se inicia con la alarma activada se detecte
            # el CAMBIO en el valor, y se ejecute el script.
            ultimo_valor = arduino.digitalRead(PIN_ALARMA_PATIO)
            while True:
                value = arduino.digitalRead(PIN_ALARMA_PATIO)
                if value != ultimo_valor:
                    if value == HIGH:
                        # Esperamos 3 segundos para confirmar que la alarma se
                        # haya disparado, y no sea sólo la activación/desactivación
                        logger.info("ALARMA PATIO: el valor ha cambiado a HIGH... esperando para"
                            " confirmar que fue disparo, y no (des)activacion")
                        time.sleep(ESPERA_PARA_RE_LEER)
                        value = arduino.digitalRead(PIN_ALARMA_PATIO)
                        if value == HIGH:
                            # REALMENTE fue disparo de alarma!
                            logger.info("ALARMA PATIO: la nueva lectura devolvio HIGH. "
                                "La alarma fue disparada")
                            ultimo_valor = value
                            subprocess.call(SCRIPT_DISPARO_ALARMA, shell=True)
                        else:
                            logger.info("ALARMA PATIO: la nueva lectura devolvio LOW. "
                                "Se trato de activacion/desactivacion de la alarma")
                    else:
                        logger.info("ALARMA PATIO: el valor ha cambiado a LOW.")
                        subprocess.call(SCRIPT_FIN_DISPARO_ALARMA, shell=True)
                time.sleep(ESPERA_ENTRE_LECTURAS)
        except:
            logger.exception("ERROR in check_disparo_de_alarma()... "
                "Haremos 'os._exit(1)' para forzar el reinicio del servidor y de Arduino")
            os._exit(1)

if __name__ == '__main__':
    Main()._start(info=True, dont_check_pyro_server=True, wait_until_pyro_server_is_up=True,
        wait_until_connected=True)
