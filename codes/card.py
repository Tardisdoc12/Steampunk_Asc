import pygame as pg
import sqlite3
import globals as gb
import sys

def createCardFromStr(str):
    return getattr(sys.modules[__name__], str)

def affichagePL(str,nbr_cara,screen,x,y,police):
    new_str=""
    length=len(str)//nbr_cara
    for i in range(length):
        new_str=str[0+(nbr_cara-1)*i:(nbr_cara-1)*(i+1)].strip()
        image_texte=police.render(new_str,1,gb.BLACK)
        screen.blit(image_texte,(x,y))
        x,y=screen.blit(image_texte,(x,y)).bottomleft
    if len(str)%nbr_cara!=0:
        new_str=str[0+(nbr_cara-1)*length:len(str)].strip()
        image_texte=police.render(new_str,1,gb.BLACK)
        screen.blit(image_texte,(x,y))

class Card:
    def __init__(self):
        ''' Properties visible of the card object'''
        self.type='card'
        self.Image=pg.image.load('../Sprites/Cards/c'+str(1)+'.png')
        self.Name=None
        self.BackGround=pg.image.load('../Sprites/Cards/card_'+'Neutre'+'.png')
        self.Cost=None
        self.surface=None
        self.Description=None
        self.target=None

        ''' Properties invisible of the card object'''
        self.scaling=1
        self.alpha=255
        self.location='deck'
        self.scan=False
        self.selected=False
        self.position=None
        self.activated=False
        self.zoom=False
        self.removable=False

    def effect(self,entity,hub):##Virtual Method
        pass

    def draw(self,screen):

        x=self.position.rect.x
        y=self.position.rect.y
        width=int(self.position.rect.w*self.scaling)
        height=int(self.position.rect.h*self.scaling)

        #Render the images of the card:
        self.surface=pg.Surface((width,height))
        image_card=pg.transform.scale(self.Image.convert_alpha(),(int(284*self.scaling),int(181*self.scaling)))
        self.surface.set_alpha(self.alpha)
        self.surface.blit(image_card,(0,0,0,0))

        background=pg.transform.scale(self.BackGround,(int(300*self.scaling),int(430*self.scaling)))
        self.surface.blit(background,(0,0,0,0))

        #Render the cost of the card:
        x_surface=self.surface.get_rect().topleft[0]+int(18*self.scaling)
        y_surface=self.surface.get_rect().topleft[1]+int(5*self.scaling)
        police=pg.font.SysFont("monospace",int(80*self.scaling))
        image_texte=police.render(str(self.Cost),1,gb.BLACK)
        self.surface.blit(image_texte,(x_surface,y_surface))

        #Render the Name of the card
        x_surface=self.surface.get_rect().center[0]-int(85*self.scaling)
        y_surface=self.surface.get_rect().center[1]-int(77*self.scaling)
        police=pg.font.SysFont("monospace",int(40*self.scaling))
        image_texte=police.render(self.Name,1,gb.BLACK)
        self.surface.blit(image_texte,(x_surface,y_surface))

        #Render the Description of the card:
        new_x=int(self.surface.get_rect().center[0]-130*self.scaling)
        new_y=int(self.surface.get_rect().center[1]+40*self.scaling)
        police=pg.font.SysFont("monospace",int(20*self.scaling))
        affichagePL(self.Description,21,self.surface,new_x,new_y,police)
        screen.blit(self.surface,(x,y))

class AttackCard(Card):
    def __init__(self):
        super().__init__()
    def effect(self,entity,hub):
        degat=self.degat
        for entitie in gb.InFight.entities:
            if entitie.type=='player':
                degat-=int(entitie.force*0.1)
                entitie.force=0
        if entity.type==self.target:
            diff=entity.defense+degat
            if diff<0:
                entity.life.changeHP(diff)
                entity.defense=0
            else:
                entity.defense=diff
            return True
        return False

class DefenseCard(Card):
    def __init__(self):
        super().__init__()
        self.target='player'
    def effect(self,entity,hub):
        if entity.type==self.target:
            entity.defense+=self.defense
            return True
        return False

class Griffe(AttackCard):
    def __init__(self):
        super().__init__()
        self.Image=pg.image.load('../Sprites/Cards/c'+str(1)+'.png')
        self.Name='Griffe'
        self.BackGround=pg.image.load('../Sprites/Cards/card_'+'Magie'+'.png')
        self.Cost=0
        self.surface=pg.Surface((30,30))
        self.Description="Inflict 5 damage to the target enemy"
        self.target='enemy'
        self.degat=-5

class Pipe(AttackCard):
    def __init__(self):
        super().__init__()
        self.Image=pg.image.load('../Sprites/Cards/c'+str(1)+'.png')
        self.Name='Pipe'
        self.BackGround=pg.image.load('../Sprites/Cards/card_'+'Normal'+'.png')
        self.Cost=1
        self.surface=pg.Surface((30,30))
        self.Description="Inflict 3 damage to the target enemy"
        self.target='enemy'
        self.degat=-3

class Formula(AttackCard):
    def __init__(self):
        super().__init__()
        self.Image=pg.image.load('../Sprites/Cards/c'+str(1)+'.png')
        self.Name='Formula'
        self.BackGround=pg.image.load('../Sprites/Cards/card_'+'Normal'+'.png')
        self.Cost=2
        self.surface=pg.Surface((30,30))
        self.Description="Inflict 9 damage to the target enemy."
        self.target='enemy'
        self.degat=-9

class Brain(AttackCard):
    def __init__(self):
        super().__init__()
        self.Image=pg.image.load('../Sprites/Cards/c'+str(1)+'.png')
        self.Name='Brain'
        self.BackGround=pg.image.load('../Sprites/Cards/card_'+'Normal'+'.png')
        self.Cost=0
        self.target='player'
        self.surface=pg.Surface((30,30))
        self.Description="Gain 25 force for the turn."
        self.force=25

    def effect(self,entity,hub):
        if entity.type=='player':
            entity.force+=self.force
            return True
        return False

class ForceShield(DefenseCard):
    def __init__(self):
        super().__init__()
        self.Image=pg.image.load('../Sprites/Cards/c'+str(1)+'.png')
        self.Name='Force Shield'
        self.BackGround=pg.image.load('../Sprites/Cards/card_'+'Mana'+'.png')
        self.Cost=1
        self.surface=pg.Surface((30,30))
        self.Description="Gain 5 shield for the next turn."
        self.defense=5

class ElectroShield(DefenseCard):
    def __init__(self):
        super().__init__()
        self.Image=pg.image.load('../Sprites/Cards/c'+str(1)+'.png')
        self.Name='Electro Shield'
        self.BackGround=pg.image.load('../Sprites/Cards/card_'+'Mana'+'.png')
        self.Cost=2
        self.surface=pg.Surface((30,30))
        self.Description="Gain 15 shield for the next turn."
        self.defense=15

class CardsDatabase:
    def __init__(self,archetype):
        self.conn=sqlite3.connect('../Database/Cards.db')
        self.createDatabase()
        self.cardsDico={}
        self.createDico(archetype)
        gb.CardsDico=self.cardsDico

    def createDatabase(self):
        c = self.conn.cursor()
        try:
            c.execute('CREATE TABLE Cards (id INTEGER PRIMARY KEY,NAME VARCHAR(50), UNLOCK INTEGER,ARCHETYPE VARCHAR(50))')

            c.execute('insert into Cards values (null,"Griffe",0,"Scientific")')
            c.execute('insert into Cards values (null,"Pipe",1,"Scientific")')
            c.execute('insert into Cards values (null,"ForceShield",1,"Scientific")')
            c.execute('insert into Cards values (null,"Formula",1,"Scientific")')
            c.execute('insert into Cards values (null,"ElectroShield",1,"Scientific")')
            c.execute('insert into Cards values (null,"Brain",1,"Scientific")')
            self.conn.commit()

            c.close()
            return True
        except:
            c.close()
            return False

    def read(self):
        c=self.conn.cursor()
        c.execute("Select * From Cards")
        for row in c:
            print(row)
            print(row[1])
        c.close()

    def add(self,Name,Description,Cost,Kind):
        c = self.conn.cursor()
        command='insert into Cards values (null,"'+Name+'","'+Description+'",'+str(Cost)+',"'+Kind+'")'
        c.execute(command)
        self.conn.commit()
        c.close()

    def createDico(self,archetype):
        c=self.conn.cursor()
        command="Select * From Cards Where ARCHETYPE='"+archetype+"' AND UNLOCK=1"
        c.execute(command)
        for row in c:
            self.cardsDico[row[1]]=row[1]

class Deck:
    def __init__(self,cardList,archetype):
        self.decklist=[]
        cardData=CardsDatabase(archetype)
        for cardName in cardList:
            self.decklist.append(createCardFromStr(cardName)())

if __name__ == '__main__':
    import engine
    cards=[]
    scaling=0.55
    cardList=["Griffe","Griffe"]
    i=0
    for cardName in cardList:
        card2=str_to_class(cardName)()
        card2.position=engine.Position(0+i*10,0,300,430)
        card2.scaling=scaling
        i+=50
        cards.append(card2)

    pg.init()
    screen=pg.display.set_mode((1000,800))
    running=True
    while running:
        for event in pg.event.get():
            if event.type==pg.QUIT:
                running=False

        screen.fill((0,0,125,0))
        for card in cards:
            card.draw(screen)
        pg.display.flip()
    pg.quit()
