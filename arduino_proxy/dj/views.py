import logging
import json

from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect,\
    HttpResponseServerError
from django.core.urlresolvers import reverse
from django.contrib import messages

from arduino_proxy.proxy import ArduinoProxy


# FIXME: for serious uses, creation of PROXY should be synchronized
PROXY = None


class JsonResponse(HttpResponse):
    def __init__(self, data, *args, **kwargs):
        content = json.dumps(data)
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
    global PROXY

    if PROXY is None:
        return HttpResponseRedirect(reverse('connect'))

    try:
        PROXY.validateConnection()
    except Exception, e:
        # FIXME: DESIGN: error hablder should be part of ArduinoProxy, not web interface...
        #    if self.validate_connection_error_handler:
        #        self.validate_connection_error_handler()
        PROXY = None
        messages.add_message(request, messages.ERROR, str(e))
        return HttpResponseRedirect(reverse('connect'))

    # At this point, PROXY exists and is valid
    arduino_type = PROXY.getArduinoTypeStruct()
    enhanced_arduino_type = PROXY.enhanceArduinoTypeStruct(arduino_type)
    avr_cpu_type = PROXY.getAvrCpuType()

    ctx = {
        'arduino_type': arduino_type,
        'avr_cpu_type': avr_cpu_type,
        'enhanced_arduino_type': enhanced_arduino_type,
    }

    return render(request, 'web-ui-main.html', ctx)


def connect(request):
    global PROXY
    if request.method == 'GET':
        return render(request, 'web-ui-connect.html', {})

    if PROXY is not None:
        raise(Exception("WHAT TO DO???"))

    if 'connect_emulator' in request.REQUEST:
        PROXY = ArduinoProxy.create_emulator()
        return HttpResponseRedirect(reverse('home'))

    serial_port = request.REQUEST['serial_port']
    speed = int(request.REQUEST['speed'])
    try:
        logging.info("Trying to connect to %s", serial_port)
        PROXY = ArduinoProxy(serial_port, speed, wait_after_open=True)
        PROXY.connect()
        return HttpResponseRedirect(reverse('home'))
    except Exception, e:
        PROXY = None
        logging.exception("Couldn't connect")
        messages.add_message(request, messages.ERROR,
            "Couldn't connect: {0}".format(str(e)))
        return HttpResponseRedirect(reverse('connect'))


def get_avr_cpu_type(request):
    try:
        return JsonResponse({
            'ok': True,
            'avrCpuType': PROXY.getAvrCpuType(),
        })
    except Exception, e:
        # FIXME: return error details and log
        logging.exception("Exception raised by proxy.getAvrCpuType()")
        return JsonErrorResponse(e)


def get_arduino_type_struct(request):
    try:
        return JsonResponse({
            'ok': True,
            'arduinoTypeStruct': PROXY.getArduinoTypeStruct(),
        })
    except Exception, e:
        # FIXME: return error details and log
        logging.exception("Exception raised by proxy.getArduinoTypeStruct()")
        return JsonErrorResponse(e)


def ping(request):
    try:
        PROXY.ping()
        return JsonResponse({
            'ok': True,
        })
    except Exception, e:
        # FIXME: return error details and log
        logging.exception("Exception raised by proxy.ping()")
        return JsonErrorResponse(e)


def validate_connection(request):
    try:
        random_value = PROXY.validateConnection()
        return JsonResponse({
            'ok': True,
            'random_value': random_value,
        })
    except Exception, e:
        # FIXME: return error details and log
        logging.exception("Exception raised by proxy.validate_connection()")
        return JsonErrorResponse(e)


def pin_mode(request):
    pin = request.REQUEST.get('pin', None)
    mode = request.REQUEST.get('mode', None)
    try:
        if mode == 'output':
            PROXY.pinMode(int(pin), ArduinoProxy.OUTPUT)
            return JsonResponse({'ok': True, })
        elif mode == 'input':
            PROXY.pinMode(int(pin), ArduinoProxy.INPUT)
            return JsonResponse({'ok': True, })
        else:
            # FIXME: return error details and log
            return JsonResponse({'ok': False, 'error': 'Invalid mode: {0}'.format(mode)})
    except Exception, e:
        # FIXME: return error details and log
        logging.exception("Exception raised by proxy.pin_mode()")
        return JsonErrorResponse(e)


def digital_write(request):
    pin = request.REQUEST.get('pin', None)
    value = request.REQUEST.get('value', None)
    try:
        if value == 'low':
            PROXY.digitalWrite(int(pin), ArduinoProxy.LOW)
            return JsonResponse({'ok': True, })
        elif value == 'high':
            PROXY.digitalWrite(int(pin), ArduinoProxy.HIGH)
            return JsonResponse({'ok': True, })
        else:
            # FIXME: return error details and log
            return JsonResponse({
                'ok': False,
                'error': 'ArduinoProxy returned an invalid value: {0}'.format(value)
            })
    except Exception, e:
        # FIXME: return error details and log
        logging.exception("Exception raised by proxy.digital_write()")
        return JsonErrorResponse(e)


def analog_write(request):
    pin = request.REQUEST.get('pin', None)
    value = request.REQUEST.get('value', None)
    try:
        PROXY.analogWrite(int(pin), int(value))
        return JsonResponse({
            'ok': True,
        })
    except Exception, e:
        # FIXME: return error details and log
        logging.exception("Exception raised by proxy.analog_write()")
        return JsonErrorResponse(e)


def analog_read(request):
    pin = request.REQUEST.get('pin', None)
    try:
        value = PROXY.analogRead(int(pin))
        return JsonResponse({
            'ok': True,
            'value': value,
        })
    except Exception, e:
        # FIXME: return error details and log
        logging.exception("Exception raised by proxy.analog_read()")
        return JsonErrorResponse(e)


def digital_read(request):
    pin = request.REQUEST.get('pin', None)
    try:
        value = PROXY.digitalRead(int(pin))
        if value == ArduinoProxy.HIGH:
            return JsonResponse({'ok': True, 'value': 1, })
        elif value == ArduinoProxy.LOW:
            return JsonResponse({'ok': True, 'value': 0, })
        else:
            # FIXME: return error details and log
            return JsonResponse({
                'ok': False,
                'error': 'ArduinoProxy returned an invalid value: {0}'.json(value)
            })
    except Exception, e:
        # FIXME: return error details and log
        logging.exception("Exception raised by proxy.digital_read()")
        return JsonErrorResponse(e)


def delay(request):
    # TODO: this wasn't tested when migrated to Django
    value = request.REQUEST.get('value', None)
    try:
        PROXY.delay(int(value))
        return JsonResponse({
            'ok': True,
        })
    except Exception, e:
        # FIXME: return error details and log
        logging.exception("Exception raised by proxy.delay()")
        return JsonErrorResponse(e)


def get_free_memory(request):
    # TODO: this wasn't tested when migrated to Django
    try:
        return JsonResponse({
            'ok': True,
            'freeMemory': PROXY.getFreeMemory(),
        })
    except Exception, e:
        # FIXME: return error details and log
        logging.exception("Exception raised by proxy.get_free_memory()")
        return JsonErrorResponse(e)


def close(request):
    global PROXY
    try:
        PROXY.close()
        PROXY = None
        return JsonResponse({
            'ok': True,
        })
    except Exception, e:
        # FIXME: return error details and log
        logging.exception("Exception raised by proxy.close()")
        return JsonErrorResponse(e)
