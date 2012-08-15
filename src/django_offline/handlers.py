__author__ = 'jond'

from PyQt4 import QtCore, QtNetwork

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
        #import pdb
        #pdb.set_trace()
        for i in dj_response.items():
            self.setRawHeader(i[0],  i[1])

        self.setRequest(request)
        self.setOperation(operation)

        self.content = dj_response.content
        self.offset = 0
        # :NOTE: This statement is commented due to a bug in PyQt where the cookie headers can't be set correctly due to
        # the cookie header expecting QList, but Python Lists are auto-converted to QVariantList, and it is incompatible.
        # This bug should be fixed in PyQt 4.8, however we need to maintain backward compatibility with 4.7
        # [WARNING] QNetworkRequest::setHeader: QVariant of type QVariantList cannot be used with header Set-Cookie
        #self.setHeader(QNetworkRequest.SetCookieHeader, self.m_reply.header(QNetworkRequest.SetCookieHeader))
        # The following code is an attempted workaround for this issue.

        self.cookies = dj_response.cookies.items()
        self.cookielist = []
        if self.cookies:
            self.cookielist = QtNetwork.QNetworkCookie().parseCookies(','.join([str(c[1]) for c in self.cookies]))

        self.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader, dj_response['Content-Type'])
        self.setHeader(QtNetwork.QNetworkRequest.ContentLengthHeader, len(self.content))
        cookiestrings = [str(c[1]) for c in self.cookies]
        self.cookiestrings = [cs[12:] for cs in cookiestrings]

        QtCore.QTimer.singleShot(0, self, QtCore.SIGNAL("readyRead()"))
        QtCore.QTimer.singleShot(0, self, QtCore.SIGNAL("finished()"))
        self.open(self.ReadOnly | self.Unbuffered)
        self.setUrl(request.url())

    def abort(self):
        pass

    def bytesAvailable(self):
        return (len(self.content) - self.offset) + QtCore.QIODevice.bytesAvailable(self)

    def isSequential(self):
        return True

    def readData(self, maxSize):
        if self.offset < len(self.content):
            end = min(self.offset + maxSize, len(self.content))
            data = self.content[self.offset:end]
            self.offset = end
            return data
