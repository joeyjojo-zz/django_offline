# -*- encoding: utf-8 -*-
__author__ = 'jond'

import urllib
import urlparse

from PyQt4 import QtNetwork, QtCore
import django.test
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.http import HttpResponse, SimpleCookie
import django.test.client
from django.core.handlers.wsgi import WSGIRequest
from django.conf import settings

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
        """
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
        """
        if request.url().host() == '127.0.0.1':
            # retreive the post data
            if data is not None:
                postargs = unicode(data.readAll())
                argd = urlparse.parse_qs(urllib.unquote_plus(postargs.encode('ascii')).decode('utf-8'),
                    keep_blank_values=True)
            # get a handle on the application
            urlstring = unicode(request.url().toString())
            handler = StaticFilesHandler(django.test.client.ClientHandler)
            handler.load_middleware()
            django_request = None
            rqconv = ConvertedRequest()
            if operation == QtNetwork.QNetworkAccessManager.PostOperation:
                django_request = rqconv.post(urlstring, argd)
            elif operation == QtNetwork.QNetworkAccessManager.GetOperation:
                django_request = rqconv.get(urlstring, argd)
            response = handler.get_response(django_request)

            reply = django_offline.handlers.FakeReply(self, request, operation, response)
        if reply is None:
            reply = QtNetwork.QNetworkAccessManager.createRequest(self, operation, request, data)
        reply.ignoreSslErrors()

        return reply

class ConvertedRequest(object):
    """
    Class that takes a QNetworkRequest and converts it to a
    request type django understands
    """

    def _base_environ(self, **request):
        """
        The base environment for a request.
        """
        # This is a minimal valid WSGI environ dictionary, plus:
        # - HTTP_COOKIE: for cookie support,
        # - REMOTE_ADDR: often useful, see #8551.
        # See http://www.python.org/dev/peps/pep-3333/#environ-variables
        environ = {
            'HTTP_COOKIE':       '',#self.cookies.output(header='', sep='; '), # these need retrieving from the cookiejar
            'PATH_INFO':         '/',
            'REMOTE_ADDR':       '127.0.0.1',
            'REQUEST_METHOD':    'GET',
            'SCRIPT_NAME':       '',
            'SERVER_NAME':       'testserver',
            'SERVER_PORT':       '80',
            'SERVER_PROTOCOL':   'HTTP/1.1',
            'wsgi.version':      (1,0),
            'wsgi.url_scheme':   'http',
            'wsgi.input':        django.test.client.FakePayload(''),
            'wsgi.errors':       '',#self.errors, # these need retreiving properly
            'wsgi.multiprocess': True,
            'wsgi.multithread':  False,
            'wsgi.run_once':     False,
            }
        #environ.update(self.defaults)
        environ.update(request)
        return environ

    def request(self, **request):
        "Construct a generic request object."
        return WSGIRequest(self._base_environ(**request))

    def get(self, path, data={}, **extra):
        "Construct a GET request"

        parsed = urlparse.urlparse(path)
        r = {
            'CONTENT_TYPE':    'text/html; charset=utf-8',
            'PATH_INFO':       self._get_path(parsed),
            'QUERY_STRING':    django.utils.http.urlencode(data, doseq=True) or parsed[4],
            'REQUEST_METHOD': 'GET',
            }
        r.update(extra)
        return self.request(**r)

    def post(self, path, data={}, content_type=django.test.client.MULTIPART_CONTENT,
             **extra):
        "Construct a POST request."

        post_data = self._encode_data(data, content_type)

        parsed = urlparse.urlparse(path)
        r = {
            'CONTENT_LENGTH': len(post_data),
            'CONTENT_TYPE':   content_type,
            'PATH_INFO':      self._get_path(parsed),
            'QUERY_STRING':   parsed[4],
            'REQUEST_METHOD': 'POST',
            'wsgi.input':     django.test.client.FakePayload(post_data),
            }
        r.update(extra)
        return self.request(**r)

    def _get_path(self, parsed):
        # If there are parameters, add them
        if parsed[3]:
            return urllib.unquote(parsed[2] + ";" + parsed[3])
        else:
            return urllib.unquote(parsed[2])

    def _encode_data(self, data, content_type, ):
        if content_type is django.test.client.MULTIPART_CONTENT:
            return django.test.client.encode_multipart(django.test.client.BOUNDARY, data)
        else:
            # Encode the content so that the byte representation is correct.
            match = django.test.client.CONTENT_TYPE_RE.match(content_type)
            if match:
                charset = match.group(1)
            else:
                charset = settings.DEFAULT_CHARSET
            return django.test.client.smart_str(data, encoding=charset)
