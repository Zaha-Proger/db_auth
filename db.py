import sqlite3 as sql

class DB:
    def __init__(self, path):
        if path != "":
            self.db = sql.connect(path)
            self.cursor = self.db.cursor()
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS date(
                                id_date INTEGER PRIMARY KEY AUTOINCREMENT,
                                month TEXT,
                                day TEXT,
                                day_week TEXT NULL
            )""")
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS authInfo(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                date_id INTEGER,
                                time TEXT,
                                proc TEXT,
                                desc TEXT,
                                FOREIGN KEY (date_id) REFERENCES date (id_date)
            )""")
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS btmp_wtmpInfo(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user TEXT,
                                tty TEXT,
                                host TEXT,
                                date_id INTEGER,
                                time TEXT,
                                session TEXT,
                                flag BOOL,
                                FOREIGN KEY (date_id) REFERENCES date (id_date)
            )""")
            self.db.commit()
        else:
            print("Not path for DB")

    def insert_secure_db(self, info_list):
        for i in range(len(info_list)-1):
            self.cursor.execute(f"SELECT id_date FROM date WHERE month = '{info_list[i][0]}' AND day = '{info_list[i][1]}'")
            id_date = self.cursor.fetchone()
            self.cursor.execute(f"INSERT INTO authInfo (date_id, time, proc, desc) VALUES (?,?,?,?)", (int(id_date), info_list[i][2], info_list[i][3], info_list[i][4]))
        self.cursor.execute("DELETE FROM authInfo WHERE rowid NOT IN (SELECT MIN(rowid) FROM authInfo GROUP BY date, time, proc, desc);")
        self.db.commit()

    def insert_BWtmp_db(self, info_list, flag):
        self.cursor.executemany("INSERT INTO btmp_wtmpInfo VALUES (?,?,?,?,?,?,?)", info_list)
        self.cursor.execute("DELETE FROM btmp_wtmpInfo WHERE rowid NOT IN (SELECT MIN(rowid) FROM btmp_wtmpInfo GROUP BY user,tty,host,day,date,time,session);")
        self.db.commit()
    
    def insert_date_db(self, info_list):
        self.cursor.executemany("REPLACE INTO date (month, day, day_week) VALUES (?, ?, ?)", info_list)
        self.cursor.execute("DELETE FROM date  WHERE rowid NOT IN (SELECT MIN(rowid) FROM date GROUP BY month, day, day_week);")
        self.db.commit()

    # def insert_btmplog_db(self, btmplog_list):
    #     self.cursor.executemany("INSERT INTO btmpLogInfo VALUES (?,?,?,?,?,?,?)", btmplog_list)
    #     self.cursor.execute("DELETE FROM btmpLogInfo WHERE rowid NOT IN (SELECT MIN(rowid) FROM btmpLogInfo GROUP BY user,tty,host,day,date,time,session);")
    #     self.db.commit()

    def close_db(self):
        self.cursor.close()
        self.db.close()
        