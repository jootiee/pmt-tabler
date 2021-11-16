import sqlite3
name = "tables/table2.db"

con = sqlite3.connect(name)
cur = con.cursor()

teams = [elem for elem in 
        cur.execute("""
        SELECT ID, NAME, SCORE FROM PLAYERS WHERE TEAM LIKE ?
        """, [1]).fetchall()]

print(teams)



'''
[(1, 'x', None, None, None, None), 
(2, None, 'x', None, None, None), 
(3, None, None, 'x', None, None), 
(4, None, None, None, 'x', None), 
(5, None, None, None, None, 'x')]
'''