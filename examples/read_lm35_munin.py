#!/usr/bin/env python
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

"""
#===============================================================================
# EXAMPLE - Reads the temperature using a LM35 (to be used from Munin)
#===============================================================================

#===============================================================================
# Run on Munin
#===============================================================================

You'll need to link the shell script to the Munin plugins directory:

    $ sudo ln -s /path/to/py-arduino/examples/read_lm35_munin.sh \
        /etc/munin/plugins/read_lm35_munin_pin0

And configure the plugin:

    $ sudo vim /etc/munin/plugin-conf.d/read_lm35_munin

    [read_lm35_munin*]
    user user-to-run
    env.PYTHONPATH /path/to/py-arduino
    env.PY_ARDUINO_VIRTUALENV /path/to/virtualenv
    env.TTY_DEVICE /dev/ttyACM0
    env.PIN 0

Restart the Munin node:

    $ sudo service munin-node restart

You can check for errors in the log file:

    $ sudo tail -f /var/log/munin/munin-node.log

To test with munin-run:

    $ sudo munin-run read_lm35_munin_pin0

Or, if you have telnet and know the Munin protocol:

    $ telnet localhost 4949
    > Trying 127.0.0.1...
    > Connected to localhost.
    > Escape character is '^]'.
    > # munin node at acer
    list
    > cpu cpuspeed df (...) read_lm35_munin_pin0 (...)
    config read_lm35_munin_pin0
    > graph_title Temperature
    > graph_args --vertical-label Temperature in C
    > graph_category Arduino
    > temp.label Temperature in C
    > temp.type GAUGE
    > .
    fetch read_lm35_munin_pin0
    > temp.value 21.48
    > .
    quit
    > Connection closed by foreign host.

#===============================================================================
# Test from the cli
#===============================================================================

To run the 'config' action of Munin:

    $ env PYTHONPATH=/path/to/py-arduino \
        TTY_DEVICE=/dev/ttyACM0 \
        PIN=0 \
        /path/to/py-arduino/virtualenv/bin/python \
        -m examples.read_lm35_munin config

You will get:

    graph_title Temperature
    graph_args --vertical-label Temperature in C
    graph_category Arduino
    temp.label Temperature in C
    temp.type GAUGE

To get the value:

    $ env PYTHONPATH=/path/to/py-arduino \
        TTY_DEVICE=/dev/ttyACM0 \
        PIN=0 \
        /path/to/py-arduino/virtualenv/bin/python \
        -m examples.read_lm35_munin

You will get:

    temp.value 21.00

"""

import os

from py_arduino.main_utils import BaseMain


class Main(BaseMain):

    optparse_usage = "usage: %prog"
    num_args = 0

    def get_device(self, options, args):
        return os.environ['TTY_DEVICE']

    def add_options(self):
        super(Main, self).add_options()
        self.parser.add_option("--graph-title",
            action="store", dest="graph_title", default="Temperature",
            help="Graph title")
        self.parser.add_option("--graph-category",
            action="store", dest="graph_category", default="py-arduino",
            help="Graph category")
        self.parser.add_option("--graph-label",
            action="store", dest="graph_label", default="Temperature",
            help="Graph label")

    def run(self, options, args, arduino):
        if len(args) == 0:
            analog_port = os.environ['PIN']
            value = arduino.analogRead(int(analog_port))
            temp = (5.0 * value * 100.0) / 1024.0
            print "temp.value {0:3.2f}".format(temp)
        else:
            if args[0] == "config":
                print "graph_title {0}".format(options.graph_title)
                print "graph_args --vertical-label {0}".format(options.graph_label)
                print "graph_category {0}".format(options.graph_category)
                print "temp.label {0}".format(options.graph_label)
                print "temp.type GAUGE"
            # TODO: print error

if __name__ == '__main__':
    Main().start()
