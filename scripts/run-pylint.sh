#!/bin/bash

# C0111: Missing docstring
# R0801: Similar lines in 2 files

BASEDIR=$(cd $(dirname $0)/.. ; pwd)
export PYTHONPATH=$BASEDIR

pylint -d C0111,R0801 \
    py_arduino/tests/test_interrupt_0.py \
    py_arduino/tests/test_lcd_functions.py \
    py_arduino/tests/test_all_functions.py \
    py_arduino/tests/test_emulator.py \
    scripts/generate-doc.sh \
    py_arduino/emulator.py \
    py_arduino/main_utils.py \
    py_arduino/arduino.py \
    $*
