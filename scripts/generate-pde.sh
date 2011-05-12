#!/bin/bash

BASEDIR="`dirname $0`/.."

export PYTHONPATH=$BASEDIR/src
export BASEDIR

python $BASEDIR/src/arduino_proxy/generate_sketch.py $*
