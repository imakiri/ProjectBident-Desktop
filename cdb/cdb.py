import re
import sqlite3
import time
from datetime import datetime as dt


class LocalStorage():
    
    def __init__(self):
        self.conn = sqlite3.connect('data.db')
        self.initDB()
    
    def initDB(self):
        c = self.conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS `Dota2 A` (
        `Time` INT NOT NULL,
        `MMR` INT,
        `BScore` INT,
        `Rank` INT,
        `Percent` INT,
        PRIMARY KEY (`Time`))
        """)
        c = self.conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS `Dota2 B` (
        `Time` INT NOT NULL,
        `MMR` INT,
        `BScore` INT,
        `Rank` INT,
        `Percent` INT,
        PRIMARY KEY (`Time`))
        """)
        self.conn.commit()
    
    def write(self, table: str, name: str, data: int):
        c = self.conn.cursor()
        names = {
            '': 'MMR',
            'b': 'BScore',
            'r': 'Rank',
            'p': 'Percent'
        }
        sqlQ = f'''INSERT INTO "Dota2 {table}"(Time, {names[name]}) VALUES (?, ?)'''
        c.execute(sqlQ, [int(time.time()), data])
        self.conn.commit()
        print('Done')
    
    def read(self, table: str):
        c = self.conn.cursor()
        sqlQ = f'SELECT * FROM "Dota2 {table}" ORDER BY Time DESC LIMIT 1'
        data = c.execute(sqlQ)
        try:
            return data.fetchall()[0]
        except:
            return None


if __name__ == '__main__':
    db = LocalStorage()
    tables = ['A', 'B']
    c = 1
    exe = True
    db.read('B')
    while exe:
        print(f'Current table: {tables[c]}')
        last = db.read(tables[c])
        try:
            print(
                f'Last record: | Date: {dt.fromtimestamp(last[0])} | MMR: {last[1]} | BScore: {last[2]} | Rank: {last[3]} | Percent: {last[4]} |')
        except:
            print('No records')
        
        tmp = input('Enter command\data: ')
        
        try:
            t = r'(e|n)|(|b|r|p)(\d{2,5})'
            r = re.fullmatch(t, tmp).groups()
        except:
            print('Wrong command\data')
        
        if r[0] == 'e':
            exe = False
            break
        elif r[0] == 'n':
            c = (c + 1) % len(tables)
        else:
            db.write(tables[c], r[1], int(r[2]))
