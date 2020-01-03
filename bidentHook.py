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


class Launcher(QApplication):
    
    def __init__(self, args):
        super(Launcher, self).__init__(args)
        
        self.setApplicationName('DotaBident')
        self.exePath = self.arguments()[0]
        self.exeDir = os.path.dirname(self.exePath)
        self.isSecondInstance = False
        self.isSocketConnected = False
        self.socket = QLocalSocket()
        
        self.processArguments()
        self.singleInstanceChecked()
        
        self.server = QLocalServer()
        self.server.newConnection.connect(self.newInstanceConnected)
        self.server.listen("Bident Server")
    
    def processArguments(self):
        self.argParser = argparse.ArgumentParser(description='Bident Parser')
        self.argParser.add_argument('-debug', action="store_true", default=False)
        self.argParser.add_argument('-token', action="store")
        self.argDict = vars(self.argParser.parse_args())
    
    def singleInstanceChecked(self):
        self.socket.connectToServer("Bident Server", QIODevice.ReadWrite)
        self.socket.readyRead.connect(self.socketConnected)
        self.socket.waitForReadyRead(500)
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
        if self.data['token'] is not None:
            print(self.data['token'])
    
    def newInstanceConnected(self):
        self.socket = self.server.nextPendingConnection()
        self.socket.write(b'Connected')
        self.socket.readyRead.connect(self.socketReading)
    
    def launchApplication(self):
        pass


if __name__ == '__main__':
    app = Launcher(sys.argv)
    if not app.isSecondInstance:
        app.exec_()
    else:
        pass
