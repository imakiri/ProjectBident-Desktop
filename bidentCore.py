import sys
import os
import multiprocessing
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import *


class Launcher(QApplication):
    
    def __init__(self, args):
        super(Launcher, self).__init__(args)
        
        self.setApplicationName("DotaBident")
        print(self.applicationDirPath())
        
        self.socket = QLocalSocket()
        self.server = QLocalServer()
        
        
        
    def socketConnected(self):
        pass
    
    def socketError(self):
        pass
    
    def socketDisconnected(self):
        pass
    
    def socketWritten(self, bytes):
        pass
    
    def socketReading(self):
        pass
    
    def newInstanceConnected(self):
        pass
    
    # def singleInstanceChecked(self):
    #     self.mainSocket.connectToServer("Bident", QIODevice.WriteOnly)
    #     if self.mainSocket.connected():
    #         pass
    #     else:
        
    def launchApplication(self):
        pass
    
        


if __name__ == '__main__':
    
    app = Launcher(sys.argv)
    app.exec_()
    