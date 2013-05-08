#!/bin/bash

BASEDIR=$( cd $(dirname $0)/.. ; pwd)

if [ -d $BASEDIR/virtualenv ] ; then
	. $BASEDIR/virtualenv/bin/activate
fi

uwsgi \
	--module=arduino_proxy.dj.wsgi:application \
	--env DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-arduino_proxy.dj.settings} \
	--master \
	--processes=1 --enable-threads \
	--home=$BASEDIR/virtualenv \
	--http=127.0.0.1:8080 \
	--python-path=$BASEDIR/PyArduinoProxy \
	--static-map /static=$BASEDIR/arduino_proxy/dj/static

