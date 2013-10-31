#!/bin/bash

BASEDIR=$(cd $(dirname $0)/..; pwd)

if [ ! -d "$BASEDIR/virtualenv" ] ; then
	echo "- Creating virtualenv..."
	virtualenv $BASEDIR/virtualenv
fi

echo "- Activating virtualenv..."
. $BASEDIR/virtualenv/bin/activate

echo "- Updating PIP from 'requirements.txt'"
pip install -r requirements.txt

echo "- Updating PIP from 'requirements-web.txt'"
pip install -r requirements-web.txt

echo "- Done!"
