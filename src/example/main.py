__author__ = 'jond'

import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'example.settings'

import wrapper.main

if __name__ == "__main__":
    wrapper.main.start("http://127.0.0.1:8000/admin")
    sys.exit()



