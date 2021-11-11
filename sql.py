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
        TEAM STRING
        );
        """)
        
        self.cur.execute("""
        CREATE TABLE repr(
        '1' STRING
        )
        """)

    def add_team(self, name="unknown"):
        self.cur.execute(f"""
        INSERT INTO TEAMS(NAME) VALUES(?)
        """, (name, ))
        
        self.con.commit()

    def add_player(self, name="unknown", team="asdlkjnassdkalshdf"):
        res = self.cur.execute(f"""
        SELECT ID FROM TEAMS WHERE NAME = ?
        """, (team, )).fetchall()[0][0]

        self.cur.execute(f"""
        INSERT INTO PLAYERS(NAME, TEAM) VALUES(?, ?)
        """, (name, res))

        self.con.commit()

    def create_grid(self):
        teams = self.cur.execute("""
        SELECT ID FROM TEAMS
        """).fetchall()

        for team in teams:
            self.cur.execute(f"""
            ALTER TABLE GRID ADD '{team[0]}' STRING;
            """)

            self.cur.execute(f"""
            INSERT INTO GRID('{team[0]}') VALUES('x');
            """)

            self.con.commit()

    def add_to_grid(self):
        

if __name__ == "__main__":
    tabler = Tabler()
    # tabler.create_table()
    # tabler.add_player()
    tabler.create_grid()
