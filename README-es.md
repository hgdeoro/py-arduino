Py-Arduino-Proxy
================

Aplicación Python para comunicarse con Arduinos. [English version.](/hgdeoro/py-arduino-proxy/blob/master/README.md "English version")

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

* PRO: utilidades de testing y la posibilidad de ver mensajes de DEBUG facilitan la ubicación de problemas y su posterior solución.

* CONTRA: actualmente tiene problemas al trabajar con interrupciones, ya que
	se pueden perder caracteres si se produce una interrupcion mientras
	se esta leyendo usando Serial.read(). Esto puede solucionarse en proximas
	versiones de Py-Arduino-Proxy.

Métodos implementados
---------------------

Actualmente están implementados los métodos básicos de Arduino. Por lo
tanto, las siguientes acciones se pueden realizar desde Python:

* Chequear la comunicación con Arduino (ping)
* Revalidar la conexión, removiendo cualquier informacióin pre-existente que pueda existir en el buffer.
* pinMode()
* digitalRead()
* digitalWrite()
* analogRead()
* analogWrite()
* Obtener el valor retornados por millis() y micros()
* Ejecutar delay() y delayMicroseconds()
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

Videos!
=======

* [Testeando leds RGB con Py-Arduino-Proxy UI](http://www.youtube.com/watch?v=yM1ZaTFAZwc "Testeando leds RGB con Py-Arduino-Proxy UI")
* [Creando metodos customizados en Py-Arduino-Proxy](http://www.youtube.com/watch?v=2kgQpQqTVUU "Creando metodos customizados en Py-Arduino-Proxy")
* [Probando shiftOut y 8 LEDs con Py-Arduino-Proxy](http://www.youtube.com/watch?v=_9MselaKcdU "Probando shiftOut y 8 LEDs con Py-Arduino-Proxy")

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
