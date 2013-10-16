import json

from django.views.decorators.csrf import csrf_exempt

from py_arduino import LOW, HIGH, \
    OUTPUT, INPUT, MODE_UNKNOWN
from py_arduino_web.pyroproxy.utils import get_arduino_pyro, server_is_up, \
    get_storage_pyro, get_status_tracker
from py_arduino_web.dj.models import Pin
from django.db.utils import IntegrityError


ARDUINO_PYRO = get_arduino_pyro()
STORAGE_PYRO = get_storage_pyro()
STATUS_TRACKER = get_status_tracker()

from py_arduino_web.dj.views import JsonResponse


def _get_arduino_data(**kwargs):
    # basic data
    enhanced_arduino_type = ARDUINO_PYRO.getArduinoTypeStruct()
    # enhance and add status
    enhanced_arduino_type = ARDUINO_PYRO.enhanceArduinoTypeStruct(enhanced_arduino_type)
    # enhance with data from storage (labels, etc.)
    enhanced_arduino_type = STORAGE_PYRO.enhanceArduinoTypeStruct(enhanced_arduino_type)
    avr_cpu_type = ARDUINO_PYRO.getAvrCpuType()

    ctx = {
        'avr_cpu_type': avr_cpu_type,
        'enhanced_arduino_type': enhanced_arduino_type,
        'bg_tasks': STATUS_TRACKER.get_serializable_background_tasks(),
    }
    ctx.update(**kwargs)

    return ctx


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

    ctx = _get_arduino_data()
    if 'indent' in request.REQUEST:
        return JsonResponse(ctx, indent=int(request.REQUEST['indent']))
    else:
        return JsonResponse(ctx)


@csrf_exempt
def digital_pin_mode(request):
    if request.method != 'POST':
        raise(Exception("Only POST allowed"))

    data = json.loads(request.body)
    try:
        pin = int(data.get('pin', None))
    except ValueError:
        raise(Exception("Invalid pin: {}".format(data.get('pin', None))))

    mode = data.get('mode', '(not specified)')

    if mode == 'output' or mode == OUTPUT:
        ARDUINO_PYRO.pinMode(pin, OUTPUT)
        return JsonResponse(_get_arduino_data(result_ok=True))

    elif mode == 'input' or mode == INPUT:
        ARDUINO_PYRO.pinMode(pin, INPUT)
        return JsonResponse(_get_arduino_data(result_ok=True))

    elif mode == MODE_UNKNOWN:
        ARDUINO_PYRO.pinMode(pin, MODE_UNKNOWN)
        return JsonResponse(_get_arduino_data(result_ok=True))

    else:
        raise(Exception("Invalid mode: {}".format(mode)))


@csrf_exempt
def read_pin(request):
    if request.method != 'POST':
        raise(Exception("Only POST allowed"))

    data = json.loads(request.body)
    try:
        pin = int(data.get('pin', None))
    except ValueError:
        raise(Exception("Invalid pin: {}".format(data.get('pin', None))))

    digital = data.get('digital', None)
    if digital is True:
        ARDUINO_PYRO.digitalRead(pin)
        return JsonResponse(_get_arduino_data(result_ok=True))

    elif digital is False:
        ARDUINO_PYRO.analogRead(pin)
        return JsonResponse(_get_arduino_data(result_ok=True))

    raise(Exception("Invalid value for 'digital: {}".format(digital)))


@csrf_exempt
def digital_write(request):
    if request.method != 'POST':
        raise(Exception("Only POST allowed"))

    data = json.loads(request.body)
    try:
        pin = int(data.get('pin', None))
    except ValueError:
        raise(Exception("Invalid pin: {}".format(data.get('pin', None))))

    digital = data.get('digital', None)
    value = data.get('value', None)

    if digital is True:
        if value in (LOW, HIGH):
            ARDUINO_PYRO.digitalWrite(pin, value)
            return JsonResponse(_get_arduino_data(result_ok=True))

        raise(Exception("Invalid value for 'value: {}".format(value)))

    elif digital is False:
        # No support for write on analog pin yet
        raise(Exception("Invalid value for 'digital: {}".format(digital)))

    raise(Exception("Invalid value for 'digital: {}".format(digital)))


@csrf_exempt
def analog_write(request):
    if request.method != 'POST':
        raise(Exception("Only POST allowed"))

    data = json.loads(request.body)
    try:
        pin = int(data.get('pin', None))
    except ValueError:
        raise(Exception("Invalid pin: {}".format(data.get('pin', None))))

    digital = data.get('digital', None)
    value = data.get('value', None)

    if digital is True:
        if type(value) != int:
            raise(Exception("Invalid type for 'value': {}".format(value)))

        ARDUINO_PYRO.analogWrite(pin, value)
        return JsonResponse(_get_arduino_data(result_ok=True))

    elif digital is False:
        # No support for write on analog pin yet
        raise(Exception("Invalid value for 'digital': {}".format(digital)))

    raise(Exception("Invalid value for 'digital': {}".format(digital)))


@csrf_exempt
def update_labels_and_ids(request):
    if request.method != 'POST':
        raise(Exception("Only POST allowed"))

    response_errors = []

    data = json.loads(request.body)
    for item in data['to_update']:
        pin = Pin.objects.get(pk=item['pk'])
        if 'pin_id' in item:
            pin.pin_id = item['pin_id']
        if 'label' in item:
            pin.label = item['label']
        try:
            pin.save()
        except IntegrityError:
            response_errors.append("Couldn't update {}".format(pin))

    return JsonResponse(_get_arduino_data(result_ok=True, response_errors=response_errors))


#===============================================================================
# Connection handling
# All this views should return the same data
#===============================================================================

@csrf_exempt
def check_connection(request):
    if request.method != 'POST':
        raise(Exception("Only POST allowed"))

    ret = {}
    try:
        ret['connected'] = ARDUINO_PYRO.is_connected()
        ret['pyro_not_contacted'] = False
        if not ret['connected']:
            ret['serial_ports'] = ARDUINO_PYRO.get_serial_ports()
    except:
        ret['connected'] = False
        ret['pyro_not_contacted'] = True

    return JsonResponse(ret)


@csrf_exempt
def connect(request):
    if request.method != 'POST':
        raise(Exception("Only POST allowed"))

    data = json.loads(request.body)
    ret = {}
    serial_port = data.get('serial_port', None)

    try:
        ARDUINO_PYRO.connect(serial_port)
        ret['connected'] = ARDUINO_PYRO.is_connected()
        ret['pyro_not_contacted'] = False
        if not ret['connected']:
            ret['serial_ports'] = ARDUINO_PYRO.get_serial_ports()
    except:
        ret['connected'] = False
        ret['pyro_not_contacted'] = True

    return JsonResponse(ret)
