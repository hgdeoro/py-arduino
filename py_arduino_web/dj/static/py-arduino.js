//-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
//    py-arduino - Access your Arduino from Python
//    Copyright (C) 2011-2013 - Horacio Guillermo de Oro <hgdeoro@gmail.com>
//
//    This file is part of py-arduino.
//
//    py-arduino is free software; you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation version 2.
//
//    py-arduino is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License version 2 for more details.
//
//    You should have received a copy of the GNU General Public License
//    along with py-arduino; see the file LICENSE.txt.
//-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

/*
 * This script defines the variable 'JsArduino', implementing
 * the 'module' pattern. JsArduino is the entry point for
 * interacting to the Python web server, and thus, to the Arduino.
 * 
 * To make it usable, you must call 'JsArduino.init()'.
 * 
 */

var JsArduino = function($) {
	
    /* Returns **somevar** is defined; otherwise, returns an empty dict */
	function _ensure_dict(somevar) { if(somevar == undefined) return {}; else return somevar; }
	
    /*
     * jsExceptions flag, used to enable/disable the reporting of errors
     * using exceptions.
     */
	var jsExceptions = false;
	
    /*
     * Initialize the module, setting private variables and calling
     * the server to get the Arduino type struct.
     */
	var init = function() {
		
		//
		// Initialize all the variables used by the module.
		//
		
		$('body').data('py-arduino', {});
		
		// Get avrCpuType
		$.ajax({
		  url: '/get_avr_cpu_type',
		  dataType: 'json',
		  async: false,
		  success: function(data, textStatus, jqXHR) {
			  if(data.ok) {
				  $('body').data('py-arduino')['avrCpuType'] = data.avrCpuType;
			  } else {
				  $('body').data('py-arduino')['avrCpuType'] = 'UNKNOWN';
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
				  $('body').data('py-arduino')['arduino_type_struct'] = data.arduinoTypeStruct;
			  } else {
				  $('body').data('py-arduino')['arduino_type_struct'] = {};
			  }
		  }
		});
		
		// Setup variables
		$('body').data('py-arduino')['digital_pin_mode'] = {};
		
		var i = 0;
		for (i=0; i<$('body').data('py-arduino')['arduino_type_struct']['digital_pins']; i++) {
			$('body').data('py-arduino')['digital_pin_mode'][i] = 'disabled';
		}
		
	};

    /*
     * Returns the global 'data' dict.
     */
	var globalData = function() {
		//
		// Returns the global data holder
		//
		
		return $('body').data('py-arduino');
	};
	
    /*
     * Returns true if the *pin* supports PWM.
     */
	var pinIsPwm = function(pin) {
		var i;
		var list = globalData()['arduino_type_struct']['pwm_pin_list'];
		for(i=0; i<list.length; i++)
			if(list[i] == pin)
				return true;
		return false;
	};
	
    /*
     * Calls **pinMode()** on Arduino.
     * 
     * Returns 'true' if pinMode() could be done.
     * Returns 'false' in case of error (or raises an exception
     *  if *jsExceptions* is enabled).
     */
	var pinMode = function(pin, mode, extra_settings) {
		extra_settings = _ensure_dict(extra_settings);
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

    /*
     * Calls **digitalWrite()** on Arduino.
     * 
     * Returns 'true' if digitalWrite() could be done.
     * Returns 'false' in case of error (or raises an exception
     *  if *jsExceptions* is enabled).
     */
	var digitalWrite = function(pin, value, extra_settings) {
		extra_settings = _ensure_dict(extra_settings);
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

    /*
     * Calls **digitalRead()** on Arduino.
     * 
     * Returns *0* for 'low', 1 for 'high' if the read went ok.
     * Returns '-1' in case of error (or raises an exception
     *  if *jsExceptions* is enabled).
     */
	var digitalRead = function(pin, extra_settings) {
		extra_settings = _ensure_dict(extra_settings);
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

    /*
     * Calls **analogRead()** on Arduino.
     * 
     * Returns the read value, from *0* to *1023* if the read went ok.
     * Returns '-1' in case of error (or raises an exception
     *  if *jsExceptions* is enabled).
     */
	var analogRead = function(pin, extra_settings) {
		extra_settings = _ensure_dict(extra_settings);
		var retValue = -1;
		var ajax_data = null;
		
		var hardcoded_settings = {
			url: '/analog_read/?pin=' + pin,
			dataType: 'json',
			async: false,
			success: function(data, textStatus, jqXHR) {
				ajax_data = data;
				if(data.ok) {
					if(data.value >= 0 && data.value <= 1023) {
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
			throw new Error("Error detected while executing analogRead().");
		}
		
		return retValue;
	}
	
    /*
     * Calls **analogWrite()** on Arduino.
     * 
     * Returns 'true' if analogWrite() could be done.
     * Returns 'false' in case of error (or raises an exception
     *  if *jsExceptions* is enabled).
     */
	var analogWrite = function(pin, value, extra_settings) {
		extra_settings = _ensure_dict(extra_settings);
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

    /*
     * Calls **delay()** on Arduino.
     * 
     * Returns 'true' if delay() could be done.
     * Returns 'false' in case of error (or raises an exception
     *  if *jsExceptions* is enabled).
     */
	var delay = function(value, extra_settings) {
		extra_settings = _ensure_dict(extra_settings);
		var retValue = false;
		var ajax_data = null;
		
		var hardcoded_settings = {
			url: '/delay/?value=' + value,
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
			throw new Error("Error detected while executing delay().");
		}
		return retValue;
	}
	
    /*
     * ping()
     * 
     * Returns 'true' if ping() could be done.
     * Returns 'false' in case of error (or raises an exception
     *  if *jsExceptions* is enabled).
     */
	var ping = function(extra_settings) {
		extra_settings = _ensure_dict(extra_settings);
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
	
    /*
     * validateConnection()
     * 
     * Returns the random generated number if validateConnection() could be done.
     * Returns 'false' in case of error (or raises an exception
     *  if *jsExceptions* is enabled).
     */
	var validateConnection = function(extra_settings) {
		extra_settings = _ensure_dict(extra_settings);
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
	
    /*
     * close()
     * 
     * Returns 'true' if close() could be done.
     * Returns 'false' in case of error (or raises an exception
     *  if *jsExceptions* is enabled).
     */
	var close = function(extra_settings) {
		extra_settings = _ensure_dict(extra_settings);
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
	
    /*
     * Calls **getFreeMemory()** on Arduino.
     * 
     * Returns the free memory on the Arduino.
     * Returns '-1' in case of error (or raises an exception
     *  if *jsExceptions* is enabled).
     */
	var getFreeMemory = function(extra_settings) {
		extra_settings = _ensure_dict(extra_settings);
		var retValue = -1;
		var ajax_data = null;
		
		var hardcoded_settings = {
			url: '/get_free_memory/',
			dataType: 'json',
			async: false,
			success: function(data, textStatus, jqXHR) {
				ajax_data = data;
				if(data.ok) {
					if(data.freeMemory >= 0) {
						retValue = data.freeMemory;
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
			throw new Error("Error detected while executing getFreeMemory().");
		}
		
		return retValue;
	}
    
    /*
     * enableJsExceptions()
     * 
     * Enables the **jsExceptions** flag.
     * 
     * When the **jsExceptions** flag is enabled, an exception is raised
     * if an error is detected.
     * 
     * When the **jsExceptions** flag is disabled, a special value
     * is returned ('false', '-1', etc.) if an error is detected.
     */
	var enableJsExceptions = function() {
		jsExceptions = true;
	}
	
    /*
     * disableJsExceptions()
     * 
     * Disables the **jsExceptions** flag.
     */
	var disableJsExceptions = function() {
		jsExceptions = false;
	}
	
    /*
     * These are the PUBLIC functions the 'JsArduino' implements.
     */
	return {
		init: init,
		globalData: globalData,
        getFreeMemory: getFreeMemory,
		enableJsExceptions: enableJsExceptions,
		disableJsExceptions: disableJsExceptions,
		pinIsPwm: pinIsPwm,
		close: close,
		delay: delay,
		pinMode: pinMode,
		digitalWrite: digitalWrite,
		digitalRead: digitalRead,
		analogWrite: analogWrite,
		analogRead: analogRead,
		validateConnection: validateConnection,
		ping: ping
	};
	
}(jQuery);
