#!/bin/bash

BASEDIR="`dirname $0`/.."

export PYTHONPATH=$BASEDIR
export BASEDIR

sphinx-build -b html $BASEDIR/scripts/sphinx $BASEDIR/docs
