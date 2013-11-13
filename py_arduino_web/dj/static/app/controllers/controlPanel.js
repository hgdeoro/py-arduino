function ControlPanelController($scope, $http, $location, $interval, $route, $templateCache) {

    var control_panel_code_url = '/renderControlPanel/';

    $scope.enableAceEditor = function() {
        
        // Remove from cache
        $templateCache.remove('/renderControlPanel/');

        $scope.aceEditor = ace.edit("editor");
        $scope.aceEditor.setTheme("ace/theme/twilight");
        $scope.aceEditor.getSession().setMode("ace/mode/html");
        
        $http.get(control_panel_code_url).success(function(data) {
            $scope.aceEditor.setValue(data);

        }).error(function(data) {
            console.error("enableAceEditor() -> $http.get() -> ERROR -> " + data);

        });

    };
    
    $scope.saveControlPanelCode = function() {
        // console.info("To save: " + $scope.aceEditor.getValue());

        $http.post(control_panel_code_url, {
            code : $scope.aceEditor.getValue()

        }).success(function(data) {
            $route.reload();

        }).error(function(data) {
            console.error("saveControlPanelCode() -> $http.post() -> ERROR -> " + data);
        });

        
    };

};
