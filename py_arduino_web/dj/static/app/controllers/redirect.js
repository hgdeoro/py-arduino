function RedirectController($scope, $http, $location) {

    $scope.doRedirect = function() {
        $http.post($scope.CONST.check_connection_url, {

        }).success(function(data) {
            if (data.connected) {
                $location.path("/pins");
            } else {
                $location.path("/connection");
            }

        }).error(function(data) {
            $location.path("/connection");

        });
    };

};
