"""
The main framework file
Starts up the application
"""
import time


__author__ = 'jond'

import sys
import os

from PySide import QtGui
import gevent
from django.core import management
from django.core.handlers.wsgi import WSGIHandler
from django.core.servers.basehttp import AdminMediaHandler, run, WSGIServerException
from django.contrib.staticfiles.handlers import StaticFilesHandler
from gevent import monkey
from greenlet import GreenletExit

import views.wwebview

monkey.patch_all()

PORT = 8000

def mainloop(app, uri):
    """
    This is necessary to cope with the gevent framework
    so we don't start the qt loop quite the same as we would normally
    @param app: The QT app to handle in gevent
    @type app: QtGui.QApplication
    """
    time.sleep(2)
    w = views.wwebview.WWebView()
    w.show()
    w.setUrl(uri)
    def handle_exit():
        raise GreenletExit
    w.onclose.connect(handle_exit)
    while True:
        app.processEvents()
        #while app.hasPendingEvents():
        #    app.processEvents()
        #    gevent.sleep()
        gevent.sleep() # don't appear to get here but cooperate again

def get_handler(*args, **options):
    """
    Returns the default WSGI handler for the runner.
    """
    return StaticFilesHandler(WSGIHandler())

def djangostartup(*args, **options):
    """
    Starts up the django server, but in a way we have control over
    """
    handler = get_handler(*args, **options)
    run('', PORT, handler)

def start(uri=None, dbpath=None):
    """
    Start the QT application
    @param uri: The uri to load in as default (i.e. the home page of the application
    @type uri: str
    """
    app = QtGui.QApplication(sys.argv)
    # Check if database file exists
    if not os.path.exists(dbpath):
        # TODO: This should be changed to a subprocess and we should communicate to the pipe
        management.call_command("syncdb")
    gevent.joinall([gevent.spawn(djangostartup, dbpath=dbpath),
                    gevent.spawn(mainloop, app, uri),
                    ])
