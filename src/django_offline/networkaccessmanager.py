# -*- encoding: utf-8 -*-
__author__ = 'jond'

import urllib
import urlparse

from PyQt4 import QtNetwork
import django
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.http import HttpResponse
import django.test.client

import django_offline.handlers

class NetworkAccessManager(QtNetwork.QNetworkAccessManager):
    """
    Our network access manager that is used instead of the default
    This allows us to jump in and interrupt the calls to usually external
    services
    """
    def createRequest(self, operation, request, data):
        """
        Deal with the request when it comes in
        """
        argd = {}
        # lets check that data is a dictionary
        if data is not None:
            postargs = unicode(data.readAll())
            argd = urlparse.parse_qs(urllib.unquote_plus(postargs.encode('ascii')).decode('utf-8'),
                                                         keep_blank_values=True)
        # Set up the handler
        from django.core.wsgi import get_wsgi_application
        handler = StaticFilesHandler(get_wsgi_application())
        # Convert the request to a django request
        dj_request = None
        rf = django.test.client.RequestFactory()
        urlstring = unicode(request.url().toString())
        if operation == QtNetwork.QNetworkAccessManager.PostOperation:
            dj_request = rf.post(urlstring, argd)
        elif operation == QtNetwork.QNetworkAccessManager.GetOperation:
            dj_request = rf.get(urlstring, argd)
        # add the response from django to the reply
        response = handler(dj_request.environ, HttpResponse)
        reply = django_offline.handlers.FakeReply(self, request, operation, response)
        # set up the reply with the correct status
        #reply.setAttribute(QtNetwork.QNetworkRequest.HttpStatusCodeAttribute, 200)
        if reply is None:
            reply = QtNetwork.QNetworkAccessManager.createRequest(self, operation, request, data)
        return reply
