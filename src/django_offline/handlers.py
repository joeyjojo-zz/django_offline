__author__ = 'jond'

from PyQt4 import QtCore, QtNetwork

import django.core.handlers.base

class FakeHandler(django.core.handlers.base.BaseHandler):
    def __init__(self):
        django.core.handlers.base.BaseHandler.__init__(self)
        # Set up middleware if needed. We couldn't do this earlier, because
        # settings weren't available.
        if self._request_middleware is None:
            try:
                # Check that middleware is still uninitialised.
                if self._request_middleware is None:
                    self.load_middleware()
            except:
                # Unload whatever middleware we got
                self._request_middleware = None
                raise



class FakeReply(QtNetwork.QNetworkReply):
    """
    The reply class that is used when a url is to be dealt with by the application
    and is not to be dealt with by the usual method
    """
    def __init__(self, parent, request, operation, dj_response):
        """
        @type args: dict
        """
        QtNetwork.QNetworkReply.__init__(self, parent)
        self.setRequest(request)
        self.setUrl(request.url())
        self.setOperation(operation)
        self.open(self.ReadOnly | self.Unbuffered)
        # if any are lists of 1 item then just send the item through
        self.content = dj_response.content
        self.offset = 0

        #self.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader, "application/json; charset=UTF-8")
        self.setHeader(QtNetwork.QNetworkRequest.ContentLengthHeader, len(self.content))

        QtCore.QTimer.singleShot(0, self, QtCore.SIGNAL("readyRead()"))
        QtCore.QTimer.singleShot(0, self, QtCore.SIGNAL("finished()"))


    def abort(self):
        pass

    def bytesAvailable(self):
        return len(self.content) - self.offset

    def isSequential(self):
        return True

    def readData(self, maxSize):
        if self.offset < len(self.content):
            end = min(self.offset + maxSize, len(self.content))
            data = self.content[self.offset:end]
            self.offset = end
            return data
