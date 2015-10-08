#!/bin/bash
# Licensed under the Apache License, Version 2.0
# Copyright (C) 2011-2015 - Horacio Guillermo de Oro <hgdeoro@gmail.com>

. ${PY_ARDUINO_VIRTUALENV}/bin/activate

python -m examples.read_lm35_munin $*
