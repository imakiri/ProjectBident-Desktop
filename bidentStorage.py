import re
import sqlite3
import time

from PyQt5.QtCore import *


class LocalStorage(QStorageInfo):
    
    def __init__(self, parent=None):
        super(LocalStorage, self).__init__(parent)
        
        self.conn = sqlite3.connect('data.db')
        self.initDB()
    
    def initDB(self):
        c = self.conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS `Dota2 D` (
        `Time` INT NOT NULL,
        `MMR` INT,
        `BScore` INT,
        `Rank` INT,
        `Percent` INT,
        PRIMARY KEY (`Time`))
        """)
    
    def write(self, name: str, data: int):
        c = self.conn.cursor()
        if name == '' or 'mmr':
            sqlQ = '''INSERT INTO "Dota2 D"(Time, MMR) VALUES (?, ?)'''
        elif name == 'b':
            sqlQ = '''INSERT INTO "Dota2 D"(Time, BScore) VALUES (?, ?)'''
        elif name == 'r':
            sqlQ = '''INSERT INTO "Dota2 D"(Time, Rank) VALUES (?, ?)'''
        elif name == 'p':
            sqlQ = '''INSERT INTO "Dota2 D"(Time, Percent) VALUES (?, ?)'''
        else:
            print('Available names: /mmr, b, r, p')
        c.execute(sqlQ, [int(time.time()), data])
        self.conn.commit()
        print('Done')
    
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
    exe = True
    while exe:
        tmp = input('Enter command\data: ')
        t = r'(e)|(|b|r|p)(\d{2,4})'
        r = re.fullmatch(t, tmp).groups()
        if r[0] == 'e':
            exe = False
            break
        db.write(r[1], int(r[2]))
