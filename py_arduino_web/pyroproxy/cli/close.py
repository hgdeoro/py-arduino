# Licensed under the Apache License, Version 2.0
# Copyright (C) 2011-2015 - Horacio Guillermo de Oro <hgdeoro@gmail.com>

from py_arduino_web.pyroproxy.utils import BasePyroMain


class Main(BasePyroMain):

    def run(self, options, args, arduino):
        print "Calling arduino.close()"
        arduino.close()

if __name__ == '__main__':
    Main().start()
