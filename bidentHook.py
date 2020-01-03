import sys
import os
import time
import math
import subprocess
from Pyro4 import *
from Pyro4.core import *
from Pyro4.naming import *

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import *


class Launcher(QApplication):
    
    def __init__(self, args):
        super(Launcher, self).__init__(args)

        self.socket = QLocalSocket()
        self.socket.connectToServer("Bident Server", QIODevice.ReadWrite)
        self.socket.readyRead.connect(self.socketConnected)

    def socketConnected(self):
        response = self.socket.readAll().data().decode('utf-8')
        if response == 'Connected':
            print('Connected')
        else:
            raise ConnectionError

if __name__ == '__main__':
    app = Launcher([])
    # socket.disconnectFromServer()
    app.exec_()