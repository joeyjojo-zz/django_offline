Django-offline
==============

Overview
--------
This project allows you to use django as way to develop a desktop application.
The django app is rendered in a QWebView and you should be able to develop the django app in the same way you normally would.

Caveats
-------
Deletion does not work

Dependencies
------------
- Python27* 
- PyQt4
- Django

Build
-----
python main.py

Footnotes
-----

* specifically 2.7.3. 2.7.2 appears to have a bug in it with cStringIO adding additional white space on reads. 2.7.2 can be made to work by replacing cStringIO with StringIO.