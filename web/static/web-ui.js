// Show an error message at the TOP of the page.
function showErrorMessage(html_msg) {
    $('#error_message_text').html(html_msg);
    $('#error_message_text').append(" <a href='javascript:hideErrorMessages(); return false;'>[hide]</a>");
    $("#error_messages").show();
}

// Show the current (jinja2 rendered) error mesage.
function showCurrentErrorMessage(html_msg) {
    $("#error_messages").show();
}

// Hide the error message.
function hideErrorMessages() {
    $('#error_messages').hide();
}

// Attach 'global' event listener of ajax errors
function attachGlobalAjaxError() {
    $("#error_messages").ajaxError(function(event, request, settings){
        showErrorMessage("<b>Error:</b> a problem occurred when communicating to the server. Url: '" + settings.url + "'");
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
