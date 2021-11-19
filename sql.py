import sqlite3
import os


class Tabler:
    def __init__(self, path):
        self.path = path
        self.con = sqlite3.connect(self.path)
        self.cur = self.con.cursor()

    def create_db(self):
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

    def add_team(self, name):
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

    def create_tour(self, tour=1, scores=None):
        try:
            self.cur.execute("""
            DROP TABLE tour{}
            """.format(tour))
        except sqlite3.OperationalError:
            pass

        try:
            self.cur.execute(f"""
            ALTER TABLE PLAYERS ADD TOUR{tour} INTEGER DEFAULT 0;
            """.format(tour))
        except sqlite3.OperationalError:
            pass

        if scores:
            rows = scores
        else:
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
        teams = [elem[0] for elem in
                 self.cur.execute("""
        SELECT NAME FROM TEAMS
        """).fetchall()]
        return teams

    def get_players(self, team):
        players = [elem for elem in
                   self.cur.execute("""
        SELECT * FROM PLAYERS WHERE TEAM = ?
        """, (team, )).fetchall()]

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

        player_scores = self.cur.execute("""
        SELECT PLAYER, SCORE FROM SCORES
        """).fetchall()

        stats = dict()

        for stat in player_scores:
            try:
                stats[stat[0]] += int(stat[1])
            except KeyError:
                stats[stat[0]] = int(stat[1])

        # for player, score in stats.items():
        #     self.cur.execute("""
        #     UPDATE PLAYERS
        #     SET SCORE = {}
        #     WHERE
        #     """)

        self.create_tour(tour=tour)

        self.con.commit()

    def get_tours(self):
        tour = sorted(list(filter(lambda x: "tour" in x, [elem[0].lower() for elem in self.cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table'").fetchall()])), key=lambda x: x[-1])
        return tour

    def edit_team(self, id, name):
        self.cur.execute("""
        UPDATE TEAMS
        SET NAME = ?
        WHERE ID = ?
        """, [name, id])
        self.con.commit()

    def edit_player(self, id, name):
        self.cur.execute("""
        UPDATE PLAYERS
        SET NAME = ?
        WHERE ID = ?
        """, [name, id])
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

        self.cur.execute("""
        DELETE FROM SCORES
        WHERE TEAM = ? or AGAINST = ?
        """, [id])

        self.con.commit()

        self.create_grid()

    def delete_player(self, id):
        self.cur.execute("""
        DELETE FROM PLAYERS
        WHERE ID = ?
        """, [id])
        self.con.commit()

    def get_scores(self, tour):
        res = [elem for elem in
               self.cur.execute("""
        SELECT TEAM, AGAINST, SCORE FROM SCORES WHERE TOUR LIKE ?
        """, [tour])]

        scores = dict()

        for score in res:
            try:
                scores[score[:2]] = scores[score[:2]] + score[-1]
            except KeyError:
                scores[score[:2]] = score[-1]

        grid = [list(elem) for elem in
                self.cur.execute("""
        SELECT * FROM TOUR{}
        """.format(tour)).fetchall()]

        sessions = dict()

        for key, value in scores.items():
            key = tuple(sorted(list(key)))

            try:
                sessions[key] = sessions[key] + " - " + str(value)
            except KeyError:
                sessions[key] = str(value)

        for index_row, row in enumerate(grid):
            for index_col, col in enumerate(row[1:]):
                if (index_row + 1, index_col + 1) in scores.keys():
                    if grid[index_row][index_col + 1] == "—":
                        grid[index_row][index_col +
                                        1] = scores[(index_row + 1, index_col + 1)]
                    else:
                        grid[index_row][index_col + 1] = str(int(grid[index_row][index_col + 1]) + int(
                            scores[(index_row + 1, index_col + 1)]))

        self.create_tour(tour=tour, scores=grid)

    def get_team_id(self, name):
        id = [elem[0] for elem in self.cur.execute(
            """select id from teams where name = ?""", [name])][0]
        return id




if __name__ == "__main__":
    tabler = Tabler()
    # tabler.create_db()
    # tabler.add_player()
    # tabler.create_grid()
    # tabler.add_team(name="alpha")
    # tabler.add_team(name="beta")
    # tabler.add_team(name="delta")
    # tabler.add_team(name="gamma")
    # tabler.add_team(name="sigma")

    # tabler.create_grid()
    # tabler.create_tour(tour=1)
    tabler.create_tour(tour=2)
    tabler.create_tour(tour=3)
    # tabler.delete_team(8)
    # tabler.delete_player(2)
    # tabler.get_scores(1)
    # tabler.get_teams()
