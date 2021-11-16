# import sqlite3
# name = "tables/table.db"

# con = sqlite3.connect(name)
# cur = con.cursor()

# # # teams = [elem for elem in 
# # #         cur.execute("""
# # #         SELECT ID, NAME, SCORE FROM PLAYERS WHERE TEAM LIKE ?
# # #         """, [1]).fetchall()]

# # # print(teams)

# cur.execute("""
# UPDATE scores
# SET PLAYER, 
# WHERE (team1, team2) = ({}, {})
# """.format())
a, b = (1, 'x', None, None, None, None), (2, None, 'x', None, None, None)

for x, y in zip(a, b):
        print(x, y)


# print("".join(list(filter(lambda x: x.isdigit(), "askdhaskhdghk123123kjasdjkhasjkhld"))))

'''
[(1, 'x', None, None, None, None), 
(2, None, 'x', None, None, None), 
(3, None, None, 'x', None, None), 
(4, None, None, None, 'x', None), 
(5, None, None, None, None, 'x')]
'''