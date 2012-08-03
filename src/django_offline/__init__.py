import os
import sys

from PyQt4 import QtGui, QtCore

def run(start_url):
    # set up django settings
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
    # then do django related importas
    import django_offline.frame
    # start up qt
    app = QtGui.QApplication(sys.argv)
    # allow debugging via pdb
    QtCore.pyqtRemoveInputHook()
    # setup the window
    win = django_offline.frame.MainWindow()
    win.show()
    u = QtCore.QUrl(start_url)
    #win.setUrl(u)
    return app.exec_()