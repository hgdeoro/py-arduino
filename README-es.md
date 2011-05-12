Py-Arduino-Proxy
================

Aplicación Python para comunicarse con Arduinos. 

Cómo funciona
-------------

Primero establecemos conexion hacia el Arduino.

![Connect](/hgdeoro/py-arduino-proxy/raw/master/examples/arduino-proxy-connect.png "Connect")

Una vez conectados, podemos ejecutar los métodos en la instancia de ArduinoProxy. Por ejemplo, para leer un pin digital:

![Digital Read](/hgdeoro/py-arduino-proxy/raw/master/examples/arduino-proxy-digital-read.png "Digital Read")

Para establecer HIGH como salida de un pin digital:

![Digital Write](/hgdeoro/py-arduino-proxy/raw/master/examples/arduino-proxy-digital-write.png "Digital Write")

Pros y contras
--------------

* PRO: muy facil de extender: es muy fácil crear un nuevo método en la
	clase ArduinoProxy (Python) y asociar dicho método a una función
	de Arduino.

* CONTRA: actualmente tiene problemas al trabajar con interrupciones, ya que
	se pueden perder caracteres si se produce una interrupcion mientras
	se esta leyendo usando Serial.read(). Esto puede solucionarse en proximas
	versiones de Py-Arduino-Proxy.

Métodos implementados
---------------------

Actualmente están implementados los métodos básicos de Arduino. Por lo
tanto, las siguientes acciones se pueden realizar desde Python:

* chequear la comunicación con Arduino (ping)
* revalidar la conexión, removiendo cualquier informacióin pre-existente que pueda existir en el buffer.
* pinMode()
* digitalRead()
* digitalWrite()
* analogRead()
* analogWrite()
* obtener el valor retornados por millis() y micros()
* ejecutar delay() y delayMicroseconds()
* watchInterrupt() y getInterruptMark() para trabajar con interrupciones

Instalación
===========

Paso 1: Bajar el código del proyecto usando Git
-----------------------------------------------

    $ cd ~
    $ git clone git://github.com/hgdeoro/py-arduino-proxy.git

Paso 2: Compilar el sketch y subirlo al Arduino
-----------------------------------------------

El sketch estará ubicado en ~/py-arduino-proxy/pde/py_arduino_proxy/py_arduino_proxy.pde
Sólo hace falta abrirlo con el IDE de Arduino, compilarlo y subirlo.

Primeras pruebas
----------------

Para comprobar que todos los pasos se realizaron con éxito, se puede usar el script ping.py, que se ejecutará
indefinidamente hasta presionar Ctrl+C:

	$ ~/py-arduino-proxy/bin/ping.py /dev/ttyACM0 
	Ping sent... OK - Time=19.834 ms
	Ping sent... OK - Time=18.816 ms
	Ping sent... OK - Time=18.772 ms
	Ping sent... OK - Time=18.940 ms
	Ping sent... OK - Time=28.531 ms
	Ping sent... OK - Time=19.002 ms
	Ping sent... OK - Time=18.784 ms
	^C

Licencia y copyright
====================

Py-Arduino-Proxy - Access your Arduino from Python
Copyright (C) 2011 - Horacio Guillermo de Oro <hgdeoro@gmail.com>

Py-Arduino-Proxy is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2.

Py-Arduino-Proxy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License version 2 for more details.

TODO: mover esto a otra pagina
------------------------------

And now is very easy add your custom methods... See at the end of [proxy.py](https://github.com/hgdeoro/py-arduino-proxy/blob/master/src/arduino_proxy/proxy.py)
for further information.

TODO: mover esto a otra pagina
------------------------------

In the 'bin' directory you'll find scripts to call the basic functions from shell scripts:

* analog_read.py
* analog_write_pwm.py
* digital_read.py
* ping.py

TODO: mover esto a otra pagina
------------------------------

Additional examples are in the 'examples' directory:

* analog_read_lm35_munin.py
* analog_read_lm35.py
* analog_write_pwm_blink.py
* digital_write_blink_led.py

TODO: mover esto a otra pagina
------------------------------

Example usage: ping
-------------------

Once the application is installed (see 'Install' below), you'll be able to
run shell scripts to communicate with Arduino:

    horacio@eeepc:~$ /usr/local/py-arduino-proxy/bin/ping.py /dev/ttyACM0 
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

TODO: mover esto a otra pagina
------------------------------

Example usage: reading temperature (in Celsius)
-----------------------------------------------

Once the application is installed (see 'Install' below), you'll be able to
check the temperature reported by a LM35 running:

    horacio@eeepc:~$ /usr/local/py-arduino-proxy/examples/analog_read_lm35.py /dev/ttyACM0 0
    13.67
    horacio@eeepc:~$ 

Here is a diagram that I've used to connect the LM35 to the Arduino:

![LM35 Circuit](https://github.com/hgdeoro/py-arduino-proxy/raw/master/examples/lm35_bb.png "LM35 Circuit")

That's taken from [http://forum.drbit.nl/viewtopic.php?id=36](http://forum.drbit.nl/viewtopic.php?id=36).

TODO: mover esto a otra pagina
------------------------------

Example: charting values with Munin
-----------------------------------

Here is a chart generated with Munin:

![Munin Chart](https://github.com/hgdeoro/py-arduino-proxy/raw/master/examples/munin-temperature-at-sunlight.png "Munin Chart").

TODO: mover esto a otra pagina
------------------------------

Example: accessing Arduino from the shell
-----------------------------------------

Read the analog port 0, from the Arduino connected in /dev/ttyACM0:

	horacio@eeepc:~$ /usr/local/py-arduino-proxy/bin/analog_read.py /dev/ttyACM0 0
	18

Read the digital port 0, from the Arduino connected in /dev/ttyACM0:

	horacio@eeepc:~$ /usr/local/py-arduino-proxy/bin/digital_read.py /dev/ttyACM0 0 
	HIGH
	horacio@eeepc:~$ /usr/local/py-arduino-proxy/bin/digital_read.py --numerical /dev/ttyACM0 0
	1

TODO: mover esto a otra pagina
------------------------------

Example usage: watching for interrupts
--------------------------------------

Using watchInterrupt(), the Arduino starts to keep track when an external interrupt occurs. You can check if an interrupt
has ocurred using getInterruptMark(). Here is an example.
    
    from arduino_proxy import ArduinoProxy
    
    proxy = ArduinoProxy('/dev/ttyACM0', 9600)
    proxy.pinMode(2, ArduinoProxy.INPUT)
    proxy.digitalWrite(2, ArduinoProxy.HIGH) # INT_0 -> pullup resistor
    proxy.watchInterrupt(0, ArduinoProxy.ATTACH_INTERRUPT_MODE_LOW)
    while True:
        if proxy.getInterruptMark(0):
            print "INTERRUPT 0 has ocurred"

You can test this with the folowing circuit:

![Interrupt circuit](https://github.com/hgdeoro/py-arduino-proxy/raw/master/examples/interrupts_bb.png "Interrupt circuit")

A full working example is [here](https://github.com/hgdeoro/py-arduino-proxy/tree/master/src/arduino_proxy/tests/test_interrupt_0.py).

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
