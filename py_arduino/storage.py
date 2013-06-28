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


def default_label(pin, is_digital):
    """Returns a default label for a pin"""
    if is_digital:
        return 'Digital pin #{0}'.format(pin)
    else:
        return 'Analog pin #{0}'.format(pin)


class Pin():

    def __init__(self, pin=None, digital=False, label=None, enabled_in_web=True,
        pin_id=None, pk=0):
        self.pk = pk
        self.pin_id = pin_id
        self.pin = pin
        self.digital = digital
        self.label = label
        self.enabled_in_web = enabled_in_web

        # Automatically set label if not provided
        if pin is not None and digital is not None and label is None:
            if digital:
                self.label = 'Digital pin #{0}'.format(pin)
            else:
                self.label = 'Analog pin #{0}'.format(pin)


class Storage():

    def get_pin(self, pin, is_digital):
        """
        Returns a Pin instance.
        """
        return Pin(pin, is_digital, )

    def get_pin_by_id(self, pin_id):
        """
        Returns the Pin instance identified by 'pin_id',
        or None if no Pin exists with that identifier.
        """
        return None
