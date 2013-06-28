py-arduino
==============

**py-arduino** is a **Python** library to communicate with **Arduinos**.

It consist of two layers:

 - a **low level tool**, very easy to use and **extend**,
 - a **web application**, including a **web interface** and **background threads**, based on Django, uWSGI, Pyro: it's multithread, allow concurrent access,
    labeling of pins to facilitate the use, etc..

The project has many **testing** utilities, a simple **emulator** and the ability to see DEBUG messages to facilitate the location of problems and subsequent solutions.


Installation
------------

To install, clone the Git repository, `cd` to the cloned directory and create a `virtualenv` (named `virtualenv`):

    $ git clone https://github.com/hgdeoro/py-arduino.git
    $ cd py-arduino
    $ virtualenv -p python2.7 virtualenv
    $ . virtualenv/bin/activate
    $ pip install -r requirements.txt

To run the tests against the emulator:

    $ python -m py_arduino.tests.test_all_functions /dev/ARDUINO_EMULATOR 

or against a real Arduino:

    $ python -m py_arduino.tests.test_all_functions /dev/ttyACM0 


<!--
The recommended way to install py-arduino is using pip and/or virtualenv.

1. Install PIP [manually](http://www.pip-installer.org/en/latest/installing.html "Install PIP"), or with your distribution's package manager (`sudo apt-get install python-pip` in Ubuntu), or create a [virtualenv](http://www.virtualenv.org/en/latest/ "Vitualenv Site").
2. Run `pip install py-arduino`
-->


Low leve tool
-------------

TODO: add low level example


Web interface
-------------

<!--
![Architecture Web Application](/hgdeoro/py-arduino-proxy/raw/master/examples/architecture-overview-webapp.png)
-->

TODO: add instructions to install from `requirements-web.txt`

To launch the web server, run:

    $ ./bin/run_uwsgi.sh

connect your Arduino, go to [http://localhost:8080/](http://localhost:8080/),
insert the serial device (something like /dev/ttyACM0)
and clic 'Connect'.

<!--
Here are some screenshots:

![connect](https://raw.github.com/hgdeoro/py-arduino-proxy/master/examples/arduino-proxy-web-interface-connect.png) and 

![main page](https://raw.github.com/hgdeoro/py-arduino-proxy/master/examples/arduino-proxy-web-interface-main.png).
-->

Console
-------

<!--
![Architecture Console](https://raw.github.com/hgdeoro/py-arduino-proxy/master/examples/architecture-overview-console.png)
-->

To ping to the Arduino, make sure it's connected and run:

	$ python -m py_arduino.cli.ping --info /dev/ttyACM0 
	INFO:root:Waiting some seconds to let the Arduino reset...
	Ping sent... OK - Time=19.893 ms
	Ping sent... OK - Time=22.675 ms
	Ping sent... OK - Time=18.798 ms


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


TODO (project rename + web thier)
---------------------------------

* rework web layer
* setup.py

TODO (project cleanup)
----------------------

* migrate wiki to to docs/ and readthedocs
* recreate sphinx files to build api docs

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
