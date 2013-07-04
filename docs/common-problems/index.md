---
layout: default
title: Common problems
---

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

This could happen because:

 1. you forgot to install the dependencies
    + See <a href="{{ site.baseurl }}/docs/how-to-install-py-arduino/">How to install py-arduino</a>.
 2. you forgot to activate the virtualenv
    + See <a href="{{ site.baseurl }}/docs/how-to-use-py-arduino/">How to use py_arduino.cli.*</a>.
