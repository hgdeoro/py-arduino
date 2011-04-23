#!/usr/bin/env python
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
import threading
import serial
import sys
import time
import unittest
import weakref

# Setup PYTHONPATH
SRC_DIR = os.path.split(os.path.realpath(__file__))[0] # SRC_DIR/arduino_proxy/tests
SRC_DIR = os.path.split(SRC_DIR)[0] # SRC_DIR/arduino_proxy
SRC_DIR = os.path.split(SRC_DIR)[0] # SRC_DIR
sys.path.append(os.path.abspath(SRC_DIR))

from arduino_proxy import ArduinoProxy

logger = logging.getLogger(__name__)

class ArduinoEmulator(threading.Thread):
    
    logger = logging.getLogger('ArduinoEmulator')
    
    def __init__(self, serial_connection):
        threading.Thread.__init__(self)
        self.serial_connection = serial_connection
        self.running = True
    
    def run_cmd(self, cmd):
        if not self.running:
            return
        logger.info("run_cmd() - cmd: %s", pprint.pformat(cmd))
        splitted = cmd.split()
        if splitted[0] == '_ping':
            self.serial_connection.write("PING_OK\n")
        else:
            logger.error("run_cmd() - INVALID COMMAND: %s", pprint.pformat(cmd))
    
    def read_cmd(self):
        buff = ''
        while self.running:
            a_char = self.serial_connection.read()
            logger.debug("self.serial_connection.read() - a_char: %s", pprint.pformat(a_char))
            if a_char == '': # timeout
                time.sleep(0.1)
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
    
class SerialConnectionMock(object):
    
    def __init__(self, other_side=None, timeout=1, *args, **kwargs):
        
        if other_side:
            # other_side != None -> Arduino side (SLAVE)
            self.master_of = None
            self.slave_of = weakref.ref(other_side)
            self.timeout = other_side.timeout
            self._lock = other_side._lock
            self.logger = logging.getLogger('SerialConnectionMock.ARDUINO')
        else:
            # other_side == None -> Python side (MASTER)
            self._out_buffer = ''
            self._in_buffer = ''
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
                self.slave_of()._in_buffer = self.slave_of()._in_buffer + buff
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
                    if self.slave_of()._out_buffer:
                        a_char = self.slave_of()._out_buffer[0]
                        self.slave_of()._out_buffer = self.slave_of()._out_buffer[1:]
                        self.logger.debug("read() -> %s", pprint.pformat(a_char))
                        return a_char
                    else:
                        wait = True
            finally:
                self._lock.release()
            if wait:
                time.sleep(0.1)
        self.logger.debug("read() -> ''")
        return ''

    def __str__(self):
        return "SerialConnectionMock\n" + \
                    " + in_buffer: %s\n" % pprint.pformat(self._in_buffer) + \
                    " + out_buffer: %s\n" % pprint.pformat(self._out_buffer)
    
class TestArduinoProxy(unittest.TestCase):
    
    def setUp(self):
        self.proxy = ArduinoProxy(tty='')
        self.proxy.serial_port = SerialConnectionMock()
        self.emulator = ArduinoEmulator(self.proxy.serial_port.get_other_side())
        self.emulator.start()
    
    def test_ping(self):
        self.proxy.ping()
    
    def tearDown(self):
        self.proxy.close()
        self.emulator.stop_running()
        self.emulator.join()
        logger.debug("tearDown(): %s", str(self.proxy.serial_port))

if __name__ == '__main__':
    args = list(sys.argv)
    if '--debug' in args:
        logging.basicConfig(level=logging.DEBUG)
        args.remove('--debug')
    else:
        logging.basicConfig(level=logging.INFO)
    
    unittest.main(argv=args)
