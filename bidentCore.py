import sys
import os
import time
import multiprocessing
import argparse
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import *


class Launcher(QApplication):
    
    def __init__(self, args):
        super(Launcher, self).__init__(args)
        
        self.setApplicationName('DotaBident')
        self.exePath = self.arguments()[0]
        self.exeDir = os.path.dirname(self.exePath)
        self.processArguments()
        # self.singleInstanceChecked()
        
   
        self.server = QLocalServer()
        
        
        self.server.newConnection.connect(self.newInstanceConnected)
   
        self.server.listen("Bident Server")
        
        
     
    def processArguments(self):
        self.argParser = argparse.ArgumentParser(description='Bident Parser')
        self.argParser.add_argument('-debug',
                                    action="store_true",
                                    default=False)
        self.argParser.add_argument('-token', action="store")
        self.argDict = vars(self.argParser.parse_args())
      
    def singleInstanceChecked(self):
        self.socket.connectToServer("Bident Server")
        time.sleep(1)
        self.socket.connected()
        
    def socketConnected(self):
        pass
    
    def socketError(self):
        pass
    
    def socketDisconnected(self):
        pass
    
    def socketWritten(self, bytes):
        pass
    
    def socketReading(self):
        data = self.socket.readAll()
        print(data)
    
    def newInstanceConnected(self):
        print("newInstanceConnected")
        self.socket = self.server.nextPendingConnection()
        self.socket.write(b'Connected')
        self.socket.readyRead.connect(self.socketReading)
        
        
    def launchApplication(self):
        pass
    
        


if __name__ == '__main__':

    app = Launcher(sys.argv)
    app.exec_()
    