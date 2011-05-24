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

from arduino_proxy import ArduinoProxy

class Root(object):
    
    def __init__(self, proxy, arduino_proxy_base_dir):
        self.proxy = proxy
        self.arduino_proxy_base_dir = arduino_proxy_base_dir
        
        self.jinja2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(
            os.path.join(self.arduino_proxy_base_dir, 'web', 'static')))
        
        # In genshi docs, this is placed at module level
        #self.loader = genshi.template.TemplateLoader(
        #    os.path.join(self.arduino_proxy_base_dir, 'web', 'static'),
        #    auto_reload=True, 
        #)
    
    @cherrypy.expose
    def index(self):
        raise cherrypy.HTTPRedirect("/static/ui.html")
    
    @cherrypy.expose
    def index2(self):
        self.proxy.validate_connection()
        template = self.jinja2_env.get_template('ui-jinja2.html')
        
        arduino_type = self.proxy.getArduinoTypeStruct()
        digital_pins = arduino_type['digital_pins']
        digital_pins_list = range(0, digital_pins)
        
        pwm_pins_bitmap = arduino_type['pwm_pins_bitmap']
        pwm_pins_bitmap = list(pwm_pins_bitmap)
        pwm_pins_bitmap_list = []
        while(len(pwm_pins_bitmap_list) != len(digital_pins_list)):
            try:
                item = pwm_pins_bitmap.pop() # remove LAST
                pwm_pins_bitmap_list.append(bool(item == '1'))
            except IndexError:
                pwm_pins_bitmap_list.append(False)
        
        return template.render(
            digital_pins=digital_pins_list, 
            pwm_pins_bitmap_list=pwm_pins_bitmap_list, 
        )
    
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
    def pin_mode_output(self, pin=None):
        try:
            self.proxy.pinMode(int(pin), ArduinoProxy.OUTPUT)
            return { 'ok': True, }
        except:
            # FIXME: return error details and log
            logging.exception("Exception raised by proxy.pinMode()")
            return { 'ok': False, }

def start_webserver(arduino_proxy_base_dir, options, args, proxy):
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
    
    conf = {
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': join(arduino_proxy_base_dir, 'web', 'static'),
        }
    }
    
    cherrypy.quickstart(Root(proxy, arduino_proxy_base_dir), '/', config=conf)
