import textwrap
import platform
from os import path
from subprocess import run, STDOUT, PIPE
from db import DB

db = DB("./auth_db.sqlite")
info_os = platform.freedesktop_os_release()
# перенаправляем `stdout` и `stderr` в переменную `output`
output = run("pkexec cat /var/log/secure*", stdout=PIPE, stderr=STDOUT, text=True, shell=True)
for i in info_os.values():
    if "debian" in i.lower():
        list = output.stdout.split("\n")
        result = []
        for i in range(len(list)-1):
            text = textwrap.dedent(list[i][list[i].find(':', 40)+2:]).strip()
            result.append((
            list[i][:10], 
            list[i][11:27],
            list[i][40:list[i].find(' ', 40)],
            textwrap.fill(text, width=120)
            ))
        break
else:
#записывается в список разделенная строка с разделителем \n
    list = output.stdout.split("\n")
    result_date = []
    result_info = []
    for i in range(len(list)-1):
        text = textwrap.dedent(list[i][list[i].find(':', 15)+2:]).strip()
        result_date.append((
            list[i][:3], 
            list[i][4:6],
            "NULL"
        ))
        result_info.append((
            list[i][:3], 
            list[i][4:6],
            list[i][7:15],
            list[i][22:list[i].find(':', 21)],
            textwrap.fill(text, width=120)
        ))
print(tuple(set(result_date)))
db.insert_date_db(tuple(set(result_date)))
print(result_info[0][0], result_info[0][1])

for i in range(len(result_info)-1):
    db.cursor.execute(f"SELECT id_date FROM date WHERE month = '{result_info[i][0]}' AND day = '{result_info[i][1]}'")
    id_date = db.cursor.fetchone()
    print(result_info[i][0], result_info[i][1])
    print(int(id_date[0]))
    print(type(result_info[i][2]))
    print(result_info[i][3])
    print(result_info[i][4])
    db.cursor.execute(f"INSERT INTO authInfo (date_id, time, proc, desc) VALUES (?, ?, ?, ?)", (int(id_date[0]),result_info[i][2],result_info[i][3],result_info[i][4]))
db.cursor.execute("DELETE FROM authInfo WHERE rowid NOT IN (SELECT MIN(rowid) FROM authInfo GROUP BY date_id, time, proc, desc);")
db.db.commit()