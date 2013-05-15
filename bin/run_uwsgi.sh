#!/bin/bash

BASEDIR=$( cd $(dirname $0)/.. ; pwd)

if [ -z "$VIRTUAL_ENV" -a -d $BASEDIR/virtualenv ] ; then
	. $BASEDIR/virtualenv/bin/activate
fi

uwsgi \
	--module=arduino_proxy.dj.wsgi:application \
	--env DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-arduino_proxy.dj.settings} \
	--master \
	--processes=${UWSGI_PROCESSES:-1} --enable-threads \
	--home=$BASEDIR/virtualenv \
	--http=${UWSGI_HTTP:-127.0.0.1:8080} \
	--python-path=$BASEDIR/PyArduinoProxy \
	--static-map /static=$BASEDIR/arduino_proxy/dj/static
