# -*- encoding: utf-8 -*-
__author__ = 'jond'

import re
import urlparse
import urllib

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
        TODO: Only deals with keyworded get requests in urls not ordered
        """
        reply = None
        if reply is None:
            reply = QtNetwork.QNetworkAccessManager.createRequest(self, operation, request, data)
        return reply
