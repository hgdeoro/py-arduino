#!/bin/bash

BASEDIR="`dirname $0`/.."

export PYTHONPATH=$BASEDIR/src
export BASEDIR

sphinx-build -b html $BASEDIR/scripts/sphinx $BASEDIR/docs
