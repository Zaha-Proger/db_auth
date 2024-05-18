import textwrap
import platform
from os import path
from subprocess import run, STDOUT, PIPE
from db import DB

db = DB("./auth_db.sqlite")

# db.cursor.execute("""
#                     CREATE VIEW IF NOT EXISTS auth_with_date AS
#                     SELECT * FROM authInfo
#                     INNER JOIN date ON authInfo.date_id = date.id_date
# """)
# db.db.commit()
db.cursor.execute("""
                  CREATE VIEW IF NOT EXISTS wtmp_with_date AS
                  SELECT
                    btmp_wtmpInfo.user,
                    btmp_wtmpInfo.tty,
                    btmp_wtmpInfo.host,
                    date.day_week,
                    date.month,
                    date.day,
                    btmp_wtmpInfo.time,
                    btmp_wtmpInfo.session 
                    FROM btmp_wtmpInfo
                    INNER JOIN date
                    ON btmp_wtmpInfo.date_id = date.id_date
                    WHERE btmp_wtmpInfo.FLAG = 0
""")
db.cursor.execute("""
                  SELECT * FROM wtmp_with_date
""")
list = db.cursor.fetchall()
for l in list:
    print(l)


# info_os = platform.freedesktop_os_release()
# # перенаправляем `stdout` и `stderr` в переменную `output`
# output = run("last", stdout=PIPE, stderr=STDOUT, text=True, shell=True)
# list = output.stdout.split("\n")
# result_info = []
# result_date = []
# for i in range(len(list)-2):
#     result_date.append((
#         list[i][43:46],
#         list[i][47:49],
#         list[i][39:42]
#     ))
#     result_info.append((
#         list[i][:9], 
#         list[i][9:22], 
#         list[i][22:39], 
#         list[i][39:42], 
#         list[i][43:46], 
#         list[i][47:49], 
#         list[i][50:63], 
#         list[i][64:]
#     ))

# print(tuple(set(result_date)))
# db.insert_date_db(tuple(set(result_date)))
# print(result_info[0][0], result_info[0][1])

# for i in range(len(result_info)-1):
#     db.cursor.execute(f"SELECT id_date FROM date WHERE month = '{result_info[i][4]}' AND day = '{result_info[i][5]}'")
#     id_date = db.cursor.fetchone()
#     print(result_info[i][5], result_info[i][6])
#     print(int(id_date[0]))
#     print(result_info[i][0])
#     print(result_info[i][1])
#     print(result_info[i][2])
#     print(result_info[i][3])
#     print(result_info[i][6])
#     print(result_info[i][7])
#     db.cursor.execute(f"INSERT INTO btmp_wtmpInfo (user, tty, host, date_id, time, session, flag) VALUES (?, ?, ?, ?, ?, ?, ?)", (result_info[i][0],result_info[i][1],result_info[i][2], int(id_date[0]),result_info[i][6], result_info[i][7], False))
# db.cursor.execute("DELETE FROM btmp_wtmpInfo WHERE rowid NOT IN (SELECT MIN(rowid) FROM btmp_wtmpInfo GROUP BY user, tty, host, date_id, time, session, flag);")

# print("---------------------------------------------------")
# print("btmp")
# print("---------------------------------------------------")

# output = run("pkexec lastb", stdout=PIPE, stderr=STDOUT, text=True, shell=True)
# list = output.stdout.split("\n")
# result_info = []
# result_date = []
# for i in range(len(list)-2):
#     result_date.append((
#         list[i][43:46],
#         list[i][47:49],
#         list[i][39:42]
#     ))
#     result_info.append((
#         list[i][:9], 
#         list[i][9:22], 
#         list[i][22:39], 
#         list[i][39:42], 
#         list[i][43:46], 
#         list[i][47:49], 
#         list[i][50:63], 
#         list[i][64:]
#     ))

# print(tuple(set(result_date)))
# db.insert_date_db(tuple(set(result_date)))

# for i in range(len(result_info)-1):
#     db.cursor.execute(f"SELECT id_date FROM date WHERE month = '{result_info[i][4]}' AND day = '{result_info[i][5]}'")
#     id_date = db.cursor.fetchone()
#     print(result_info[i][5], result_info[i][6])
#     print(int(id_date[0]))
#     print(result_info[i][0])
#     print(result_info[i][1])
#     print(result_info[i][2])
#     print(result_info[i][3])
#     print(result_info[i][6])
#     print(result_info[i][7])
#     db.cursor.execute(f"INSERT INTO btmp_wtmpInfo (user, tty, host, date_id, time, session, flag) VALUES (?, ?, ?, ?, ?, ?, ?)", (result_info[i][0],result_info[i][1],result_info[i][2], int(id_date[0]),result_info[i][6], result_info[i][7], True))
# db.cursor.execute("DELETE FROM btmp_wtmpInfo WHERE rowid NOT IN (SELECT MIN(rowid) FROM btmp_wtmpInfo GROUP BY user, tty, host, date_id, time, session, flag);")

# db.db.commit()











