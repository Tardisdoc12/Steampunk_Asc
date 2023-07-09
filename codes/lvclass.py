import sqlite3

class LVL:
    def __init__(self):
        self.conn=sqlite3.connect("../Database/Games.db")
        self.lvlDico={}
        self.createDatabase()
        self.createDico()

    def createDatabase(self):
        c=self.conn.cursor()
        try:
            c.execute("CREATE TABLE lvldata (id INTEGER PRIMARY KEY, XP INTEGER)")
            c.execute("INSERT INTO lvldata (null,1500)")
            c.execute("INSERT INTO lvldata (null,2500)")
            c.execute("INSERT INTO lvldata (null,4500)")
            c.execute("INSERT INTO lvldata (null,7000)")
            c.execute("INSERT INTO lvldata (null,9000)")
            c.execute("INSERT INTO lvldata (null,10000)")
            c.execute("INSERT INTO lvldata (null,15000)")
            self.conn.commit()
            c.close()
        except:
            c.close()

    def createDico(self):
        c=self.conn.cursor()
        try:
            c.execute("SELECT * FROM lvldata")
            for row in c:
                self.lvlDico[row[0]]=row[1]
            c.close()
        except:
            c.close()
