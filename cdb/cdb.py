import os
import re
import sqlite3
import sys
import time


class Data():
    
    def __init__(self, workDir):
        self.workDir = workDir
        self.conn = sqlite3.connect(f'{self.workDir}/data.db')
        self.initDB()
    
    def initDB(self):
        c = self.conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS Names (
            Name CHAR UNIQUE
                    NOT NULL
                    PRIMARY KEY
        );
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS MMR (
            Time INT PRIMARY KEY ASC
                    UNIQUE
                    NOT NULL,
            Name CHAR REFERENCES Names (Name) MATCH [FULL]
                    NOT NULL,
            MMR INT NOT NULL
        )
        WITHOUT ROWID;
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS BScore (
            Time INT PRIMARY KEY ASC
                    UNIQUE
                    NOT NULL,
            Name CHAR REFERENCES Names (Name) MATCH [FULL]
                    NOT NULL,
            BScore INT NOT NULL
        )
        WITHOUT ROWID;
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS Rank (
            Time INT PRIMARY KEY ASC
                    UNIQUE
                    NOT NULL,
            Name CHAR REFERENCES Names (Name) MATCH [FULL]
                    NOT NULL,
            Rank INT NOT NULL
        )
        WITHOUT ROWID;
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS Percent (
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
        
        self.tables = ['MMR', 'BScore', 'Rank', 'Percent']
    
    def create(self, name: str):
        c = self.conn.cursor()
        try:
            c.execute(f"""
            INSERT INTO Names (Name)
            VALUES ('{name}');
            """)
            self.conn.commit()
        except Exception as e:
            return e
    
    def write(self, tableName: str, name: str, data: int):
        c = self.conn.cursor()
        try:
            c.execute(f'''INSERT INTO "{t}"(Time, Name, {t}) VALUES (?, ?, ?)''',
                      [int(time.time()), str(name), int(data)])
            self.conn.commit()
        except Exception as e:
            return e
    
    def read(self, name: str) -> dict:
        try:
            c = self.conn.cursor()
            mmr = c.execute(f"""SELECT MMR FROM MMR WHERE Name = '{name}' ORDER BY Time DESC LIMIT 1;""").fetchall()
            bScore = c.execute(
                f"""SELECT BScore FROM BScore WHERE Name = '{name}' ORDER BY Time DESC LIMIT 1;""").fetchall()
            rank = c.execute(f"""SELECT Rank FROM Rank WHERE Name = '{name}' ORDER BY Time DESC LIMIT 1;""").fetchall()
            percent = c.execute(
                f"""SELECT Percent FROM Percent WHERE Name = '{name}' ORDER BY Time DESC LIMIT 1;""").fetchall()
            data = dict(zip(self.tables, list(map(self._read, [mmr, bScore, rank, percent]))))
            return data
        except Exception as e:
            return e
    
    def readNames(self) -> list:
        return ['']
    
    def readLast(self) -> str:
        return 'a'
    
    @staticmethod
    def _read(l: list or tuple) -> object:
        try:
            return l[0][0]
        except IndexError:
            return None


class Core(Data):
    t = r'(\D)(?:\S|\s+)(\w+)|(/1)(\d+)'
    exe = True
    
    def __init__(cls, *args):
        super().__init__(*args)
        cls.last = super().readLast()
    
    @classmethod
    def parse(cls, data: str):
        try:
            return re.fullmatch(cls.t, data).groups()
        except Exception as e:
            return e
    
    @classmethod
    def execute(cls, command: str, data):
        try:
            if command == 'e':
                cls.exe = False
                return Exception
            elif command == 'c':
                if type(data) != str:
                    raise AttributeError(data)
                super().create(data)
            elif command == 'p':
                names = super().readNames()
                print(names)
            elif command == 'h':
                help = ''
                print(help)
            elif command == '':
                if type(data) != list or tuple:
                    raise AttributeError(data)
                super().write(data)
            else:
                print('Command doesn\'n exist')
                raise AttributeError(command)
        except Exception as e:
            print(e)


def main(workDir):
    core = Core(workDir)
    
    while core.exe:
        print(f'Table: {core.last}')
        print('Last record:', str(core.read(core.last))[1: -1])
        c = core.parse(input('Enter command and data: '))
        print(c)
        # core.execute()
        # break


if __name__ == '__main__':
    main(os.path.dirname(sys.argv[0]))
    # try:
    #     main(os.path.dirname(sys.argv[0]))
    # except Exception as e:
    #     print(e)
    #     input('Press Enter to exit')
