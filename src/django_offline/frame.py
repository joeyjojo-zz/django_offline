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
        """
        Creates a tab with a webview in it
        """
        tw = WebViewWidget()
        # set up the page
        nam = self.findChild(django_offline.networkaccessmanager.NetworkAccessManager, "nam")
        if nam:
            tw.setupNetworkManager(nam)
        self.tabWidget.addTab(tw, tabtitle)
        # hook up the tab widget so we know when it has changed
        self.tabWidget.currentChanged.connect(self.handleTabChanged)
        self.connectTabWidget()
        return tw

    def setUrl(self, url):
        """
        Sets the URL of the currently opened tab
        """
        self.currentWebWidget().setUrl(url)

    def setLocationBarText(self, loc):
        """
        Updates the text in the location bar at the top of the app chrome
        """
        self.lineEdit.setText(loc)

    def connectTabWidget(self):
        """
        Connect tab widget to link widget to main frame
        """
        self.setLocationBarText(self.tabWidget.currentWidget().url())
        # hook up the loading events to the main window
        wv = self.currentWebWidget()
        if wv:
            wv.loadStarted.connect(self.handlePageLoadStarted)
            wv.loadProgress.connect(self.handlePageLoadProgress)
            wv.loadFinished.connect(self.handlePageLoadFinished)

    def handleTabChanged(self, e):
        """
        When the selected tab changes perform necessary operations
        such as update the url in the location bar
        """
        self.connectTabWidget()

    def handlePageLoadStarted(self):
        """
        When the page load starts updates the main window
        """
        self.setLocationBarText(self.tabWidget.currentWidget().url())

    def handlePageLoadProgress(self, p):
        """
        When the page load progresses updates the mian window
        """
        pass

    def handlePageLoadFinished(self, success):
        """
        When the page load completes updates the main window
        """
        self.setLocationBarText(self.tabWidget.currentWidget().url())
        self.backButton.setDisabled(True)
        self.nextButton.setDisabled(True)
        # update the buttons states
        wv = self.currentWebWidget()
        if wv:
            history = wv.webView.history()
            if history:
                self.backButton.setDisabled(not history.canGoBack())
                self.nextButton.setDisabled(not history.canGoForward())



    def currentWebWidget(self):
        return self.tabWidget.currentWidget()

class WebViewWidget(QtGui.QWidget, django_offline.forms.WebView.Ui_Form):
    """
    The webview widget onto our django application
    """

    loadStarted = QtCore.pyqtSignal()
    loadProgress = QtCore.pyqtSignal(int)
    loadFinished = QtCore.pyqtSignal(bool)

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

    def url(self):
        """
        Returns the current url of the tab
        """
        webView = self.findChild(QtWebKit.QWebView, "webView")
        if webView:
            return unicode(webView.url().toString())
        return ''

    def setupNetworkManager(self, nam):
        """
        Set up our custom network manager that can interrupt requests
        """
        wv = self.findChild(QtWebKit.QWebView, 'webView')
        if wv:
            webpage = QtWebKit.QWebPage()
            webpage.setNetworkAccessManager(nam)
            wv.setPage(webpage)
            # set up other hooks
            # hook up the loading events to the main window
            wv.loadStarted.connect(self.loadStarted)
            wv.loadProgress.connect(self.loadProgress)
            wv.loadFinished.connect(self.loadFinished)

    def webView(self):
        return self.findChild(QtWebKit.QWebView, "webView")