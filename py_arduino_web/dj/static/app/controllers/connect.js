function ConnectController($scope, $http, $location) {

    $scope.data = {};
    $scope.flags = {};

    $scope.flags.checkingConnection = true;
    $scope.flags.connecting = false;
    $scope.flags.emulator_port = '/dev/ARDUINO_EMULATOR';

    //
    // Django views should return:
    //
    // data['connected'] = False
    // data['serial_ports'] = ( ... )
    // data['pyro_not_contacted'] = False
    //

    $scope.checkConnection = function() {
        $http.post($scope.CONST.check_connection_url, {

        }).success(function(data) {
            $scope.flags.checkingConnection = false;
            $scope.data = data;

        }).error(function(data) {
            $scope.flags.checkingConnection = false;
            $scope.data = {};

        });
    };

    $scope.connectArduino = function(serial_port) {
        // ret['connection_attempt_ok'] = True
        // ret['connection_attempt_failed'] = True

        $scope.safeApply(function() {
            $scope.flags.connecting = true;
        });

        // $scope.flags.connecting = true;

        $http.post($scope.CONST.connect_url, {
            serial_port : serial_port

        }).success(function(data) {
            $scope.flags.checkingConnection = false;
            $scope.flags.connecting = false;
            $scope.data = data;

        }).error(function(data) {
            $scope.flags.checkingConnection = false;
            $scope.flags.connecting = false;
            $scope.data = {};

        });
    };

    $scope.disconnectArduino = function(serial_port) {
        $http.post($scope.CONST.disconnect_url, {

        }).success(function(data) {
            $scope.flags.checkingConnection = false;
            $scope.data = data;

        }).error(function(data) {
            $scope.flags.checkingConnection = false;
            $scope.data = {};

        });
    };

};
