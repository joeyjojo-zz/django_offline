from example import settings

__author__ = 'jond'

import os
import sys
import subprocess

os.environ['DJANGO_SETTINGS_MODULE'] = 'example.settings'

import wrapper.main
from django.core import management
from django.contrib.auth.models import User



def onetimestartup():
    # Check if database file exists
    if not os.path.exists(settings.getfullpathtodb()):
        # TODO: This should be changed to a subprocess and we should communicate to the pipe
        management.call_command("syncdb")
        # TODO: Figure out why this didnt work!
        #user = User.objects.create_user("admin", "a@b.com")
        #user.is_superuser = True
        #user.set_password('a')
        #user.save()



if __name__ == "__main__":
    onetimestartup()
    theproc = subprocess.Popen([sys.executable, "manage.py", "runserver"])
    wrapper.main.start("http://127.0.0.1:8000/admin/")
    #wrapper.main.start("http://www.google.com")
