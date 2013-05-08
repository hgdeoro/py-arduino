import logging

from django.db import models

from arduino_proxy.storage import Storage

FallbackStorage = Storage()

logger = logging.getLogger(__name__)


class Pin(models.Model):
    pin = models.PositiveIntegerField()
    digital = models.BooleanField()
    label = models.CharField(max_length=64)

    def __unicode__(self):
        if self.digital:
            return u"Digital pin #{0}".format(self.pin)
        else:
            return u"Analog pin #{0}".format(self.pin)

    class Meta:
        unique_together = (('pin', 'digital',),)


class DjStorage():

    def __init__(self):
        # Force access to the database, to raise exception if no DB exists
        Pin.objects.count()

    def get_label(self, pin, is_digital):
        """
        Returns the label of the pin `pin`.
        `is_digital` is True for digital pins, False for analog
        """
        try:
            pin_obj = Pin.objects.get(pin=pin, digital=is_digital)
            return pin_obj.label
        except Pin.DoesNotExist:
            default_label = FallbackStorage.get_label(pin, is_digital)
            try:
                pin_obj = Pin.objects.create(pin=pin, digital=is_digital, label=default_label)
                return pin_obj.label
            except:
                return default_label
