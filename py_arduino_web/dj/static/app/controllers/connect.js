function ConnectController($scope, $http, $location, remoteArduino) {

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
        remoteArduino.callArduinoMethod('check_connection').success(function(data) {

            // TODO: remove this!
            data = data.method_returned;

            $scope.flags.checkingConnection = false;
            $scope.data = data;

            if ((!data) || (data && !data.connected)) {
                $scope.resetExtras();
            }

        }).error(function(data) {

            // TODO: remove this!
            data = data.method_returned;

            $scope.resetExtras();
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

        remoteArduino.callArduinoMethod('connect', serial_port).success(function(data) {

            // TODO: remove this!
            data = data.method_returned;

            $scope.flags.checkingConnection = false;
            $scope.flags.connecting = false;
            $scope.data = data;

        }).error(function(data) {

            // TODO: remove this!
            data = data.method_returned;

            $scope.flags.checkingConnection = false;
            $scope.flags.connecting = false;
            $scope.data = {};

        });
    };

    $scope.disconnectArduino = function(serial_port) {
        $scope.resetExtras();

        remoteArduino.callArduinoMethod('disconnect').success(function(data) {

            // TODO: remove this!
            data = data.method_returned;

            $scope.flags.checkingConnection = false;
            $scope.data = data;

        }).error(function(data) {

            // TODO: remove this!
            data = data.method_returned;

            $scope.flags.checkingConnection = false;
            $scope.data = {};

        });
    };

};
