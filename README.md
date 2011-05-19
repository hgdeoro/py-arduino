Py-Arduino-Proxy
================

Python application to communicate with Arduinos. [Versión en español.](/hgdeoro/py-arduino-proxy/blob/master/README-es.md "Versión en español")

How it works 
------------- 

First connect to the Arduino. 

![Connect](/hgdeoro/py-arduino-proxy/raw/master/examples/arduino-proxy-connect.png "Connect")

Once connected, we can execute the methods on the instance of ArduinoProxy. For example, to read a digital pin: 

![Digital Read](/hgdeoro/py-arduino-proxy/raw/master/examples/arduino-proxy-digital-read.png "Digital Read")

To set output HIGH on a digital pin: 

![Digital Write](/hgdeoro/py-arduino-proxy/raw/master/examples/arduino-proxy-digital-write.png "Digital Write")

Pros and cons 
-------------- 

* PRO: very easy to extend: it is very easy to create a new method in ArduinoProxy class (Python) and attach this method to a Arduino function. 

* PRO: testing utilities and the ability to see DEBUG messages facilitate the location of problems and subsequent solutions.

* CONS: currently has problems working with interruptions, since characters may be lost if an interruption occurs while 
reading the serial with Serial.read(). This can be fixed in next versions of Py-Arduino-Proxy. 

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

Installation
============

Step 1: Download the project code using Git
-------------------------------------------

    $ cd ~
    $ git clone git://github.com/hgdeoro/py-arduino-proxy.git

Step 2: Compile and upload the Arduino sketch
---------------------------------------------

The sketch will be located in ~/py-arduino-proxy/pde/py_arduino_proxy/py_arduino_proxy.pde

You only need to open it with the Arduino IDE, compile and upload. 

First tests
-----------

To verify that all steps were completed successfully, you can use the ping.py script. It will execute
indefinitely until you press Ctrl+C:

	$ ~/py-arduino-proxy/bin/ping.py /dev/ttyACM0 
	Ping sent... OK - Time=19.834 ms
	Ping sent... OK - Time=18.816 ms
	Ping sent... OK - Time=18.772 ms
	Ping sent... OK - Time=18.940 ms
	Ping sent... OK - Time=28.531 ms
	Ping sent... OK - Time=19.002 ms
	Ping sent... OK - Time=18.784 ms
	^C

Videos!
=======

* [Testing RGB leds with Py-Arduino-Proxy UI](http://www.youtube.com/watch?v=yM1ZaTFAZwc "Testing RGB leds with Py-Arduino-Proxy UI")
* [Writing a custom method in Py-Arduino-Proxy](http://www.youtube.com/watch?v=2kgQpQqTVUU "Writing a custom method in Py-Arduino-Proxy")
* [Testing shiftOut and 8 LEDs with Py-Arduino-Proxy](http://www.youtube.com/watch?v=_9MselaKcdU "Testing shiftOut and 8 LEDs with Py-Arduino-Proxy")

Python API
==========

You can get some initial API documentation [here](http://www.hgdeoro.com.ar/~horacio/py-arduino-proxy/index.html).

License y copyright
===================

Py-Arduino-Proxy - Access your Arduino from Python
Copyright (C) 2011 - Horacio Guillermo de Oro <hgdeoro@gmail.com>

Py-Arduino-Proxy is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2.

Py-Arduino-Proxy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License version 2 for more details.
