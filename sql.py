import sqlite3
import os


class Tabler:
    def __init__(self, path_tables="tables", path_table="table1.db"):
        self.path_tables = path_tables
        if path_table:
            self.path_table = os.path.join(self.path_tables, path_table)
            self.con = sqlite3.connect(self.path_table)
            self.cur = self.con.cursor()

    def create_table(self):
        paths_tables = list(filter(lambda x: "table" in x, os.listdir(self.path_tables)))
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
        TOUR1 INT
        );
        """)
        
        self.cur.execute("""
        CREATE TABLE repr(
        Team STRING
        )
        """)

        self.cur.execute("""
        CREATE TABLE  scores(
        Team1 STRING; Score STRING, Team2 STRING
        )
        """)

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

    def fill_table(self):
        self.cur.execute("""
        DROP TABLE repr
        """)

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
                        values.append("—")
                else:
                    values.append(teams[rows_index])

            self.cur.execute("""
            INSERT INTO REPR(Team, {}) VALUES({})
            """.format(", ".join(teams), ", ".join([f"'{elem}'" for elem in values])))

        

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
        SELECT ID, NAME, SCORE FROM PLAYERS WHERE TEAM LIKE ?
        """, [team]).fetchall()]

        return players

    def change_score(self, player, score):
        self.cur.execute("""
        UPDATE PLAYERS
        SET SCORE = ?
        WHERE ID = ?
        """, [score, player])
        self.con.commit()


if __name__ == "__main__":
    tabler = Tabler()
    tabler.create_table()
    # tabler.add_player()
    # tabler.create_grid()
    # tabler.add_team(name="shutoku")
    # tabler.fill_table()