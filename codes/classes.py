import pygame as pg
import sqlite3
import player
import life as lf
import sys
import engine

def createList(list):
    list_final=[]
    for i in list:
        list_final.append(str(i))
    return list_final

def createClassFromStr(str):
    return getattr(sys.modules[__name__], str)

class ClassDatabase:
    def __init__(self):
        self.conn=sqlite3.connect('../Database/Classes.db')
        self.classes={}
        self.create_Database()
        self.createDico()

    def create_Database(self):
        c = self.conn.cursor()
        try:
            c.execute('CREATE TABLE Classes (id INTEGER PRIMARY KEY,NAME VARCHAR(50),DECK VARCHAR(50), LEVEL INTEGER,UNLOCK INTEGER)')

            c.execute('insert into Classes values (null,"Scientific","Pipe Pipe Pipe Pipe Pipe ForceShield ForceShield ForceShield ForceShield ForceShield",1,1)')
            c.execute('insert into Classes values (null,"Miner"," ",1,0)')
            c.execute('insert into Classes values (null,"Thief"," ",1,0)')
            c.execute('insert into Classes values (null,"Engeneer"," ",1,0)')
            self.conn.commit()

            c.close()
            return True
        except:
            c.close()
            return False

    def createDico(self):
        c=self.conn.cursor()
        c.execute('Select * From Classes')
        for row in c:
            self.classes[row[1]]=(row[1],row[3],createList(row[2].split()),row[4])

class Scientific(player.Player):
    def __init__(self):
        super().__init__()
        #Image for animations:
        run0=pg.image.load('../Sprites/Player/run/spr_maincharal_b_0.png')
        run1=pg.image.load('../Sprites/Player/run/spr_maincharal_b_1.png')
        entityAnimation= engine.Animation([run0])
        entityRun= engine.Animation([run0,run1])
        self.animations.add('idle',engine.Animation([run0]))
        self.animations.add('run',engine.Animation([run0,run1]))
        #other Properties of the archetype:
        self.pa=3
        self.archetype="Scientific"
        self.life=lf.Life(life=50,x=self.position.rect.x,y=self.position.rect.h+5)

class Miner(player.Player):
        def __init__(self):
            super().__init__()
            #Image for animations:
            run0=pg.image.load('../Sprites/Player/run/spr_maincharal_b_0.png')
            run1=pg.image.load('../Sprites/Player/run/spr_maincharal_b_1.png')
            entityAnimation= engine.Animation([run0])
            entityRun= engine.Animation([run0,run1])
            self.animations.add('idle',engine.Animation([run0]))
            self.animations.add('run',engine.Animation([run0,run1]))
            #other Properties of the archetype:
            self.pa=3
            self.archetype="Miner"
            self.life=lf.Life(life=80,x=self.position.rect.x,y=self.position.rect.h+5)

class Thief(player.Player):
    pass

class Engeneer(player.Player):
    pass

if __name__ == '__main__':
    classData=ClassDatabase()
    print(classData.classes['Scientific'])
