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
        self.createWebViewTab("Main Tab")

    def createWebViewTab(self, tabtitle):
        return self.tabWidget.addTab(WebViewWidget(), tabtitle)

class WebViewWidget(QtGui.QWidget, django_offline.forms.WebView.Ui_Form):
    """
    The webview widget onto our django application
    """
    def __init__(self):
        QtGui.QWidget.__init__(self)
        django_offline.forms.WebView.Ui_Form.__init__(self)
        self.setupUi(self)