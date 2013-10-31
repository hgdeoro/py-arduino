#!/bin/bash

BASEDIR=$(cd $(dirname $0)/..; pwd)

$BASEDIR/bin/run_uwsgi.sh --mule=$BASEDIR/examples/bg_autoconnect.py $*

