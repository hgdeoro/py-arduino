##-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
##    py-arduino - Access your Arduino from Python
##    Copyright (C) 2011-2013 - Horacio Guillermo de Oro <hgdeoro@gmail.com>
##
##    This file is part of py-arduino.
##
##    py-arduino is free software; you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation version 2.
##
##    py-arduino is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License version 2 for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with py-arduino; see the file LICENSE.txt.
##-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


#===============================================================================
# Interfaces & utils
#===============================================================================

def default_label(pin, is_digital):
    """Returns a default label for a pin"""
    if is_digital:
        return 'Digital pin #{0}'.format(pin)
    else:
        return 'Analog pin #{0}'.format(pin)


class BaseStorage():

    def enhanceArduinoTypeStruct(self, arduino_type_struct):
        """
        Returns an enhanced copy of `arduino_type_struct` with data from storage.

        The `arduino_type_struct` must be previously
        enhanced by `PyArduino.enhanceArduinoTypeStruct()`.

        To each item of `digital_pins_struct`, adds:
            + pk (int)
            + label (str)
            + pin_id (str)
            + enabled_in_web (bool)
        To each item of `analog_pins_struct`, adds:
            + pk (int)
            + label (str)
            + pin_id (str)
            + enabled_in_web (bool)
        """
        # arduino_type_struct['digital_pins_items']
        # arduino_type_struct['analog_pins_items']
        assert 'digital_pins_items' in arduino_type_struct
        assert 'analog_pins_items' in arduino_type_struct
        assert 'digital_pins_struct' in arduino_type_struct
        assert 'analog_pins_struct' in arduino_type_struct

        # create 'structs' for each digital pin
        for dp, dp_struct in zip(
            arduino_type_struct['digital_pins_items'],
            arduino_type_struct['digital_pins_struct']):

            # Assert we are 'synchronized'
            assert dp == dp_struct['pin']

            d_pin_obj = self.get_pin(dp, True)
            dp_struct.update({
                'pk': d_pin_obj.pk,
                #'pin': dp,
                #'digital': True,
                #'pwm': (dp in arduino_type_struct['pwm_pin_list']),
                'label': d_pin_obj.label,
                'pin_id': d_pin_obj.pin_id,
                'enabled_in_web': d_pin_obj.enabled_in_web,
                #'status.mode': d_pin_status.mode,
                #'status.read_value': d_pin_status.read_value,
                #'status.written_value': d_pin_status.written_value,
            })

        del dp  # to avoid bugs (happened!)
        del dp_struct  # to avoid bugs (happened!)
        del d_pin_obj  # to avoid bugs (happened!)

        # create 'structs' for each analog pin
        for ap, ap_struct in zip(
            arduino_type_struct['analog_pins_items'],
            arduino_type_struct['analog_pins_struct']):

            # Assert we are 'synchronized'
            assert ap == ap_struct['pin']

            a_pin_obj = self.get_pin(ap, False)
            ap_struct.update({
                'pk': a_pin_obj.pk,
                #'pin': ap,
                #'digital': True,
                #'pwm': False,
                'label': a_pin_obj.label,
                'pin_id': a_pin_obj.pin_id,
                'enabled_in_web': a_pin_obj.enabled_in_web,
                #'status.mode': a_pin_status.mode,
                #'status.read_value': a_pin_status.read_value,
                #'status.written_value': a_pin_status.written_value,
            })

        return arduino_type_struct


#===============================================================================
# Dummy implementations
#===============================================================================

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


class Storage(BaseStorage):

    def get_pin(self, pin, is_digital):
        """
        Returns a Pin instance.
        """
        return Pin(pin, is_digital,)

    def get_pin_by_id(self, pin_id):
        """
        Returns the Pin instance identified by 'pin_id',
        or None if no Pin exists with that identifier.
        """
        return None
