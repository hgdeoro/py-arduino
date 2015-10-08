import logging
import json

import Pyro4
from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponseServerError, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response

from py_arduino_web.pyroproxy.utils import get_arduino_pyro, get_storage_pyro
from py_arduino_web.dj.models import ControlPanel

ARDUINO_PYRO = get_arduino_pyro()
STORAGE_PYRO = get_storage_pyro()


class JsonResponse(HttpResponse):
    def __init__(self, data, indent=None, *args, **kwargs):
        content = json.dumps(data, indent=indent)
        mimetype = kwargs.get('mimetype', 'application/json')
        super(JsonResponse, self).__init__(content=content, mimetype=mimetype,
                                           *args, **kwargs)


class JsonErrorResponse(HttpResponseServerError):
    def __init__(self, exception, *args, **kwargs):
        content = json.dumps({
            'ok': False,
            'exception': str(exception),
        })
        mimetype = kwargs.get('mimetype', 'application/json')
        super(JsonErrorResponse, self).__init__(content=content, mimetype=mimetype,
                                                *args, **kwargs)


def home(request):
    return HttpResponseRedirect('/static/app/index.html')
    #    if not server_is_up():
    #        return HttpResponseRedirect(reverse('connect'))
    #
    #    if not ARDUINO_PYRO.is_connected():
    #        return HttpResponseRedirect(reverse('connect'))
    #
    #    try:
    #        ARDUINO_PYRO.validateConnection()
    #    except Exception, e:
    #        # FIXME: DESIGN: error hablder should be part of PyArduino, not web interface...
    #        #    if self.validate_connection_error_handler:
    #        #        self.validate_connection_error_handler()
    #        ARDUINO_PYRO.close()
    #        messages.add_message(request, messages.ERROR, str(e))
    #        return HttpResponseRedirect(reverse('connect'))
    #
    #    # At this point, ARDUINO_PYRO exists and is valid
    #    arduino_type = ARDUINO_PYRO.getArduinoTypeStruct()
    #    enhanced_arduino_type = ARDUINO_PYRO.enhanceArduinoTypeStruct(arduino_type)
    #    enhanced_arduino_type = STORAGE_PYRO.enhanceArduinoTypeStruct(enhanced_arduino_type)
    #    avr_cpu_type = ARDUINO_PYRO.getAvrCpuType()
    #
    #    ctx = {
    #        'arduino_type': arduino_type,
    #        'avr_cpu_type': avr_cpu_type,
    #        'enhanced_arduino_type': enhanced_arduino_type,
    #    }
    #
    #    return render(request, 'web-ui-main.html', ctx)


def get_free_memory(request):
    # TODO: this wasn't tested when migrated to Django
    try:
        return JsonResponse({
            'ok': True,
            'freeMemory': ARDUINO_PYRO.getFreeMemory(),
        })
    except Exception, e:
        # FIXME: return error details and log
        logging.exception("Exception raised by arduino.get_free_memory(). " +
                          "".join(Pyro4.util.getPyroTraceback()))
        return JsonErrorResponse(e)


def ping(request):
    try:
        ARDUINO_PYRO.ping()
        return JsonResponse({
            'ok': True,
        })
    except Exception, e:
        # FIXME: return error details and log
        logging.exception("Exception raised by arduino.ping(). " +
                          "".join(Pyro4.util.getPyroTraceback()))
        return JsonErrorResponse(e)


def validate_connection(request):
    try:
        random_value = ARDUINO_PYRO.validateConnection()
        return JsonResponse({
            'ok': True,
            'random_value': random_value,
        })
    except Exception, e:
        # FIXME: return error details and log
        logging.exception("Exception raised by arduino.validate_connection(). " +
                          "".join(Pyro4.util.getPyroTraceback()))
        return JsonErrorResponse(e)


def control_panel_html(request):
    try:
        cp = ControlPanel.objects.get(name='default')
        return HttpResponse(cp.html)
    except ControlPanel.DoesNotExist:
        return HttpResponse("<p>Control panel with name 'default' not found.</p>")


def control_panel_js(request):
    try:
        cp = ControlPanel.objects.get(name='default')
        return HttpResponse(cp.js, content_type='application/javascript')
    except ControlPanel.DoesNotExist:
        return HttpResponse("/* Control panel with name 'default' not found. */")


def control_panel_combined(request):
    try:
        cp = ControlPanel.objects.get(name='default')
        return JsonResponse({
            'html': cp.html,
            'header': cp.header,
            'js': cp.js,
        })
    except ControlPanel.DoesNotExist:
        return HttpResponse("Control panel with name 'default' not found.")


@csrf_exempt
def control_panel_update(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    data = json.loads(request.body)
    control_panel = ControlPanel.objects.get(name='default')
    control_panel.html = data['html']
    control_panel.header = data['header']
    control_panel.js = data['js']
    control_panel.save()
    return HttpResponse('ok')


@csrf_exempt
def control_panel_view(request):
    try:
        cp = ControlPanel.objects.get(name='default')
        html_contents = cp.html
        html_header = cp.header
    except ControlPanel.DoesNotExist:
        html_contents = ''
        html_header = ''

    ctx = {
        'html_header': html_header,
        'html_contents': html_contents,
    }
    return render_to_response('py-arduino/control_panel_view.html', ctx)
