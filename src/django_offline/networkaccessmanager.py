# -*- encoding: utf-8 -*-
__author__ = 'jond'

import urllib
import urlparse
import time

from PyQt4 import QtNetwork, QtCore
import django.test
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.http import HttpRequest, SimpleCookie
import django.test.client
from django.core.handlers.wsgi import WSGIRequest
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.utils.importlib import import_module

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
        t = time.time()
        print 'request in', t
        argd = {}
        reply = None
        fullheader = ''
        if request.url().host() == '127.0.0.1':
            # retreive the post data
            if data is not None:
                dataread = data.readAll()
                postargs = str(dataread) # interesting that we don't unicode it here, but this seems to work
                contenttypeheader = str(request.header(QtNetwork.QNetworkRequest.ContentTypeHeader).toString()).split(';')[0]
                if contenttypeheader == 'multipart/form-data':
                    argd = postargs
                    fullheader = str(request.header(QtNetwork.QNetworkRequest.ContentTypeHeader).toString())
                elif contenttypeheader == 'application/x-www-form-urlencoded':
                    argd = postargs
                    fullheader = str(request.header(QtNetwork.QNetworkRequest.ContentTypeHeader).toString())
                else:
                    argd = urlparse.parse_qs(urllib.unquote_plus(postargs.encode('ascii')).decode('utf-8'),
                                             keep_blank_values=True)

            # get a handle on the application
            urlstring = unicode(request.url().toString())
            handler = StaticFilesHandler(django.test.client.ClientHandler)
            handler.load_middleware()
            django_request = None
            rqconv = ConvertedRequest(self.cookieJar())
            # doesn't matter because sqlite is unencrypted anyway!
            # currently used because django requires a username and password
            rqconv.login(username='default', password='default')
            if operation == QtNetwork.QNetworkAccessManager.PostOperation:
                if argd == {}:
                    # handle empty post data
                    argd = ''
                django_request = rqconv.post(urlstring, argd, content_type=fullheader)
            elif operation == QtNetwork.QNetworkAccessManager.GetOperation:
                django_request = rqconv.get(urlstring, argd)
            response = handler.get_response(django_request)

            reply = django_offline.handlers.FakeReply(self, request, operation, response)
        if reply is None:
            reply = QtNetwork.QNetworkAccessManager.createRequest(self, operation, request, data)
        reply.ignoreSslErrors()
        to = time.time()
        print 'request out', to, 'taken', to-t
        return reply

class ConvertedRequest(object):
    """
    Class that takes a QNetworkRequest and converts it to a
    request type django understands
    """
    def __init__(self, cookiejar):
        d={}
        for cookie in cookiejar.cookiesForUrl(QtCore.QUrl('http://127.0.0.1')):
            d[str(cookie.name())] = str(cookie.value())
        self.cookies = SimpleCookie(d)

    def _base_environ(self, **request):
        """
        The base environment for a request.
        """
        # This is a minimal valid WSGI environ dictionary, plus:
        # - HTTP_COOKIE: for cookie support,
        # - REMOTE_ADDR: often useful, see #8551.
        # See http://www.python.org/dev/peps/pep-3333/#environ-variables
        environ = {



            'HTTP_COOKIE':       self.cookies.output(header='', sep='; '), # these need retrieving from the cookiejar
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

    def post(self, path, data='', content_type=None,
             **extra):
        "Construct a POST request."

        if content_type is None:
            raise Exception()
        post_data = data

        parsed = urlparse.urlparse(path)
        r = {
            'CONTENT_LENGTH': len(post_data),
            'CONTENT_TYPE':   content_type,
            'PATH_INFO':      self._get_path(parsed),
            'QUERY_STRING':   parsed[4],
            'REQUEST_METHOD': 'POST',
            'wsgi.input':     django.test.client.FakePayload(post_data),
            '_body': post_data
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
            dataencode = django.test.client.encode_multipart(django.test.client.BOUNDARY, data)
            return dataencode
        else:
            # Encode the content so that the byte representation is correct.
            match = django.test.client.CONTENT_TYPE_RE.match(content_type)
            if match:
                charset = match.group(1)
            else:
                charset = settings.DEFAULT_CHARSET
            return django.test.client.smart_str(data, encoding=charset)

    def login(self, **credentials):
        """
        Sets the Factory to appear as if it has successfully logged into a site.

        Returns True if login is possible; False if the provided credentials
        are incorrect, or the user is inactive, or if the sessions framework is
        not available.
        """
        self.session = None
        user = authenticate(**credentials)
        if user and user.is_active\
        and 'django.contrib.sessions' in settings.INSTALLED_APPS:
            engine = import_module(settings.SESSION_ENGINE)

            # Create a fake request to store login details.
            request = HttpRequest()
            if self.session:
                request.session = self.session
            else:
                request.session = engine.SessionStore()
            login(request, user)

            # Save the session values.
            request.session.save()

            # Set the cookie to represent the session.
            session_cookie = settings.SESSION_COOKIE_NAME
            self.cookies[session_cookie] = request.session.session_key
            cookie_data = {
                'max-age': None,
                'path': '/',
                'domain': settings.SESSION_COOKIE_DOMAIN,
                'secure': settings.SESSION_COOKIE_SECURE or None,
                'expires': None,
                }
            self.cookies[session_cookie].update(cookie_data)

            return True
        else:
            return False
