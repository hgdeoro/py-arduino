import logging

from django.db import models

from arduino_proxy.storage import Storage, default_label

FallbackStorage = Storage()

logger = logging.getLogger(__name__)


class Pin(models.Model):
    pin = models.PositiveIntegerField()
    digital = models.BooleanField()
    label = models.CharField(max_length=64)
    #pin_id = models.CharField(max_length=64, unique=True)

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

    def get_pin(self, pin, is_digital):
        try:
            return Pin.objects.get(pin=pin, digital=is_digital)
        except Pin.DoesNotExist:
            return Pin.objects.create(pin=pin, digital=is_digital,
                label=default_label(pin, is_digital))
