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
        if self.readNames() == []:
            pass
        else:
            print(f'NAMES: {str(self.readNames())[1: -1]}')
    
    def initDB(self):
        c = self.conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS Names (
            Name CHAR UNIQUE NOT NULL PRIMARY KEY);
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS MMR (
            Time INT PRIMARY KEY ASC UNIQUE NOT NULL,
            Name CHAR REFERENCES Names (Name) MATCH [FULL] NOT NULL,
            MMR INT NOT NULL)
        WITHOUT ROWID;
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS BScore (
            Time INT PRIMARY KEY ASC UNIQUE  NOT NULL,
            Name CHAR REFERENCES Names (Name) MATCH [FULL] NOT NULL,
            BScore INT NOT NULL)
        WITHOUT ROWID;
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS Rank (
            Time INT PRIMARY KEY ASC UNIQUE NOT NULL,
            Name CHAR REFERENCES Names (Name) MATCH [FULL] NOT NULL,
            Rank INT NOT NULL)
        WITHOUT ROWID;
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS Percent (
            Time INT PRIMARY KEY ASC UNIQUE NOT NULL,
            Name CHAR REFERENCES Names (Name) MATCH [FULL] NOT NULL,
            Percent INT NOT NULL)
        WITHOUT ROWID;
        """)
        self.conn.commit()
        
        self.tables = ['MMR', 'BScore', 'Rank', 'Percent']

    def create(self, name: str, remove=False):
        c = self.conn.cursor()
        try:
            if remove is True and input('All existing data associated with this name will be erased. Do you want to continue? y/n ') == 'y':
                c.execute(f"""DELETE FROM Names WHERE Name="{name}";""")
                c.execute(f"""DELETE FROM MMR WHERE Name="{name}";""")
                c.execute(f"""DELETE FROM BScore WHERE Name="{name}";""")
                c.execute(f"""DELETE FROM Rank WHERE Name="{name}";""")
                c.execute(f"""DELETE FROM Percent WHERE Name="{name}";""")
            else:
                c.execute(f"""INSERT INTO Names (Name) VALUES ("{name}");""")
            self.conn.commit()
        except Exception as e:
            raise e
        finally:
            c.close()

    def write(self, name: str, tableName: str = None, data: int = None, remove=False):
        c = self.conn.cursor()
        try:
            if remove is True:
                mmr = ('MMR', self._read2(c.execute(f"""SELECT Time FROM MMR WHERE Name="{name}" ORDER BY Time DESC LIMIT 1;""").fetchall()))
                bScore = ('BScore', self._read2(c.execute(f"""SELECT Time FROM BScore WHERE Name="{name}" ORDER BY Time DESC LIMIT 1;""").fetchall()))
                rank = ('Rank', self._read2(c.execute(f"""SELECT Time FROM Rank WHERE Name="{name}" ORDER BY Time DESC LIMIT 1;""").fetchall()))
                percent = ('Percent', self._read2(c.execute(f"""SELECT Time FROM Percent WHERE Name="{name}" ORDER BY Time DESC LIMIT 1;""").fetchall()))
                data = [mmr, bScore, rank, percent]
                data.sort(key=self._sort, reverse=True)
                last = data[0]
                if input(f'Last record for \"{name}\" in {last[0]} will be erased. Do you want to continue? y/n ') == 'y':
                    c.execute(f"""DELETE FROM {last[0]} WHERE Time={last[1]};""")
            else:
                c.execute(f"""INSERT INTO "{tableName}" (Time, Name, {tableName}) VALUES (?, ?, ?)""", (int(time.time()), str(name), int(data)))
            self.conn.commit()
        except Exception as e:
            raise e
        finally:
            c.close()
    
    def read(self, name: str) -> dict:
        c = self.conn.cursor()
        try:
            mmr = c.execute(f"""SELECT MMR FROM MMR WHERE Name="{name}" ORDER BY Time DESC LIMIT 1;""").fetchall()
            bScore = c.execute(f"""SELECT BScore FROM BScore WHERE Name="{name}" ORDER BY Time DESC LIMIT 1;""").fetchall()
            rank = c.execute(f"""SELECT Rank FROM Rank WHERE Name="{name}" ORDER BY Time DESC LIMIT 1;""").fetchall()
            percent = c.execute(f"""SELECT Percent FROM Percent WHERE Name="{name}" ORDER BY Time DESC LIMIT 1;""").fetchall()
            data = dict(zip(self.tables, list(map(self._read2, [mmr, bScore, rank, percent]))))
            return data
        except Exception as e:
            raise e
        finally:
            c.close()

    def readNames(self, name=None) -> list:
        c = self.conn.cursor()
        try:
            if name is not None:
                return self._read2(c.execute(f"""SELECT Name FROM Names WHERE Name = "{name}" LIMIT 1;""").fetchall())
            else:
                names = c.execute(f"""SELECT Name FROM Names ORDER BY Name ASC;""").fetchall()
                return list(map(self._read, names))
        except Exception as e:
            raise e
        finally:
            c.close()

    def readLast(self) -> str:
        c = self.conn.cursor()
        try:
            data = []
            data.extend(c.execute(f"""SELECT Time, Name FROM MMR ORDER BY Time DESC LIMIT 1;""").fetchall())
            data.extend(c.execute(f"""SELECT Time, Name FROM BScore ORDER BY Time DESC LIMIT 1;""").fetchall())
            data.extend(c.execute(f"""SELECT Time, Name FROM Rank ORDER BY Time DESC LIMIT 1;""").fetchall())
            data.extend(c.execute(f"""SELECT Time, Name FROM Percent ORDER BY Time DESC LIMIT 1;""").fetchall())
            data.sort(key=lambda x: x[0], reverse=True)
            if data == []:
                return self.readNames()
            else:
                return [data[0][1]]
        except Exception as e:
            raise e
        finally:
            c.close()

    @staticmethod
    def _sort(l: list or tuple) -> object:
        if l[1] is not None:
            return l[1]
        else:
            return 0

    @staticmethod
    def _read(l: list or tuple) -> object:
        try:
            return l[0]
        except IndexError:
            return None

    @staticmethod
    def _read2(l: list or tuple) -> object:
        try:
            return l[0][0]
        except IndexError:
            return None


class Core(Data):
    t = r'(\D|)\s?(.*)'
    exe = True
    commands = ('e', 'c', 'd', 'r', 'n', 's', 'i', 'h', '', 'b', 'r', 'p')
    h = '''Commands:
           h - Help
           e - Exit
           c - Create a name
           d - Delete a name
           r - Delete the last record for a current name
           s - Set a current name
           n - List of names
           i - Name info
             - Create an MMR record for a current name
           b - Create a BScore record for a current name
           r - Create a Rank record for a current name
           p - Create a Percent record a for current name
        Syntax:
           2400 - Create an MMR record with a value 2400 for a current name
           c В раю без изменений or cВ раю без изменений - Create a name \'В раю без изменений\'
           b7800 or b 7800 - Create a BScore record with a value 7800
           '''
    
    def __init__(self, *args):
        super().__init__(*args)
        self.__class__.currentName = super().readLast()
        if super().readLast() is None:
            print(self.h)
            print(self.__class__.currentName)
        else:
            try:
                self.__class__.currentName[0]
                self.__class__.currentName.extend(self.readNames().remove(super().readLast()))
            except:
                print(self.h)
                self.__class__.currentName = [None]
        self.info()
    
    @classmethod
    def parse(cls, data: str):
        try:
            return re.fullmatch(cls.t, data).groups()
        except Exception as e:
            return e
    
    def info(self):
        print(f'CURRENT NAME: \'{self.__class__.currentName[0]}\'')
        print('LAST RECORD:', str(self.read(self.__class__.currentName[0]))[1: -1])
    
    def execute(self, command: str, data: str = None):
        cls = self.__class__
        try:
            if command == cls.commands[0]:
                cls.exe = False
            elif command == cls.commands[1]:
                super().create(data)
                try:
                    cls.currentName.insert(0, super().readNames(data))
                except:
                    pass
                names = super().readNames()
                print(f'NAMES: {str(self.readNames())[1: -1]}')
                print(f'CURRENT NAME: {cls.currentName[0]}')
                last = str(super().read(cls.currentName[0]))
                print('LAST RECORD:', last[1: -1])
            elif command == cls.commands[2]:
                super().create(data, remove=True)
                cls.currentName.pop(0)
                names = super().readNames()
                print(f'NAMES: {str(self.readNames())[1: -1]}')
            elif command == cls.commands[3]:
                self.write(cls.currentName[0], remove=True)
                print(cls.currentName)
                self.info()
            elif command == cls.commands[4]:
                names = super().readNames()
                print(f'NAMES: {str(self.readNames())[1: -1]}')
            elif command == cls.commands[5]:
                try:
                    cls.currentName[0] = super().readNames(data)
                    print(f'CURRENT NAME: {cls.currentName[0]}')
                    last = str(super().read(cls.currentName[0]))
                    print('LAST RECORD:', last[1: -1])
                except Exception as e:
                    raise e
                    print(f'Name \'{data}\' doesn\'t exist')
            elif command == cls.commands[6]:
                self.info()
            elif command == cls.commands[7]:
                print(cls.h)
            elif command == cls.commands[8]:
                super().write(name=cls.currentName[0], tableName=self.tables[0], data=data)
                self.info()
            elif command == cls.commands[9]:
                super().write(name=cls.currentName[0], tableName=self.tables[1], data=data)
                self.info()
            elif command == cls.commands[10]:
                super().write(name=cls.currentName[0], tableName=self.tables[2], data=data)
                self.info()
            elif command == cls.commands[11]:
                super().write(name=cls.currentName[0], tableName=self.tables[3], data=data)
                self.info()
            else:
                print('Command doesn\'n exist')
                # raise AttributeError(command)
        except Exception as e:
            raise e


def main(workDir):
    core = Core(workDir)

    while core.exe:
        cd = core.parse(input('\nEnter command and data: '))
        core.execute(cd[0], cd[1])


if __name__ == '__main__':
    main(os.path.dirname(sys.argv[0]))
    # try:
    #     main(os.path.dirname(sys.argv[0]))
    # except Exception as e:
    #     print(e)
    #     input('Press Enter to exit')
