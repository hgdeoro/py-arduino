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
    if not server_is_up():
        return HttpResponseRedirect(reverse('connect'))

    if not ARDUINO_PYRO.is_connected():
        return HttpResponseRedirect(reverse('connect'))

    try:
        ARDUINO_PYRO.validateConnection()
    except Exception, e:
        # FIXME: DESIGN: error hablder should be part of PyArduino, not web interface...
        #    if self.validate_connection_error_handler:
        #        self.validate_connection_error_handler()
        ARDUINO_PYRO.close()
        messages.add_message(request, messages.ERROR, str(e))
        return HttpResponseRedirect(reverse('connect'))

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

    return render(request, 'web-ui-main.html', ctx)


def connect(request):

    if request.method == 'GET':
        if server_is_up():
            return render(request, 'web-ui-connect.html', {
                'serial_ports': ARDUINO_PYRO.get_serial_ports(),
            })
        else:
            return render(request, 'web-ui-connect.html', {
                'show_start_pyroproxy_server_msg': True,
            })

    if ARDUINO_PYRO.is_connected():
        raise(Exception("PyArduino is already connected"))

    if 'connect_emulator' in request.REQUEST:
        serial_port = DEVICE_FOR_EMULATOR
        speed = None
    else:
        serial_port = request.REQUEST['serial_port']
        speed = int(request.REQUEST['speed'])

    try:
        logging.info("Trying to connect to %s", serial_port)
        ARDUINO_PYRO.connect(tty=serial_port, speed=speed)
        return HttpResponseRedirect(reverse('home'))
    except Exception, e:
        try:
            ARDUINO_PYRO.close()
        except:
            pass
        logging.error("Couldn't connect. " + "".join(Pyro4.util.getPyroTraceback()))
        messages.add_message(request, messages.ERROR,
            "Couldn't connect: {0}".format(str(e)))
        return HttpResponseRedirect(reverse('connect'))


def get_avr_cpu_type(request):
    try:
        return JsonResponse({
            'ok': True,
            'avrCpuType': ARDUINO_PYRO.getAvrCpuType(),
        })
    except Exception, e:
        # FIXME: return error details and log
        logging.exception("Exception raised by arduino.getAvrCpuType(). " +
            "".join(Pyro4.util.getPyroTraceback()))
        return JsonErrorResponse(e)


def get_arduino_type_struct(request):
    try:
        return JsonResponse({
            'ok': True,
            'arduinoTypeStruct': ARDUINO_PYRO.getArduinoTypeStruct(),
        })
    except Exception, e:
        # FIXME: return error details and log
        logging.exception("Exception raised by arduino.getArduinoTypeStruct(). " +
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


def pin_mode(request):
    pin = request.REQUEST.get('pin', None)
    mode = request.REQUEST.get('mode', None)
    try:
        if mode == 'output':
            ARDUINO_PYRO.pinMode(int(pin), OUTPUT)
            return JsonResponse({'ok': True, })
        elif mode == 'input':
            ARDUINO_PYRO.pinMode(int(pin), INPUT)
            return JsonResponse({'ok': True, })
        else:
            # FIXME: return error details and log
            return JsonResponse({'ok': False, 'error': 'Invalid mode: {0}'.format(mode)})
    except Exception, e:
        # FIXME: return error details and log
        logging.exception("Exception raised by arduino.pin_mode(). " +
            "".join(Pyro4.util.getPyroTraceback()))
        return JsonErrorResponse(e)


def digital_write(request):
    pin = request.REQUEST.get('pin', None)
    value = request.REQUEST.get('value', None)
    try:
        if value == 'low':
            ARDUINO_PYRO.digitalWrite(int(pin), LOW)
            return JsonResponse({'ok': True, })
        elif value == 'high':
            ARDUINO_PYRO.digitalWrite(int(pin), HIGH)
            return JsonResponse({'ok': True, })
        else:
            # FIXME: return error details and log
            return JsonResponse({
                'ok': False,
                'error': 'PyArduino returned an invalid value: {0}'.format(value)
            })
    except Exception, e:
        # FIXME: return error details and log
        logging.exception("Exception raised by arduino.digital_write(). " +
            "".join(Pyro4.util.getPyroTraceback()))
        return JsonErrorResponse(e)


def analog_write(request):
    pin = request.REQUEST.get('pin', None)
    value = request.REQUEST.get('value', None)
    try:
        ARDUINO_PYRO.analogWrite(int(pin), int(value))
        return JsonResponse({
            'ok': True,
        })
    except Exception, e:
        # FIXME: return error details and log
        logging.exception("Exception raised by arduino.analog_write(). " +
            "".join(Pyro4.util.getPyroTraceback()))
        return JsonErrorResponse(e)


def analog_read(request):
    pin = request.REQUEST.get('pin', None)
    try:
        value = ARDUINO_PYRO.analogRead(int(pin))
        return JsonResponse({
            'ok': True,
            'value': value,
        })
    except Exception, e:
        # FIXME: return error details and log
        logging.exception("Exception raised by arduino.analog_read(). " +
            "".join(Pyro4.util.getPyroTraceback()))
        return JsonErrorResponse(e)


def digital_read(request):
    pin = request.REQUEST.get('pin', None)
    try:
        value = ARDUINO_PYRO.digitalRead(int(pin))
        if value == HIGH:
            return JsonResponse({'ok': True, 'value': 1, })
        elif value == LOW:
            return JsonResponse({'ok': True, 'value': 0, })
        else:
            # FIXME: return error details and log
            return JsonResponse({
                'ok': False,
                'error': 'PyArduino returned an invalid value: {0}'.json(value)
            })
    except Exception, e:
        # FIXME: return error details and log
        logging.exception("Exception raised by arduino.digital_read(). " +
            "".join(Pyro4.util.getPyroTraceback()))
        return JsonErrorResponse(e)


def delay(request):
    # TODO: this wasn't tested when migrated to Django
    value = request.REQUEST.get('value', None)
    try:
        ARDUINO_PYRO.delay(int(value))
        return JsonResponse({
            'ok': True,
        })
    except Exception, e:
        # FIXME: return error details and log
        logging.exception("Exception raised by arduino.delay(). " +
            "".join(Pyro4.util.getPyroTraceback()))
        return JsonErrorResponse(e)


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


def close(request):
    try:
        ARDUINO_PYRO.close()
        return JsonResponse({
            'ok': True,
        })
    except Exception, e:
        # FIXME: return error details and log
        logging.exception("Exception raised by arduino.close(). " +
            "".join(Pyro4.util.getPyroTraceback()))
        return JsonErrorResponse(e)
