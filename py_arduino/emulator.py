##-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
##    py-arduino - Access your Arduino from Python
##    Copyright (C) 2011-2013 - Horacio Guillermo de Oro <hgdeoro@gmail.com>
##
##    This file is part of py-arduino.
##
##    py-arduino is free software; you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation version 2.
##
##    py-arduino is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License version 2 for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with py-arduino; see the file LICENSE.txt.
##-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

import logging
import os
import pprint
import random
import threading
import time
import weakref

from py_arduino import HIGH, LOW, INVALID_CMD


class ArduinoEmulator(threading.Thread):
    """
    Arduino emulator :-D
    
    Reads commands from serial console and responds.
    """

    def __init__(self, serial_connection):
        threading.Thread.__init__(self)
        self.daemon = True
        self.serial_connection = serial_connection
        self.running = True
        self.logger = logging.getLogger('ArduinoEmulator')

    def _validate_parameters(self, splitted_params):
        """
        Validate the parameters.
        If parameters are OK: returns True
        If something is wrong: write response using serial connection and return False.
        """
        #define READ_ONE_PARAM_EMPTY_RESPONSE 							1
        #define UNEXPECTED_RESPONSE_FROM_READ_ONE_PARAM		4
        #define UNEXPECTED_RESPONSE_FROM_READ_PARAMETERS		5
        #define FUNCTION_NOT_FOUND													6
        for item in splitted_params:
            if len(item) > 16:
                # READ_ONE_PARAM_ERROR_PARAMETER_TOO_LARGE = 2
                self.serial_connection.write("%s 2\n" % INVALID_CMD)
                return False

        if len(splitted_params) > 10:
            # READ_PARAMETERS_ERROR_TOO_MANY_PARAMETERS = 3
            self.serial_connection.write("%s 3\n" % INVALID_CMD)
            return False

        return True

    def run_cmd(self, cmd):  # pylint: disable=R0912
        if not self.running:
            return

        def _get_int(env_name, default_value):
            value = os.environ.get(env_name, '')
            try:
                return int(value)
            except:
                return default_value

        self.logger.info("run_cmd() - cmd: %s", pprint.pformat(cmd))
        splitted = cmd.split()

        if not self._validate_parameters(splitted):
            return

        if splitted[0] == '_ping':
            self.serial_connection.write("PING_OK\n")
        elif splitted[0] == '_aRd':
            value = random.randint(0, 1023)
            self.serial_connection.write("%d\n" % value)
        elif splitted[0] == '_dRd':
            value = [HIGH, LOW][random.randint(0, 1)]
            self.serial_connection.write("%d\n" % value)
        elif splitted[0] == '_dWrt':
            self.serial_connection.write("DW_OK\n")
        elif splitted[0] == '_aWrt':
            self.serial_connection.write("AW_OK\n")
        elif splitted[0] == '_vCnt':
            self.serial_connection.write("%s\n" % splitted[1])
        elif splitted[0] == '_pMd':
            self.serial_connection.write("PM_OK\n")
        elif splitted[0] == '_dy':  # delay()
            if int(splitted[1]) / 1000.0 > self.serial_connection.timeout:
                time.sleep(int(splitted[1]) / 1000.0)  # So timeout is detected
                self.serial_connection.write("D_OK\n")
            else:
                time.sleep(int(splitted[1]) / 10000.0)
                self.serial_connection.write("D_OK\n")
        elif splitted[0] == '_dMs':  # delayMicroseconds()
            self.serial_connection.write("DMS_OK\n")
        elif splitted[0] == '_ms':
            self.serial_connection.write("%d\n" % random.randint(0, 999999))
        elif splitted[0] == '_mc':
            self.serial_connection.write("%d\n" % random.randint(0, 999999))
        elif splitted[0] == '_eD':
            self.serial_connection.write("ENA\n")
        elif splitted[0] == '_dD':
            self.serial_connection.write("DIS\n")
        elif splitted[0] == '_gACT':
            self.serial_connection.write("ARDUINO_EMULATOR\n")
        elif splitted[0] == '_gFM':  # getFreeMemory()
            self.serial_connection.write("%d\n" % random.randint(800, 1200))
        elif splitted[0] == '_sftO':  # shiftOut()
            self.serial_connection.write("SOOK\n")

        elif splitted[0] == '_gATS':
            analog_pins = _get_int("emulator_analog_pins", 5)
            digital_pins = _get_int("emulator_digital_pins", 5)
            pwm_pins_bitmap = os.environ.get("emulator_pwm_pins_bitmap", "")
            if not pwm_pins_bitmap or len(pwm_pins_bitmap) != digital_pins:
                pwm_pins_bitmap = ''.join([str(i % 2) for i in range(0, digital_pins)])
            eeprom_size = _get_int("emulator_eeprom_size", 2)
            flash_size = _get_int("emulator_flash_size", 16)
            ram_size = _get_int("emulator_ram_size", 4)

            arduino_type_struct = "%d %d %s %d %d %d\n" % (
                analog_pins,
                digital_pins,
                pwm_pins_bitmap,
                eeprom_size,
                flash_size,
                ram_size,
            )
            self.serial_connection.write(arduino_type_struct)

        elif splitted[0] == '_lcdClr':  # lcdClear()
            print "LCD: lcdClear()"
            self.serial_connection.write("LCLROK\n")

        elif splitted[0] == '_lcdW':  # lcdWrite()
            print "LCD[col=%d][row=%d]: %s" % (int(splitted[1]), int(splitted[2]),
                ' '.join(splitted[3:]))
            self.serial_connection.write("LWOK\n")

        elif splitted[0] == '_strAR':  # streamingAnalogRead()
            # If message sent to real Arduino is delayed, maybe some more data is sent from Arduino
            # splitted[1] -> pin
            # splitted[2] -> count
            for i in range(0, int(splitted[2])):
                self.serial_connection.write("%d\n" % random.randint(0, 1023))
            self.serial_connection.write("SR_OK\n")

        elif splitted[0] == '_strDR':  # streamingDigitalRead()
            # splitted[1] -> pin
            # splitted[2] -> count
            for i in range(0, int(splitted[2])):
                self.serial_connection.write("%d\n" % random.randint(0, 1))
            self.serial_connection.write("SR_OK\n")

        elif splitted[0] == '_emonStp':  # energyMonitorSetup()
            assert int(splitted[1]) >= 0
            assert float(splitted[2]) >= 0
            assert float(splitted[3]) >= 0
            assert int(splitted[4]) >= 0
            assert float(splitted[5]) >= 0
            self.serial_connection.write("EMON_S_OK\n")

        elif splitted[0] == '_emonRd':  # energyMonitorRead()
            assert int(splitted[1]) >= 0
            assert int(splitted[2]) >= 0

            # self.serial_connection.write("EMON_R_OK,1.1,2.2,3.3,4.4,5.5\n")
            self.serial_connection.write("EMON_R_OK,1.1,2.2,3.3,{},{}\n".format(
                random.randint(200, 240) / 1.0,
                random.randint(10, 40) / 1.0
            ))

            #            #    'realPower': realPower,
            #            #    'apparentPower': apparentPower,
            #            #    'powerFactor': powerFactor,
            #            #    'Vrms': Vrms,
            #            #    'Irms': Irms,
            #            self.serial_connection.write("EMON_R_OK,{},{},{},{},{}\n".format(
            #                random.randint(0, 100) / 10.0,
            #                random.randint(0, 100) / 10.0,
            #                random.randint(0, 100) / 10.0,
            #                random.randint(180, 240) / 1.0,
            #                random.randint(5, 40) / 1.0,
            #            ))

        else:
            # FUNCTION_NOT_FOUND = 6
            self.serial_connection.write("%s 6\n" % INVALID_CMD)
            self.logger.error("run_cmd() - INVALID COMMAND: %s", pprint.pformat(cmd))

    def read_cmd(self):
        buff = ''
        while self.running:
            a_char = self.serial_connection.read()
            self.logger.debug("self.serial_connection.read() - a_char: %s", pprint.pformat(a_char))
            if a_char == '':  # timeout
                time.sleep(0.001)
                continue

            if a_char == '\n':  # new line
                return buff

            buff = buff + a_char

        # self.running == False
        return ''

    def run(self):
        self.logger.info("run() started!")
        while self.running:
            self.logger.debug("self.running == True")
            cmd = self.read_cmd()
            self.run_cmd(cmd)

        self.logger.info("run() finished!")

    def stop_running(self):
        self.running = False

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class SerialConnectionArduinoEmulator(object):
    """
    Virtual serial connection to the Arduino Emulator. There are 2 endpoints.
    The MASTER endpoint, on the PyArduino side,
    and the SLAVE endpoint, on the Arduino Emulator side.
    """
    def __init__(self, other_side=None, timeout=1,  # pylint: disable=W0613
            initial_in_buffer_contents='', *args, **kwargs):

        if other_side:
            # other_side != None -> Arduino side (SLAVE)
            # ie: this instance (`self`) is for the side of the Arduino:
            # - write() sends data to python
            # - read() reads data sent from python to Arduino
            self.master_of = None
            self.slave_of = weakref.ref(other_side)
            self.timeout = other_side.timeout
            self._lock = other_side._lock  # pylint: disable=W0212
            self.logger = logging.getLogger('SerialConnectionArduinoEmulator.ARDUINO')
            self.emulator = None
        else:
            # other_side == None -> Python side (MASTER)
            # ie: this instance (`self`) is for the side of the Python:
            # - write() sends data to Arduino
            # - read() reads data sent from Arduino to python
            self._out_buffer = ''
            self._in_buffer = initial_in_buffer_contents
            self.timeout = timeout
            self._lock = threading.RLock()
            self.master_of = SerialConnectionArduinoEmulator(other_side=self)
            self.slave_of = None
            self.logger = logging.getLogger('SerialConnectionArduinoEmulator.PYTHON')
            self.emulator = ArduinoEmulator(self.get_other_side())
            self.emulator.start()

    def get_other_side(self):
        if self.master_of:
            return self.master_of  # ref
        else:
            return self.slave_of()  # ref

    def close(self):
        self.emulator.stop_running()
        self.logger.info("emulator.stop_running() OK... Will join the threads...")
        self.emulator.join()
        self.logger.info("Threads joined OK.")

    def write(self, buff):
        self._lock.acquire()
        try:
            self.logger.debug("write(%s)", pprint.pformat(buff))
            if self.master_of:
                self._out_buffer = self._out_buffer + buff
            else:
                self.slave_of()._in_buffer = \
                    self.slave_of()._in_buffer + buff  # pylint: disable=W0212
        finally:
            self._lock.release()

    def flush(self):
        pass

    def inWaiting(self):
        self._lock.acquire()
        try:
            if self.master_of:
                # WE are in the master side
                return len(self._in_buffer)
            else:
                # WE are in the slave side
                return len(self.slave_of()._out_buffer)
        finally:
            self._lock.release()

    def read(self):
        start = time.time()
        while (time.time() - start) < self.timeout:  # timeout
            self.logger.debug("read(): timeout not reached")
            wait = False
            self._lock.acquire()
            try:
                if self.master_of:
                    # WE are in the master side
                    if self._in_buffer:
                        a_char = self._in_buffer[0]
                        self._in_buffer = self._in_buffer[1:]
                        self.logger.debug("read() -> %s", pprint.pformat(a_char))
                        return a_char
                    else:
                        wait = True
                else:
                    # WE are in the slave side
                    if self.slave_of()._out_buffer:  # pylint: disable=W0212
                        a_char = self.slave_of()._out_buffer[0]  # pylint: disable=W0212
                        self.slave_of()._out_buffer = \
                            self.slave_of()._out_buffer[1:]  # pylint: disable=W0212
                        self.logger.debug("read() -> %s", pprint.pformat(a_char))
                        return a_char
                    else:
                        wait = True
            finally:
                self._lock.release()
            if wait:
                time.sleep(0.001)
        self.logger.debug("read() -> ''")
        return ''

    def getTimeout(self):  # pylint: disable=C0103
        return self.timeout

    def inject_to_in_buffer(self, text):
        self._in_buffer = self._in_buffer + text

    def __str__(self):
        return "SerialConnectionArduinoEmulator\n" + \
                    " + in_buffer: %s\n" % pprint.pformat(self._in_buffer) + \
                    " + out_buffer: %s\n" % pprint.pformat(self._out_buffer)
