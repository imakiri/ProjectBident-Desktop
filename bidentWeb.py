import sys
import os
import time
import multiprocessing
import argparse
import ast
import yaml
from openapi3 import OpenAPI
from pyswagger import App, Security
from pyswagger.contrib.client.requests import Client
from pyswagger.utils import jp_compose

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import *

class Cookie(QNetworkCookie):
    
    def __init__(self, parent=None):
        super(Cookie, self).__init__(parent)
        
        
class Stratz(QNetworkAccessManager):
    
    def __init__(self, parent=None):
        super(Stratz, self).__init__(parent)
        
        self.initOpenAPI()
        
    def initOpenAPI(self):
        with open('stratzAPI.yaml') as f:
            spec = yaml.safe_load(f.read())
        app = App._create_('spec')
        auth = Security
            