import logging
import json
import Pyro4

from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect, \
    HttpResponseServerError
from django.core.urlresolvers import reverse
from django.contrib import messages

from py_arduino import DEVICE_FOR_EMULATOR, LOW, HIGH, \
    OUTPUT, INPUT
from py_arduino_web.pyroproxy.utils import get_arduino_pyro, server_is_up,\
    get_storage_pyro


ARDUINO_PYRO = get_arduino_pyro()
STORAGE_PYRO = get_storage_pyro()

from py_arduino_web.dj.views import JsonResponse


def get_arduino_data(request):

    if not server_is_up():
        raise(Exception("Pyro server isn't running"))

    if not ARDUINO_PYRO.is_connected():
        raise(Exception("Arduino isn't connected"))

    #    try:
    #        ARDUINO_PYRO.validateConnection()
    #    except Exception, e:
    #        # FIXME: DESIGN: error hablder should be part of PyArduino, not web interface...
    #        #    if self.validate_connection_error_handler:
    #        #        self.validate_connection_error_handler()
    #        ARDUINO_PYRO.close()
    #        messages.add_message(request, messages.ERROR, str(e))
    #        return HttpResponseRedirect(reverse('connect'))
    ARDUINO_PYRO.validateConnection()

    # At this point, ARDUINO_PYRO exists and is valid
    arduino_type = ARDUINO_PYRO.getArduinoTypeStruct()
    enhanced_arduino_type = ARDUINO_PYRO.enhanceArduinoTypeStruct(arduino_type)
    enhanced_arduino_type = STORAGE_PYRO.enhanceArduinoTypeStruct(enhanced_arduino_type)
    avr_cpu_type = ARDUINO_PYRO.getAvrCpuType()

    ctx = {
        'arduino_type': arduino_type,
        'avr_cpu_type': avr_cpu_type,
        'enhanced_arduino_type': enhanced_arduino_type,
    }

    return JsonResponse(ctx)
