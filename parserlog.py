import textwrap
import platform
from os import path
from subprocess import run, STDOUT, PIPE

class ParseLog():
    def __init__(self, db):
        self.db = db
        self.cmd = ""

    def get_cmd(self, flag):
        if flag == 1:
            if path.exists("/var/log/secure"):
                self.cmd = "pkexec cat /var/log/secure*"
            else:
                self.cmd = "pkexec cat /var/log/auth.log*"
        elif flag == 2:
            self.cmd = "last"
        elif flag == 3:
            self.cmd = "pkexec lastb"

    def log_secure(self):
        self.get_cmd(1)

        # перенаправляем `stdout` и `stderr` в переменную `output`
        output = run(self.cmd, stdout=PIPE, stderr=STDOUT, text=True, shell=True)

        #записывается в список разделенная строка с разделителем \n
        list = output.stdout.split("\n")

        # заполнение списка списков, где каждый элемент -- строка, разбитая на части
        result = []
        for i in range(len(list)-1):
            text = textwrap.dedent(list[i][list[i].find(':', 15)+2:]).strip()
            result.append((
                        list[i][:6], 
                        list[i][7:15],
                        list[i][16:list[i].find(':', 15)],
                        textwrap.fill(text, width=120)
            ))

        self.db.insert_secure_db(result)

    def log_last(self):
        self.get_cmd(2)
        # перенаправляем `stdout` и `stderr` в переменную `output`
        output = run(self.cmd.split(), stdout=PIPE, stderr=STDOUT, text=True)
        list = output.stdout.split("\n")
        
        result = []
        for i in range(len(list)-3):
            result.append((
                                list[i][:9], 
                                list[i][9:22],
                                list[i][22:39],
                                list[i][39:42],
                                list[i][43:50],
                                list[i][50:63],
                                list[i][64:]
                    ))
        self.db.insert_lastlog_db(result)
        # db.close_db()

    def log_btmp(self):
        self.get_cmd(3)
        # перенаправляем `stdout` и `stderr` в переменную `output`
        output = run(self.cmd.split(), stdout=PIPE, stderr=STDOUT, text=True)
        list = output.stdout.split("\n")
        
        result = []
        for i in range(len(list)-3):
            result.append((
                                list[i][:9], 
                                list[i][9:22],
                                list[i][22:39],
                                list[i][39:42],
                                list[i][43:50],
                                list[i][50:63],
                                list[i][64:]
                    ))
        self.db.insert_btmplog_db(result)
