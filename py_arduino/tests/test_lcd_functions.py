#!/usr/bin/env python
# Licensed under the Apache License, Version 2.0
# Copyright (C) 2011-2015 - Horacio Guillermo de Oro <hgdeoro@gmail.com>

import time

from py_arduino.main_utils import BaseMain


class Main(BaseMain):
    def run(self, options, args, arduino):
        print "Clearing LCD", arduino.lcdClear()
        raw_input("Press any key to continue...")

        print "'Hello, world!' on row 0", arduino.lcdMessage("Hello, world!")
        raw_input("Press any key to continue...")

        print "'Hello, world!' on row 1", arduino.lcdMessage(["", "Hello, world!"])
        raw_input("Press any key to continue...")

        print "'Hello, world!' on row 0, 'bye bye world' on line 1", \
            arduino.lcdMessage(["Hello, world!", "bye bye world"])
        raw_input("Press any key to continue...")

        print "Filling screen with letters and numbers"
        for a_char in ['a', 'b', 'c', 'x', 'y', 'z']:
            arduino.lcdMessage([a_char * 16, a_char * 16])
            time.sleep(0.1)
        raw_input("Press any key to continue...")

        print "Moving an @"
        for i in range(0, 32):
            arduino.lcdWrite("@", i % 16, i / 16, clear_lcd=True)  # msg, col, row
            time.sleep(0.2)
            # raw_input("Press any key to continue...")


if __name__ == '__main__':
    Main().start()
