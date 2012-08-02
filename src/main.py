__author__ = 'jond'

import sys
import os

from PyQt4 import QtCore, QtGui

import django_offline.frame

if __name__ == '__main__':
    # set up django settings
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
    # start up the model
    #setup_all(True)
    #create_all()
    # start up qt
    app = QtGui.QApplication(sys.argv)
    win = django_offline.frame.MainWindow()
    win.show()
    u = QtCore.QUrl('http://127.0.0.1:8000')
    win.setUrl(u)
    sys.exit(app.exec_())