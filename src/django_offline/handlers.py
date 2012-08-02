__author__ = 'jond'

from PyQt4 import QtCore, QtNetwork

class FakeReply(QtNetwork.QNetworkReply):
    """
    The reply class that is used when a url is to be dealt with by the application
    and is not to be dealt with by the usual method
    """
    def __init__(self, parent, request, operation, f, args={}):
        """
        @type args: dict
        """
        QtNetwork.QNetworkReply.__init__(self, parent)
        self.setRequest(request)
        self.setUrl(request.url())
        self.setOperation(operation)
        self.open(self.ReadOnly | self.Unbuffered)
        # if any are lists of 1 item then just send the item through
        for k, v in args.items():
            if type(v) is type([]):
                if len(v) is 1:
                    args[k] = v[0]
        self.content = f(**args)
        self.offset = 0

        self.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader, "application/json; charset=UTF-8")
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
