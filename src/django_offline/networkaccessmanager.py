# -*- encoding: utf-8 -*-
__author__ = 'jond'

import urllib
import urlparse

from PyQt4 import QtNetwork, QtCore
import django.test
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.http import HttpResponse, SimpleCookie
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
        reply = None
        if request.url().host() == '127.0.0.1':
            # lets check that data is a dictionary
            if data is not None:
                postargs = unicode(data.readAll())
                argd = urlparse.parse_qs(urllib.unquote_plus(postargs.encode('ascii')).decode('utf-8'),
                                                             keep_blank_values=True)
            # Set up the handler
            from django.core.wsgi import get_wsgi_application
            handler = StaticFilesHandler(get_wsgi_application())
            print request.header(QtNetwork.QNetworkRequest.CookieHeader)
            # Convert the request to a django request
            d={}
            for cookie in self.cookieJar().cookiesForUrl(QtCore.QUrl('http://127.0.0.1')):
                d[str(cookie.name())] = str(cookie.value())
            cookies = SimpleCookie(d)
            dj_request = None
            print 'something', cookies
            print 'nothing', cookies.output(header='', sep='; ')
            rf = django.test.Client(enforce_csrf_checks=True, Cookie=cookies.output(header='', sep='; '))
            rf.login(username='jond', password='jond')
            urlstring = unicode(request.url().toString())
            if operation == QtNetwork.QNetworkAccessManager.PostOperation:
                dj_request = rf.post(urlstring, argd, Cookie=cookies.output(header='', sep='; '))
            elif operation == QtNetwork.QNetworkAccessManager.GetOperation:
                dj_request = rf.get(urlstring, argd)
            # transfer the cookies from the cookie jar into the request



            #print "bar", dj_request.environ
            # add the response from django to the reply
            reply = django_offline.handlers.FakeReply(self, request, operation, dj_request)
            # set up the reply with the correct status
            reply.setAttribute(QtNetwork.QNetworkRequest.HttpStatusCodeAttribute, dj_request.status_code)
        if reply is None:
            reply = QtNetwork.QNetworkAccessManager.createRequest(self, operation, request, data)
        reply.ignoreSslErrors()
        return reply
