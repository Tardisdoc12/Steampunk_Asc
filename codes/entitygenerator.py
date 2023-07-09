import pygame as pg
import sqlite3
import globals
import enemy
import classes
import random
import engine
import importlib

'''
On the floor of middle rooms the y=339
On the floor of upper rooms the y=200
On the floor of lower rooms the y=700
'''

class EnemyDatabase:
    def __init__(self,floor=1):
        self.conn=sqlite3.connect('../Database/Enemy.db')
        self.createDatabase()
        self.enemyDico={}
        self.createEnemyDico(floor)
        globals.EnemyDico=self.enemyDico

    def createDatabase(self):
        c=self.conn.cursor()
        try:
            c.execute('CREATE TABLE enemy (id INTEGER PRIMARY KEY,ARCHETYPE VARCHAR(50),PATERN_ATTACK VARCHAR(50),FLOOR INTEGER)')
            c.execute('insert into enemy values (null,"Chest","attack attack attack attack attack",1)')
            c.execute('insert into enemy values (null,"RobotMinion","attack defense defense attack attack",1)')
            self.conn.commit()
            c.close()
        except:
            c.close()

    def createEnemyDico(self,floor=1):
        c=self.conn.cursor()
        try:
            command="SELECT * FROM enemy WHERE FLOOR="+str(floor)
        except:
            command="SELECT * FROM enemy WHERE FLOOR="+floor
        c.execute(command)
        for row in c:
            self.enemyDico[row[1]]=(row[0],row[1],row[2].split())
        c.close()

def choice(entityPossible,floor=1):
    choiceEntity=[]
    if floor==1:
        SellerOrNot=0
        for i in range (0,5):
            choiceEntity.append(random.choice(entityPossible))
            if choiceEntity[-1]=="Enemy":
                enemy=random.choice(list(globals.EnemyDico.keys()))
                choiceEntity[-1]=enemy
            if choiceEntity[-1]!="Seller":
                SellerOrNot+=1
        if SellerOrNot>1:
            for entity in choiceEntity:
                if SellerOrNot!=1 and entity=="Seller":
                    choiceEntity.remove(entity)
                    choiceEntity.append("Collectible")
                    SellerOrNot-=1
        elif SellerOrNot>0:
            choiceEntity.pop()
            choiceEntity.append("Seller")
    return choiceEntity

def verif(x,y,old_x,old_y):
    rect=pg.Rect(x,y,5,5)
    for plateform in globals.world.plateforms:
        if rect.colliderect(plateform.position.rect) and plateform.type=='plateform':
            return True
    for index in range (len(old_x)):
        rect_old=pg.Rect(old_x[index],old_y[index],210,5)
        if rect.colliderect(rect_old):
            return True
    return False

class EntityGenerator:
    def __init__(self,floor=1):
        self.entities=[]
        '''Seul entitée Obligatoire le joueur : '''
        player1=classes.createClassFromStr(globals.archetype[0])()
        player1.position.rect.topleft=(50,339)
        player1.camera=engine.Camera(0,0,700,700)
        player1.camera.trackEntity(player1)
        self.entities.append(player1)
        self.enemyDico=EnemyDatabase(floor)

        '''On créait une liste de toutes les entitées possible avec les probabilités:
                        87%=mob,
                        8.6%=collectible
                        4.35%=seller '''

        entityPossible=["Seller","Collectible","Collectible"]
        for i in range (0,20):
            entityPossible.append("Enemy")

        ''' On randomise le choix des entitées qui seront présentes finalement:'''

        choiceEntity=choice(entityPossible)

        ''' Il faut maintenant randomiser leurs positions. '''
        old_x,old_y=[],[]
        for entity in choiceEntity:
            x,y=0,0
            if entity!="Seller" and entity!="Collectible":
                while verif(x,y,old_x,old_y):
                    x=random.randint(300,1400)
                    y=random.choice([339,700,200,339,339])
                old_x.append(x)
                old_y.append(y)
                self.entities.append(enemy.createEnemyFromStr(entity)())
                self.entities[-1].position.rect.topleft=(x,y)
            elif entity=="Collectible":
                pass
            else:
                pass
