#!/bin/bash

# C0111: Missing docstring
# R0801: Similar lines in 2 files

BASEDIR=`dirname $0`

export PYTHONPATH=$BASEDIR/src
# export PYTHONPATH=src

# find $BASEDIR/src -type f -name '*.py' | grep -v '__init__.py' | xargs pylint --rcfile=$BASEDIR/pylintrc $*
# find $BASEDIR/src -type f -name '*.py' | xargs pylint -d R0801 $*

find $BASEDIR/src -type f -name '*.py' | xargs pylint -d C0111,R0801 $*
