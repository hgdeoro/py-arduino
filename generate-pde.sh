#!/bin/bash

BASEDIR=`dirname $0`

export PYTHONPATH=$BASEDIR/src

python src/arduino_proxy/proxy.py $*
