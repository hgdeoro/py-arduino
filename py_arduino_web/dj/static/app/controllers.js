var pyArduinoModule = angular.module('PyArduino', []);

// /angular/get_arduino_data

pyArduinoModule.controller('PinsController', function($scope) {
	$scope.pins = [ 1, 2, 3, 4 ];
});
