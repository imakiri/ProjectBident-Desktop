import json
import re
import sqlite3
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
        CREATE TABLE Names (
            Name CHAR UNIQUE
                    NOT NULL
                    PRIMARY KEY
        );
        """)
        c = self.conn.cursor()
        c.execute("""
        CREATE TABLE MMR (
            Time INT PRIMARY KEY ASC
                    UNIQUE
                    NOT NULL,
            Name CHAR REFERENCES Names (Name) MATCH [FULL]
                    NOT NULL,
            MMR INT NOT NULL
        )
        WITHOUT ROWID;
        """)
        c = self.conn.cursor()
        c.execute("""
        CREATE TABLE BScore (
            Time INT PRIMARY KEY ASC
                    UNIQUE
                    NOT NULL,
            Name CHAR REFERENCES Names (Name) MATCH [FULL]
                    NOT NULL,
            BScore INT NOT NULL
        )
        WITHOUT ROWID;
        """)
        c = self.conn.cursor()
        c.execute("""
        CREATE TABLE Rank (
            Time INT PRIMARY KEY ASC
                    UNIQUE
                    NOT NULL,
            Name CHAR REFERENCES Names (Name) MATCH [FULL]
                    NOT NULL,
            Rank INT NOT NULL
        )
        WITHOUT ROWID;
        """)
        c = self.conn.cursor()
        c.execute("""
        CREATE TABLE Percent (
            Time INT PRIMARY KEY ASC
                    UNIQUE
                    NOT NULL,
            Name CHAR REFERENCES Names (Name) MATCH [FULL]
                    NOT NULL,
            Percent INT NOT NULL
        )
        WITHOUT ROWID;
        """)
        self.conn.commit()
    
        self.tables = {
            '': 'MMR',
            'b': 'BScore',
            'r': 'Rank',
            'p': 'Percent'
        }

    def initSettings(self):
        default = {
            'default table': 0
        }
        try:
            s = open(f'{self.workDir}/settings.json', 'r+')
            settings = json.load(s)
            self.settings = json.load(s)
            settings['default table']
            print('Settings has been loaded')
        except json.decoder.JSONDecodeError:
            json.dump(default, open(f'{self.workDir}/settings.json', 'w+'))
            s = open(f'{self.workDir}/settings.json', 'r')
            self.settings = json.load(s)
            print('Settings has been restored to default')
        except FileNotFoundError:
            json.dump(default, open(f'{self.workDir}/settings.json', 'w+'))
            s = open(f'{self.workDir}/settings.json', 'r')
            self.settings = json.load(s)
            print('Settings has been restored to default')
        except Exception as e:
            print(e)
            exe = False
            pass

    def changeSettings(self, name: str, value: int):
        self.settings: dict
        self.settings[name] = value
        try:
            s = open(f'{self.workDir}/settings.json', 'w+')
            json.dump(self.settings, s)
        except Exception as e:
            print(e)

    def write(self, tableCode: str, name: str, data: int):
        c = self.conn.cursor()
        t = self.tables[tableCode]
        sqlQ = f'''INSERT INTO "{t}"(Time, Name, {t}) VALUES (?, ?, ?)'''
        c.execute(sqlQ, [int(time.time()), name, data])
        self.conn.commit()
        print('Done')

    def readLast(self, table: str):
        ###################################################################################
        c = self.conn.cursor()
        sqlQ = f'SELECT * FROM "Dota2 {table}" ORDER BY Time DESC LIMIT 4'
        data = c.execute(sqlQ).fetchall()
        try:
            return list(map(lambda y: list(filter(lambda x: x is not None, y))[0], zip(*data)))
        except:
            return None
        ###################################################################################


def main(workDir):
    db = LocalStorage(workDir)
    tables = {}
    c = db.settings['Last name']
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
            t = r'(\D).*|(\d{1,5})|b(\d{1,5})|r(\d{2})|p(\d{1,3})'
            r = re.fullmatch(t, tmp).groups()
        except:
            print('Wrong command\data\n')
        
        if r[0] == 'e':
            exe = False
            break
        elif r[0] == 'n':
            c = (c + 1) % len(tables)
            print(
                '------------------------------------------------------------------------------------------------------------------------')
        elif r[0] == 'd':
            c = (c + 1) % len(tables)
            db.changeSettings('default table', c)
            print(
                '------------------------------------------------------------------------------------------------------------------------')
        elif r[0] == '':
            try:
                db.write(r[0], )
                print(
                    '------------------------------------------------------------------------------------------------------------------------')


if __name__ == '__main__':
    pass
    # try:
    #     main(os.path.dirname(sys.argv[0]))
    # except Exception as e:
    #     print(e)
    #     input('Press Enter to exit')
