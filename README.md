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

That's taken from [http://forum.drbit.nl/viewtopic.php?id=36](http://forum.drbit.nl/viewtopic.php?id=36).

Install: python application
---------------------------

You can install into /usr/local with 2 commands:

    $ cd /usr/local
    $ sudo git clone git://github.com/hgdeoro/py-arduino-proxy.git

Install: upload sketch
----------------------

Open the sketch with Arduino (the file will be located at /usr/local/py-arduino-proxy/pde/py-arduino-proxy.pde),
compile and upload it. You'll need to put a 10k resistor joining Ground to PIN 12 (see image below: 'Workaround for Ubuntu').
You can see the sketch online [here](https://github.com/hgdeoro/py-arduino-proxy/blob/master/pde/py-arduino-proxy.pde).

Workaround for Ubuntu
---------------------

> Are you using an Arduino Uno on Linux? If so, you may have noticed that
> writing to the serial port in a loop can cause the Arduino Editor/Programmer
> software to appear to lock up, or even Linux having trouble using the
> serial port for your Uno.

I've made a simple workaround for this problem: [see the code](https://gist.github.com/922501)

Before calling 'loop()', the program pauses itself until the PIN 12 become 'LOW'.
As a visual aid, while the program is waiting, the onboard LED keeps blinking. Once
a 'LOW' on PIN 12 is detected, the program start the execution.

The 'LOW' could be done attaching a 10k resistor from the GROUND to the PIN 12.
After that, the onboard LED will be ON (no blinking), and the program will keep
running (you can remove the resistor).

Note: this must be done every time the Arduino is powered-on, and every time you
reset the Arduino (pushing the RESET button, or connecting through the serial console).
Since the Arduino auto-reset every time you connect using the USB serial port
(from the IDE, or from py-arduino-proxy), it's advisable to keep the 10k resistor
connecting Ground to PIN 12.

The next time you need to upload a new program, remove the resistor, and you won't be affected by the bug,
since the real program in 'loop()' won't be sending data using the serial port.

![Workaround for Ubuntu](https://github.com/hgdeoro/py-arduino-proxy/raw/master/examples/ubuntu-workaround_bb.png "Workaround for Ubuntu")

