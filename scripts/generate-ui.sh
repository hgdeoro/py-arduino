#!/bin/bash

cd `dirname $0`

pyuic4 -o src/arduino_proxy/ui/main_ui.py      ui/Main.ui
pyrcc4 -o src/arduino_proxy/ui/resources_rc.py ui/resources.qrc
