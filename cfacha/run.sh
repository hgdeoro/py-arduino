#!/bin/bash

BASEDIR=$(cd $(dirname $0)/..; pwd)

$BASEDIR/bin/run_uwsgi.sh $*

