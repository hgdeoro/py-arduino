##-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
##    PyArduinoProxy - Access your Arduino from Python
##    Copyright (C) 2011-2013 - Horacio Guillermo de Oro <hgdeoro@gmail.com>
##
##    This file is part of PyArduinoProxy.
##
##    PyArduinoProxy is free software; you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation version 2.
##
##    PyArduinoProxy is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License version 2 for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with PyArduinoProxy; see the file LICENSE.txt.
##-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

import logging
import multiprocessing
import os
import time

from django.conf import settings
from gunicorn.app.djangoapp import DjangoApplication


def start_pyarduinoproxy():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arduino_proxy.dj.settings")
    logger = logging.getLogger('pyarduinoproxy')
    # Setup Django internals
    # See:
    # - (1) https://docs.djangoproject.com/en/1.5/topics/settings/#django.conf.settings.configure
    # - (2) https://docs.djangoproject.com/en/1.5/ref/settings/#time-zone
    # TODO: add required environment variables (see link #2)
    logger.info("Configuring Django...")
    settings.configure()
    logger.info("Django configured OK")
    time.sleep(2)
    logger.info("PyArduinoProxy finished...")


def start_gunicorn():
    logger = logging.getLogger('gunicorn')
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arduino_proxy.dj.settings")
    logger.info("Starting Gunicorn via DjangoApplication")
    DjangoApplication("%(prog)s [OPTIONS] [SETTINGS_PATH]").run()
    logger.info("Gunicorn finished...")


def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Creating Process instances...")
    py_arduino_proxy = multiprocessing.Process(target=start_pyarduinoproxy, args=[])
    django = multiprocessing.Process(target=start_gunicorn, args=[])

    logging.info("Starting processes...")
    py_arduino_proxy.start()
    django.start()

    logging.info("Waiting for join()")
    py_arduino_proxy.join()
    django.join()

    logging.info("Finished!!")

if __name__ == '__main__':
    main()
