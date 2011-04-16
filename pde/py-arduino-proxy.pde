
/*
 * THIS FILE IS GENERATED AUTOMATICALLI WITH generate-pde.sh
 * WHICH IS PART OF THE PROJECT "PyArduinoProxy"
 */
    


#define PIN_ONBOARD_LED 13  // DIGITAL
#define PIN_START_BUTTON 12 // DIGITAL

char lastCmd[128]; // buffer size of Serial

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

void setup() {
    // Pin 13 has an LED connected on most Arduino boards.
    pinMode(PIN_ONBOARD_LED, OUTPUT);
    pinMode(PIN_START_BUTTON, INPUT);

    wait_start();

    Serial.begin(9600);
}

void readCmd() {
    int incomingByte = -1;
    int pos = 0;
    
    while (pos < 127) {
        incomingByte = Serial.read();
        if(incomingByte == -1) {
            if(pos == 0)
                delay(10);
            continue;
        }
        // "\n" == 10
        if(incomingByte == 10) {
            lastCmd[pos] = 0x00;
            return;
        }
        lastCmd[pos++] = incomingByte;
    }
    
    if(pos == 127)
        lastCmd[pos] = 0x00;
}

void sendInvalidCmdResponse() {
    Serial.println("INVALID_CMD");
}

void sendOkResponse() {
    Serial.println("OK");
}

void sendPingOkResponse() {
    Serial.println("PING_OK");
}

int stringToInt(String str) {
    char buff[str.length() + 1];
    str.toCharArray(buff, (str.length() + 1));
    return atoi(buff); 
}

void sendIntResponse(int value) {
    Serial.println(value, DEC);
}


void _analogRead(String cmd) {
    if(!cmd.startsWith("analogRead")) {
        return;
    }
    int index_of_pin = cmd.indexOf(' ');
    String pin = cmd.substring(index_of_pin);
    int value = analogRead(stringToInt(pin));
    sendIntResponse(value);
    return;
}
        

void _digitalWrite(String cmd) {
    if(!cmd.startsWith("_digitalWrite")) {
        return;
    }
    int index_of_pin = cmd.indexOf(' ');
    int index_of_value = cmd.indexOf(' ', index_of_pin+1);
    String pin = cmd.substring(index_of_pin, index_of_value);
    String value = cmd.substring(index_of_value);
    if(value.equals("H")) {
        digitalWrite(stringToInt(pin), HIGH);
        sendOkResponse();
        return;
    }
    if(value.equals("L")) {
        digitalWrite(stringToInt(pin), LOW);
        sendOkResponse();
        return;
    }
    sendInvalidCmdResponse();
}
        

void _pinMode(String cmd) {
    if(!cmd.startsWith("pinMode")) {
        return;
    }
    int index_of_pin = cmd.indexOf(' ');
    int index_of_mode = cmd.indexOf(' ', index_of_pin+1);
    String pin = cmd.substring(index_of_pin, index_of_mode);
    String mode = cmd.substring(index_of_mode);
    if(mode.equals("I")) {
        pinMode(stringToInt(pin), INPUT);
        sendOkResponse();
        return;
    }
    if(mode.equals("O")) {
        pinMode(stringToInt(pin), OUTPUT);
        sendOkResponse();
        return;
    }
    sendInvalidCmdResponse();
}
        

void _ping(String cmd) {
    if(!cmd.startsWith("_ping")) {
        return;
    }
    sendPingOkResponse();
}
        
void loop() {
    readCmd();
    _analogRead(String(lastCmd));
    _digitalWrite(String(lastCmd));
    _pinMode(String(lastCmd));
    _ping(String(lastCmd));
}
