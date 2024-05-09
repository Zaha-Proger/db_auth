import sqlite3 as sql

class DB:
    def __init__(self, path):
        if path != "":
            self.db = sql.connect(path)
            self.cursor = self.db.cursor()
            #удаление таблицы для дебага. не забуть удалить
            self.cursor.execute("""DROP TABLE IF EXISTS authInfo""")
            # id INTEGER PRIMARY KEY AUTOINCREMENT,
            self.cursor.execute("""CREATE TABLE authInfo(
                                date TEXT,
                                time TEXT,
                                proc TEXT,
                                desc TEXT
            )""")
            self.cursor.execute("""DROP TABLE IF EXISTS lastLogInfo""")
            # id INTEGER PRIMARY KEY AUTOINCREMENT,
            self.cursor.execute("""CREATE TABLE lastLogInfo(
                                user TEXT,
                                proc TEXT,
                                out TEXT,
                                day TEXT,
                                date TEXT,
                                time TEXT,
                                rangeTime TEXT
            )""")
            self.db.commit()
        else:
            print("Not path for DB")

    def insert_secure_db(self, info_list):
        self.cursor.executemany("INSERT INTO authInfo VALUES (?,?,?,?)", info_list)
        self.cursor.execute("DELETE FROM authInfo WHERE rowid NOT IN (SELECT MIN(rowid) FROM authInfo GROUP BY date, time, proc, desc);")
        self.db.commit()

    def insert_lastlog_db(self, lastlog_list):
        self.cursor.executemany("INSERT INTO lastLogInfo VALUES (?,?,?,?,?,?,?)", lastlog_list)
        self.cursor.execute("DELETE FROM lastLogInfo  WHERE rowid NOT IN (SELECT MIN(rowid) FROM lastLogInfo GROUP BY user, proc,out,day,date,time,rangeTime);")
        self.db.commit()

    def close_db(self):
        self.db.close()