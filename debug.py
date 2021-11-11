import sqlite3
name = "tables/table1.db"

con = sqlite3.connect(name)
cur = con.cursor()

cur.execute("""
DROP TABLE repr
""")

rows = [row for row in 
cur.execute("""
SELECT * FROM GRID
""")]


teams = [team[0] for team in 
cur.execute("""
SELECT NAME FROM TEAMS
""").fetchall()]

cmd_teams = " STRING, ".join(teams) + " STRING"

cur.execute("""
CREATE TABLE repr(
Team STRING, {}
)
""".format(cmd_teams))

for rows_index, row in enumerate(rows):
    values = list()
    for index, elem in enumerate(row):
        if index:
            if elem:
                values.append(elem)
            else:
                values.append("-")
        else:
            values.append(teams[rows_index])

    cur.execute("""
    INSERT INTO REPR(Team, {}) VALUES({})
    """.format(", ".join(teams), ", ".join([f"'{elem}'" for elem in values])))

con.commit()


'''
[(1, 'x', None, None, None, None), 
(2, None, 'x', None, None, None), 
(3, None, None, 'x', None, None), 
(4, None, None, None, 'x', None), 
(5, None, None, None, None, 'x')]
'''