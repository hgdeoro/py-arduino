from django.contrib import admin
from arduino_proxy.dj.models import Pin


class PinAdmin(admin.ModelAdmin):
    list_display = ('label', 'pin', 'pin_type', 'pin_id',)
    ordering = ('digital', 'pin',)
    readonly_fields = ('pin', 'pin_type')
    fields = ('pin', 'pin_type', 'label', 'pin_id',)

    def pin_type(self, obj):
        if obj.digital:
            return u"Digital"
        else:
            return u"Analog"

    pin_type.short_description = 'Pin Type'

admin.site.register(Pin, PinAdmin)
