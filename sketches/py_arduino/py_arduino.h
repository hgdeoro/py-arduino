#ifndef	PY_ARDUINO_PROXY_H
#define PY_ARDUINO_PROXY_H

#ifdef __cplusplus
extern "C" {
#endif

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// typedef for proxied functions.

typedef void (* proxied_function_ptr) ();

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Configuration of LCD

// PY_ARDUINO_PROXY_LCD_SUPPORT will be defined automatically in the .pde file
// if 'generate-pde.sh' is called with the '--lcd' argument.

#define PY_ARDUINO_PROXY_LCD_SUPPORT_COLS  16
#define PY_ARDUINO_PROXY_LCD_SUPPORT_ROWS   2

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
