py-arduino
==============

**py-arduino** is a **Python** tool/library to communicate with **Arduino**
through USB (serial port), plus a web application on top of it.

The **low level tool** is simple to use and extend, only requires `pyserial`.
Many scripts are included to let you quickly start using it (see `py_arduino.cli.*`).

The **web application** allows read and write to pins from a web page,
easily implement _background tasks_, manages the concurrent access to the Arduino
(from the web interface, background tasks, cron, command line, etc.), and more...
It uses Django, PyRO and uWSGI.

The project has some **testing** utilities, and an **emulator**, to allow make some
test without actually having an Arduino connected.

## Other characteristics

* Python methods named around Arduino's methods
* Handles connections timeouts
* Can recover after timeouts and connection's troubles - see: `validateConnection()`
* Easy to extend
* Easy to debug (with `--arduino-debug`, which dumps all the data transmitted to/from Arduino)
* Growing [documentation](http://hgdeoro.github.io/py-arduino/)

Implemented methods  
===================

The basic methods of Arduino are implemented. The following actions can be done from Python: 

* `pinMode()`
* `digitalRead()`
* `digitalWrite()`
* `analogRead()`
* `analogWrite()`
* `millis()`, `micro()`
* `delay()`, delayMicroseconds()`
* `shiftOut()`

There are other extra methods:

* `ping()` to check communication with Arduino
* `getFreeMemory()` returns free Arduino memory
* `autoconnect()` to automatically connect to any available serial port
* `validateConnection()` to recover after communications problems
* `watchInterrupt()`, `getInterruptMark()` to work with interrupts (Prototype/Work In Progress)
* `enableDebug()`, `disableDebug()`, `enableDebugToLcd()` to show debug messages
* `getAvrCpuType()`, `getArduinoTypeStruct()` to get information about the Arduino
* `streamingAnalogRead()`, `streamingDigitalRead()` eficientlly receive much values (Prototype/Work In Progress)

And support for:

* `lcdMessage()`, `lcdWrite()`, `lcdClear()` show messages on LCDs, based on the Hitachi HD44780 (or a compatible) chipset
* `dht11_read()` read temperature and humidity with DHT11 sensor
* `ds18x20_read()` read temperature with DS18x20 sensor


Quick installation instructions (low level tool/library)
========================================================

Quick instructions ([see full install instructions and other documentation here](http://hgdeoro.github.io/py-arduino/))

    $ git clone https://github.com/hgdeoro/py-arduino.git
    $ cd py-arduino
    $ virtualenv -p python2.7 virtualenv
    $ . virtualenv/bin/activate
    $ pip install -r requirements.txt

Then upload the __sketch__ from `sketches/py_arduino`, and test:

    $ python -m py_arduino.cli.ping /dev/ttyACM0

<!--
### Running the tests

To run the tests against the emulator (if you don't have an Arduino):

    $ python -m py_arduino.tests.test_all_functions /dev/ARDUINO_EMULATOR 

To run the tests against a real Arduino, you have to upload the __sketch__ (from `sketches/py_arduino`), an execute:

    $ python -m py_arduino.tests.test_all_functions /dev/ttyACM0 
-->


Installation (web application)
==============================

 * Note: this instructions will be shortly moved to [http://hgdeoro.github.io/py-arduino/](http://hgdeoro.github.io/py-arduino/)

To install the web application, follow the steps on `Installation (low level tool/library)`, and then:

    $ pip install -r requirements-web.txt
    $ python -m py_arduino_web.dj.manage syncdb --noinput --migrate

(that will create a Sqlite3 database at `~/py_arduino.sqlite`).

To launch the web server, run:

    $ ./bin/run_uwsgi.sh

connect your Arduino, go to [http://localhost:8080/](http://localhost:8080/),
insert the serial device (something like /dev/ttyACM0)
and clic 'Connect'.

To use the Django Admin (to modify pin labels, etc.), you'll need to create an user:

    $ python -m py_arduino_web.dj.manage createsuperuser


<!--
Here are some screenshots:

![connect](https://raw.github.com/hgdeoro/py-arduino-proxy/master/examples/arduino-proxy-web-interface-connect.png) and 

![main page](https://raw.github.com/hgdeoro/py-arduino-proxy/master/examples/arduino-proxy-web-interface-main.png).
-->


<!--
The recommended way to install py-arduino is using pip and/or virtualenv.

1. Install PIP [manually](http://www.pip-installer.org/en/latest/installing.html "Install PIP"), or with your distribution's package manager (`sudo apt-get install python-pip` in Ubuntu), or create a [virtualenv](http://www.virtualenv.org/en/latest/ "Vitualenv Site").
2. Run `pip install py-arduino`
-->



<!--
How it works 
------------

First connect to the Arduino. 

![Connect](https://raw.github.com/hgdeoro/py-arduino-proxy/master/examples/arduino-proxy-connect.png "Connect")

Once connected, we can execute the methods on the instance of PyArduino. For example, to read a digital pin: 

![Digital Read](https://raw.github.com/hgdeoro/py-arduino-proxy/master/examples/arduino-proxy-digital-read.png "Digital Read")

To set output HIGH on a digital pin: 

![Digital Write](https://raw.github.com/hgdeoro/py-arduino-proxy/master/examples/arduino-proxy-digital-write.png "Digital Write")
-->

<!--
Videos!
=======

* [Web interface + emulator + analog pins](http://www.youtube.com/watch?v=fMhAJlvZQco "Web interface + emulator + analog pins")
* [Web interface](http://www.youtube.com/watch?v=QE6UJSs3b6Q "Web interface")
* [Testing shiftOut and 8 LEDs with py-arduino](http://www.youtube.com/watch?v=_9MselaKcdU "Testing shiftOut and 8 LEDs with py-arduino")
* [Writing a custom method in py-arduino](http://www.youtube.com/watch?v=2kgQpQqTVUU "Writing a custom method in py-arduino")
* [Testing RGB leds with py-arduino UI](http://www.youtube.com/watch?v=yM1ZaTFAZwc "Testing RGB leds with py-arduino UI")
-->

<!--
Python API
==========

You can get some initial API documentation [here](http://www.hgdeoro.com.ar/~horacio/py-arduino-proxy/index.html).
-->

TODOs
=============

* Add **INPUT_PULLUP** to pinMode()
* Add missing basic functions: tone(), analogReference()
* Add support to use analog pins as digital pins
* Better streaming support
* Multi-read (read multiple pins in a single operation)
* Finish support for interrupt
* Make hardware-specific functionality optional (LCD, DHT11, etc.)

License y copyright
===================

    py-arduino - Access your Arduino from Python
    Copyright (C) 2011-2013 - Horacio Guillermo de Oro <hgdeoro@gmail.com>
    
    py-arduino is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation version 2.
    
    py-arduino is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License version 2 for more details.

