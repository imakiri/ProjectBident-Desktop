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
        
        self.conn = sqlite3.connect('data.db')
        self.c = self.conn.cursor()
        self.initDB()
        
    def initDB(self):
        self.c.execute("""
        CREATE TABLE IF NOT EXISTS `Settings` ()
        """)
        self.c.execute("""
        CREATE TABLE IF NOT EXISTS `Accounts` (
        `idAccount` INT NOT NULL,
        `Name` VARCHAR(64) NOT NULL,
        `Avatar` BLOB NULL,
        `Service` VARCHAR(64) NOT NULL,
        `Cookie` JSON NULL,
        `Date Added` TIMESTAMP NOT NULL,
        PRIMARY KEY (`idAccount`))
        """)
        self.c.execute("""
        CREATE TABLE IF NOT EXISTS `Services` (
        `idService` INT NOT NULL,
        `Name` VARCHAR(64) NULL,
        PRIMARY KEY (`idService`))
        """)
    
    def setSetting(self, id, key):
        pass
    
    def getSetting(self, id):
        pass
    
    def setAccount(self, name, service):
        pass
    
    def setAccountAvatar(self, name, image):
        pass
    
    def getAccountData(self, name):
        pass
    
    def getAccountsData(self):
        pass
    
    def setCookie(self, name, data):
        pass
    
    def getCookie(self, name):
        pass
    
    def setService(self, name, data):
        pass
    
    def getServiceData(self, name):
        pass

if __name__ == '__main__':
    db = LocalStorage()

        
    