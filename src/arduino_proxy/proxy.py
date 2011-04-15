# TODO: _unindent() could be a annotation

import serial

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

def _unindent(spaces, the_string):
    lines = []
    start = ' '*spaces
    for a_line in the_string.splitlines():
        if a_line.startswith(start):
            lines.append(a_line[spaces:])
        else:
            lines.append(a_line)
    return '\n'.join(lines)

class InvalidCommand(Exception):
    """
    The Arduino reported an error in the command
    """
    pass

class InvalidResponse(Exception):
    """
    The response from the Arduino isn't valid.
    """
    pass

class ArduinoProxy(object):
    
    INPUT = "I"
    OUTPUT = "O"
    
    HIGH = "H"
    LOW = "L"
    
    INVALID_CMD = "INVALID_CMD"
    
    def __init__(self, tty, speed=9600):
        # For communicating with the computer, use one of these rates: 300, 1200, 2400, 4800,
        #    9600, 14400, 19200, 28800, 38400, 57600, or 115200.        
        self.tty = tty
        self.speed = speed
        self.serial_port = None
        if tty != '':
            self.serial_port = serial.Serial(port=tty, baudrate=speed, bytesize=8, parity='N',
                stopbits=1, timeout=5)
    
    def _setup(self):
        return _unindent(8, """
        
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
        
            Serial.begin(%(speed)d);
        }
        
        void readCmd() {
            int incomingByte = -1;
            int pos = 0;
            
            while (pos < 127) {
                incomingByte = Serial.read();
                if(incomingByte == -1) {
                    if(pos == 0)
                        delay(100);
                    else 
                        delay(5);
                    continue;
                }
                // "\\n" == 10
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
            Serial.println("%(INVALID_CMD)s");
        }
        
        void sendOkResponse() {
            Serial.println("OK");
        }
        
        int stringToInt(String str) {
            char buff[str.length() + 1];
            str.toCharArray(buff, (str.length() + 1));
            return atoi(buff); 
        }
        
        void sendIntResponse(int value) {
            Serial.println(value, DEC);
        }
        """ % {
            'speed': self.speed, 
            'INVALID_CMD': ArduinoProxy.INVALID_CMD, 
        })
    
    _setup.include_in_pde = True
    _setup.proxy_function = False
    
    def sendCmd(self, cmd):
        """
        Sends a command to the arduino. The command is terminated with a 0x00.
        Returns the response as a string.
        """
        self.serial_port.write(cmd)
        self.serial_port.write("\n")
        self.serial_port.flush()
        
        #    response_buffer = StringIO()
        #    while True:
        #        byte = self.serial_port.read()
        #        if byte == 0x00:
        #            break
        #        else:
        #            response_buffer.write(byte)
        #
        #    response = response_buffer.getvalue()
        
        response = self.serial_port.readline(eol='\r\n')
        
        if not len(response):
            raise(InvalidResponse())

        if response == ArduinoProxy.INVALID_CMD:
            raise(InvalidCommand())

        return response
    
    # Digital I/O
    def _pinMode(self):
        return _unindent(12, """
            void _pinMode(String cmd) {
                if(!cmd.startsWith("%(method)s")) {
                    return;
                }
                int index_of_pin = cmd.indexOf(' ');
                int index_of_mode = cmd.indexOf(' ', index_of_pin+1);
                String pin = cmd.substring(index_of_pin, index_of_mode);
                String mode = cmd.substring(index_of_mode);
                if(mode.equals("%(INPUT)s")) {
                    pinMode(stringToInt(pin), INPUT);
                    sendOkResponse();
                    return;
                }
                if(mode.equals("%(OUTPUT)s")) {
                    pinMode(stringToInt(pin), OUTPUT);
                    sendOkResponse();
                    return;
                }
                sendInvalidCmdResponse();
            }
        """ % {
        'method': 'pinMode', 
        'INPUT': ArduinoProxy.INPUT, 
        'OUTPUT': ArduinoProxy.OUTPUT, 
        })
    
    _pinMode.include_in_pde = True
    _pinMode.proxy_function = True
    
    def pinMode(self, pin, mode):
        """
        * ...vast majority of Arduino (Atmega) analog pins, may be configured, and used,
        in exactly the same manner as digital pins.
        * Arduino (Atmega) pins default to inputs: high-impedance state (extremely small demands
        on the circuit)
        * NOTE: Digital pin 13 is harder to use as a digital input than the other digital pins
        because it has an LED and resistor attached to it that's soldered to the board
        * it is a good idea to connect OUTPUT pins to other devices with 470omh or 1k resistors
        
        TODO: The analog input pins can be used as digital pins, referred to as A0, A1, etc.
        """
        cmd = "_pinMode %d %s" % (pin, mode)
        ret = self.sendCmd(cmd)
        return ret

    def _digitalWrite(self):
        return _unindent(12, """
            void _digitalWrite(String cmd) {
                if(!cmd.startsWith("%(method)s")) {
                    return;
                }
                int index_of_pin = cmd.indexOf(' ');
                int index_of_value = cmd.indexOf(' ', index_of_pin+1);
                String pin = cmd.substring(index_of_pin, index_of_value);
                String value = cmd.substring(index_of_value);
                if(value.equals("%(HIGH)s")) {
                    digitalWrite(stringToInt(pin), HIGH);
                    sendOkResponse();
                    return;
                }
                if(value.equals("%(LOW)s")) {
                    digitalWrite(stringToInt(pin), LOW);
                    sendOkResponse();
                    return;
                }
                sendInvalidCmdResponse();
            }
        """ % {
        'method': '_digitalWrite', 
        'HIGH': ArduinoProxy.HIGH, 
        'LOW': ArduinoProxy.LOW, 
        })
    
    _digitalWrite.include_in_pde = True
    _digitalWrite.proxy_function = True
    
    def digitalWrite(self, value):
        # FIXME: validate pin and value
        cmd = "_digitalWrite %d %s" % (pin, value)
        ret = self.sendCmd(cmd)
        return ret
    
    def digitalRead(self):
        pass

    #Analog I/O
    def analogReference(self):
        pass
    
    def _analogRead(self):
        return _unindent(12, """
            void _analogRead(String cmd) {
                if(!cmd.startsWith("%(method)s")) {
                    return;
                }
                int index_of_pin = cmd.indexOf(' ');
                String pin = cmd.substring(index_of_pin);
                int value = analogRead(stringToInt(pin));
                sendIntResponse(value);
                return;
            }
        """ % {
        'method': 'analogRead', 
    })
    
    _analogRead.include_in_pde = True
    _analogRead.proxy_function = True
    
    def analogRead(self, pin):
        """
        * map input voltages between 0 and 5 volts into integer values between 0 and 1023.
        """
        cmd = "_analogRead %d" % (pin)
        ret = self.sendCmd(cmd)
        return ret
    
    def analogWrite(self):
        pass

    def _ping(self):
        return _unindent(12, """
            void _ping(String cmd) {
                if(!cmd.startsWith("%(method)s")) {
                    return;
                }
                sendOkResponse();
            }
        """ % {
        'method': '_ping', 
        })
    
    _ping.include_in_pde = True
    _ping.proxy_function = True
    
    def ping(self):
        # FIXME: validate pin and value
        cmd = "_ping"
        ret = self.sendCmd(cmd)
        return ret

if __name__ == '__main__':
    proxy = ArduinoProxy('')

    print _unindent(8, """
        /*
         * THIS FILE IS GENERATED AUTOMATICALLI WITH generate-pde.sh
         * WHICH IS PART OF THE PROJECT "PyArduinoProxy"
         */
    """)
    
    # All this functions have 'include_in_pde' == True
    pde_functions = [getattr(proxy, a_function) for a_function in dir(proxy)
        if getattr(getattr(proxy, a_function), 'include_in_pde', None) is True]
    
    # First functions that have 'proxy_function' == False
    for a_function in [a_function for a_function in pde_functions
            if getattr(a_function, 'proxy_function', None) is False]:
        print a_function()
    
    # Now the real, interesting functions...
    for a_function in [a_function for a_function in pde_functions
            if getattr(a_function, 'proxy_function', None) is True]:
        print a_function()
    
    # Now, generate the loop()
    print "void loop() {"
    print "    readCmd();"
    
    for a_function in [a_function for a_function in pde_functions
            if getattr(a_function, 'proxy_function', None) is True]:
        print "    " + a_function.__name__ + "(String(lastCmd));"
    print "}"
