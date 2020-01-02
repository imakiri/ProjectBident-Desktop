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

if __name__ == '__main__':
    
    socket = QLocalSocket()
    socket.connectToServer("Bident Server", QIODevice.WriteOnly)