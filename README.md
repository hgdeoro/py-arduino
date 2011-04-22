Py-Arduino-Proxy
================

Python application to communicate with Arduinos. The current version let you:

* check communication with Arduino (ping)
* set pinMode()
* write digital values (LOW, HIGIH) with digitalWrite()
* read analog values with analogRead()

Example usage: ping
-------------------

Once the application is installed (see 'Install' below), you'll be able to
run shell scripts to communicate with Arduino:

    horacio@eeepc:~$ /usr/local/py-arduino-proxy/src/arduino_proxy/tests/ping.py /dev/ttyACM0 
    Warning: waiting some seconds to let the Arduino reset...
    Ping sent... OK - Time=21.800 ms
    Ping sent... OK - Time=22.630 ms
    Ping sent... OK - Time=22.696 ms
    Ping sent... OK - Time=22.718 ms
    Ping sent... OK - Time=23.725 ms
    Ping sent... OK - Time=21.686 ms
    Ping sent... OK - Time=22.661 ms
    Ping sent... OK - Time=22.717 ms
    Ping sent... OK - Time=22.655 ms
    ^C
    horacio@eeepc:~$ 

Example usage: reading temperature (in Celsius)
-----------------------------------------------

Once the application is installed (see 'Install' below), you'll be able to
check the temperature reported by a LM35 running:

    horacio@eeepc:~$ /usr/local/py-arduino-proxy/src/arduino_proxy/tests/analog_read_lm35.py /dev/ttyACM0 0
    13.67
    horacio@eeepc:~$ 

Here is a diagram that I've used to connect the LM35 to the Arduino:

![LM35 Circuit](https://github.com/hgdeoro/py-arduino-proxy/raw/master/examples/lm35_bb.png "LM35 Circuit")

Install: python application
---------------------------

You can install into /usr/local with 2 commands:

    $ cd /usr/local
    $ sudo git clone git://github.com/hgdeoro/py-arduino-proxy.git

Install: upload sketch
----------------------

Open the sketch with Arduino (the file will be located at /usr/local/py-arduino-proxy/pde/py-arduino-proxy.pde),
compile and upload it.

Workaround for firmware bug
---------------------------

TODO: DOCUMENT THIS!

