PyArduinoProxy = function($) {
	
	function _f(somevar) { if(somevar == undefined) return {}; else return somevar; }
	
	var jsExceptions = false;
	
	var init = function() {
		
		//
		// Initialize all the variables used by the module.
		//
		
		$('body').data('py-arduino-proxy', {});
		
		// Get avrCpuType
		$.ajax({
		  url: '/get_avr_cpu_type',
		  dataType: 'json',
		  async: false,
		  success: function(data, textStatus, jqXHR) {
			  if(data.ok) {
				  $('body').data('py-arduino-proxy')['avrCpuType'] = data.avrCpuType;
			  } else {
				  $('body').data('py-arduino-proxy')['avrCpuType'] = 'UNKNOWN';
			  }
		  }
		});
	
		// Get arduino_type_struct
		$.ajax({
		  url: '/get_arduino_type_struct',
		  dataType: 'json',
		  async: false,
		  success: function(data, textStatus, jqXHR) {
			  if(data.ok) {
				  $('body').data('py-arduino-proxy')['arduino_type_struct'] = data.arduinoTypeStruct;
			  } else {
				  $('body').data('py-arduino-proxy')['arduino_type_struct'] = {};
			  }
		  }
		});
		
		// Setup variables
		$('body').data('py-arduino-proxy')['digital_pin_mode'] = {};
		
		var i = 0;
		for (i=0; i<$('body').data('py-arduino-proxy')['arduino_type_struct']['digital_pins']; i++) {
			$('body').data('py-arduino-proxy')['digital_pin_mode'][i] = 'disabled';
		}
		
	};

	//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	// Returns the global 'data' dict
	//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	
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
		var ajax_data = null;
		
		var hardcoded_settings = {
			url: '/pin_mode/?pin=' + pin + '&mode=' + mode,
			dataType: 'json',
			async: false,
			success: function(data, textStatus, jqXHR) {
				ajax_data = data;
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
			if(jsExceptions && !retValue) {
				if(ajax_data.exception) throw new Error(ajax_data.exception);
				if(ajax_data.error) throw new Error(ajax_data.error);
				throw new Error("Error detected while executing pinMode().");
			}
			return retValue;
		} else {
			if(jsExceptions)
				throw new Error("pinMode(): invalid mode: " + mode);
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
		var ajax_data = null;
		
		var hardcoded_settings = {
			url: '/digital_write/?pin=' + pin + '&value=' + value,
			dataType: 'json',
			async: false,
			success: function(data, textStatus, jqXHR) {
				ajax_data = data;
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
		if(jsExceptions && !retValue) {
			if(ajax_data.exception) throw new Error(ajax_data.exception);
			if(ajax_data.error) throw new Error(ajax_data.error);
			throw new Error("Error detected executing digitalWrite().");
		}
		return retValue;
	}

	var digitalRead = function(pin, extra_settings) {
		
		//
		// Digital Read
		//
		// Returns 0 for 'low', 1 for 'high', -1 if error.
		//
		
		extra_settings = _f(extra_settings);
		var retValue = -1;
		var ajax_data = null;
		
		var hardcoded_settings = {
			url: '/digital_read/?pin=' + pin,
			dataType: 'json',
			async: false,
			success: function(data, textStatus, jqXHR) {
				ajax_data = data;
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
		if(jsExceptions && (retValue == -1)) {
			if(ajax_data.exception) throw new Error(ajax_data.exception);
			if(ajax_data.error) throw new Error(ajax_data.error);
			throw new Error("Error detected while executing digitalRead().");
		}
		
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
		var ajax_data = null;
		
		var hardcoded_settings = {
			url: '/analog_write/?pin=' + pin + '&value=' + value,
			dataType: 'json',
			async: false,
			success: function(data, textStatus, jqXHR) {
				ajax_data = data;
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
		if(jsExceptions && !retValue) {
			if(ajax_data.exception) throw new Error(ajax_data.exception);
			if(ajax_data.error) throw new Error(ajax_data.error);
			throw new Error("Error detected while executing analogWrite().");
		}
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
		var ajax_data = null;
		
		var hardcoded_settings = {
			url: '/ping',
			dataType: 'json',
			async: false,
			success: function(data, textStatus, jqXHR) {
				ajax_data = data;
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
		if(jsExceptions && !retValue) {
			if(ajax_data.exception) throw new Error(ajax_data.exception);
			if(ajax_data.error) throw new Error(ajax_data.error);
			throw new Error("Error detected while executing ping().");
		}
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
		var ajax_data = null;
		
		var hardcoded_settings = {
			url: '/validate_connection',
			dataType: 'json',
			async: false,
			success: function(data, textStatus, jqXHR) {
				ajax_data = data;
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
		if(jsExceptions && retValue === false) {
			if(ajax_data.exception) throw new Error(ajax_data.exception);
			if(ajax_data.error) throw new Error(ajax_data.error);
			throw new Error("Error detected while executing validateConnection().");
		}
		return retValue;

	}
	
	var close = function(extra_settings) {
		
		//
		// close the proxy
		//
		
		extra_settings = _f(extra_settings);
		var retValue = false;
		var ajax_data = null;
		
		var hardcoded_settings = {
			url: '/close',
			dataType: 'json',
			async: false,
			success: function(data, textStatus, jqXHR) {
				ajax_data = data;
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
		if(jsExceptions && !retValue) {
			if(ajax_data.exception) throw new Error(ajax_data.exception);
			if(ajax_data.error) throw new Error(ajax_data.error);
			throw new Error("Error detected while executing close().");
		}
		return retValue;
	}
	
	var enableJsExceptions = function() {
		jsExceptions = true;
	}
	
	var disableJsExceptions = function() {
		jsExceptions = false;
	}
	
	return {
		init: init,
		globalData: globalData,
		enableJsExceptions: enableJsExceptions,
		disableJsExceptions: disableJsExceptions,
		close: close,
		pinMode: pinMode,
		digitalWrite: digitalWrite,
		digitalRead: digitalRead,
		analogWrite: analogWrite,
		validateConnection: validateConnection,
		ping: ping
	};
	
}(jQuery);
