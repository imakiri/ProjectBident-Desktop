import sys
import os
import multiprocessing
from Pyro4.core import *
from Pyro4.naming import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class Init(object):
    
    def

@expose
class Service(object):

    @oneway
    def launch(self):
        print("Launch")


if __name__ == '__main__':
    
    deamon = Daemon(port=4560)
    uri = deamon.register(Service, "Bident", )
    print(uri)
    deamon.requestLoop()
