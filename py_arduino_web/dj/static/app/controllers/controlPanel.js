function ControlPanelController($scope, $http, $location, $interval, $route, $templateCache) {

    var control_panel_combined_url = '/control_panel/combined/';
    var control_panel_html_url = '/control_panel/html/';
    var control_panel_js_url = '/control_panel/js/';
    var control_panel_update_url = '/control_panel/update/';

    $scope.enableAceEditor = function() {
        
        // Remove from cache
        $templateCache.remove(control_panel_combined_url);
        $templateCache.remove(control_panel_html_url);
        $templateCache.remove(control_panel_js_url);

        $scope.aceEditorHeader = ace.edit("editor_header");
        $scope.aceEditorHeader.setTheme("ace/theme/twilight");
        $scope.aceEditorHeader.getSession().setMode("ace/mode/html");

        $scope.aceEditorHtml = ace.edit("editor_html");
        $scope.aceEditorHtml.setTheme("ace/theme/twilight");
        $scope.aceEditorHtml.getSession().setMode("ace/mode/html");
        
        $scope.aceEditorJs = ace.edit("editor_js");
        $scope.aceEditorJs.setTheme("ace/theme/twilight");
        $scope.aceEditorJs.getSession().setMode("ace/mode/javascript");
        
        $http.get(control_panel_combined_url).success(function(data) {
            $scope.aceEditorHeader.setValue(data.header);
            $scope.aceEditorHtml.setValue(data.html);
            $scope.aceEditorJs.setValue(data.js);

        }).error(function(data) {
            console.error("enableAceEditor() -> $http.get() -> ERROR -> " + data);

        });

    };
    
    $scope.saveControlPanelCode = function() {
        // console.info("To save: " + $scope.aceEditorHtml.getValue());

        $http.post(control_panel_update_url, {
            header : $scope.aceEditorHeader.getValue(),
            html : $scope.aceEditorHtml.getValue(),
            js : $scope.aceEditorJs.getValue()

        }).success(function(data) {
            $route.reload();

        }).error(function(data) {
            console.error("saveControlPanelCode() -> $http.post() -> ERROR -> " + data);
        });

        
    };

};
