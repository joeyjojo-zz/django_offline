import sys
import py2exe
import os

"""
We need to do this so that py2exe includes the correct dlls in the dist folder.
"""

dllList = ('qtnetwork.pyd','qtxmlpatterns4.dll',)
origIsSystemDLL = py2exe.build_exe.isSystemDLL
def isSystemDLL(pathname):
    if os.path.basename(pathname).lower() in dllList:
        return 0
    return origIsSystemDLL(pathname)
py2exe.build_exe.isSystemDLL = isSystemDLL 

""" New for 3.0 build - bundle flag (experimental).
    If set to 1:
        bundle required files into the executable
        (including the zipfile)
"""
bundle = 0
if "bundle" in sys.argv[2:]:
    bundle = 1
    sys.argv.remove("bundle")

try:
    # if this doesn't work, try import modulefinder
    import py2exe.mf as modulefinder
    import win32com
    for p in win32com.__path__[1:]:
        modulefinder.AddPackagePath("win32com", p)
    for extra in ["win32com.shell"]: #,"win32com.mapi"
        __import__(extra)
        m = sys.modules[extra]
        for p in m.__path__[1:]:
            modulefinder.AddPackagePath(extra, p)
except ImportError:
    # no build path setup, no worries.
    pass

from distutils.core import setup


# SETUP PY2EXE PARAMETERS HERE:

script_list = [
    {'script':'%s.py' % 'main',
     'name':'BPT-RTI',
     'version':'0.0.0.1',
     'language':'en-gb',
     'company_name':'HM Revenue & Customs',
    }
]

options = {
    "py2exe": {
        "packages":["django.db", "django.middleware", "django.contrib", "django.template", "polls"],
        "includes": ["sip"],
        "excludes": ["wx"],
        "dll_excludes": ["w9xpopen.exe", "MSVCP90.dll"],
    }
}

zipfile = "python/main.zip"

options["py2exe"]["excludes"].append("Pennant.PennantDebug")

if bundle:
    zipfile = None
    options["py2exe"]["bundle_files"] = 1
    

setup(windows=script_list, options=options, zipfile=zipfile)