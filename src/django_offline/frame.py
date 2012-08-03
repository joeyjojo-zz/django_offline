from PyQt4 import QtCore, QtGui, QtWebKit

import django_offline.forms.MainWindow
import django_offline.forms.WebView
import django_offline.networkaccessmanager

class MainWindow(QtGui.QMainWindow, django_offline.forms.MainWindow.Ui_MainWindow):
    """
    The main, and only, window of the application
    """
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        django_offline.forms.MainWindow.Ui_MainWindow.__init__(self)
        self.setupUi(self)
        # add the main tab
        self.nam = django_offline.networkaccessmanager.NetworkAccessManager(self)
        self.nam.setObjectName('nam')
        self.createWebViewTab("Main Tab")


    def createWebViewTab(self, tabtitle):
        tw = WebViewWidget()
        nam = self.findChild(django_offline.networkaccessmanager.NetworkAccessManager, "nam")
        if nam:
            tw.setupNetworkManager(nam)
        self.tabWidget.addTab(tw, tabtitle)
        return tw

    def setUrl(self, url):
        """
        Sets the URL of the currently opened tab
        """
        self.tabWidget.currentWidget().setUrl(url)


class WebViewWidget(QtGui.QWidget, django_offline.forms.WebView.Ui_Form):
    """
    The webview widget onto our django application
    """
    def __init__(self):
        QtGui.QWidget.__init__(self)
        django_offline.forms.WebView.Ui_Form.__init__(self)
        self.setupUi(self)
        # set up the qwebview how we want it
        gs = QtWebKit.QWebSettings.globalSettings()
        gs.setAttribute(QtWebKit.QWebSettings.PluginsEnabled, True)
        gs.setAttribute(QtWebKit.QWebSettings.JavascriptEnabled, True)
        gs.setAttribute(QtWebKit.QWebSettings.AutoLoadImages, True)
        gs.setAttribute(QtWebKit.QWebSettings.JavascriptCanOpenWindows, True)
        gs.setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)
        gs.setAttribute(QtWebKit.QWebSettings.LocalContentCanAccessRemoteUrls, True)

    def setUrl(self, urlstr):
        """
        Set the url of the webview, should only be used on startup
        """
        webView = self.findChild(QtWebKit.QWebView, "webView")
        if webView:
            webView.setUrl(QtCore.QUrl(urlstr))

    def setupNetworkManager(self, nam):
        """
        Set up our custom network manager that can interrupt requests
        """
        wv = self.findChild(QtWebKit.QWebView, 'webView')
        if wv:
            webpage = QtWebKit.QWebPage()
            webpage.setNetworkAccessManager(nam)
            wv.setPage(webpage)
