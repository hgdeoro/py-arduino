from django.conf.urls import patterns, include, url
from django.contrib import admin
#from django.conf import settings

from arduino_proxy.dj.views import EXPORT_VIEWS

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

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

for func_name in EXPORT_VIEWS:
    urlpatterns += patterns('',
        url(r'^' + func_name + r'$',
            'arduino_proxy.dj.views.' + func_name,
            name=func_name),
    )


urlpatterns += patterns('django.contrib.staticfiles.views',
    url(r'^static/(?P<path>.*)$', 'serve'),
)
