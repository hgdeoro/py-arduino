
Running the tests
-----------------

To run the tests against the emulator (if you don't have an Arduino), you can
use the special value of `/dev/ARDUINO_EMULATOR` as device::

    $ python -m py_arduino.tests.test_all_functions /dev/ARDUINO_EMULATOR

To run the tests against a real Arduino, just run::

    $ python -m py_arduino.tests.test_all_functions /dev/ttyACM0


Recreating the sketch file
--------------------------

In case you change any of the Arduino / C code, or add a custom method to PyArduino,
you will need to recrete the sketch files::

    $ python sketches/generate_sketch.py <OUTPUT_DIRECTORY>

For example::

    $ python sketches/generate_sketch.py sketches/py_arduino

