from django.conf.urls import patterns, include, url
from django.contrib import admin
#from django.conf import settings

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
    # Global URLs
    url(r'^$', 'py_arduino_web.dj.views.home', name='home'),
    # url(r'^connect/?$', 'py_arduino_web.dj.views.connect', name='connect'),

    # URLs for methods
    #    url(r'^pin_mode/?$', 'py_arduino_web.dj.views.pin_mode', name='pin_mode'),
    #    url(r'^digital_write/?$', 'py_arduino_web.dj.views.digital_write', name='digital_write'),
    #    url(r'^analog_write/?$', 'py_arduino_web.dj.views.analog_write', name='analog_write'),
    #    url(r'^analog_read/?$', 'py_arduino_web.dj.views.analog_read', name='analog_read'),
    #    url(r'^digital_read/?$', 'py_arduino_web.dj.views.digital_read', name='digital_read'),
    #    url(r'^delay/?$', 'py_arduino_web.dj.views.delay', name='delay'),
    #    url(r'^get_avr_cpu_type$', 'py_arduino_web.dj.views.get_avr_cpu_type',
    #        name='get_avr_cpu_type'),
    #    url(r'^get_arduino_type_struct$', 'py_arduino_web.dj.views.get_arduino_type_struct',
    #        name='get_arduino_type_struct'),
    #    url(r'^ping$', 'py_arduino_web.dj.views.ping', name='ping'),
    #    url(r'^validate_connection$', 'py_arduino_web.dj.views.validate_connection',
    #        name='validate_connection'),
    #    url(r'^get_free_memory$', 'py_arduino_web.dj.views.get_free_memory',
    #        name='get_free_memory'),
    #    url(r'^close$', 'py_arduino_web.dj.views.close', name='close'),

    url(r'^angular/get_arduino_data/?$', 'py_arduino_web.dj.views_angularjs.get_arduino_data',
        name='ng_get_arduino_data'),
    url(r'^angular/update_labels_and_ids/?$',
        'py_arduino_web.dj.views_angularjs.update_labels_and_ids',
        name='ng_update_labels_and_ids'),
    url(r'^angular/call_arduino_method/?$',
        'py_arduino_web.dj.views_angularjs.call_arduino_method',
        name='ng_call_arduino_method'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('django.contrib.staticfiles.views',
    url(r'^static/(?P<path>.*)$', 'serve'),
)
