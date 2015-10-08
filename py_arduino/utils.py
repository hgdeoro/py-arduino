# Licensed under the Apache License, Version 2.0
# Copyright (C) 2011-2015 - Horacio Guillermo de Oro <hgdeoro@gmail.com>


class WrappedBoolean(object):
    """Wraps a boolean, to emulate passing variables by reference"""

    def __init__(self, value):
        assert value is True or value is False
        self._value = value

    def setTrue(self):
        self._value = True

    def setFalse(self):
        self._value = False

    def get(self):
        return self._value


def synchronized(lock):
    """Synchronization decorator"""

    def wrap(f):
        def new_function(*args, **kw):
            lock.acquire()
            try:
                return f(*args, **kw)
            finally:
                lock.release()
        return new_function
    return wrap
