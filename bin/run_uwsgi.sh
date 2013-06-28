#!/bin/bash

BASEDIR=$( cd $(dirname $0)/.. ; pwd)

if [ -z "$VIRTUAL_ENV" -a -d $BASEDIR/virtualenv ] ; then
	. $BASEDIR/virtualenv/bin/activate
fi

uwsgi \
	--module=py_arduino_web.dj.wsgi:application \
	--env DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-py_arduino_web.dj.settings} \
	--master \
	--processes=${UWSGI_PROCESSES:-1} --enable-threads \
	--home=$BASEDIR/virtualenv \
	--http=${UWSGI_HTTP:-127.0.0.1:8080} \
	--python-path=$BASEDIR \
	--static-map /static=$BASEDIR/py_arduino_web/dj/static \
	--mule=$BASEDIR/py_arduino_web/pyroproxy/server.py \
	$*
