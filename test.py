from pysqlcipher3 import dbapi2 as sqlite
conn = sqlite.connect('test.db')
c = conn.cursor()
password = 'password'

c.execute(f"PRAGMA key='{password}'")

# c.execute('''create table IF NOT EXISTS stocks (date text, trans text, symbol text, qty real, price real)''')
# c.execute("""insert into stocks values ('2006-01-05','BUY','RHAT',100,35.14)""")
c.execute("""SELECT * FROM stocks""")
print(c.fetchall())
conn.commit()
c.close()