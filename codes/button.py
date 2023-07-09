import pygame as pg
import engine
import globals

class Button:
    def __init__(self,x,y,name):
        idle=pg.image.load('../Sprites/Button/button.png')
        selected=pg.image.load('../Sprites/Button/button_selected.png')
        pressed=pg.image.load('../Sprites/Button/button_valider.png')
        self.animations={
            'idle':idle,
            'selected':selected,
            'pressed':pressed
        }
        self.name=name
        self.type='button'
        self.state='idle'
        self.selected=False
        self.pressed=False
        self.scaling=0.4
        self.intention=None
        self.position=engine.Position(x,y,int(700*self.scaling),int(200*self.scaling))

    def draw(self,screen):
        x,y=self.position.rect.topleft
        width=self.position.rect.w
        height=self.position.rect.h
        anim=pg.transform.scale(self.animations[self.state],(width,height))
        screen.blit(anim,(x,y))
        police_x=self.position.rect.x+self.position.rect.w/2
        police_y=self.position.rect.y+self.position.rect.h/2
        police=pg.font.SysFont("monospace",int(100*self.scaling))
        image_texte=police.render(self.name,1,globals.YELLOW)
        police_x-=image_texte.get_rect().w/2
        police_y-=image_texte.get_rect().h/2
        screen.blit(image_texte,(police_x,police_y))

if __name__ == '__main__':
    import level
    pg.init()
    screen=pg.display.set_mode((800,500))
    running=True
    button=Button(10,10,"Start")
    x,y=button.position.rect.bottomleft
    button1=Button(x,y+10,"Quit")
    entities=[button,button1]
    level1=level.Level(entities=entities)
    globals.world=level1
    buttonSystem=engine.ButtonSystem()
    while running:
        for event in pg.event.get():
            if event.type==pg.QUIT:
                running=False
        if button1.pressed:
            running=False
        buttonSystem.update()
        screen.fill(globals.BLACK)
        button.draw(screen)
        button1.draw(screen)
        pg.display.flip()
    pg.quit()
