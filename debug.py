import sqlite3
name = "tables/asd.db"
open(name, "w").close()


con = sqlite3.connect("asd.db")
cur = con.cursor()
cur.execute("""CREATE TABLE CUSTOMERS(
  ID   INT              NOT NULL,
  NAME VARCHAR (20)     NOT NULL,
  AGE  INT              NOT NULL,
  ADDRESS  CHAR (25) ,
  SALARY   DECIMAL (18, 2),       
  PRIMARY KEY (ID)
);""")