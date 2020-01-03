import sys
import os
import time
import math
from PySide2.QtWinExtras import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import *

class GUI(QObject):
    
    def __init__(self, parent):
        super(GUI, self).__init__(parent)
        
        self.guiSettings()
        
    def guiSettings(self):
        pass
        
    def showWelcomeWindow(self):
        pass

class WindowInterface(QWidget):
    
    def __init__(self, parent):
        super(WindowInterface, self).__init__()
        self.uiClass = parent
        self.coreClass = self.uiClass.parent()
    
    def ui(self):
        return self.uiClass
    
    def core(self):
        return self.coreClass


class UserLayer(QWidget):
    
    def __init__(self, parent=None):
        super(UserLayer, self).__init__(parent)


class ContentLayer():
    
    def __init__(self, parent=None):
        super(ContentLayer, self).__init__(parent)


class BackgroundLayerL(QLabel):
    
    def __init__(self, parent=None):
        super(BackgroundLayerL, self).__init__(parent)