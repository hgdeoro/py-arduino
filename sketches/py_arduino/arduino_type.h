// 
//    FILE: arduino_type.h
//    DATE: 2011-05-18
// PURPOSE: Specify Arduino Capabilities
//
//   URL: http://arduino.cc/forum/index.php/topic,61528.msg445142.html#msg445142
//
// HISTORY:
// 2011-05-18 Rob Tillaart <rob.tillaart@gmail.com>: initial version
// 2011-05-19 Horacio G. de Oro <hgdeoro@gmail.com>: removed board_name, voltage, RAM, SerialPorts, clockSpeed
//  and added bitmap for PWM pins.
//

#ifndef arduino_type_h
#define arduino_type_h

#include <Arduino.h>
#include "avr_cpunames.h"
#include "inttypes.h"

struct arduino_type
{ 
  // char board_name[16];   // use 'arduino.getAvrCpuType()' to the CPU name.
  uint8_t analog_pins;      // how many analog pins
  uint8_t digital_pins;     // excl analog pins that can be used as digital ones
  uint16_t pwm_pins_bitmap; // bitmap of digital pin with PWM support
  // uint8_t voltage;       // whole part only
  uint8_t ram_size;         // KiB - uint8_t: MAX=255
  uint8_t eeprom_size;      // KiB - uint8_t: MAX=255
  uint16_t flash_size;       // KiB - uint16_t: MAX=65535
  // uint8_t SerialPorts;
  // uint8_t clockSpeed;   // *10e6
} 

// #if defined (__AVR_AT94K__)
// this_arduino_type = {
//  1, 2, 0x00, 5, 8, 2, 1, 8
// }; // not checked

#if defined (__AVR_ATmega328P__)

  //
  // Arduino UNO
  // - PWM pins on Uno: 3, 5, 6, 9, 10, 11
  //
  
  this_arduino_type = {
    6, 14, 1<<3 | 1<<5 | 1<<6 | 1<<9 | 1<<10 | 1<<11, 2, 1, 32
  };

// #elif defined (__AVR_ATmega644__) // Sanguino?
// this_arduino_type = { 
//  6, 13, 0x00, 5, 32, 2, 1, 16
// }; // not checked

#elif defined (__AVR_ATmega1280__)

  //
  // Arduino Mega - http://arduino.cc/en/Main/ArduinoBoardMega
  // - PWM pins on Mega: 2 to 13
  //
  
  this_arduino_type = { 
    16, 54, 0x00 | 1<<2 | 1<<3 | 1<<4 | 1<<5 | 1<<6 | 1<<7 | 1<<8 | 1<<9 | 1<<10 | 1<<11 | 1<<12 | 1<<13, 8, 4, 128
  };

#elif defined (__AVR_ATmega2560__)

  //
  // Arduino Mega - http://arduino.cc/en/Main/ArduinoBoardMega2560
  // - PWM pins on Mega: 2 to 13
  //
  
  this_arduino_type = { 
    16, 54, 0x00 | 1<<2 | 1<<3 | 1<<4 | 1<<5 | 1<<6 | 1<<7 | 1<<8 | 1<<9 | 1<<10 | 1<<11 | 1<<12 | 1<<13, 8, 4, 256
  };

#else
  
  this_arduino_type = { 
    0, 0, 0x00, 0, 0
  };

#endif 

#endif // ArduinoType_h
