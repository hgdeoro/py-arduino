var pyArduinoModule = angular.module('PyArduino', [ 'uiSlider' ]);

// pyArduinoModule.factory('pyArduinoHttpClient', [ '$http', function($http) {
// var get_arduino_data_url = '/angular/get_arduino_data/';
// return {
// get_arduino_data : function() {
// return $http.get(get_arduino_data_url);
// }
// };
// } ]);

pyArduinoModule.filter('is_number', function() {
    return function(input) {
        return typeof input == "number";
    };
});

pyArduinoModule.filter('as_high_low', function() {
    return function(input) {
        if (input == 0)
            return 'LOW';
        if (input == 1)
            return 'HIGH';
        return '?';
    };
});

pyArduinoModule.filter('written_pwm_value', function() {
    return function(pin_struct) {
        if (pin_struct.status.analog_written_value != null) {
            if (pin_struct.status.analog_written_value == 0)
                return 'LOW (0)';
            if (pin_struct.status.analog_written_value == 255)
                return 'HIGH (255)';
            return pin_struct.status.analog_written_value;
        }

        if (pin_struct.status.written_value == 0)
            return 'LOW';
        if (pin_struct.status.written_value == 1)
            return 'HIGH';
        return '?';
    };
});

pyArduinoModule.controller('GlobalController', function($scope) {

    $scope.CONST = {
        INPUT : 0,
        OUTPUT : 1,
        LOW : 0,
        HIGH : 1
    };

    $scope.avr_cpu_type = '(unknown)';
    $scope.enhanced_arduino_type = {};

});

pyArduinoModule.controller('PinsController', function($scope, $http) {

    var get_arduino_data_url = '/angular/get_arduino_data/';
    var digital_pin_mode_url = '/angular/digital_pin_mode/';
    var read_pin_url = '/angular/read_pin/';
    var digital_write_url = '/angular/digital_write/';
    var analog_write_url = '/angular/analog_write/';

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
        $scope.editMode = false;
        // TODO: save changes!
    };

    /*
     * Pin Mode
     */

    $scope.pinModeDisabled = function(pinStruct) {
        $scope.setDigitalPinMode(pinStruct.pin, MODE_PIN_UNKNOWN);
        $scope.refreshCssForButtons();
    };

    $scope.pinModeInput = function(pinStruct) {
        $scope.setDigitalPinMode(pinStruct.pin, INPUT);
        $scope.refreshCssForButtons();
    };

    $scope.pinModeOutput = function(pinStruct) {
        $scope.setDigitalPinMode(pinStruct.pin, OUTPUT);
        $scope.refreshCssForButtons();
    };

    /*
     * refreshCssForButtons()
     */
    $scope.refreshCssForButtons = function() {

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

    };

    /*
     * refreshPinInfo()
     */
    $scope.refreshPinInfo = function() {
        console.info("refreshPinInfo()");

        $http.get(get_arduino_data_url).success(function(data) {
            $scope.avr_cpu_type = data.avr_cpu_type;
            $scope.enhanced_arduino_type = data.enhanced_arduino_type;
            $scope.refreshCssForButtons();

        }).error(function(data) {
            console.error("refreshPinInfo() -> $http.get() -> ERROR -> " + data);
        });
    };

    /*
     * setDigitalPinMode()
     */
    $scope.setDigitalPinMode = function(pin, mode) {

        console.info("setPinMode()");
        $http.post(digital_pin_mode_url, {
            pin : pin,
            mode : mode

        }).success(function(data) {
            $scope.avr_cpu_type = data.avr_cpu_type;
            $scope.enhanced_arduino_type = data.enhanced_arduino_type;
            $scope.refreshCssForButtons();

        }).error(function(data) {
            console.error("setPinMode() -> $http.post() -> ERROR -> " + data);
        });

    };

    /*
     * readPin()
     */
    $scope.readPin = function(pin_struct) {

        console.info("readPin()");
        $http.post(read_pin_url, {
            pin : pin_struct.pin,
            digital : pin_struct.digital

        }).success(function(data) {
            $scope.avr_cpu_type = data.avr_cpu_type;
            $scope.enhanced_arduino_type = data.enhanced_arduino_type;
            $scope.refreshCssForButtons();

        }).error(function(data) {
            console.error("readPin() -> $http.post() -> ERROR -> " + data);
        });

    };

    /*
     * digitalWrite()
     */
    $scope.digitalWrite = function(pin_struct, value) {

        console.info("digitalWrite()");
        $http.post(digital_write_url, {
            pin : pin_struct.pin,
            digital : pin_struct.digital,
            value : value

        }).success(function(data) {
            $scope.avr_cpu_type = data.avr_cpu_type;
            $scope.enhanced_arduino_type = data.enhanced_arduino_type;
            $scope.refreshCssForButtons();

        }).error(function(data) {
            console.error("digitalWrite() -> $http.post() -> ERROR -> " + data);
        });

    };

    /*
     * analogWrite()
     */
    $scope.analogWrite = function(pin_struct) {

        console.info("analogWrite()");

        if (typeof(pin_struct._tmp_analog_write) == "undefined") {
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

        $http.post(analog_write_url, {
            pin : pin_struct.pin,
            digital : pin_struct.digital,
            value : value

        }).success(function(data) {
            $scope.avr_cpu_type = data.avr_cpu_type;
            $scope.enhanced_arduino_type = data.enhanced_arduino_type;
            $scope.refreshCssForButtons();

        }).error(function(data) {
            console.error("analogWrite() -> $http.post() -> ERROR -> " + data);
        });

    };

});
