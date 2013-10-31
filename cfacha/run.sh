#!/bin/bash

BASEDIR=$(cd $(dirname $0)/..; pwd)

$BASEDIR/bin/run_uwsgi.sh \
	--mule=$BASEDIR/examples/bg_autoconnect.py \
	--mule=$BASEDIR/cfacha/mule_check_activacion_alarma.py \
	--mule=$BASEDIR/cfacha/mule_check_disparo_alarma.py \
	--mule=$BASEDIR/cfacha/mule_check_ds18x20_temperatura_pileta.py \
	$*
