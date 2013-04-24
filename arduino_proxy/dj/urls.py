from django.conf.urls import patterns, include, url
from django.contrib import admin
#from django.conf import settings

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^dj/', include('dj.foo.urls')),
    url(r'^$', 'arduino_proxy.dj.views.home', name='home'),

    url(r'^pin_mode/?$', 'arduino_proxy.dj.views.pin_mode', name='pin_mode'),
    url(r'^digital_write/?$', 'arduino_proxy.dj.views.digital_write', name='digital_write'),
    url(r'^analog_write/?$', 'arduino_proxy.dj.views.analog_write', name='analog_write'),
    url(r'^analog_read/?$', 'arduino_proxy.dj.views.analog_read', name='analog_read'),
    url(r'^digital_read/?$', 'arduino_proxy.dj.views.digital_read', name='digital_read'),
    url(r'^delay/?$', 'arduino_proxy.dj.views.delay', name='delay'),
    url(r'^get_avr_cpu_type$', 'arduino_proxy.dj.views.get_avr_cpu_type',
        name='get_avr_cpu_type'),
    url(r'^get_arduino_type_struct$', 'arduino_proxy.dj.views.get_arduino_type_struct',
        name='get_arduino_type_struct'),
    url(r'^ping$', 'arduino_proxy.dj.views.ping', name='ping'),
    url(r'^validate_connection$', 'arduino_proxy.dj.views.validate_connection',
        name='validate_connection'),
    url(r'^get_free_memory$', 'arduino_proxy.dj.views.get_free_memory',
        name='get_free_memory'),
    url(r'^close$', 'arduino_proxy.dj.views.close', name='close'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('django.contrib.staticfiles.views',
    url(r'^static/(?P<path>.*)$', 'serve'),
)
