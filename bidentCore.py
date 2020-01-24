import sys
import os
import time
import multiprocessing
import argparse
import ast
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import *

import bidentGUI
import bidentStorage


class App(QApplication):
    
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        
        self.exePath = self.arguments()[0] # Path to the program
        self.exeDir = os.path.dirname(self.exePath) # Path to dir
        
        self.setAppSettings()
        
        self.appSettings()
        
        gui = bidentGUI.GUI(self)
        gui.showWelcomeWindow()
        
        self.exec_()
        
    def appSettings(self):
        self.setWindowIcon(QIcon(f"{self.exeDir}\data\logo.ico"))
        styleFile = QFile(f"{self.exeDir}\data\S1.qss")
        styleFile.open(QFile.ReadOnly)
        style = QTextStream(styleFile)
        self.setStyleSheet(style.readAll())
        
    def dir(self):
        return self.exeDir
    
    def path(self):
        return self.exePath
    
    def quit(self):
        super(App, self).quit()


class Dota(QObject):
    
    def __init__(self, parent=None):
        super(Dota, self).__init__(parent)


