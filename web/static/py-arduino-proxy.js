PyArduinoProxy = function($) {
	
	//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	// Returns the 'data' dict
	//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	
	function _f(somevar) { if(somevar == undefined) return {}; else return somevar; }

	var globalData = function() {
		//
		// Returns the global data holder
		//
		
		return $('body').data('py-arduino-proxy');
	};
	
	var pinMode = function(pin, mode, extra_settings) {
		
		//
		// Sets the pin mode
		//
		// Returns 'true' if pinMode() could be done. 'false' in case of error.
		//
		
		extra_settings = _f(extra_settings);
		var retValue = false;
		
		var hardcoded_settings = {
			url: '/pin_mode/?pin=' + pin + '&mode=' + mode,
			dataType: 'json',
			async: false,
			success: function(data, textStatus, jqXHR) {
				if(data.ok) {
					globalData()['digital_pin_mode'][pin] = mode;
					retValue = true;
				} else {
					retValue = false;
				}
				if('success' in extra_settings)
					extra_settings.success(data, textStatus, jqXHR);
			},
			error: function(jqXHR, textStatus, errorThrown) {
				retValue = false;
				if('error' in extra_settings)
					extra_settings.error(jqXHR, textStatus, errorThrown);
			}
		};
		
		var settings = $.extend({}, extra_settings, hardcoded_settings);

		if(mode == 'disabled') {
			globalData()['digital_pin_mode'][pin] = 'disabled';
			return true;
		} else if(mode == 'input' || mode == 'output') {
			$.ajax(settings);
			return retValue;
		} else {
			// TODO: INVALID MODE - raise exception or show message
			return false;
		}
	};

	var digitalWrite = function(pin, value, extra_settings) {
		
		//
		// Digital Write
		//
		// Returns 'true' if digitalWrite() could be done. 'false' in case of error.
		//
		
		extra_settings = _f(extra_settings);
		var retValue = false;
		
		var hardcoded_settings = {
			url: '/digital_write/?pin=' + pin + '&value=' + value,
			dataType: 'json',
			async: false,
			success: function(data, textStatus, jqXHR) {
				if(data.ok) {
					retValue = true;
				} else {
					retValue = false;
				}
				if('success' in extra_settings)
					extra_settings.success(data, textStatus, jqXHR);
			},
			error: function(jqXHR, textStatus, errorThrown) {
				retValue = false;
				if('error' in extra_settings)
					extra_settings.error(jqXHR, textStatus, errorThrown);
			}
		}
		
		var settings = $.extend({}, extra_settings, hardcoded_settings);

		if (value == 'low' || value == 'high') {
			$.ajax(settings);
			return retValue;
		} else {
			return false;
		}
	}

	var digitalRead = function(pin, extra_settings) {
		
		//
		// Digital Read
		//
		// Returns 0 for 'low', 1 for 'high', -1 if error.
		//
		
		extra_settings = _f(extra_settings);
		var retValue = -1;
		
		var hardcoded_settings = {
			url: '/digital_read/?pin=' + pin,
			dataType: 'json',
			async: false,
			success: function(data, textStatus, jqXHR) {
				if(data.ok) {
					if(data.value == 0 || data.value == 1) {
						retValue = data.value;
					} else {
						retValue = -1;
					}
				} else {
					retValue = -1;
				}
				if('success' in extra_settings)
					extra_settings.success(data, textStatus, jqXHR);
			},
			error: function(jqXHR, textStatus, errorThrown) {
				retValue = -1;
				if('error' in extra_settings)
					extra_settings.error(jqXHR, textStatus, errorThrown);
			}
		}
		
		var settings = $.extend({}, extra_settings, hardcoded_settings);

		$.ajax(settings);
		return retValue;
	}
	
	var analogWrite = function(pin, value, extra_settings) {
		
		//
		// analogWrite()
		//
		// Returns 'true' if analogWrite() could be done. 'false' in case of error.
		//
		
		extra_settings = _f(extra_settings);
		var retValue = false;
		
		var hardcoded_settings = {
			url: '/analog_write/?pin=' + pin + '&value=' + value,
			dataType: 'json',
			async: false,
			success: function(data, textStatus, jqXHR) {
				if(data.ok) {
					retValue = true;
				} else {
					retValue = false;
				}
				if('success' in extra_settings)
					extra_settings.success(data, textStatus, jqXHR);
			},
			error: function(jqXHR, textStatus, errorThrown) {
				retValue = false;
				if('error' in extra_settings)
					extra_settings.error(jqXHR, textStatus, errorThrown);
			}
		}
		
		var settings = $.extend({}, extra_settings, hardcoded_settings);

		$.ajax(settings);
		return retValue;
	}
	
	var ping = function(extra_settings) {
		
		//
		// Ping
		//
		// Returns 'true' if ping() could be done. 'false' in case of error.
		//
		
		extra_settings = _f(extra_settings);
		var retValue = false;
		
		var hardcoded_settings = {
			url: '/ping',
			dataType: 'json',
			async: false,
			success: function(data, textStatus, jqXHR) {
				if(data.ok) {
					retValue = true;
				} else {
					retValue = false;
				}
				if('success' in extra_settings)
					extra_settings.success(data, textStatus, jqXHR);
			},
			error: function(jqXHR, textStatus, errorThrown) {
				retValue = false;
				if('error' in extra_settings)
					extra_settings.error(jqXHR, textStatus, errorThrown);
			}
		}
		
		var settings = $.extend({}, extra_settings, hardcoded_settings);

		$.ajax(settings);
		return retValue;

	}
	
	var validateConnection = function(extra_settings) {
		
		//
		// validateConnection()
		//
		// Returns the random generated number if validateConnection() was done ok,
		//  'false' otherwise.
		//
		
		extra_settings = _f(extra_settings);
		var retValue = false;
		
		var hardcoded_settings = {
			url: '/validate_connection',
			dataType: 'json',
			async: false,
			success: function(data, textStatus, jqXHR) {
				if(data.ok) {
					retValue = data.random_value;
				} else {
					retValue = false;
				}
				if('success' in extra_settings)
					extra_settings.success(data, textStatus, jqXHR);
			},
			error: function(jqXHR, textStatus, errorThrown) {
				retValue = false;
				if('error' in extra_settings)
					extra_settings.error(jqXHR, textStatus, errorThrown);
			}
		}
		
		var settings = $.extend({}, extra_settings, hardcoded_settings);

		$.ajax(settings);
		return retValue;

	}
	
	return {
		globalData: globalData,
		pinMode: pinMode,
		digitalWrite: digitalWrite,
		digitalRead: digitalRead,
		analogWrite: analogWrite,
		validateConnection: validateConnection,
		ping: ping
	};
	
}(jQuery);
