#ifndef	PY_ARDUINO_PROXY_H
#define PY_ARDUINO_PROXY_H

#ifdef __cplusplus
extern "C" {
#endif

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// typedef for proxied functions.

typedef void (* proxied_function_ptr) ();

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Define PY_ARDUINO_PROXY_LCD_SUPPORT to support LCD

//#define PY_ARDUINO_PROXY_LCD_SUPPORT

#define PY_ARDUINO_PROXY_LCD_SUPPORT_rs     7
#define PY_ARDUINO_PROXY_LCD_SUPPORT_enable 6
#define PY_ARDUINO_PROXY_LCD_SUPPORT_d4     5
#define PY_ARDUINO_PROXY_LCD_SUPPORT_d5     4
#define PY_ARDUINO_PROXY_LCD_SUPPORT_d6     3
#define PY_ARDUINO_PROXY_LCD_SUPPORT_d7     2

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//  END
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#ifdef  __cplusplus
}
#endif

#endif
