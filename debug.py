import sqlite3

con = sqlite3.connect("tables/table.db")
cur = con.cursor()

print([elem for elem in cur.execute("SELECT * FROM sqlite_master WHERE type='table'").fetchall()])