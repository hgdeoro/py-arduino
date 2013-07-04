---
layout: default
title: py_arduino.cli.* Reference
---

# py_arduino.cli.*: Reference

You can see the source code [here](https://github.com/hgdeoro/py-arduino/tree/master/py_arduino/cli).

## ping

To check the connectivity to the Arduino

    $ python -m py_arduino.cli.ping /dev/ttyACM0

#### Default invocation

    $ python -m py_arduino.cli.ping /dev/ttyACM0

![Ping](ping.jpg) 

#### Showing logging's _info_ messages

    $ python -m py_arduino.cli.ping --info /dev/ttyACM0

![Ping --info](ping-info.jpg) 

#### Showing logging's _debug_ messages

    $ python -m py_arduino.cli.ping --debug /dev/ttyACM0

![Ping --debug](ping-debug.jpg) 

## ipython

Start an IPython interactive session.

    $ python -m py_arduino.cli.ipython /dev/ttyACM0

To use this, you'll need to install _ipython_ with:

    $ pip install ipython

Here you can see the interactive session with a customized message.
The sessions starts with the Arduino connected.

![IPython](ipython.jpg) 

In this example, we import some constants, set the PIN 13 to `OUTPUT` mode,
and write a `LOW` first, and then a `HIGH`.

![IPython - Use onboard LED on pin 13](ipython-pin-13.jpg) 

## analog_read

TODO: add documentation! But you can see the
[source code](https://github.com/hgdeoro/py-arduino/blob/master/py_arduino/cli/analog_read.py).

## analog_write

TODO: add documentation! But you can see the
[source code](https://github.com/hgdeoro/py-arduino/blob/master/py_arduino/cli/analog_write.py).

## digital_read

TODO: add documentation! But you can see the
[source code](https://github.com/hgdeoro/py-arduino/blob/master/py_arduino/cli/digital_read.py).

## digital_write

TODO: add documentation! But you can see the
[source code](https://github.com/hgdeoro/py-arduino/blob/master/py_arduino/cli/digital_write.py).
