// Attach 'global' event listener of ajax errors
function attachGlobalAjaxError() {
	// http://api.jquery.com/ajaxError/
	$(document).ajaxError(function(event, request, settings){
        var msg = "<b>Error:</b> a problem occurred when communicating to the server. Url: '" + settings.url + "'";
        alert(msg);
        // FIXME: remove 'alert' and show the message in the HTML
    });
}

/*
 * Executes ping(). Write result to $("#ping_result").
 */
function ping() {
    $("#ping_result").html('waiting for response...');
    var start = new Date().getTime();
    var value = PyArduinoProxy.ping();
    var end = new Date().getTime();
    if(value) {
      $("#ping_result").html('PING OK - ' + (end-start) + ' ms');
    } else {
      $("#ping_result").html('no response');
    }
}

/*
 * Executes validateConnection(). Write result to $("#validate_connection_result").
 */
function validateConnection() {
    $("#validate_connection_result").html('waiting for response...');
    var value = PyArduinoProxy.validateConnection();
    if(value === false) {
        $("#validate_connection_result").html('ERROR');
    } else {
        $("#validate_connection_result").html('validation OK - ID: ' + value);
    }
}

/*
 * Closes proxy and returns to '/' (even if an error is detected).
 * Report errors using alert().
 */
function closeProxy() {
    var value = PyArduinoProxy.close();
    if(value === true) {
        window.location.replace("/");
    } else {
        alert("Error detected when trying to close the proxy.");
        window.location.replace("/");
    }
}

function redirectToMainPage() {
    window.location.replace("/");
}

function redirectToJsPrototyper() {
    window.location.replace("/js_prototyper");
}
