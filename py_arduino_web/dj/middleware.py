##-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
##    py-arduino - Access your Arduino from Python
##    Copyright (C) 2011-2013 - Horacio Guillermo de Oro <hgdeoro@gmail.com>
##
##    This file is part of py-arduino.
##
##    py-arduino is free software; you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation version 2.
##
##    py-arduino is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License version 2 for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with py-arduino; see the file LICENSE.txt.
##-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

import logging

from Pyro4.errors import ConnectionClosedError
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages


class PyroproxyConnectionMiddleware(object):
    """
    Middleware that shows descriptive error on Pyro connection errors.
    """
    _middleware_logger = logging.getLogger('PyroproxyConnectionMiddleware')

    def process_exception(self, request, exception):
        if isinstance(exception, ConnectionClosedError):
            self._middleware_logger.error("ConnectionClosedError detected...")
            messages.add_message(request, messages.ERROR, "ConnectionClosedError detected")
            return HttpResponseRedirect(reverse('home'))

        return None
