import logging

from django.db import models

from py_arduino_web.storage import Storage, default_label, BaseStorage

FallbackStorage = Storage()

logger = logging.getLogger(__name__)


class Pin(models.Model):
    pin = models.PositiveIntegerField()
    digital = models.BooleanField()
    label = models.CharField(max_length=64,
        help_text="Descriptive text for a pin. Ej: 'Status Led'")
    pin_id = models.CharField(max_length=64, unique=True, null=True, blank=True,
        help_text="Unique identifier for internal use of a pin. Ej: 'status-led'")
    enabled_in_web = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.pin_id is not None and len(self.pin_id.strip()) == 0:
            self.pin_id = None
        super(Pin, self).save(*args, **kwargs) # Call the "real" save() method.

    def __unicode__(self):
        if self.digital:
            ret = u"Digital pin #{0}".format(self.pin)
        else:
            ret = u"Analog pin #{0}".format(self.pin)
        if self.label:
            ret = u"{0} ('{1}')".format(ret, self.label)
        return ret

    class Meta:
        unique_together = (('pin', 'digital',),)


class DjStorage(BaseStorage):

    def __init__(self):
        # Force access to the database, to raise exception if no DB exists
        Pin.objects.count()

    def get_pin(self, pin, is_digital):
        try:
            return Pin.objects.get(pin=pin, digital=is_digital)
        except Pin.DoesNotExist:
            return Pin.objects.create(pin=pin, digital=is_digital,
                label=default_label(pin, is_digital), enabled_in_web=True)

    def get_pin_by_id(self, pin_id):
        """
        Returns the Pin instance identified by 'pin_id',
        or None if no Pin exists with that identifier.
        """
        try:
            return Pin.objects.get(pin_id=pin_id)
        except Pin.DoesNotExist:
            return None
