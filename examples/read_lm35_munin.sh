#!/bin/bash

. ${PY_ARDUINO_VIRTUALENV}/bin/activate

python -m examples.read_lm35_munin $*
