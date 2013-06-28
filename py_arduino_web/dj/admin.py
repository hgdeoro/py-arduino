from django.contrib import admin
from django import forms

from py_arduino_web.dj.models import Pin


class PinFormAdmin(forms.ModelForm):

    class Meta:
        model = Pin

    def clean_pin_idpin_id(self):
        if not self.cleaned_data["pin_id"].strip():
            return None
        return self.cleaned_data["pin_id"]


class PinAdmin(admin.ModelAdmin):
    list_display = ('label', 'pin', 'pin_type', 'pin_id', 'enabled_in_web')
    ordering = ('digital', 'pin',)
    readonly_fields = ('pin', 'pin_type')
    fields = ('pin', 'pin_type', 'label', 'pin_id', 'enabled_in_web')

    def pin_type(self, obj):
        if obj.digital:
            return u"Digital"
        else:
            return u"Analog"

    pin_type.short_description = 'Pin Type'

admin.site.register(Pin, PinAdmin)
