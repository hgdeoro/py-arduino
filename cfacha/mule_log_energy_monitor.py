import logging
import os
import time

from py_arduino_web.pyroproxy.utils import BasePyroMain
import datetime


SENSORES = [
    dict(
         ARCHIVO='/home/registros/consumo.txt',
         V_PIN=1,
         V_CALIBRATION=239,
         V_PHASE_SHIFT=1.7,
         C_PIN=0,
         C_CALIBRATION=30,
         NO_WL=1,
         TIMEOUT=2,
    ),
    dict(
         ARCHIVO='/home/registros/consumo-2.txt',
         V_PIN=3,
         V_CALIBRATION=239,
         V_PHASE_SHIFT=1.7,
         C_PIN=2,
         C_CALIBRATION=30,
         NO_WL=1,
         TIMEOUT=2,
    ),
    dict(
         ARCHIVO='/home/registros/consumo-3.txt',
         V_PIN=5,
         V_CALIBRATION=239,
         V_PHASE_SHIFT=1.7,
         C_PIN=4,
         C_CALIBRATION=30,
         NO_WL=1,
         TIMEOUT=2,
    ),
]

ESPERA_ENTRE_LECTURAS = 20


class Main(BasePyroMain):

    logger = logging.getLogger(os.path.split(__file__)[-1])

    def run(self, arduino):
        self.logger.info("Iniciando...")

        if not arduino.is_connected():
            self.logger.debug("Arduino is not connected...")
            while not arduino.is_connected():
                self.logger.info("Waiting until connected...")
                time.sleep(5)
            self.logger.info("Connected!")

        try:
            self.logger.debug("Entering loop...")
            while True:

                for sensor in SENSORES:
                    try:
                        self.logger.debug("Calling energyMonitorSetup()")
                        arduino.energyMonitorSetup(sensor['V_PIN'],
                                                   sensor['V_CALIBRATION'],
                                                   sensor['V_PHASE_SHIFT'],
                                                   sensor['C_PIN'],
                                                   sensor['C_CALIBRATION']
                                                   )
                    except:
                        self.logger.exception("Error detected when "
                                              "called bg_setup()")
                        return

                    realPower, apparentPower, powerFactor, Vrms, Irms = \
                        arduino.energyMonitorRead(sensor['NO_WL'],
                                                  sensor['TIMEOUT'])
                    with open(sensor['ARCHIVO'], 'a') as f:
                        f.write("{:0.2f},{:0.2f},{:0.2f},{:0.2f},{:0.2f}"
                                "".format(realPower, apparentPower,
                                          powerFactor, Vrms, Irms))
                        f.write(",")
                        f.write(datetime.datetime.now().strftime(
                            "%H:%M:%S %Y-%m-%d"))
                        f.write("\n")
                        f.close()

                    time.sleep(ESPERA_ENTRE_LECTURAS)

        except:
            self.logger.exception("Error detected in loop")
            return


if __name__ == '__main__':
    Main()._start(info=True, dont_check_pyro_server=True,
                  wait_until_pyro_server_is_up=True,
                  wait_until_connected=True)
