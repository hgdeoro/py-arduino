function ControlPanelController($scope, $http, $location, $interval, $route, $templateCache) {

    var control_panel_code_url = '/renderControlPanel/';

    $scope.enableAceEditor = function() {
        
        // Remove from cache
        $templateCache.remove(control_panel_code_url);

        $scope.aceEditorHtml = ace.edit("editor_html");
        $scope.aceEditorHtml.setTheme("ace/theme/twilight");
        $scope.aceEditorHtml.getSession().setMode("ace/mode/html");
        
        $scope.aceEditorJs = ace.edit("editor_js");
        $scope.aceEditorJs.setTheme("ace/theme/twilight");
        $scope.aceEditorJs.getSession().setMode("ace/mode/javascript");
        
        $http.get(control_panel_code_url).success(function(data) {
            $scope.aceEditorHtml.setValue(data.html);
            $scope.aceEditorJs.setValue(data.js);

        }).error(function(data) {
            console.error("enableAceEditor() -> $http.get() -> ERROR -> " + data);

        });

    };
    
    $scope.saveControlPanelCode = function() {
        // console.info("To save: " + $scope.aceEditorHtml.getValue());

        $http.post(control_panel_code_url, {
            html : $scope.aceEditorHtml.getValue(),
            js : $scope.aceEditorJs.getValue()

        }).success(function(data) {
            $route.reload();

        }).error(function(data) {
            console.error("saveControlPanelCode() -> $http.post() -> ERROR -> " + data);
        });

        
    };

};
