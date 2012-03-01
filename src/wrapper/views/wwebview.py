__author__ = 'jond'
from PySide import QtGui, QtCore, QtWebKit
import wrapper.views.gen.webvieww

class WWebView(QtGui.QMainWindow, wrapper.views.gen.webvieww.Ui_MainWindow):

    onclose = QtCore.Signal()


    def __init__(self, *args):
        QtGui.QMainWindow.__init__(self, None)
        self.setupUi(self)
        # setup link delegation so we can setup a hook
        #self.webView.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        settings = QtWebKit.QWebSettings.globalSettings()
        settings.setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)


    def setUrl(self, url):
        self.webView.setUrl(QtCore.QUrl(url))

    def closeEvent(self, e):
        """
        Called when the window is attempting to close
        e type: QtGui.QCloseEvent
        """
        self.onclose.emit()
        QtGui.QMainWindow.closeEvent(self, e)