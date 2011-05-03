#!/bin/bash

cd `dirname $0`

pyuic4 -o main_ui.py Main.ui

pyrcc4 -o resources_rc.py resources.qrc
