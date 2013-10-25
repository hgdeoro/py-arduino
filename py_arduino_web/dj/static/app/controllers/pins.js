function PinsController($scope, $http, $location, $interval, remoteArduino) {

    var get_arduino_data_url = '/angular/get_arduino_data/';
    var digital_pin_mode_url = '/angular/digital_pin_mode/';
    var read_pin_url = '/angular/read_pin/';
    var digital_write_url = '/angular/digital_write/';
    var analog_write_url = '/angular/analog_write/';
    var update_labels_and_ids_url = '/angular/update_labels_and_ids/';

    var MODE_PIN_UNKNOWN = null; // 'None' of PyArduino
    var INPUT = 0;
    var OUTPUT = 1;
    var LOW = 0;
    var HIGH = 1;

    var CSS_FOR_SELECTED_MODE = 'btn-success';
    var CSS_FOR_NON_SELECTED_MODE = 'btn-default';

    /*
     * Edit mode
     */

    $scope.editMode = false;

    $scope.editModeEnter = function() {
        $scope.editMode = true;
    };

    $scope.editModeExit = function() {
        console.info("editModeExit()");

        var to_update = Array();

        function smart_add(pin_struct) {
            var include = false;
            var a_pin = {
                pk : pin_struct.pk
            }
            if (Boolean(pin_struct._pin_label_modified)) {
                console.info("Modified (label): " + pin_struct.label);
                a_pin.label = pin_struct.label;
                include = true;
            }
            if (Boolean(pin_struct._pin_id_modified)) {
                console.info("Modified (id): " + pin_struct.pin_id);
                a_pin.pin_id = pin_struct.pin_id;
                include = true;
            }
            if (include)
                to_update.push(a_pin);
        }

        var i = 0;
        for (i = 0; i < $scope.enhanced_arduino_type.digital_pins_struct.length; i++) {
            var pin_struct = $scope.enhanced_arduino_type.digital_pins_struct[i];
            smart_add(pin_struct);
        }

        for (i = 0; i < $scope.enhanced_arduino_type.analog_pins_struct.length; i++) {
            var pin_struct = $scope.enhanced_arduino_type.analog_pins_struct[i];
            smart_add(pin_struct);
        }

        $http.post(update_labels_and_ids_url, {
            to_update : to_update

        }).success(function(data) {
            $scope.editMode = false;
            $scope.refreshUi(data);

        }).error(function(data) {
            console.error("editModeExit() -> $http.post() -> ERROR -> " + data);
        });

    };

    $scope.pinIdModified = function(pinStruct) {
        pinStruct._pin_id_modified = true;
    };

    $scope.pinLabelModified = function(pinStruct) {
        pinStruct._pin_label_modified = true;
    };

    /*
     * Pin Mode
     */

    $scope.pinModeDisabled = function(pinStruct) {
        $scope.setDigitalPinMode(pinStruct.pin, MODE_PIN_UNKNOWN);
    };

    $scope.pinModeInput = function(pinStruct) {
        $scope.setDigitalPinMode(pinStruct.pin, INPUT);
    };

    $scope.pinModeOutput = function(pinStruct) {
        $scope.setDigitalPinMode(pinStruct.pin, OUTPUT);
    };

    /*
     * refreshUi()
     */
    $scope.refreshUi = function(data) {

        $scope.resetExtras();
        $scope.extras.avr_cpu_type = data.avr_cpu_type;
        $scope.extras.bg_tasks = data.bg_tasks;
        $scope.enhanced_arduino_type = data.enhanced_arduino_type;

        var i = 0;

        // "digital_pins_struct": [{
        // "status": {
        // .. "read_value": null,
        // .. "written_value": null,
        // .. "mode_is_input": true,
        // .. "mode": 0,
        // .. "digital": true,
        // .. "mode_is_unknown": false,
        // .. "mode_is_output": false
        // },
        // "enabled_in_web": true,
        // "pin": 0,
        // "pin_id": null,
        // "label": "Digital pin #0",
        // "digital": true,
        // "pk": 1,
        // "pwm": false

        for (i = 0; i < $scope.enhanced_arduino_type.digital_pins_struct.length; i++) {
            var pin_struct = $scope.enhanced_arduino_type.digital_pins_struct[i];
            // Allow modifications from UI
            pin_struct.enabled = !(pin_struct.enabled_in_web == false || pin_struct.status.bg_task_name);
            // CSS
            if (pin_struct.status.mode_is_input) {
                pin_struct.css_for_button_unknown_mode = CSS_FOR_NON_SELECTED_MODE;
                pin_struct.css_for_button_input_mode = CSS_FOR_SELECTED_MODE;
                pin_struct.css_for_button_output_mode = CSS_FOR_NON_SELECTED_MODE;
            } else if (pin_struct.status.mode_is_output) {
                pin_struct.css_for_button_unknown_mode = CSS_FOR_NON_SELECTED_MODE;
                pin_struct.css_for_button_input_mode = CSS_FOR_NON_SELECTED_MODE;
                pin_struct.css_for_button_output_mode = CSS_FOR_SELECTED_MODE;
            } else {
                pin_struct.css_for_button_unknown_mode = CSS_FOR_SELECTED_MODE;
                pin_struct.css_for_button_input_mode = CSS_FOR_NON_SELECTED_MODE;
                pin_struct.css_for_button_output_mode = CSS_FOR_NON_SELECTED_MODE;
            }
        }

        // "analog_pins_struct": [{
        // "status": {
        // .. "read_value": null,
        // .. "written_value": null,
        // .. "mode_is_input": false,
        // .. "mode": null,
        // .. "digital": false,
        // .. "mode_is_unknown": true,
        // .. "mode_is_output": false
        // },
        // "enabled_in_web": true,
        // "pin": 0,
        // "pin_id": null,
        // "label": "Analog pin #0",
        // "digital": false,
        // "pk": 55,
        // "pwm": false

        for (i = 0; i < $scope.enhanced_arduino_type.analog_pins_struct.length; i++) {
            var pin_struct = $scope.enhanced_arduino_type.analog_pins_struct[i];
            // Allow modifications from UI
            pin_struct.enabled = !(pin_struct.enabled_in_web == false || pin_struct.status.bg_task_name);
            // CSS
            if (pin_struct.status.mode_is_input) {
                pin_struct.css_for_button_unknown_mode = CSS_FOR_NON_SELECTED_MODE;
                pin_struct.css_for_button_input_mode = CSS_FOR_SELECTED_MODE;
                pin_struct.css_for_button_output_mode = CSS_FOR_NON_SELECTED_MODE;
            } else {
                pin_struct.css_for_button_unknown_mode = CSS_FOR_SELECTED_MODE;
                pin_struct.css_for_button_input_mode = CSS_FOR_NON_SELECTED_MODE;
                pin_struct.css_for_button_output_mode = CSS_FOR_NON_SELECTED_MODE;
            }
        }

        if (data.response_errors)
            for (i = 0; i < data.response_errors.length; i++) {
                $scope.extras.errors.push(data.response_errors[i]);
            }
    };

    /*
     * refreshPinInfo()
     */
    $scope.refreshPinInfo = function() {
        console.info("refreshPinInfo()");

        $http.get(get_arduino_data_url).success(function(data) {
            $scope.refreshUi(data);

        }).error(function(data) {
            // Check connection problem!
            // If error was caused because Arduino isn't connected, we should
            // redirect to /connection
            if (data && data.try_connect) {
                $location.path("/connection");
                return;
            }

            console.error("refreshPinInfo() -> $http.get() -> ERROR -> " + data);
        });
    };

    /*
     * autoRefresh
     */

    // $scope.getBackgroundProcessesStatus

    $scope.startAutoRefresh = function() {
        if ($scope.extras.intervalAutoRefresh)
            return;
        $scope.extras.intervalAutoRefresh = $interval(function() {
            $scope.refreshPinInfo();
        }, 5000);
    };

    $scope.stopAutoRefresh = function() {
        console.info("stopAutoRefresh()");
        $interval.cancel($scope.extras.intervalAutoRefresh);
        $scope.extras.intervalAutoRefresh = null;
    };

    /*
     * setDigitalPinMode()
     */
    $scope.setDigitalPinMode = function(pin, mode) {
        console.info("setPinMode()");
        remoteArduino.callArduinoMethod('pinMode', pin, mode).success(function(data) {
            data = data.method_returned; // TODO: remove this!
            $scope.refreshUi(data);

        }).error(function(data) {
            data = data.method_returned; // TODO: remove this!
            console.error("setPinMode() -> $http.post() -> ERROR -> " + data);
        });

    };

    /*
     * readPin()
     */
    $scope.readPin = function(pin_struct) {
        console.info("readPin()");
        remoteArduino.callArduinoMethod('read_pin', pin_struct.pin, pin_struct.digital).success(function(data) {
            data = data.method_returned; // TODO: remove this!
            $scope.refreshUi(data);

        }).error(function(data) {
            data = data.method_returned; // TODO: remove this!
            console.error("readPin() -> $http.post() -> ERROR -> " + data);
        });

    };

    /*
     * digitalWrite()
     */
    $scope.digitalWrite = function(pin_struct, value) {
        console.info("digitalWrite()");
        remoteArduino.callArduinoMethod('digital_write', pin_struct.pin, pin_struct.digital, value).success(function(data) {
            data = data.method_returned; // TODO: remove this!
            $scope.refreshUi(data);

        }).error(function(data) {
            data = data.method_returned; // TODO: remove this!
            console.error("digitalWrite() -> $http.post() -> ERROR -> " + data);
        });

    };

    /*
     * analogWrite()
     */
    $scope.analogWrite = function(pin_struct) {

        console.info("analogWrite()");

        if (typeof (pin_struct._tmp_analog_write) == "undefined") {
            alert("Invalid value for PWM");
            return;
        }

        var tmp = '' + pin_struct._tmp_analog_write;
        tmp = tmp.trim();
        pin_struct._tmp_analog_write = '';

        if (isNaN(tmp) || tmp == '') {
            alert("Not a valid value: " + tmp);
            return;
        }

        var value = Number(tmp);

        if (value < 0 || value > 255) {
            alert("Not a valid value: " + value);
            return;
        }

        remoteArduino.callArduinoMethod('analog_write', pin_struct.pin, pin_struct.digital, value).success(function(data) {
            data = data.method_returned; // TODO: remove this!
            $scope.refreshUi(data);

        }).error(function(data) {
            data = data.method_returned; // TODO: remove this!
            console.error("analogWrite() -> $http.post() -> ERROR -> " + data);
        });

    };

};
