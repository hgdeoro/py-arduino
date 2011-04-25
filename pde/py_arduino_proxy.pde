
//
// THIS FILE IS GENERATED AUTOMATICALLI WITH generate-pde.sh
// WHICH IS PART OF THE PROJECT "PyArduinoProxy"
//
    

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <inttypes.h>

#include "py_arduino_proxy.h"

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// If PY_ARDUINO_PROXY_DEVEL is defined, the generated code
// is targeted to test and develop the sketch in a PC,
// this means the code won't run on Arduino

// #define PY_ARDUINO_PROXY_DEVEL // removed when generating the sketch.

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// MAX_RECEIVED_PARAMETERS: max count of parameter received from Serial.
// The first parameter is the function name to execute.

#define MAX_RECEIVED_PARAMETERS 10

char* received_parameters[MAX_RECEIVED_PARAMETERS] = { 0 };

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Size of temporal array for storing each of the parameters
// received from Serial. This limit the max. length that a
// parameter may have.

#define TEMPORARY_ARRAY_SIZE 64

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Flag setted when a newline was found while reading from Serial.

int new_line_found = 0;

#define PIN_ONBOARD_LED 13  // DIGITAL
#define PIN_START_BUTTON 12 // DIGITAL

#ifndef PY_ARDUINO_PROXY_DEVEL
	
// >>>>>>>>>>>>>>>>>>>> PLACEHOLDER <<<<<<<<<<<<<<<<<<<<
	

void _analogRead() {
    int pin = atoi(received_parameters[1]);
    int value = analogRead(pin);
    send_int_response(value);
    return;
}
        


void _connect() {
    Serial.println(received_parameters[1]);
}
        


void _digitalRead() {
    int pin = atoi(received_parameters[1]);
    int value = digitalRead(pin);
    send_int_response(value);
    return;
}
        


void _digitalWrite() {
    int pin = atoi(received_parameters[1]);
    int value = atoi(received_parameters[2]);
    
    if(value != HIGH && value != LOW) {
        send_invalid_parameter_response();
        return;
    }
    
    digitalWrite(pin, value);
    send_ok_response();
}
        


void _pinMode() {
    int pin = atoi(received_parameters[1]);
    int mode = atoi(received_parameters[2]);
    if(mode != INPUT && mode != OUTPUT) {
        send_invalid_parameter_response();
        return;
    }
    // FIXME: validate pin
    pinMode(pin, mode);
    send_ok_response();
}
        


void _ping() {
    Serial.println("PING_OK");
}
        
 // {***PLACEHOLDER***}
	
	// PROXIED_FUNCTION_COUNT: how many proxied functions we have
// >>>>>>>>>>>>>>>>>>>> PLACEHOLDER <<<<<<<<<<<<<<<<<<<<
	#define PROXIED_FUNCTION_COUNT 6 // {***PLACEHOLDER***}
	
// >>>>>>>>>>>>>>>>>>>> PLACEHOLDER <<<<<<<<<<<<<<<<<<<<
	proxied_function_ptr function_ptr[PROXIED_FUNCTION_COUNT] = { _analogRead, _connect, _digitalRead, _digitalWrite, _pinMode, _ping,  }; // {***PLACEHOLDER***}
// >>>>>>>>>>>>>>>>>>>> PLACEHOLDER <<<<<<<<<<<<<<<<<<<<
	char*               function_name[PROXIED_FUNCTION_COUNT] = { "_analogRead", "_connect", "_digitalRead", "_digitalWrite", "_pinMode", "_ping",  }; // {***PLACEHOLDER***}
	
	# define read_char() Serial.read()
	
	void setup_serial() {
// >>>>>>>>>>>>>>>>>>>> PLACEHOLDER <<<<<<<<<<<<<<<<<<<<
		Serial.begin(9600); // {***PLACEHOLDER***}
	}
	
	void wait_start() {
		digitalWrite(PIN_START_BUTTON, HIGH); // turn on pullup resistors
		int state = HIGH;
		while(digitalRead(PIN_START_BUTTON) == HIGH) {
			digitalWrite(PIN_ONBOARD_LED, state); // turn the onboard led ON/OFF
			state = !state;
			delay(100);
		}
		digitalWrite(PIN_ONBOARD_LED, HIGH); // turn the onboard led ON
	}
	
	void send_int_response(int value) {
		Serial.println(value, DEC);
	}

	void send_invalid_parameter_response() {
// >>>>>>>>>>>>>>>>>>>> PLACEHOLDER <<<<<<<<<<<<<<<<<<<<
		Serial.println("INVALID_CMD"); // {***PLACEHOLDER***}
	}
	
	void send_invalid_cmd_response() {
// >>>>>>>>>>>>>>>>>>>> PLACEHOLDER <<<<<<<<<<<<<<<<<<<<
		Serial.println("INVALID_CMD"); // {***PLACEHOLDER***}
	}
	
	void send_ok_response() {
		Serial.println("OK");
	}
	
#endif

#ifdef PY_ARDUINO_PROXY_DEVEL // Taken from : wiring.h - Partial implementation of the Wiring API for the ATmega8. Part of Arduino - http://www.arduino.cc/

#define HIGH 0x1
#define LOW  0x0

#define INPUT 0x0
#define OUTPUT 0x1

#define true 0x1
#define false 0x0

#define CHANGE 1
#define FALLING 2
#define RISING 3

#define interrupts() sei()
#define noInterrupts() cli()

typedef unsigned int word;

#define bit(b) (1UL << (b))

typedef uint8_t boolean;
typedef uint8_t byte;

void pinMode(uint8_t a, uint8_t b) { }
void digitalWrite(uint8_t a, uint8_t b) { }
int digitalRead(uint8_t a) { return 0; }
int analogRead(uint8_t a) { return 0; }
void analogReference(uint8_t mode) { }
void analogWrite(uint8_t a, int b) { }

unsigned long millis(void) { return 0; }
unsigned long micros(void) { return 0; }
void delay(unsigned long a) { }
void delayMicroseconds(unsigned int us) { }
unsigned long pulseIn(uint8_t pin, uint8_t state, unsigned long timeout) { return 0; }

// void attachInterrupt(uint8_t a, void (*)(void) b, int mode) { }
// void detachInterrupt(uint8_t a) { }

#endif

#ifdef PY_ARDUINO_PROXY_DEVEL

	void _ping() {
		printf("ping()\n");
	}
	
	void _analogRead() {
		printf("_analogRead() PIN %s\n", received_parameters[1]);
	}

	// PROXIED_FUNCTION_COUNT: how many proxied functions we have
	#define PROXIED_FUNCTION_COUNT 2

	proxied_function_ptr function_ptr[PROXIED_FUNCTION_COUNT] = { _ping, _analogRead, };
	char* function_name[PROXIED_FUNCTION_COUNT] = { "_ping", "_analogRead", };

	int read_char() {
		char* text = "_ping\n_analogRead 5\n_some_invalid_command\n";
		static int next_return = 0;
		int ret = (int) text[next_return];
		next_return = next_return + 1;
		if(next_return >= strlen(text))
			next_return = 0;
		return ret;
	}
	
	void send_invalid_cmd_response() {
		printf("INVALID FUNCTION: '%s'\n", received_parameters[0]);
	}
	
	void wait_start() { }
	
	void setup_serial() { }
	
	void send_int_response(int value) { }
	
	void send_invalid_parameter_response() { }
	
#endif

void read_one_param(char* tmp_array) {
	
	int i;
	for(i=0; i<TEMPORARY_ARRAY_SIZE; i++)
		tmp_array[i] = 0x00; // reset
	
	int incomingByte;
	int pos = 0;
	while (pos < (TEMPORARY_ARRAY_SIZE-1)) {

		incomingByte = read_char();
		if(incomingByte == -1) {
			// no data
			if(pos == 0 && received_parameters[0] == NULL) {
				// wait 10ms only if no data was received
				delay(10);
			}
			continue;
		}

		// " " == 32
		if(incomingByte == 32) {
			if(pos == 0) {
				// Ignore leading white spaces
				continue;
			}
			// got a space... return!
			return;
		}
		
		// "\\n" == 10
		if(incomingByte == 10) {
			new_line_found = 1;
			return;
		}

		tmp_array[pos++] = incomingByte;

	} // while
	
	// pos == (TEMPORARY_ARRAY_SIZE-1)
	return;
	
}

void read_parameters() {
	
	static char tmp_array[TEMPORARY_ARRAY_SIZE];
	
	int i;
	for(i=0; i<MAX_RECEIVED_PARAMETERS; i++) {
		if(received_parameters[i] != NULL) {
			free(received_parameters[i]); // free
			received_parameters[i] = NULL; // reset
		}
	}
	
	int param_index = 0;
	new_line_found = 0;
	
	for(param_index=0; param_index<MAX_RECEIVED_PARAMETERS && !new_line_found; param_index++) {
		read_one_param(tmp_array);
		
		if(strlen(tmp_array) == 0 &&  new_line_found) {
			return;
		}
		
		received_parameters[param_index] = (char*) malloc(strlen(tmp_array)+1);
		strcpy(received_parameters[param_index], &tmp_array[0]);
	}
	
	if(new_line_found) {
		return;
	} else {
		while(! new_line_found) {
			read_one_param(tmp_array);
		}
	}
	
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

void loop() {
	read_parameters();
	
	#ifdef PY_ARDUINO_PROXY_DEVEL
	int i;
	for(i=0; i<MAX_RECEIVED_PARAMETERS; i++) {
		if(received_parameters[i] != NULL) {
			printf(" -> Parametro[%d]: %s\n", i, received_parameters[i]);
		}
	}
	#endif
	
	proxied_function_ptr function = get_function_by_name(received_parameters[0]);
	if(function != NULL) {
		(function)();
	} else {
		send_invalid_cmd_response();
	}
}

void setup() {
	// Pin 13 has an LED connected on most Arduino boards.
	pinMode(PIN_ONBOARD_LED, OUTPUT);
	pinMode(PIN_START_BUTTON, INPUT);

	wait_start();

	setup_serial();
}

#ifdef PY_ARDUINO_PROXY_DEVEL

int main() {
	setup();
	loop();
	loop();
	loop();
	return 0;
}

#endif
