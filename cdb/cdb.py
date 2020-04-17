import json
import os
import re
import sqlite3
import sys
import time
from datetime import datetime as dt


class LocalStorage():
    
    def __init__(self, workDir):
        self.workDir = workDir
        self.conn = sqlite3.connect(f'{self.workDir}/data.db')
        self.initDB()
        self.initSettings()
    
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

    def initSettings(self):
        default = {
            'default table': 0
        }
        try:
            s = open('settings.json', 'r+')
            settings = json.load(s)
            settings['default table']
            print('Settings has been loaded')
        except json.decoder.JSONDecodeError:
            s = open('settings.json', 'r+')
            json.dump(default, s)
            print('Settings has been restored to default')
        except FileNotFoundError:
            s = open('settings.json', 'w+')
            json.dump(default, s)
            print('Settings has been restored to default')
        except Exception as e:
            print(e)
            exe = False
            pass

        self.s = s
        self.settings = json.load(s)

    def changeSettings(self, name: str, value: int):
        self.settings: dict
        self.settings[name] = value
        try:
            json.dump(self.settings, self.s)
        except Exception as e:
            print(e)

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

    def readLast(self, table: str):
        c = self.conn.cursor()
        sqlQ = f'SELECT * FROM "Dota2 {table}" ORDER BY Time DESC LIMIT 4'
        data = c.execute(sqlQ).fetchall()
        try:
            return list(map(lambda y: list(filter(lambda x: x is not None, y))[0], zip(*data)))
        except:
            return None


def main(workDir):
    db = LocalStorage(workDir)
    tables = ['A', 'B']
    c = db.settings['default table']
    exe = True
    
    while exe:
        print(f'Current table: {tables[c]}')
        last = db.readLast(tables[c])
        try:
            print(
                f'Last record: | Date: {dt.fromtimestamp(last[0])} | MMR: {last[1]} | BScore: {last[2]} | Rank: {last[3]} | Percent: {last[4]} |')
        except:
            print('No records')
        
        tmp = input('Enter command\data: ')
        
        try:
            t = r'(e|n|d)|(|b|r|p)(\d{2,5})'
            r = re.fullmatch(t, tmp).groups()
        except:
            print('Wrong command\data\n')
        
        if r[0] == 'e':
            exe = False
            break
        elif r[0] == 'n':
            c = (c + 1) % len(tables)
            print(
                '-------------------------------------------------------------------------------------------------------------------------')
        elif r[0] == 'd':
            c = (c + 1) % len(tables)
            db.changeSettings('default table', c)
            print(
                '-------------------------------------------------------------------------------------------------------------------------')
        else:
            db.write(tables[c], r[1], int(r[2]))
            print(
                '-------------------------------------------------------------------------------------------------------------------------')


if __name__ == '__main__':
    main(os.path.dirname(sys.argv[0]))
    # try:
    #     main(os.path.dirname(sys.argv[0]))
    # except Exception as e:
    #     print(e)
    #     input('Press Enter to exit')
