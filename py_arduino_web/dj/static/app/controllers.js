var pyArduinoModule = angular.module('PyArduino', []);

// pyArduinoModule.factory('pyArduinoHttpClient', [ '$http', function($http) {
// var get_arduino_data_url = '/angular/get_arduino_data/';
// return {
// get_arduino_data : function() {
// return $http.get(get_arduino_data_url);
// }
// };
// } ]);

pyArduinoModule.controller('GlobalController', function($scope) {

    $scope.avr_cpu_type = '(unknown)';
    $scope.arduino_type = {};
    $scope.enhanced_arduino_type = {};

});

pyArduinoModule.controller('PinsController', function($scope, $http) {

    var get_arduino_data_url = '/angular/get_arduino_data/';

    $scope.loadPinInfo = function() {
        console.info("loadPinInfo()");
        $http.get(get_arduino_data_url).success(function(data) {

            console.debug("$http.get() -> success -> " + data);
            $scope.avr_cpu_type = data.avr_cpu_type;
            $scope.arduino_type = data.arduino_type;
            $scope.enhanced_arduino_type = data.enhanced_arduino_type;

            console.debug("$scope.avr_cpu_type: " + $scope.avr_cpu_type);
            console.debug("$scope.arduino_type: " + $scope.arduino_type);
            console.debug("$scope.enhanced_arduino_type: " + $scope.enhanced_arduino_type);
            console.debug("$scope.enhanced_arduino_type.digital_pins_struct: " + $scope.enhanced_arduino_type.digital_pins_struct);

            // "enhanced_arduino_type": {
            // "digital_pins_struct": [
            // .... {
            // .... .... "pwm": false,
            // .... .... "enabled_in_web": true,
            // .... .... "pin": 0,
            // .... .... "pin_id": null,
            // .... .... "status.written_value": null,
            // .... .... "status.read_value": null,
            // .... .... "status.mode": null,
            // .... .... "digital": true,
            // .... .... "pk": 1,
            // .... .... "label": "Digital pin #0"
            // .... },
            // ],
            // "analog_pins_struct": [
            // .... {
            // .... "pwm": false,
            // .... "enabled_in_web": true,
            // .... "pin": 0,
            // .... "pin_id": null,
            // .... "status.written_value": null,
            // .... "status.read_value": null,
            // .... "status.mode": null,
            // .... "digital": true,
            // .... "pk": 55,
            // .... "label": "Analog pin #0"
            // .... },
            // ],

        }).error(function(data) {
            console.error("$http.get() -> ERROR -> " + data);
        });
    }
});
