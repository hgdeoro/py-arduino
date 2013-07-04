---
layout: default
title: How to install py-arduino
---

## Install from GitHub

#### Clone the repository

    ~/$  git clone https://github.com/hgdeoro/py-arduino.git

#### cd to it

    ~/$  cd py-arduino

#### Install virtualenv & required libraries

    ~/py-arduino$  virtualenv -p python2.7 virtualenv
    ~/py-arduino$  . virtualenv/bin/activate
    (virtualenv)~/py-arduino$  pip install -r requirements.txt

#### Open the sketch and upload

Open the sketch at `py-arduino/sketches/py_arduino/py_arduino.ino`,
verify and upload to Arduino.

![Arduino sketch](install-sketch.jpg "Arduino sketch")

#### Test it

    (virtualenv)~/py-arduino$  python -m py_arduino.cli.ping /dev/ttyACM0
    Ping sent... OK - Time=18.295 ms
    Ping sent... OK - Time=19.658 ms
    Ping sent... OK - Time=23.358 ms
    ^C
    (virtualenv)~/py-arduino$

## A note about virtualenv

You must activate the virtualenv to use py-arduino, using something like:

`source /path/to/py-arduino/virtualenv/bin/activate`

or

`. /path/to/py-arduino/virtualenv/bin/activate`

(note the __space__ between the __.__ and the path to __activate__).

After activating the virtualenv, your prompt will chage: a __(virtualenv)__ will be prepended.

## ImportError: No module named serial

    ~/py-arduino$ python -m py_arduino.cli.ping /dev/ttyACM0 
    Traceback (most recent call last):
      File "/usr/lib/python2.7/runpy.py", line 162, in _run_module_as_main
        "__main__", fname, loader, pkg_name)
      File "/usr/lib/python2.7/runpy.py", line 72, in _run_code
        exec code in run_globals
      File "/mnt/seguro/home/horacio/python/py-arduino/py_arduino/cli/ping.py", line 25, in <module>
        from py_arduino.main_utils import BaseMain
      File "py_arduino/main_utils.py", line 24, in <module>
        from py_arduino.arduino import PyArduino
      File "py_arduino/arduino.py", line 29, in <module>
        import serial
    ImportError: No module named serial

If you got the error `ImportError: No module named serial`, this could be because:

 + you forgot to activate the virtualenv -> `source /path/to/py-arduino/virtualenv/bin/activate`
 + you forgot to install the dependencies -> `pip install -r requirements.txt`

See above for the details.

