import pygame as pg
import engine
import inputmanager
import life
import globals
import random
import sys

def DrawCircleWritting(screen,x,y,radius,color,fontSize,text):
    image=pg.Surface((int(radius*2),int(radius*2)))
    image.fill((0,0,100,0))
    pg.draw.circle(image,color,image.get_rect().center,radius)

    police=pg.font.SysFont("monospace",fontSize)
    image_texte=police.render(text,1,globals.BLACK)
    image.blit(image_texte,(image.get_rect().w//2-image_texte.get_rect().w//2,image.get_rect().h//2-image_texte.get_rect().h//2))
    screen.blit(image,(x,y))

def createEnemyFromStr(str):
    return getattr(sys.modules[__name__], str)

class Enemy(engine.Entity):
    def __init__(self):
        super().__init__()
        x,y=0,0
        self.type ='enemy'
        self.scaling=0.11
        self.battle=False
        self.intention=None
        self.archetype=None
        self.balise=40
        self.degat=0
        self.gainDefense=0
        self.forceGain=0
        self.save_balise=40
        self.nextTurn=None
        self.position=engine.Position(x,y,int(570*self.scaling),int(593*self.scaling))
        self.life=None
        self.nbrTurn=0
        self.attackPossible=None

    def putAt(self,x,y):
        self.position.rect.x=x
        self.position.rect.y=y

    def attack(self):
        self.nextTurn.append(random.choice(self.attackPossible))
        if self.nextTurn[0]=="attack":
            for entity in globals.InFight.entities:
                if entity.type=="player":
                    degat=self.degat
                    degat-=int(self.force*0.15)
                    self.force=0
                    diff=entity.defense+degat
                    if diff<0:
                        entity.life.changeHP(diff)
                        entity.defense=0
                    else:
                        entity.defense=diff
        elif self.nextTurn[0]=="defense":
            self.defense+=self.gainDefense
        else:
            self.nbrTurn=0
            self.force=self.forceGain
        self.nextTurn.pop(0)

    def draw(self,screen,x,y,offsetX,offsetY):
        s=self.state
        a=self.animations.animationList[s]
        x=self.position.rect.x+offsetX
        y=self.position.rect.y+offsetY
        if self.life is not None and self.battle:
            self.life.x=self.position.rect.x-self.life.back.get_rect().w//2+offsetX
            self.life.y=self.position.rect.y+self.position.rect.h+offsetY+10
            if self.defense>0:
                self.life.draw(screen,globals.BLUE)
            else:
                self.life.draw(screen)
            if self.nextTurn is not None:
                x_inte=self.position.rect.x-20
                y_inte=self.position.rect.y-40
                radius=20
                if self.nextTurn[0]=="attack":
                    DrawCircleWritting(screen,x_inte,y_inte,radius,globals.RED,10,"a")
                elif self.nextTurn[0]=="defense":
                    DrawCircleWritting(screen,x_inte,y_inte,radius,globals.BLUE,10,"d")
                else:
                    DrawCircleWritting(screen,x_inte,y_inte,radius,globals.PURPLE,10,"u")
        a.draw(screen,x,y,self.direction=='right',False,self.position.rect.w,self.position.rect.h)

class Chest(Enemy):
    def __init__(self):
        super().__init__()
        idle=pg.image.load('../Sprites/Ennemies/chest.png')
        idle_anim=engine.Animation([idle])
        self.animations.add('idle',idle_anim)
        self.animations.add('run',idle_anim)
        self.archetype='Chest'
        self.degat=-5
        self.gainDefense=5
        self.forceGain=10
        self.attackPossible=["attack","defense","attack","defense"]
        self.nextTurn=[random.choice(self.attackPossible)]
        self.life=life.Life(30,self.position.rect.x,self.position.rect.y+self.position.rect.h+10)

class RobotMinion(Enemy):
    def __init__(self):
        super().__init__()
        idle=pg.image.load('../Sprites/Ennemies/ennemy3.png')
        idle_anim=engine.Animation([idle])
        self.animations.add('idle',idle_anim)
        self.animations.add('run',idle_anim)
        self.scaling=0.1
        self.position=engine.Position(0,0,int(557*self.scaling),int(506*self.scaling))
        self.archetype='RobotMinion'
        self.gainDefense=10
        self.degat=-9
        self.forceGain=20
        self.attackPossible=["attack","defense","update","attack","update"]
        self.nextTurn=[random.choice(self.attackPossible)]
        self.life=life.Life(40,self.position.rect.x,self.position.rect.y+self.position.rect.h+10)

class Angel(Enemy):
    def __init__(self):
        super().__init__()
        idle=pg.image.load('../Sprites/Ennemies/chest.png')
        idle_anim=engine.Animation([idle])
        self.animations.add('idle',idle_anim)
        self.animations.add('run',idle_anim)
        self.archetype='Angel'
        self.gainDefense=10
        self.degat=-10
        self.forceGain=15
        self.attackPossible=["attack","attack","update","attack","update"]
        self.nextTurn=[random.choice(self.attackPossible)]
        self.life=life.Life(40,self.position.rect.x,self.position.rect.y+self.position.rect.h+10)

if __name__ == '__main__':
    enemy=Enemy(x=10,y=10)

    pg.init()
    running=True
    screen=pg.display.set_mode((800,900))

    while running:
        for event in pg.event.get():
            if event.type==pg.QUIT:
                running=False
        screen.fill((175,125,120))
        enemy.draw(screen,10,10,0,0)
        pg.display.flip()
