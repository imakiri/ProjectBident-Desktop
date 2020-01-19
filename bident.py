import sys
import os
import time
import multiprocessing
import ast
import urllib.parse
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import *

import bidentCore


class Launcher(QObject):
    
    def __init__(self, argv):
        super(Launcher, self).__init__()
        self.arguments = argv
        
        self.si = QApplication(self.arguments)
        self.isSecondInstance = False
        self.isSocketConnected = False
        self.socket = QLocalSocket()
        
        self.processArguments()
        self.singleInstanceChecked()
        
        self.server = QLocalServer()
        self.server.newConnection.connect(self.newInstanceConnected)
        self.server.listen("Bident Server")
    
    def processArguments(self):
        try:
            temp = urllib.parse.urlparse(self.arguments[1])
            if temp[0] == 'bident':
                self.argDict = urllib.parse.parse_qs(temp[4])
        except:
            self.argDict = []
    
    def singleInstanceChecked(self):
        self.socket.connectToServer("Bident Server", QIODevice.ReadWrite)
        self.socket.readyRead.connect(self.socketConnected)
        self.socket.waitForReadyRead(5000)
        if self.isSocketConnected:
            self.socketWritten(self.argDict)
            self.socket.disconnectFromServer()
            self.isSecondInstance = True
        else:
            pass
    
    def socketConnected(self):
        response = self.socket.readAll().data().decode('utf-8')
        if response == 'Connected':
            self.isSocketConnected = True
        else:
            self.socket.disconnectFromServer()
            raise ConnectionError
    
    def socketWritten(self, data):
        self.socket.write(bytes(str(data), encoding='utf-8'))
    
    def socketReading(self):
        self.data = ast.literal_eval(self.socket.readAll().data().decode('utf-8'))
        print(self.data)
    
    def newInstanceConnected(self):
        print('newInstanceConnected')
        self.socket = self.server.nextPendingConnection()
        self.socket.write(b'Connected')
        self.socket.readyRead.connect(self.socketReading)
    
    def launchApplication(self):
        self.app = bidentCore.App(self.arguments)
        self.app.exec_()

if __name__ == '__main__':
    launcher = Launcher(sys.argv)
    if not launcher.isSecondInstance:
        launcher.launchApplication()
    else:
        pass
