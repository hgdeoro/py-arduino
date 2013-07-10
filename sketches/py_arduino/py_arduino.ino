
//
// THIS FILE WAS GENERATED AUTOMATICALLY on 2013-07-10 01:16:39.227545
// WITH 'sketches/generate_sketch.py'
// WHICH IS PART OF THE PROJECT "py-arduino"
//


#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <inttypes.h>

#include "avr_cpunames.h"

#include "py_arduino.h"
#include "arduino_type.h"

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// MAX_RECEIVED_PARAMETERS: max count of parameter received from Serial.
// The first parameter is the function name to execute.

#define MAX_RECEIVED_PARAMETERS 10

char* received_parameters[MAX_RECEIVED_PARAMETERS] = { 0 };

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Size of temporal array for storing each of the parameters
// received from Serial. This limit the max. length that a
// parameter may have.

#define TEMPORARY_ARRAY_SIZE 24

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Interrupts

// >>>>>>>>>>>>>>>>>>>> PLACEHOLDER <<<<<<<<<<<<<<<<<<<<
#define ATTACH_INTERRUPT_MODE_LOW 'L' // {***PLACEHOLDER***}
// >>>>>>>>>>>>>>>>>>>> PLACEHOLDER <<<<<<<<<<<<<<<<<<<<
#define ATTACH_INTERRUPT_MODE_CHANGE 'C' // {***PLACEHOLDER***}
// >>>>>>>>>>>>>>>>>>>> PLACEHOLDER <<<<<<<<<<<<<<<<<<<<
#define ATTACH_INTERRUPT_MODE_RISING 'R' // {***PLACEHOLDER***}
// >>>>>>>>>>>>>>>>>>>> PLACEHOLDER <<<<<<<<<<<<<<<<<<<<
#define ATTACH_INTERRUPT_MODE_FALLING 'F' // {***PLACEHOLDER***}

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Dynamically generated headers inclusions

// >>>>>>>>>>>>>>>>>>>> PLACEHOLDER <<<<<<<<<<<<<<<<<<<<

// headers for dht11_read()

#include "dht11.h"


// headers for ds18x20_read()

#include "OneWire.h"


// headers for lcdWrite()

// If you want to disable LCD support once the sketch file is generated,
// you can define PY_ARDUINO_LCD_SUPPORT = 0
#define PY_ARDUINO_LCD_SUPPORT 1

#if PY_ARDUINO_LCD_SUPPORT == 1
    #include <LiquidCrystal.h>
    #define PY_ARDUINO_LCD_SUPPORT_COLS  16
    #define PY_ARDUINO_LCD_SUPPORT_ROWS   2
    #define PY_ARDUINO_LCD_SUPPORT_rs     7
    #define PY_ARDUINO_LCD_SUPPORT_enable 6
    #define PY_ARDUINO_LCD_SUPPORT_d4     5
    #define PY_ARDUINO_LCD_SUPPORT_d5     4
    #define PY_ARDUINO_LCD_SUPPORT_d6     3
    #define PY_ARDUINO_LCD_SUPPORT_d7     2
#endif

 // {***PLACEHOLDER***}

volatile uint8_t detected_interrupts = 0x00;

void set_mark_interrupt_0() { detected_interrupts = detected_interrupts | 0x01; }
void set_mark_interrupt_1() { detected_interrupts = detected_interrupts | 0x02; }

void clear_mark_interrupt_0() { detected_interrupts = detected_interrupts & (~0x01); }
void clear_mark_interrupt_1() { detected_interrupts = detected_interrupts & (~0x02); }

uint8_t check_mark_interrupt_0() { return detected_interrupts & 0x01; }
uint8_t check_mark_interrupt_1() { return detected_interrupts & 0x02; }

uint8_t debug_enabled = 0;

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Dynamically generated global variables

// >>>>>>>>>>>>>>>>>>>> PLACEHOLDER <<<<<<<<<<<<<<<<<<<<

// globals for lcdWrite()

#if PY_ARDUINO_LCD_SUPPORT == 1
    LiquidCrystal lcd = LiquidCrystal(
        PY_ARDUINO_LCD_SUPPORT_rs,
        PY_ARDUINO_LCD_SUPPORT_enable,
        PY_ARDUINO_LCD_SUPPORT_d4,
        PY_ARDUINO_LCD_SUPPORT_d5,
        PY_ARDUINO_LCD_SUPPORT_d6,
        PY_ARDUINO_LCD_SUPPORT_d7
    );
#endif

 // {***PLACEHOLDER***}

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Dynamically generated source of functions

// >>>>>>>>>>>>>>>>>>>> PLACEHOLDER <<<<<<<<<<<<<<<<<<<<
	
// sources for analogRead()

void _aRd() {
    int pin = atoi(received_parameters[1]);
    int value = analogRead(pin);
    send_int_response(value);
    return;
}


// sources for analogWrite()

void _aWrt() {
    int pin = atoi(received_parameters[1]);
    int value = atoi(received_parameters[2]);

    if(value < 0 || value > 255) {
        send_invalid_parameter_response(1); // received_parameters[2]
        return;
    }

    analogWrite(pin, value);
    send_char_array_response("AW_OK");
}


// sources for delay()

void _dy() {
    int value = atoi(received_parameters[1]);

    if(value < 0) {
        send_invalid_parameter_response(0); // received_parameters[1]
        return;
    }

    delay(value);
    send_char_array_response("D_OK");
}


// sources for delayMicroseconds()

void _dMs() {
    int value = atoi(received_parameters[1]);

    if(value < 0) {
        send_invalid_parameter_response(0); // received_parameters[1]
        return;
    }

    delayMicroseconds(value);
    send_char_array_response("DMS_OK");
}


// sources for dht11_read()

void _dht11Rd() {
    int pin = atoi(received_parameters[1]);
    dht11 DHT11;
    int checksum_ok = DHT11.read(pin);
    switch (checksum_ok)
    {
        case DHTLIB_OK:
            Serial.print("DHTLIB_OK,");
            break;
        case DHTLIB_ERROR_CHECKSUM:
            send_char_array_response("DHTLIB_ERROR_CHECKSUM");
            return;
        case DHTLIB_ERROR_TIMEOUT:
            send_char_array_response("DHTLIB_ERROR_TIMEOUT");
            return;
        default:
            send_char_array_response("DHTLIB_UNKNOWN_ERROR");
            return;
    }
    Serial.print(DHT11.temperature);
    Serial.print(",");
    Serial.print(DHT11.humidity);
    Serial.print("\n");
    return;
}


// sources for digitalRead()

void _dRd() {
    int pin = atoi(received_parameters[1]);
    int value = digitalRead(pin);
    send_int_response(value);
    return;
}


// sources for digitalWrite()

void _dWrt() {
    int pin = atoi(received_parameters[1]);
    int value = atoi(received_parameters[2]);

    if(value != HIGH && value != LOW) {
        send_invalid_parameter_response(1); // received_parameters[2]
        return;
    }

    digitalWrite(pin, value);
    send_char_array_response("DW_OK");
}


// sources for disableDebug()

void _dD() {
    debug_enabled = 0;
    send_char_array_response("DIS");
}


// sources for ds18x20_read()

void _ds18x20Rd()
{
    int pin = atoi(received_parameters[1]);
    OneWire ds(pin);
    byte i;
    byte present = 0;
    byte type_s;
    byte data[12];
    byte addr[8];

    if ( !ds.search(addr))
    {
        send_char_array_response("DS18X20_NO_MORE_ADDRESSES");
        return;
    }

    if (OneWire::crc8(addr, 7) != addr[7])
    {
        send_char_array_response("DS18X20_CRC_INVALID");
        return;
    }

    // the first ROM byte indicates which chip
    switch (addr[0])
    {
        case 0x10:
            type_s = 1;
            break;
        case 0x28:
            type_s = 0;
            break;
        case 0x22:
            type_s = 0;
            break;
        default:
            send_char_array_response("DS18X20_DEVICE_NOT_OF_FAMILY");
            return;
    }

    ds.reset();
    ds.select(addr);
    ds.write(0x44, 1); // start conversion, with parasite power on at the end

    delay(1000);     // maybe 750ms is enough, maybe not
    // we might do a ds.depower() here, but the reset will take care of it.

    present = ds.reset();
    ds.select(addr);
    ds.write(0xBE); // Read Scratchpad

    for ( i = 0; i < 9; i++) {           // we need 9 bytes
        data[i] = ds.read();
    }

    // Convert the data to actual temperature
    // because the result is a 16 bit signed integer, it should
    // be stored to an "int16_t" type, which is always 16 bits
    // even when compiled on a 32 bit processor.
    int16_t raw = (data[1] << 8) | data[0];
    if (type_s) {
        raw = raw << 3; // 9 bit resolution default
        if (data[7] == 0x10) {
            // "count remain" gives full 12 bit resolution
            raw = (raw & 0xFFF0) + 12 - data[6];
        }
    } else {
        byte cfg = (data[4] & 0x60);
        // at lower res, the low bits are undefined, so let's zero them
        if (cfg == 0x00) raw = raw & ~7;  // 9 bit resolution, 93.75 ms
        else if (cfg == 0x20) raw = raw & ~3; // 10 bit res, 187.5 ms
        else if (cfg == 0x40) raw = raw & ~1; // 11 bit res, 375 ms
        //// default is 12 bit resolution, 750 ms conversion time
    }
    Serial.print("DS18X20_OK,");
    Serial.print(raw);
    Serial.print("\n");
    return;

    //celsius = (float)raw / 16.0;
    //fahrenheit = celsius * 1.8 + 32.0;
}


// sources for enableDebug()

void _eD() {
    debug_enabled = 1;
    send_char_array_response("ENA");
}


// sources for enableDebugToLcd()

void _eDL() {
    #if PY_ARDUINO_LCD_SUPPORT == 1
        debug_enabled = 2;
        send_char_array_response("ENA");
    #else
        send_unsupported_cmd_response();
    #endif
}


// sources for getArduinoTypeStruct()

void _gATS() {
    Serial.print(this_arduino_type.analog_pins, DEC);
    Serial.print(" ");
    Serial.print(this_arduino_type.digital_pins, DEC);
    Serial.print(" ");
    Serial.print(this_arduino_type.pwm_pins_bitmap, BIN);
    Serial.print(" ");
    Serial.print(this_arduino_type.eeprom_size, DEC);
    Serial.print(" ");
    Serial.print(this_arduino_type.flash_size, DEC);
    Serial.print(" ");
    Serial.print(this_arduino_type.ram_size, DEC);
    Serial.print("\n");
}


// sources for getAvrCpuType()

void _gACT() {
    send_char_array_response(_AVR_CPU_NAME_);
}


// sources for getFreeMemory()

void _gFM() {
    send_int_response(freeMemory());
}


// sources for getInterruptMark()

void _gIM() {
    int interrupt = atoi(received_parameters[1]);
    if (interrupt == 0) {
        if(check_mark_interrupt_0()) {
            clear_mark_interrupt_0();
            send_char_array_response("GIM_ON");
        } else {
            send_char_array_response("GIM_OFF");
        }
        return;
    } else if (interrupt == 1) {
        if(check_mark_interrupt_1()) {
            clear_mark_interrupt_1();
            send_char_array_response("GIM_ON");
        } else {
            send_char_array_response("GIM_OFF");
        }
        return;
    } else {
        send_invalid_parameter_response(0); // received_parameters[1]
        return;
    }
}


// sources for lcdClear()

void _lcdClr() {
    #if PY_ARDUINO_LCD_SUPPORT == 1
        lcd.clear();
        send_char_array_response("LCLROK");
    #else
        send_unsupported_cmd_response();
    #endif
}


// sources for lcdWrite()

void _lcdW() {
    #if PY_ARDUINO_LCD_SUPPORT == 1
        int col = atoi(received_parameters[1]);
        int row = atoi(received_parameters[2]);
        lcd.setCursor(col, row);
        // reuse 'col' variable
        for(col=3; col<MAX_RECEIVED_PARAMETERS; col++) {
            if(received_parameters[col] == NULL)
                break;
            lcd.print(received_parameters[col]);
            if(col+1<MAX_RECEIVED_PARAMETERS && received_parameters[col+1] != NULL) {
                lcd.print(" ");
            }
        }
        send_char_array_response("LWOK");
    #else
        send_unsupported_cmd_response();
    #endif
}


// sources for micros()

void _mc() {
    send_debug();
    Serial.print(micros());
    Serial.print("\n");
}


// sources for millis()

void _ms() {
    send_debug();
    Serial.print(millis());
    Serial.print("\n");
}


// sources for pinMode()

void _pMd() {
    int pin = atoi(received_parameters[1]);
    int mode = atoi(received_parameters[2]);
    if(mode != INPUT && mode != OUTPUT) {
        send_invalid_parameter_response(1); // received_parameters[2]
        return;
    }
    // FIXME: validate pin
    pinMode(pin, mode);
    send_char_array_response("PM_OK");
}


// sources for ping()

void _ping() {
    send_char_array_response("PING_OK");
}


// sources for shiftOut()

void _sftO() {
    int dataPin = atoi(received_parameters[1]);
    int clockPin = atoi(received_parameters[2]);
    int bitOrder = atoi(received_parameters[3]);
    int value = atoi(received_parameters[4]);
    shiftOut(dataPin, clockPin, bitOrder, value);
    send_char_array_response("SOOK");
}


// sources for streamingAnalogRead()

void _strAR() {
    int pin = atoi(received_parameters[1]);
    int count = atoi(received_parameters[2]);
    int value;
    int i;
    for(i=0; i<count; i++) {
        value = analogRead(pin);
        send_int_response(value);
    }
    send_char_array_response("SR_OK"); // streaming read ok
}


// sources for streamingDigitalRead()

void _strDR() {
    int pin = atoi(received_parameters[1]);
    int count = atoi(received_parameters[2]);
    int value;
    int i;
    for(i=0; i<count; i++) {
        int value = digitalRead(pin);
        send_int_response(value);
    }
    send_char_array_response("SR_OK"); // streaming read ok
}


// sources for validateConnection()

void _vCnt() {
    send_char_array_response(received_parameters[1]);
}


// sources for watchInterrupt()

void _wI() {
    int mode;
    if(received_parameters[2][0] == ATTACH_INTERRUPT_MODE_LOW) {
        mode = LOW;
    } else if(received_parameters[2][0] == ATTACH_INTERRUPT_MODE_CHANGE) {
        mode = CHANGE;
    } else if(received_parameters[2][0] == ATTACH_INTERRUPT_MODE_RISING) {
        mode = RISING;
    } else if(received_parameters[2][0] == ATTACH_INTERRUPT_MODE_FALLING) {
        mode = FALLING;
    } else {
        send_invalid_parameter_response(1); // received_parameters[2]
        return;
    }
    int interrupt = atoi(received_parameters[1]);
    if (interrupt == 0) {
        attachInterrupt(interrupt, set_mark_interrupt_0, mode);
        send_char_array_response("WI_OK");
    } else if (interrupt == 1) {
        attachInterrupt(interrupt, set_mark_interrupt_1, mode);
        send_char_array_response("WI_OK");
    } else {
        send_invalid_parameter_response(0); // received_parameters[1]
        return;
    }
}

 // {***PLACEHOLDER***}
	
	// PROXIED_FUNCTION_COUNT: how many proxied functions we have
// >>>>>>>>>>>>>>>>>>>> PLACEHOLDER <<<<<<<<<<<<<<<<<<<<
	#define PROXIED_FUNCTION_COUNT 26 // {***PLACEHOLDER***}
	
// >>>>>>>>>>>>>>>>>>>> PLACEHOLDER <<<<<<<<<<<<<<<<<<<<
	proxied_function_ptr function_ptr[PROXIED_FUNCTION_COUNT] = { _aRd, _aWrt, _dy, _dMs, _dht11Rd, _dRd, _dWrt, _dD, _ds18x20Rd, _eD, _eDL, _gATS, _gACT, _gFM, _gIM, _lcdClr, _lcdW, _mc, _ms, _pMd, _ping, _sftO, _strAR, _strDR, _vCnt, _wI,  }; // {***PLACEHOLDER***}
// >>>>>>>>>>>>>>>>>>>> PLACEHOLDER <<<<<<<<<<<<<<<<<<<<
	char*               function_name[PROXIED_FUNCTION_COUNT] = { "_aRd", "_aWrt", "_dy", "_dMs", "_dht11Rd", "_dRd", "_dWrt", "_dD", "_ds18x20Rd", "_eD", "_eDL", "_gATS", "_gACT", "_gFM", "_gIM", "_lcdClr", "_lcdW", "_mc", "_ms", "_pMd", "_ping", "_sftO", "_strAR", "_strDR", "_vCnt", "_wI",  }; // {***PLACEHOLDER***}
	
	#define read_char() Serial.read()
	
	void setup_serial() {
// >>>>>>>>>>>>>>>>>>>> PLACEHOLDER <<<<<<<<<<<<<<<<<<<<
		Serial.begin(9600); // {***PLACEHOLDER***}
	}

	void send_int_response(int value) {
		Serial.print(value, DEC);
		Serial.print("\n");
	}
	
	// param_num: which parameter is invalid. Starts with '0'.
	// received_parameters[1] -> '0'
	// received_parameters[2] -> '1'
	// received_parameters[3] -> '2'
	void send_invalid_parameter_response(int param_num) {
// >>>>>>>>>>>>>>>>>>>> PLACEHOLDER <<<<<<<<<<<<<<<<<<<<
		Serial.print("INVALID_PARAMETER "); // {***PLACEHOLDER***}
		Serial.print(param_num, DEC);
		Serial.print("\n");
	}
	
	// error_code == 0 -> UNKNOWN ERROR CORE or WITHOUT ERROR CODE
	void send_invalid_cmd_response(int error_code) {
// >>>>>>>>>>>>>>>>>>>> PLACEHOLDER <<<<<<<<<<<<<<<<<<<<
		Serial.print("INVALID_CMD "); // {***PLACEHOLDER***}
		Serial.print(error_code, DEC);
		Serial.print("\n");
	}

	// Inform that the command is not supported.
	// This is used in LCD commands, to report that the command existed,
	// but it's unsupported because the sktech was generated with NO
	// support for LCDs.
	void send_unsupported_cmd_response() {
// >>>>>>>>>>>>>>>>>>>> PLACEHOLDER <<<<<<<<<<<<<<<<<<<<
		Serial.print("UNSUPPORTED_CMD "); // {***PLACEHOLDER***}
		Serial.print(received_parameters[0]); // The command
		Serial.print("\n");
	}
	
	void send_ok_response() {
		Serial.print("OK");
		Serial.print("\n");
	}
	
	void send_char_array_response(char* response) {
		Serial.print(response);
		Serial.print("\n");
	}
	
	void send_debug() {
		if(debug_enabled == 0) return;
		int i;
		for(i=0; i<MAX_RECEIVED_PARAMETERS; i++) {
					Serial.print("> received_parameters[");
					Serial.print(i);
					Serial.print("] -> ");
			if(received_parameters[i] != NULL) {
						Serial.print(received_parameters[i]);
						Serial.print("\n");
			} else {
						Serial.print("null");
						Serial.print("\n");
					}
		}
	}
	
// Define all the possible return values. This is used as a 'code' for
// reporing errors to python.

#define RETURN_OK												0
#define READ_ONE_PARAM_NEW_LINE_FOUND							7
#define READ_ONE_PARAM_EMPTY_RESPONSE 							1
#define READ_ONE_PARAM_ERROR_PARAMETER_TOO_LARGE 				2
#define READ_PARAMETERS_ERROR_TOO_MANY_PARAMETERS 				3
#define UNEXPECTED_RESPONSE_FROM_READ_ONE_PARAM					4
#define UNEXPECTED_RESPONSE_FROM_READ_PARAMETERS				5
#define FUNCTION_NOT_FOUND										6

extern unsigned int __bss_end;
extern unsigned int __heap_start;
extern void *__brkval;

int freeMemory() {
  int free_memory;

  if((int)__brkval == 0)
     free_memory = ((int)&free_memory) - ((int)&__bss_end);
  else
    free_memory = ((int)&free_memory) - ((int)__brkval);

  return free_memory;
}

//
// Read one parameter from serial and store it in the 'tmp_array'.
//
// Parameters:
// * tmp_array: where to store the chars read from serial.
//
// Returns:
// * RETURN_OK a complete parameter was read.
// * READ_ONE_PARAM_EMPTY_RESPONSE no parameter was read, because
//		nothing was received when read() the serial connection.
// * READ_ONE_PARAM_ERROR_PARAMETER_TOO_LARGE a parameter was read,
//    	but larger than the buffer. (TEMPORARY_ARRAY_SIZE)
//

uint8_t read_one_param(char* tmp_array) {
	
	int incomingByte;
	int pos = 0;
	while (pos < (TEMPORARY_ARRAY_SIZE-1)) {

		incomingByte = read_char();
		if(incomingByte == -1) {
			// no data
			if(pos == 0 && received_parameters[0] == NULL) {
				// return 0 and let Arduino run other tasks
				// instead of waiting with delay().
				return READ_ONE_PARAM_EMPTY_RESPONSE;
			}
			
			// TODO: test this situation, sending 1 character at a time,
			// and waiting between each character sent.
			
			continue;
		}

		// "\t" == 9 -> got a tab
		if(incomingByte == 9) {
			if(pos == 0) {
				// Ignore leading tabs chars
				continue;
			}
			// got a tab! mark end of string and return
			tmp_array[pos] = 0x00;
			return RETURN_OK;
		}
		
		// "\\n" == 10 -> we've reached end of the command
		if(incomingByte == 10) {
			tmp_array[pos] = 0x00; // mark end of string
			return READ_ONE_PARAM_NEW_LINE_FOUND;
		}

		tmp_array[pos++] = incomingByte;

	} // while
	
	// The tmp_array is full. Some character don't fit-in it, and will
	//  be lost!

	// pos == (TEMPORARY_ARRAY_SIZE-1)
	tmp_array[pos] = 0x00; // mark end of string
	
	return READ_ONE_PARAM_ERROR_PARAMETER_TOO_LARGE;
}

//
// Read parameters from serial and store them in received_parameters.
//
// Returns:
// * RETURN_OK all the parameters were read.
// * READ_ONE_PARAM_EMPTY_RESPONSE no parameter was read.
// * READ_ONE_PARAM_ERROR_PARAMETER_TOO_LARGE: a parameter was larger
//			than the permitted. (TEMPORARY_ARRAY_SIZE)
// * READ_PARAMETERS_ERROR_TOO_MANY_PARAMETERS: found more parameters
//			than the permitted. (MAX_RECEIVED_PARAMETERS)
//

uint8_t read_parameters() {
	
	static char tmp_array[TEMPORARY_ARRAY_SIZE];
	
	// Reset 'received_parameters', only if wasn't done earlier...
	if(received_parameters[0] != NULL) {
		int i;
		for(i=0; i<MAX_RECEIVED_PARAMETERS; i++) {
			if(received_parameters[i] != NULL) {
				free(received_parameters[i]); // free
				received_parameters[i] = NULL; // reset
			} else {
				// we can suppose that if this is NULL, the others will
				// be NULL
				break;
			}
		}
	}
	
	int param_index = 0;
	
	for(param_index=0; param_index<MAX_RECEIVED_PARAMETERS;) {
		
		tmp_array[0] = 0x00;
		uint8_t read_status = read_one_param(tmp_array);
		
		if(read_status == RETURN_OK || read_status == READ_ONE_PARAM_NEW_LINE_FOUND) {
			
			if(tmp_array[0] != 0x00) {
				received_parameters[param_index] = (char*) malloc(strlen(tmp_array)+1);
				strcpy(received_parameters[param_index++], &tmp_array[0]);
			}

			if(read_status == RETURN_OK) {
				continue;
			} else {
				return RETURN_OK;
			}
			
			
		} else if(read_status == READ_ONE_PARAM_EMPTY_RESPONSE) {
			if(param_index == 0) {
				// nothing was read, and we are NOT in the middle of a command
				return READ_ONE_PARAM_EMPTY_RESPONSE;
			} else {
				// we are in the middle of something... try again and again...
				continue;
			}
			
		} else if(read_status == READ_ONE_PARAM_ERROR_PARAMETER_TOO_LARGE) {
			// the parameter is larger that the admited.
			while(read_char() != 10); // 10 == '\n'
			return READ_ONE_PARAM_ERROR_PARAMETER_TOO_LARGE;
			
		} else {
			return UNEXPECTED_RESPONSE_FROM_READ_ONE_PARAM;
		}
	}
	
	// Al the 'received_parameters' were used!
	while(read_char() != 10); // 10 == '\n'
	return READ_PARAMETERS_ERROR_TOO_MANY_PARAMETERS;

}

proxied_function_ptr get_function_by_name(char* name) {
	int i;
	for(i=0; i<PROXIED_FUNCTION_COUNT; i++) {
		if(strcmp(name, function_name[i]) == 0) {
			return function_ptr[i];
		}
	}
	return NULL;
}

void setup() {

	setup_serial();

	// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	// Dynamically generated code to execute on setup()

// >>>>>>>>>>>>>>>>>>>> PLACEHOLDER <<<<<<<<<<<<<<<<<<<<
	
// setup code for lcdWrite()

#if PY_ARDUINO_LCD_SUPPORT == 1
    lcd.begin(
        PY_ARDUINO_LCD_SUPPORT_COLS,
        PY_ARDUINO_LCD_SUPPORT_ROWS
    );
    lcd.clear();
    lcd.print("PyArduino");
    lcd.setCursor(0, 1); // column, line
    lcd.print("READY!");
#endif

 // {***PLACEHOLDER***}

}

void loop() {
	uint8_t ret = read_parameters();
	
	if(ret == RETURN_OK) {
		send_debug();
		proxied_function_ptr function = get_function_by_name(received_parameters[0]);
		if(function != NULL) {
			
			(function)();
			
		} else {
			send_invalid_cmd_response(FUNCTION_NOT_FOUND);
			
		}
	} else if(ret == READ_ONE_PARAM_EMPTY_RESPONSE) {
		delay(10);
	} else if(ret == READ_ONE_PARAM_ERROR_PARAMETER_TOO_LARGE
		|| ret == READ_PARAMETERS_ERROR_TOO_MANY_PARAMETERS) {
		send_debug();
		send_invalid_cmd_response(ret);
		
	} else {
		send_debug();
		send_invalid_cmd_response(UNEXPECTED_RESPONSE_FROM_READ_PARAMETERS);
	}
}
