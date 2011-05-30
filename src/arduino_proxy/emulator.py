##-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
##    Py-Arduino-Proxy - Access your Arduino from Python
##    Copyright (C) 2011 - Horacio Guillermo de Oro <hgdeoro@gmail.com>
##
##    This file is part of Py-Arduino-Proxy.
##
##    Py-Arduino-Proxy is free software; you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation version 2.
##
##    Py-Arduino-Proxy is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License version 2 for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with Py-Arduino-Proxy; see the file LICENSE.txt.
##-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

import logging
import os
import pprint
import random
import sys
import threading
import time
import unittest
import weakref

logger = logging.getLogger(__name__) # pylint: disable=C0103

class ArduinoEmulator(threading.Thread):
    """
    Arduino emulator :-D
    
    Reads commands from serial console and responds.
    """
    
    logger = logging.getLogger('ArduinoEmulator')
    
    def __init__(self, serial_connection):
        threading.Thread.__init__(self)
        self.daemon = True
        self.serial_connection = serial_connection
        self.running = True
    
    def run_cmd(self, cmd): #  # pylint: disable=R0912
        if not self.running:
            return
        
        from arduino_proxy.proxy import ArduinoProxy
        
        logger.info("run_cmd() - cmd: %s", pprint.pformat(cmd))
        splitted = cmd.split()
        if splitted[0] == '_ping':
            self.serial_connection.write("PING_OK\n")
        elif splitted[0] == '_aRd':
            value = random.randint(0, 1023)
            self.serial_connection.write("%d\n" % value)
        elif splitted[0] == '_dRd':
            value = [ArduinoProxy.HIGH, ArduinoProxy.LOW][random.randint(0, 1)]
            self.serial_connection.write("%d\n" % value)
        elif splitted[0] == '_dWrt':
            self.serial_connection.write("DW_OK\n")
        elif splitted[0] == '_aWrt':
            self.serial_connection.write("AW_OK\n")
        elif splitted[0] == '_vCnt':
            self.serial_connection.write("%s\n" % splitted[1])
        elif splitted[0] == '_pMd':
            self.serial_connection.write("PM_OK\n")
        elif splitted[0] == '_dy':
            time.sleep(int(splitted[1])/10000.0)
            self.serial_connection.write("D_OK\n")
        elif splitted[0] == '_dMs':
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
            self.serial_connection.write("_AVR_CPU_NAME__EMULATOR_\n")
        elif splitted[0] == '_gATS':
            self.serial_connection.write("2 5 00111 2 32\n")
        else:
            self.serial_connection.write("%s 0\n" % ArduinoProxy.INVALID_CMD)
            logger.error("run_cmd() - INVALID COMMAND: %s", pprint.pformat(cmd))
    
    def read_cmd(self):
        buff = ''
        while self.running:
            a_char = self.serial_connection.read()
            logger.debug("self.serial_connection.read() - a_char: %s", pprint.pformat(a_char))
            if a_char == '': # timeout
                time.sleep(0.001)
                continue
            
            if a_char == '\n': # new line
                return buff
            
            buff = buff + a_char
        
        # self.running == False
        return ''
    
    def run(self):
        ArduinoEmulator.logger.info("run() started!")
        while self.running:
            ArduinoEmulator.logger.debug("self.running == True")
            cmd = self.read_cmd()
            self.run_cmd(cmd)
        
        ArduinoEmulator.logger.info("run() finished!")

    def stop_running(self):
        self.running = False

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SerialConnectionMock(object):
    """
    Virtual serial connection. There are 2 endpoints.
    The MASTER endpoint, on the Py-Arduino-Proxy side,
    and the SLAVE endpoint, on the Arduino Emulator side.
    """
    def __init__(self, other_side=None, timeout=1, # pylint: disable=W0613
            initial_in_buffer_contents='', initial_out_buffer_contents='', *args, **kwargs):
        
        if other_side:
            # other_side != None -> Arduino side (SLAVE)
            self.master_of = None
            self.slave_of = weakref.ref(other_side)
            self.timeout = other_side.timeout
            self._lock = other_side._lock # pylint: disable=W0212
            self.logger = logging.getLogger('SerialConnectionMock.ARDUINO')
        else:
            # other_side == None -> Python side (MASTER)
            self._out_buffer = initial_out_buffer_contents
            self._in_buffer = initial_in_buffer_contents
            self.timeout = timeout
            self._lock = threading.RLock()
            self.master_of = SerialConnectionMock(other_side=self)
            self.slave_of = None
            self.logger = logging.getLogger('SerialConnectionMock.PYTHON')
    
    def get_other_side(self):
        if self.master_of:
            return self.master_of # ref
        else:
            return self.slave_of() # ref
    
    def close(self):
        pass
        
    def write(self, buff):
        self._lock.acquire()
        try:
            self.logger.debug("write(%s)", pprint.pformat(buff))
            if self.master_of:
                self._out_buffer = self._out_buffer + buff
            else:
                self.slave_of()._in_buffer = \
                    self.slave_of()._in_buffer + buff # pylint: disable=W0212
        finally:
            self._lock.release()
    
    def flush(self):
        pass
    
    def read(self):
        start = time.time()
        while (time.time() - start) < self.timeout: # timeout
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
                    if self.slave_of()._out_buffer: # pylint: disable=W0212
                        a_char = self.slave_of()._out_buffer[0] # pylint: disable=W0212
                        self.slave_of()._out_buffer = \
                            self.slave_of()._out_buffer[1:] # pylint: disable=W0212
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
    
    def getTimeout(self): # pylint: disable=C0103
        return self.timeout
    
    def __str__(self):
        return "SerialConnectionMock\n" + \
                    " + in_buffer: %s\n" % pprint.pformat(self._in_buffer) + \
                    " + out_buffer: %s\n" % pprint.pformat(self._out_buffer)

