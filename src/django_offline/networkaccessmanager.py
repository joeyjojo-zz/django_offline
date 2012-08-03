# -*- encoding: utf-8 -*-
import django
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.http import HttpResponse

__author__ = 'jond'

import os


import django.test.client

import django_offline.handlers

from PyQt4 import QtCore, QtNetwork

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
        if data is None:
            data = {}

        # Set up the handler
        from django.core.wsgi import get_wsgi_application
        handler = StaticFilesHandler(get_wsgi_application())
        # Convert the request to a django request
        dj_request = None
        rf = django.test.client.RequestFactory()
        urlstring = unicode(request.url().toString())
        if operation == QtNetwork.QNetworkAccessManager.PostOperation:
            dj_request = rf.post(urlstring, data)
        elif operation == QtNetwork.QNetworkAccessManager.GetOperation:
            dj_request = rf.get(urlstring, data)
        # add the response from django to the reply
        response = handler(dj_request.environ, HttpResponse)
        reply = django_offline.handlers.FakeReply(self, request, operation, response)
        # set up the reply with the correct status
        #reply.setAttribute(QtNetwork.QNetworkRequest.HttpStatusCodeAttribute, 200)
        if reply is None:
            reply = QtNetwork.QNetworkAccessManager.createRequest(self, operation, request, data)
        return reply
