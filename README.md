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

Workaround for Ubuntu
---------------------

> Are you using an Arduino Uno on Linux? If so, you may have noticed that
> writing to the serial port in a loop can cause the Arduino Editor/Programmer
> software to appear to lock up, or even Linux having trouble using the
> serial port for your Uno.

I've made a [simple workaround](https://gist.github.com/922501) for this problem:

<script src="https://gist.github.com/922501.js?file=wait_push_button_to_start.pde"></script>

When the scripts starts, it waits to the PIN 12 to become 'LOW' (and while waiting,
the onboard led, associated with PIN 13, keeps blinking).

To let the 'loop()' start, make a connection between Ground and PIN 12 (using a 10k resistor).
You can put that resistor, so the Arduino doesn't keep waiting. The next time you need to
upload a new program, remove the resistor, and you won't be affected by the bug.

![Workaround for Ubuntu](https://github.com/hgdeoro/py-arduino-proxy/raw/master/examples/ubuntu-workaround_bb.png "Workaround for Ubuntu")

