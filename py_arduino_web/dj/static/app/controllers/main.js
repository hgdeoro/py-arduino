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

pyArduinoModule.factory('remoteArduino', function($http) {
    var remoteArduinoService = {

        // get_pin_status : function() {
        //
        // //
        // //
        // http://stackoverflow.com/questions/12505760/angularjs-processing-http-response-in-service
        // //
        //
        // var promise =
        // $http.get('/angular/get_arduino_data/').then(function(response) {
        // console.info('remoteArduino.get_pin_status(): OK');
        // //
        // // data – {string|Object} – The response body transformed with
        // // the transform functions.
        // //
        // // status – {number} – HTTP status code of the response.
        // //
        // // headers – {function([headerName])} – Header getter function.
        // //
        // // config – {Object} – The configuration object that was used to
        // // generate the request.
        // //
        // response.ok = true;
        // response.error = false;
        // return response;
        //
        // }, function(response) {
        // console.error('remoteArduino.get_pin_status(): ERROR - response: ' +
        // response);
        // response.ok = false;
        // response.error = true;
        // return response;
        // });
        // return promise;
        // },

        callArduinoMethod : function(arduino_method) {
            // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions_and_function_scope/arguments
            var functionArgs = Array.prototype.slice.call(arguments, 1);
            return $http.post('/angular/call_arduino_method/', {
                functionName : arduino_method,
                functionArgs : functionArgs
            });
        },

    };

    // factory function body that constructs shinyNewServiceInstance
    return remoteArduinoService;
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

    $scope.extras = {
        avr_cpu_type : '', // default to empty string
        errors : [],
        bg_tasks : [],
    };

    $scope.enhanced_arduino_type = {};

    $scope.resetExtras = function() {
        $scope.extras.avr_cpu_type = '';
        $scope.extras.bg_tasks = [];
    };

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
