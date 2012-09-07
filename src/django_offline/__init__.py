import os
import sys

from PyQt4 import QtGui, QtCore
from django.core.management import call_command

def run(start_url):
    # set up django settings
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
    # then do django related importas
    import django_offline.frame
    # set up the database
    start_db()
    # start up qt
    app = QtGui.QApplication(sys.argv)
    # allow debugging via pdb
    QtCore.pyqtRemoveInputHook()
    # setup the window
    win = django_offline.frame.MainWindow()
    win.show()
    win.setUrl(start_url)
    return app.exec_()

def start_db():
    # setup the database on startup
    # should probably put checks here to make sure we don't do daft things
    # maybe integrate 'south'?
    call_command('syncdb', interactive=False,)