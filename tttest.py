from random import *
import sqlite3


n = 0
con = sqlite3.connect('databaze.sqlite')
cur = con.cursor()
result = cur.execute(f"""SELECT * FROM data""").fetchall()

print(result[0])