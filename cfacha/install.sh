#!/bin/bash

BASEDIR=$(cd $(dirname $0)/..; pwd)

if [ ! -d "$BASEDIR/virtualenv" ] ; then
	echo "- Creating virtualenv..."
	virtualenv $BASEDIR/virtualenv
fi

export PYTHONPATH=$BASEDIR

echo "- Activating virtualenv..."
. $BASEDIR/virtualenv/bin/activate

echo "- Updating PIP from 'requirements.txt'"
pip install -r $BASEDIR/requirements.txt

echo "- Updating PIP from 'requirements-web.txt'"
pip install -r $BASEDIR/requirements-web.txt

echo "- SyncDB (si falla es porque la BD ya fue creada)"
python -m py_arduino_web.dj.manage syncdb --noinput --migrate

echo "- Done!"
