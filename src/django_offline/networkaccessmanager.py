# -*- encoding: utf-8 -*-
import django

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
        handler = django_offline.handlers.FakeHandler()
        # Convert the request to a django request
        dj_request = None
        rf = django.test.client.RequestFactory()
        urlstring = unicode(request.url().toString())
        if operation == QtNetwork.QNetworkAccessManager.PostOperation:
            dj_request = rf.post(urlstring, data)
        elif operation == QtNetwork.QNetworkAccessManager.GetOperation:
            dj_request = rf.get(urlstring, data)
        # add the response from django to the reply
        response = handler.get_response(dj_request)
        reply = django_offline.handlers.FakeReply(self, request, operation, response)
        # set up the reply with the correct status
        #reply.setAttribute(QtNetwork.QNetworkRequest.HttpStatusCodeAttribute, 200)
        if reply is None:
            reply = QtNetwork.QNetworkAccessManager.createRequest(self, operation, request, data)
        return reply
