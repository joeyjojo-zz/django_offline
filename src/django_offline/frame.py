from PyQt4 import QtCore, QtGui, QtWebKit

import django_offline.networkaccessmanager

class MainWindow(QtGui.QMainWindow):
    """
    The main, and only, window of the application
    """
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi()

    def setupUi(self):
        """
        Setup the ui of the window that the webapp will operate in
        """
        centralwidget = QtGui.QWidget()
        centralwidget.setObjectName("centralwidget")
        horizontalLayout = QtGui.QHBoxLayout(centralwidget)
        horizontalLayout.setObjectName("horizontalLayout")
        webView = QtWebKit.QWebView(centralwidget)
        webView.setObjectName("webView")
        webpage = QtWebKit.QWebPage()
        self.setupNetworkManager(webpage)
        webView.setPage(webpage)
        horizontalLayout.addWidget(webView)
        horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(centralwidget)

        # setup webkit how we want it
        gs = QtWebKit.QWebSettings.globalSettings()
        gs.setAttribute(QtWebKit.QWebSettings.PluginsEnabled, True)
        gs.setAttribute(QtWebKit.QWebSettings.JavascriptEnabled, True)
        gs.setAttribute(QtWebKit.QWebSettings.AutoLoadImages, True)
        gs.setAttribute(QtWebKit.QWebSettings.JavascriptCanOpenWindows, True)
        gs.setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)
        gs.setAttribute(QtWebKit.QWebSettings.LocalContentCanAccessRemoteUrls, True)

        # setup app details
        QtGui.QApplication.setApplicationName("EXAMPLEAPP")
        QtGui.QApplication.setOrganizationName("DEFMYFUNC")

    def setUrl(self, urlstr):
        """
        Set the url of the webview, should only be used on startup
        """
        webView = self.findChild(QtWebKit.QWebView, "webView")
        if webView:
            webView.setUrl(QtCore.QUrl(urlstr))

    def setupNetworkManager(self, page):
        """
        Set up our custom network manager that can interrupt requests
        """
        # set up the network request intercepter
        page.setNetworkAccessManager(django_offline.networkaccessmanager.NetworkAccessManager())