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
        self.setRequest(request)
        self.setOperation(operation)

        self.content = dj_response.content
        self.offset = 0

        self.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader, dj_response['Content-Type'])
        self.setHeader(QtNetwork.QNetworkRequest.ContentLengthHeader, len(self.content))

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
