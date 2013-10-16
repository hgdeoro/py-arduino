var pyArduinoModule = angular.module('PyArduino', [ /* 'uiSlider' */]);

pyArduinoModule.config(function($routeProvider) {

    $routeProvider.when('/', {
        controller : RedirectController,
        templateUrl : '/static/app/redirect.html',

    }).when('/connection', {
        controller : ConnectController,
        templateUrl : '/static/app/connect.html',

    }).when('/pins', {
        controller : PinsController,
        templateUrl : '/static/app/pins.html',

    // }).otherwise({
    // controller : aController,
    // templateUrl : '/path/to/template',

    });

});

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
            // if (pin_struct.status.analog_written_value == 0)
            // return 'LOW (0)';
            // if (pin_struct.status.analog_written_value == 255)
            // return 'HIGH (255)';
            return pin_struct.status.analog_written_value;
        }

        if (pin_struct.status.written_value == 0)
            return 'LOW';
        if (pin_struct.status.written_value == 1)
            return 'HIGH';
        return '?';
    };
});

pyArduinoModule.controller('GlobalController', function($scope, $location) {

    $scope.CONST = {
        INPUT : 0,
        OUTPUT : 1,
        LOW : 0,
        HIGH : 1,
        check_connection_url : '/angular/check_connection/',
        connect_url : '/angular/connect/',
        disconnect_url : '/angular/disconnect/',
    };

    $scope.avr_cpu_type = '(unknown)';
    $scope.extras = {
        avr_cpu_type : '(unknown)',
        errors : [],
        bg_tasks : [],
    };
    $scope.enhanced_arduino_type = {};

    $scope.isCurrentPath = function(path) {
        return $location.path() == path;
    };

    $scope.safeApply = function(fn) {
        var phase = this.$root.$$phase;
        if (phase == '$apply' || phase == '$digest') {
            if (fn && (typeof (fn) === 'function')) {
                fn();
            }
        } else {
            this.$apply(fn);
        }
    };

});
