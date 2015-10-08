# Licensed under the Apache License, Version 2.0
# Copyright (C) 2011-2015 - Horacio Guillermo de Oro <hgdeoro@gmail.com>

import logging

from Pyro4.errors import ConnectionClosedError
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.models import User


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


class AutomaticLoginUserMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            return
        if not request.path_info.startswith('/admin'):
            return

        try:
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        except:
            pass

        user = auth.authenticate(username='admin', password='admin')
        if user:
            request.user = user
            auth.login(request, user)
