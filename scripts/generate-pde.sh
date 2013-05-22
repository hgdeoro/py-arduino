#!/bin/bash

BASEDIR=$(cd $(dirname $0)/..; pwd)

export PYTHONPATH=$BASEDIR
export BASEDIR

python $BASEDIR/arduino_proxy/generate_sketch.py $*
