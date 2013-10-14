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

    $scope.arduino_data = {
        arduino_type : '',
        avr_cpu_type : '(unknown)',
        enhanced_arduino_type : ''
    };

});

pyArduinoModule.controller('PinsController', function($scope, $http) {

    $scope.pins = [ 1, 2, 3, 4 ];

    var get_arduino_data_url = '/angular/get_arduino_data/';

    $scope.loadPinInfo = function() {
        console.info("loadPinInfo()");
        $http.get(get_arduino_data_url).success(function(data) {

            console.debug("$http.get() -> success -> " + data);
            console.debug("data.arduino_type: " + data.arduino_type);
            console.debug("data.avr_cpu_type: " + data.avr_cpu_type);
            console.debug("data.enhanced_arduino_type: " + data.enhanced_arduino_type);

            $scope.arduino_data.arduino_type = data.arduino_type;
            $scope.arduino_data.avr_cpu_type = data.avr_cpu_type;
            $scope.arduino_data.arduino_type = data.enhanced_arduino_type;
            // $scope.arduino_data = data;

        }).error(function(data) {
            console.error("$http.get() -> ERROR -> " + data);
        });
    }
});
