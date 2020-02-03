import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import bidentDota
import bidentGUI
import bidentStorage


class App(QApplication):
    
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
    
        self.exePath = self.arguments()[0]  # Path to the program
        self.exeDir = os.path.dirname(self.exePath)  # Path to dir
        self.version = '15'
    
        self.setAppSettings()
        self.setApplicationVersion(self.version)
        # self.setStyle(ProxyStyle())
        
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
        try:
            super(App, self).quit()
            # QApplication.quit()
            sys.exit()
        except Exception as e:
            print(e)


class ProxyStyle(QProxyStyle):
    def drawControl(self, element, opt, painter, widget):
        if element == QStyle.CE_TabBarTabLabel:
            ic = self.pixelMetric(QStyle.PM_TabBarIconSize)
            r = QRect(opt.rect)
            w =  0 if opt.icon.isNull() else opt.rect.width() + self.pixelMetric(QStyle.PM_TabBarIconSize)
            r.setHeight(opt.fontMetrics.width(opt.text) + w)
            r.moveBottom(opt.rect.bottom())
            opt.rect = r
        QProxyStyle.drawControl(self, element, opt, painter, widget)


