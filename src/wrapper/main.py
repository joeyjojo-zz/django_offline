"""
The main framework file
Starts up the application
"""
__author__ = 'jond'

import sys

from PySide import QtGui

import views.wwebview

def start(uri=None):
    """
    Start the QT application
    @param uri: The uri to load in as default (i.e. the home page of the application
    @type uri: str
    """
    # start up the app
    app = QtGui.QApplication(sys.argv)
    w = views.wwebview.WWebView()
    w.setUrl(uri)
    w.show()
    app.exec_()
    sys.exit()


