#include <stdlib.h>
#include <stdio.h>
#include <string.h>

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// If PY_ARDUINO_PROXY_DEVEL is defined, the generated code
// is targeted to test and develop the sketch in a PC,
// this means the code won't run on Arduino

#define PY_ARDUINO_PROXY_DEVEL // removed when generating the sketch.

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// typedef for proxied functions.

typedef void (* proxied_function_ptr) ();

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// MAX_RECEIVED_PARAMETERS: max count of parameter received from Serial.
// The first parameter is the function name to execute.

#define MAX_RECEIVED_PARAMETERS 10

char* received_parameters[MAX_RECEIVED_PARAMETERS] = { 0 };

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Size of temporal array for storing each of the parameters
// received from Serial. This limit the max. length that a
// parameter may have.

#define TEMPORARY_ARRAY_SIZE 32

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Flag setted when a newline was found while reading from Serial.

int new_line_found = 0;

#ifndef PY_ARDUINO_PROXY_DEVEL
	
	// PROXIED_FUNCTION_COUNT: how many proxied functions we have
	#define PROXIED_FUNCTION_COUNT %(PROXIED_FUNCTION_COUNT)s // {***PLACEHOLDER***}
	
	proxied_function_ptr function_ptr[PROXIED_FUNCTION_COUNT] = { 0 };
	char* function_name[PROXIED_FUNCTION_COUNT] = { 0 };

	int readChar() {
		return Serial.read();
	}
	
	void setup_command_arrays() {
		%(setup_command_arrays)s // {***PLACEHOLDER***}
	}
	
#endif

#ifdef PY_ARDUINO_PROXY_DEVEL

	// PROXIED_FUNCTION_COUNT: how many proxied functions we have
	#define PROXIED_FUNCTION_COUNT 2

	proxied_function_ptr function_ptr[PROXIED_FUNCTION_COUNT] = { 0 };
	char* function_name[PROXIED_FUNCTION_COUNT] = { 0 };

	int readChar() {
		char* text = "_ping\n_analogRead 5\n_some_invalid_command\n";
		static int next_return = 0;
		int ret = (int) text[next_return];
		next_return = next_return + 1;
		if(next_return >= strlen(text))
			next_return = 0;
		return ret;
	}
	
	void delay(int d) { }
	
	void _ping() {
		printf("ping()\n");
	}
	
	void _analogRead() {
		printf("_analogRead() PIN %s\n", received_parameters[1]);
	}
	
	void setup_command_arrays() {
		function_ptr[0] = _ping;
		function_name[0] = "_ping";
		function_ptr[1] = _analogRead;
		function_name[1] = "_analogRead";
	}
	
	void sendInvalidCmdResponse() {
		printf("INVALID FUNCTION: '%s'\n", received_parameters[0]);
	}
	
#endif

void read_one_param(char* tmp_array) {
	
	int i;
	for(i=0; i<TEMPORARY_ARRAY_SIZE; i++)
		tmp_array[i] = 0x00; // reset
	
	int incomingByte;
	int pos = 0;
	while (pos < (TEMPORARY_ARRAY_SIZE-1)) {

		incomingByte = readChar();
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
	
	//#ifdef PY_ARDUINO_PROXY_DEVEL
	//int i;
	//for(i=0; i<MAX_RECEIVED_PARAMETERS; i++) {
	//	if(received_parameters[i] != NULL) {
	//		printf("Parametro[%d]: %s\n", i, received_parameters[i]);
	//	}
	//}
	//#endif
	
	proxied_function_ptr function = get_function_by_name(received_parameters[0]);
	if(function != NULL) {
		(function)();
	} else {
		sendInvalidCmdResponse();
	}
}

#ifdef PY_ARDUINO_PROXY_DEVEL

void setup() {
	setup_command_arrays();
}

int main() {
	setup();
	loop();
	loop();
	loop();
	return 0;
}

#endif
