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

import cherrypy
import jinja2
import logging
import simplejson
import os
import sys

from os.path import split, realpath, join, abspath

from arduino_proxy import ArduinoProxy, ArduinoProxyException

logger = logging.getLogger(__name__)

class Root(object):
    
    def __init__(self, jinja2_env):
        self.proxy = None
        self.jinja2_env = jinja2_env
    
    @cherrypy.expose
    def index(self, serial_port=None, speed=None):
        error_message = None
        if serial_port is not None:
            if serial_port:
                try:
                    logger.info("Trying to connect to %s", serial_port)
                    proxy = ArduinoProxy(tty=serial_port, speed=int(speed))
                    logger.info("Connected OK")
                    self.proxy = proxy
                except ArduinoProxy, ap_exception:
                    error_message = str(ap_exception)
                    logger.exception("Couldn't create instance of ArduinoProxy")
                except Exception, exception:
                    error_message = str( exception)
                    logger.exception("Couldn't create instance of ArduinoProxy")
            else:
                error_message = "Must specify a serial port."
        
        if self.proxy is not None:
            try:
                self.proxy.validate_connection()
                arduino_type = self.proxy.getArduinoTypeStruct()
                return self.generate_ui(arduino_type)
            except ArduinoProxyException, e:
                self.proxy = None
                error_message = str(e)
        
        template = self.jinja2_env.get_template('select-serial-port.html')
        return template.render(error_message=error_message)
    
    def generate_ui(self, arduino_type):
        template = self.jinja2_env.get_template('py-arduino-proxy-main.html')
        
        return template.render(arduino_type=arduino_type)
    
    ## ~~~~~~ Here start AJAX methods
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def ping(self):
        try:
            self.proxy.ping()
            return { 'ok': True, }
        except:
            # FIXME: return error details and log
            logging.exception("Exception raised by proxy.ping()")
            return { 'ok': False, }

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def validate_connection(self):
        try:
            random_value = self.proxy.validate_connection()
            return { 'ok': True, 'random_value': random_value, }
        except:
            # FIXME: return error details and log
            logging.exception("Exception raised by proxy.validate_connection()")
            return { 'ok': False, }

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def pin_mode(self, pin=None, mode=None):
        try:
            if mode == 'output':
                self.proxy.pinMode(int(pin), ArduinoProxy.OUTPUT)
                return { 'ok': True, }
            elif mode == 'input':
                self.proxy.pinMode(int(pin), ArduinoProxy.INPUT)
                return { 'ok': True, }
            else:
                # FIXME: return error details and log
                return { 'ok': False, }
        except:
            # FIXME: return error details and log
            logging.exception("Exception raised by proxy.pinMode()")
            return { 'ok': False, }

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def digital_write(self, pin=None, value=None):
        try:
            if value == 'low':
                self.proxy.digitalWrite(int(pin), ArduinoProxy.LOW)
                return { 'ok': True, }
            elif value == 'high':
                self.proxy.digitalWrite(int(pin), ArduinoProxy.HIGH)
                return { 'ok': True, }
            else:
                # FIXME: return error details and log
                return { 'ok': False, }
        except:
            # FIXME: return error details and log
            logging.exception("Exception raised by proxy.digitalWrite()")
            return { 'ok': False, }

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def analog_write(self, pin=None, value=None):
        try:
            self.proxy.analogWrite(int(pin), int(value))
            return { 'ok': True, }
        except:
            # FIXME: return error details and log
            logging.exception("Exception raised by proxy.analogWrite()")
            return { 'ok': False, }
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def digital_read(self, pin=None):
        try:
            value = self.proxy.digitalRead(int(pin))
            if value == ArduinoProxy.HIGH:
                return { 'ok': True, 'value': 1, }
            elif value == ArduinoProxy.LOW:
                return { 'ok': True, 'value': 0, }
            else:
                # FIXME: return error details and log
                return { 'ok': False, }
        except:
            # FIXME: return error details and log
            logging.exception("Exception raised by proxy.analogWrite()")
            return { 'ok': False, }

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_avr_cpu_type(self):
        try:
            return {
                'ok': True,
                'avrCpuType': self.proxy.getAvrCpuType(),
            }
        except:
            # FIXME: return error details and log
            logging.exception("Exception raised by proxy.getAvrCpuType()")
            return { 'ok': False, }

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_arduino_type_struct(self):
        try:
            return {
                'ok': True,
                'arduinoTypeStruct': self.proxy.getArduinoTypeStruct(),
            }
        except:
            # FIXME: return error details and log
            logging.exception("Exception raised by proxy.getArduinoTypeStruct()")
            return { 'ok': False, }

def start_webserver(arduino_proxy_base_dir):
    conf = {
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': join(arduino_proxy_base_dir, 'web', 'static'),
        }
    }
    
    jinja2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(
        os.path.join(arduino_proxy_base_dir, 'web', 'static')))
    
    cherrypy.config.update({
        'log.screen': False,
    })
    
    cherrypy.quickstart(Root(jinja2_env), '/', config=conf)

    # cherrypy.log.error_log.setLevel(logging.ERROR)
    # cherrypy.log.access_log.setLevel(logging.ERROR)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # CherryPy examples 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #
    #    # Set up site-wide config first so we get a log if errors occur.
    #    cherrypy.config.update({'environment': 'production',
    #                            'log.error_file': 'site.log',
    #                            'log.screen': True})
    #        
    #    conf = {'/feed': {'tools.staticdir.on': True,
    #                      'tools.staticdir.dir': os.path.join(current_dir, 'feeds'),
    #                      'tools.staticdir.content_types': {'rss': 'application/xml',
    #                                                        'atom': 'application/atom+xml'}}}
    #    cherrypy.quickstart(Root(), '/', config=conf)
    #
    #    cherrypy.config.update({
    #        'server.socket_host': '64.72.221.48',
    #        'server.socket_port': 80,
    #    })
    #
    #    config = {'/': 
    #        {
    #            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
    #            'tools.trailing_slash.on': False,
    #        }
    #    }
    #    cherrypy.tree.mount(Root(), "/script_name_root", config=config)
