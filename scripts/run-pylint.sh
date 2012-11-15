#!/bin/bash

# C0111: Missing docstring
# R0801: Similar lines in 2 files

BASEDIR=$(cd $(dirname $0)/.. ; pwd)
export PYTHONPATH=$BASEDIR/src

# find $BASEDIR/src -type f -name '*.py' | grep -v '__init__.py' | xargs pylint --rcfile=$BASEDIR/pylintrc $*
# find $BASEDIR/src -type f -name '*.py' | xargs pylint -d R0801 $*
# find $BASEDIR/src -type f -name '*.py' | grep -v src/arduino_proxy/ui/main_ui.py | grep -v src/arduino_proxy/ui/resources_rc.py | xargs pylint -d C0111,R0801 $*

pylint -d C0111,R0801 \
    src/arduino_proxy/tests/test_interrupt_0.py \
    src/arduino_proxy/tests/test_lcd_functions.py \
    src/arduino_proxy/tests/test_all_functions.py \
    src/arduino_proxy/tests/emulator.py \
    src/arduino_proxy/emulator.py \
    src/arduino_proxy/generate_sketch.py \
    src/arduino_proxy/main_utils.py \
    src/arduino_proxy/proxy.py \
    $*
