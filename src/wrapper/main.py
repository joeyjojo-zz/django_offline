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
from gevent import monkey

import views.wwebview
from example import settings

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
    print "in main loop"
    while True:
        app.processEvents()
        while app.hasPendingEvents():
            app.processEvents()

            gevent.sleep()

        gevent.sleep() # don't appear to get here but cooperate again

def get_handler(*args, **options):
    """
    Returns the default WSGI handler for the runner.
    """
    return WSGIHandler()

def djangostartup(*args, **options):
    """

    """
    print "in django startup"
    # Check if database file exists
    if not os.path.exists(settings.getfullpathtodb()):
        # TODO: This should be changed to a subprocess and we should communicate to the pipe
        management.call_command("syncdb")
        # TODO: Figure out why this didnt work!
        #user = User.objects.create_user("admin", "a@b.com")
        #user.is_superuser = True
        #user.set_password('a')
        #user.save()
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    #management.call_command("runserver")

    #application = django.core.handlers.wsgi.WSGIHandler()
    #print 'Listening on port %s and on port 843 (flash policy server)' % PORT
    #SocketIOServer(('', PORT), application, resource="socket.io").serve_forever()
    handler = get_handler(*args, **options)
    run('', PORT, handler)

def start(uri=None):
    """
    Start the QT application
    @param uri: The uri to load in as default (i.e. the home page of the application
    @type uri: str
    """
    app = QtGui.QApplication(sys.argv)
    gevent.joinall([gevent.spawn(djangostartup),
                    gevent.spawn(mainloop, app, uri),
                    ])
    #djangostartup()


