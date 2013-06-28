// Attach 'global' event listener of ajax errors
function attachGlobalAjaxError() {
	// http://api.jquery.com/ajaxError/
	$(document).ajaxError(function(event, request, settings){
        var msg = "A problem occurred when communicating to the server. Url: '" + settings.url + "'";
        // alert(msg);
        simpleLogConsoleLogError(msg);
        // FIXME: remove 'alert' and show the message in the HTML
    });
}

/*
 * Executes ping(). Write result to $("#ping_result").
 */
function ping() {
    $("#ping_result").html('waiting for response...');
    var start = new Date().getTime();
    var value = JsArduino.ping();
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
    var value = JsArduino.validateConnection();
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
    var value = JsArduino.close();
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

/*
 * Simple Log Console
 */
function simpleLogConsoleClear() {
	$("#simple_log_console").html('');
}

function simpleLogConsoleLogInfo(msg) {
	$.tmpl("info_message_template", [{ log_message: msg, date: new Date() }]).appendTo("#simple_log_console");
}

function simpleLogConsoleLogError(msg) {
	$.tmpl("error_message_template", [{ log_message: msg, date: new Date() }]).appendTo("#simple_log_console");
}
