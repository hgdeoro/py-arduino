#!/bin/bash

# C0111:  1: Missing docstring

BASEDIR=`dirname $0`

export PYTHONPATH=$BASEDIR/src
# export PYTHONPATH=src

# find $BASEDIR/src -type f -name '*.py' | grep -v '__init__.py' | xargs pylint --rcfile=$BASEDIR/pylintrc $*
# find $BASEDIR/src -type f -name '*.py' | xargs pylint -d R0801 $*

find $BASEDIR/src -type f -name '*.py' | xargs pylint $*
