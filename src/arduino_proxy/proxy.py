
class ArduinoProxy(object):
    
    INPUT = "I"
    OUTPUT = "O"
    
    def __init__(self, tty):
        self._tty = tty
        # self._speed = speed
    
    def __arduino_setup(self):
        # FIXME: implementar!
        return """
        char lastCmd[128];
        
        void setup() {
            // Serial.xxxxxxx()
            
        }
        
        void readCmd() {
            int incomingByte = 0xff;
            int pos = 0;
            lastCmd[0] = 0;
            
            while (Serial.available() > 0 && pos < 128) {
                // read the incoming byte:
                lastCmd[pos] = Serial.read();
                if(lastCmd[pos] == 0) {
                    break;
                }
                pos++;
            }
        }

        void sendOkResponse() {
            // Serial.writeXxxxx("OK")
        }
        
        int stringToInt(String str) {
            char buff[str.length() + 1];
            str.toCharArray(buff, (str.length() + 1));
            return atoi(buff); 
        }
        void sendIntResponse(int value) {
            // Serial.writeXxxxx(value, INTEGER)
        }
        """

    ##def __arduino_loop(self):
    ##    # FIXME: implementar!
    ##    return """
    ##    void loop() {
    ##    }
    ##    """
    
    def sendCmd(self, cmd):
        # FIXME: implementar
        
        # Serial.send("%s\x00" % cmd)
        
        pass
    
    # Digital I/O
    def __arduino__pinMode(self):
        return """
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
            }
        """ % {
        'method': 'pinMode', 
        'INPUT': ArduinoProxy.INPUT, 
        'OUTPUT': ArduinoProxy.OUTPUT, 
    }
    
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

    def digitalWrite(self):
        pass
    
    def digitalRead(self):
        pass

    #Analog I/O
    def analogReference(self):
        pass
    
    def __arduino__analogRead(self):
        return """
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
    }
    
    def analogRead(self, pin):
        """
        * map input voltages between 0 and 5 volts into integer values between 0 and 1023.
        """
        cmd = "_analogRead %d" % (pin)
        ret = self.sendCmd(cmd)
        return ret
    
    def analogWrite(self):
        pass

if __name__ == '__main__':
    proxy = ArduinoProxy('')
    methods = [a_method[len('_ArduinoProxy__arduino_'):]
        for a_method in dir(proxy)
            if a_method.startswith('_ArduinoProxy__arduino_')]
    
    for method_name in methods:
        method = getattr(proxy, '_ArduinoProxy__arduino_' + method_name)
        print method()

    print "void loop() {"
    print "    readCmd();"
    for method_name in methods:
        if method_name in ['setup']:
            continue
        print "    //" + method_name + "(cmd);"
        print "    " + method_name + "(String(lastCmd));"
    print "}"
