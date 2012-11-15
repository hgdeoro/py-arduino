Py-Arduino-Proxy
================

![Architecture overview](/hgdeoro/py-arduino-proxy/raw/master/examples/architecture-overview.png "Architecture overview")

**Py-Arduino-Proxy** is a **Python** library to communicate with **Arduinos**.
[Mis articulos de PyArduinoProxy](http://blog.hgdeoro.com.ar/search/label/pyarduinoproxy "Mis articulos de PyArduinoProxy").

It's a **low level tool**, very easy to **extend** (it is very easy to create a new method in ArduinoProxy class and attach this method to a Arduino function).
The project has many **testing** utilities and the ability to see DEBUG messages, to facilitate the location of problems and subsequent solutions.

A **web interface** is in progress. See the [Web-Interface wiki page](https://github.com/hgdeoro/py-arduino-proxy/wiki/Web-Interface) for instructions and screenshots.

*Unresolved issues: currently, there are problems when working with interrupts, since characters may be lost if an interrupt occurs while 
reading the serial with Serial.read(). This is an inherent problem of serial communication of Arduino, but may be fixed in next versions of Py-Arduino-Proxy
if a work-around is found.*

Installation
------------

The recommended way to install PyArduinoProxy is using pip and/or virtualenv.

1. Install PIP [manually](http://www.pip-installer.org/en/latest/installing.html "Install PIP"), or with your distribution's package manager (`sudo apt-get install python-pip` in Ubuntu), or create a [virtualenv](http://www.virtualenv.org/en/latest/ "Vitualenv Site").
2. Run `pip install pyarduinoproxy`

Launch web interface
--------------------

Just run:

    $ python -m arduino_proxy.webui --info

and go to `http://localhost:8080/connect`, insert the serial device (something like /dev/ttyACM0)
and clic 'Connect'. Here are some screenshots:
[connect](/hgdeoro/py-arduino-proxy/raw/master/examples/arduino-proxy-web-interface-connect.png) and 
[main page](/hgdeoro/py-arduino-proxy/raw/master/examples/arduino-proxy-web-interface-main.png).


How it works 
------------

First connect to the Arduino. 

![Connect](/hgdeoro/py-arduino-proxy/raw/master/examples/arduino-proxy-connect.png "Connect")

Once connected, we can execute the methods on the instance of ArduinoProxy. For example, to read a digital pin: 

![Digital Read](/hgdeoro/py-arduino-proxy/raw/master/examples/arduino-proxy-digital-read.png "Digital Read")

To set output HIGH on a digital pin: 

![Digital Write](/hgdeoro/py-arduino-proxy/raw/master/examples/arduino-proxy-digital-write.png "Digital Write")

Implemented methods  
------------------- 

The basic methods of Arduino are implemented. The following actions can be done from Python: 

* Check communication with Arduino (ping) 
* pinMode()
* digitalRead()
* digitalWrite()
* analogRead()
* analogWrite()
* Get the value returned by millis() and micro()
* Run delay() and delayMicroseconds()
* watchInterrupt() and getInterruptMark() to work with interrupts
* shiftOut()
* Show messages on LCDs, based on the Hitachi HD44780 (or a compatible) chipset.

Videos!
=======

* [Web interface + emulator + analog pins](http://www.youtube.com/watch?v=fMhAJlvZQco "Web interface + emulator + analog pins")
* [Web interface](http://www.youtube.com/watch?v=QE6UJSs3b6Q "Web interface")
* [Testing shiftOut and 8 LEDs with Py-Arduino-Proxy](http://www.youtube.com/watch?v=_9MselaKcdU "Testing shiftOut and 8 LEDs with Py-Arduino-Proxy")
* [Writing a custom method in Py-Arduino-Proxy](http://www.youtube.com/watch?v=2kgQpQqTVUU "Writing a custom method in Py-Arduino-Proxy")
* [Testing RGB leds with Py-Arduino-Proxy UI](http://www.youtube.com/watch?v=yM1ZaTFAZwc "Testing RGB leds with Py-Arduino-Proxy UI")

<!--
Python API
==========

You can get some initial API documentation [here](http://www.hgdeoro.com.ar/~horacio/py-arduino-proxy/index.html).
-->

License y copyright
===================

Py-Arduino-Proxy - Access your Arduino from Python
Copyright (C) 2011-2012 - Horacio Guillermo de Oro <hgdeoro@gmail.com>

Py-Arduino-Proxy is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2.

Py-Arduino-Proxy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License version 2 for more details.
