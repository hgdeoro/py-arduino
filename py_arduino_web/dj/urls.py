from django.conf.urls import patterns, include, url
from django.contrib import admin
#from django.conf import settings

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
    # Global URLs
    url(r'^$', 'py_arduino_web.dj.views.home', name='home'),
    # url(r'^connect/?$', 'py_arduino_web.dj.views.connect', name='connect'),

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
