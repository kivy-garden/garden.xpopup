"""
XPopup package.
Usefull extensions of the Popup class

Package Structure
=================

Modules:

* __init__.py: API imports

* xpopup.py: extension for the :class:`~kivy.uix.popup.Popup`

* xbase.py: contains the base class for all the xpopup classes (based on
  xpopup)

* notification.py: contains classes of the pop-up notifications

* form.py: contains classes of the UI-forms

* file.py: contains classes of the popup for file system browsing

* demo_app.py: contains demo application widget

* main.py, android.txt - files for `Kivy Launcher` on android

"""

from notification import XNotification, XConfirmation, XMessage, XError,\
    XProgress, XNotifyBase
from form import XSlider, XTextInput, XNotes, XAuthorization, XForm
from file import XFileOpen, XFileSave, XFolder, XFilePopup
from xbase import XBase
from xpopup import XPopup

__author__ = 'ophermit'

__version__ = '0.2'
