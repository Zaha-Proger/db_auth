import sqlite3 as sql

class DB:
    def __init__(self, path):
        if path != "":
            self.db = sql.connect(path)
            self.cursor = self.db.cursor()
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS authInfo(
                                date TEXT,
                                time TEXT,
                                proc TEXT,
                                desc TEXT
            )""")
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS lastLogInfo(
                                user TEXT,
                                tty TEXT,
                                host TEXT,
                                day TEXT,
                                date TEXT,
                                time TEXT,
                                session TEXT
            )""")
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS btmpLogInfo(
                                user TEXT,
                                tty TEXT,
                                host TEXT,
                                day TEXT,
                                date TEXT,
                                time TEXT,
                                session TEXT
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
        self.cursor.execute("DELETE FROM lastLogInfo  WHERE rowid NOT IN (SELECT MIN(rowid) FROM lastLogInfo GROUP BY user,tty,host,day,date,time,session);")
        self.db.commit()

    def insert_btmplog_db(self, btmplog_list):
        self.cursor.executemany("INSERT INTO btmpLogInfo VALUES (?,?,?,?,?,?,?)", btmplog_list)
        self.cursor.execute("DELETE FROM btmpLogInfo WHERE rowid NOT IN (SELECT MIN(rowid) FROM btmpLogInfo GROUP BY user,tty,host,day,date,time,session);")
        self.db.commit()

    def close_db(self):
        self.cursor.close()
        self.db.close()
        