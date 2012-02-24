__author__ = 'jond'

import os
import sys


import settings
import wrapper.main

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    wrapper.main.start("http://127.0.0.1:8000/admin", settings.getfullpathtodb())
    sys.exit()



