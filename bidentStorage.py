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


class LocalStorage(QStorageInfo):
    
    def __init__(self, parent=None):
        super(LocalStorage, self).__init__(parent)