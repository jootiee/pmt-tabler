import sqlite3
import os


class Tabler:
    def __init__(self, path_tables="tables", path_table="table.db"):
        self.path_tables = path_tables
        if path_table:
            self.path_table = os.path.join(self.path_tables, path_table)
            self.con = sqlite3.connect(self.path_table)
            self.cur = self.con.cursor()

    def create_db(self):
        paths_tables = list(filter(lambda x: "table" in x,
                            os.listdir(self.path_tables)))
        if paths_tables:
            name = self.path_tables + "/"
            number = ""
            counter = False
            for elem in sorted(paths_tables, key=lambda x: x[5], reverse=True)[0]:
                if elem.isdigit():
                    number += elem
                    counter = True
                else:
                    if counter:
                        counter = False
                        name += str(int(number) + 1) + elem
                    else:
                        name += elem
        else:
            name = os.path.join(self.path_tables, "table1.db")
        self.path_table = name
        self.con = sqlite3.connect(self.path_table)
        self.cur = self.con.cursor()

        self.cur.execute("""
        CREATE TABLE grid(
        ID  INTEGER PRIMARY KEY AUTOINCREMENT
        )
        """)

        # self.cur.execute("""
        # CREATE TABLE sessions(
        # ID  INTEGER PRIMARY KEY AUTOINCREMENT,
        # TEAMS STRING,
        # SCORE STRING, 
        # TOUR INTEGER
        # )
        # """)

        self.cur.execute("""
        CREATE TABLE teams(
        ID  INTEGER PRIMARY KEY AUTOINCREMENT,
        NAME STRING
        );
        """)

        self.cur.execute("""
        CREATE TABLE players(
        ID  INTEGER PRIMARY KEY AUTOINCREMENT,
        NAME STRING,
        TEAM STRING,
        TOUR1 INT DEFAULT 0
        );
        """)


        self.cur.execute("""
        CREATE TABLE  scores(
        PLAYER INTEGER,
        TEAM INTEGER, 
        SCORE INTEGER, 
        AGAINST INTEGER, 
        Tour INTEGER
        )""")

    def add_team(self, name="unknown"):
        self.cur.execute(f"""
        INSERT INTO TEAMS(NAME) VALUES(?)
        """, (name, ))

        teams = sorted(list(set([elem[0] for elem in
                                 self.cur.execute("""
        SELECT ID FROM TEAMS
        """)]) - set([elem[0] for elem in
                                     self.cur.execute("""
        SELECT ID FROM GRID
        """)])))

        self.add_to_grid(teams)

    def add_player(self, name="unknown", team="unknown"):
        id = self.cur.execute(f"""
        SELECT ID FROM TEAMS WHERE NAME = ?
        """, (team, )).fetchall()[0][0]

        self.cur.execute(f"""
        INSERT INTO PLAYERS(NAME, TEAM) VALUES(?, ?)
        """, (name, id))

        self.con.commit()

    def create_grid(self):
        teams = [team[0] for team in
                 self.cur.execute("""
        SELECT ID FROM TEAMS
        """).fetchall()]

        try:
            self.cur.execute("""
            CREATE TABLE grid(
            ID  INTEGER PRIMARY KEY AUTOINCREMENT
            )
            """)
        except Exception:
            pass

        self.add_to_grid(teams)

    def add_to_grid(self, teams):
        for team in teams:
            self.cur.execute(f"""
            ALTER TABLE GRID ADD '{team}' STRING;
            """)

            self.cur.execute(f"""
            INSERT INTO GRID('{team}') VALUES('x');
            """)

            self.con.commit()

    def create_tour(self, tour=1):
        try: 
            self.cur.execute("""
            DROP TABLE tour{}
            """.format(tour))
        except sqlite3.OperationalError:
            pass

        rows = [row for row in
                self.cur.execute("""
        SELECT * FROM GRID
        """)]

        teams = [team[0] for team in
                 self.cur.execute("""
        SELECT NAME FROM TEAMS
        """).fetchall()]

        cmd_teams = " STRING, ".join(teams) + " STRING"

        self.cur.execute("""
        CREATE TABLE tour{}(
        Team STRING, {}
        )
        """.format(tour, cmd_teams))

        for rows_index, row in enumerate(rows):
            values = list()
            for index, elem in enumerate(row):
                if index:
                    if elem:
                        values.append(elem)
                    else:
                        values.append("—")
                else:
                    values.append(teams[rows_index])

            self.cur.execute("""
            INSERT INTO TOUR{}(Team, {}) VALUES({})
            """.format(tour, ", ".join(teams), ", ".join([f"'{elem}'" for elem in values])))

        self.con.commit()

    def get_teams(self):
        teams = [elem[1] for elem in
                 self.cur.execute("""
        SELECT ID, NAME FROM TEAMS
        """).fetchall()]

        return teams

    def get_players(self, team):
        players = [elem for elem in
                   self.cur.execute("""
        SELECT * FROM PLAYERS WHERE TEAM LIKE {}
        """.format(team)).fetchall()]

        return players

    def change_score(self, player, against, team, score, tour):
        # self.cur.execute("""
        # UPDATE PLAYERS
        # SET TOUR{} = {}
        # WHERE ID = {}
        # """.format(str(tour), score1, player1))

        # self.cur.execute("""
        # UPDATE PLAYERS
        # SET TOUR{} = {}
        # WHERE ID = {}
        # """.format(str(tour), score2, player2))
        
        rows = [elem for elem in 
        self.cur.execute("""
        SELECT PLAYER, TEAM, AGAINST, TOUR FROM SCORES
        """).fetchall()]
        if (player, team, against, tour) in rows:
            self.cur.execute("""
            UPDATE scores
            SET SCORE = {}
            WHERE (PLAYER, TEAM, AGAINST, TOUR) = ({}, {}, {}, {})
            """.format(score, player, team, against, tour))
        else:
            self.cur.execute("""
            INSERT INTO SCORES(PLAYER, TEAM, SCORE, AGAINST, TOUR) VALUES(?, ?, ?, ?, ?)
            """, (player, team, score, against, tour))
        
        self.create_tour(tour=tour)

        self.con.commit()

    def get_tours(self):
        tour = sorted(list(filter(lambda x: "tour" in x, [elem[0] for elem in self.cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table';").fetchall()])), key=lambda x: x[-1])
        return tour

    def edit_team(self, id, name):
        self.cur.execute("""
        UPDATE TEAMS
        SET NAME = ?
        WHERE ID = ?
        """, [name, id])
        self.con.commit()

    def edit_player(self, id, name, team):
        self.cur.execute("""
        UPDATE PLAYERS
        SET NAME = ?,
        SET TEAM = ?
        WHERE ID = ?
        """, [name, team, id])
        self.con.commit()

    def delete_team(self, id):
        self.cur.execute("""
        DROP TABLE grid""")

        self.cur.execute("""
        DELETE FROM TEAMS
        WHERE ID = ?
        """, [id])

        self.cur.execute("""
        DELETE FROM PLAYERS
        WHERE TEAM = ?
        """, [id])

        self.con.commit()

        self.create_grid()

    def delete_player(self, id):
        self.cur.execute("""
        DELETE FROM PLAYERS
        WHERE ID = ?
        """, [id])
        self.con.commit()



if __name__ == "__main__":
    tabler = Tabler()
    # tabler.create_db()
    # tabler.add_player()
    tabler.create_grid()
    # tabler.add_team(name="shutoku")
    # tabler.create_grid()
    tabler.create_tour(tour=1)
    # tabler.delete_team(8)
    # tabler.delete_player(2)
