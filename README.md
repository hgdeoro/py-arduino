PyArduinoProxy
==============

<!--
![Architecture overview](/hgdeoro/py-arduino-proxy/raw/master/examples/architecture-overview.png "Architecture overview")
-->

**NOTE: this is v2 of PyArduinoProxy, the status of the project is currently 'WIP - work in progress' and this README isn't fully updated yet**

**PyArduinoProxy** is a **Python** library to communicate with **Arduino**.
<!--
[Mis articulos de PyArduinoProxy](http://blog.hgdeoro.com.ar/search/label/pyarduinoproxy "Mis articulos de PyArduinoProxy").
-->

It's:

 - a **low level tool**, very easy to use and **extend** (it is very easy to create a new method in ArduinoProxy class and attach this method to a Arduino function).
 - a **service**, including a **web interface** and **background threads**, based on uWSGI and Pyro, it's multithread, allow concurrent access,
    labeling of pins to facilitate the use.

The project has many **testing** utilities, an **emulator** and the ability to see DEBUG messages to facilitate the location of problems and subsequent solutions.


Installation
------------

To install, clone the Git repository, `cd` to the cloned directory and create a `virtualenv` (named `virtualenv`):

    $ git clone https://github.com/hgdeoro/py-arduino-proxy.git
    $ cd py-arduino-proxy/
    $ virtualenv -p python2.7 virtualenv
    $ . virtualenv/bin/activate
    $ pip install -r requirements.txt

<!--
The recommended way to install PyArduinoProxy is using pip and/or virtualenv.

1. Install PIP [manually](http://www.pip-installer.org/en/latest/installing.html "Install PIP"), or with your distribution's package manager (`sudo apt-get install python-pip` in Ubuntu), or create a [virtualenv](http://www.virtualenv.org/en/latest/ "Vitualenv Site").
2. Run `pip install pyarduinoproxy`
-->

Web interface
-------------

<!--
![Architecture Web Application](/hgdeoro/py-arduino-proxy/raw/master/examples/architecture-overview-webapp.png)
-->

To launch the web server, run:

    $ ./bin/run_uwsgi.sh

connect your Arduino, go to [http://localhost:8080/connect](http://localhost:8080/connect),
insert the serial device (something like /dev/ttyACM0)
and clic 'Connect'. Here are some screenshots:

[connect](https://raw.github.com/hgdeoro/py-arduino-proxy/raw/master/examples/arduino-proxy-web-interface-connect.png) and 

[main page](https://raw.github.com/hgdeoro/py-arduino-proxy/raw/master/examples/arduino-proxy-web-interface-main.png).

Console
-------

![Architecture Console](https://raw.github.com/hgdeoro/py-arduino-proxy/raw/master/examples/architecture-overview-console.png)

To ping to the Arduino, make sure it's connected and run:

	$ python -m arduino_proxy.cli.ping --info /dev/ttyACM0 
	INFO:root:Waiting some seconds to let the Arduino reset...
	Ping sent... OK - Time=19.893 ms
	Ping sent... OK - Time=22.675 ms
	Ping sent... OK - Time=18.798 ms

How it works 
------------

First connect to the Arduino. 

![Connect](https://raw.github.com/hgdeoro/py-arduino-proxy/raw/master/examples/arduino-proxy-connect.png "Connect")

Once connected, we can execute the methods on the instance of ArduinoProxy. For example, to read a digital pin: 

![Digital Read](https://raw.github.com/hgdeoro/py-arduino-proxy/raw/master/examples/arduino-proxy-digital-read.png "Digital Read")

To set output HIGH on a digital pin: 

![Digital Write](https://raw.github.com/hgdeoro/py-arduino-proxy/raw/master/examples/arduino-proxy-digital-write.png "Digital Write")

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
* Read temperature and humidity with DHT11 sensors.

<!--
Videos!
=======

* [Web interface + emulator + analog pins](http://www.youtube.com/watch?v=fMhAJlvZQco "Web interface + emulator + analog pins")
* [Web interface](http://www.youtube.com/watch?v=QE6UJSs3b6Q "Web interface")
* [Testing shiftOut and 8 LEDs with PyArduinoProxy](http://www.youtube.com/watch?v=_9MselaKcdU "Testing shiftOut and 8 LEDs with PyArduinoProxy")
* [Writing a custom method in PyArduinoProxy](http://www.youtube.com/watch?v=2kgQpQqTVUU "Writing a custom method in PyArduinoProxy")
* [Testing RGB leds with PyArduinoProxy UI](http://www.youtube.com/watch?v=yM1ZaTFAZwc "Testing RGB leds with PyArduinoProxy UI")
-->

<!--
Python API
==========

You can get some initial API documentation [here](http://www.hgdeoro.com.ar/~horacio/py-arduino-proxy/index.html).
-->

License y copyright
===================

PyArduinoProxy - Access your Arduino from Python
Copyright (C) 2011-2013 - Horacio Guillermo de Oro <hgdeoro@gmail.com>

PyArduinoProxy is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2.

PyArduinoProxy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License version 2 for more details.
