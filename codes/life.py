import pygame as pg
import globals

class Life:
    def __init__(self,life=0,x=0,y=0):
        self.life=life
        self.lifeInFight=life
        self.originalLife=life
        self.gamma=100/self.life
        self.hpBar=pg.Surface((self.life,5))
        self.back=pg.Surface((int(self.life*self.gamma),5))
        self.x=x
        self.y=y

    def changeHP(self,change):
        if self.life>0:
            if abs(change)>self.life and change//abs(change)<0:
                self.life=0
            else:
                while change!=0:
                    self.life+=(change//abs(change))
                    if self.lifeInFight<self.life:
                        self.gamma=100/self.life
                        self.lifeInFight=self.life
                    change-=(change//abs(change))

    def draw(self,screen,color=globals.GREEN):
        self.hpBar.fill(color)
        self.back.fill(globals.RED)
        screen.blit(self.back,(self.x,self.y))
        #Blit the remaining life
        police=pg.font.SysFont("monospace",10)
        police.set_bold(True)
        image_texte=police.render(str(self.life)+'/'+str(self.lifeInFight),1,globals.WHITE)
        y=self.y-2
        x=self.x+self.back.get_rect().w+5
        screen.blit(image_texte,(x,y))
        surface=pg.transform.scale(self.hpBar,(int(self.gamma*self.life),self.hpBar.get_rect().h))
        screen.blit(surface,(self.x,self.y))

if __name__=='__main__':
    pg.init()
    life=Life(life=90,x=500,y=400)
    screen=pg.display.set_mode(globals.SCREEN_SIZE)
    pg.display.set_caption("Life test")
    running=True

    while running:
        for event in pg.event.get():
            if event.type==pg.QUIT:
                running=False
            if event.type==pg.KEYDOWN:
                if event.key==pg.K_a:
                    life.changeHP(-5)
                if event.key==pg.K_q:
                    life.changeHP(5)
        screen.fill(globals.BLACK)
        life.draw(screen)
        pg.display.flip()

    pg.quit()
