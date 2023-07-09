#ALL the IMPORT:
import pygame as pg
import utilities as utl
import globals
from inputstream import InputStream
import engine
import card
import levelgenerator as lg
import button
import entitygenerator as eg
import level
import classes
import hub
import random
import turn

def winFightFunc(level):
    if len(level.entities)==1 and level.entities[0].type=='player':
        return True
    return False

def looseFightFunc(level):
    for entity in level.entities:
        if entity.type=='player' and entity.life.life==0:
            return True
    return False

''' ALL SCENES OF THE GAME. THEY ARE MANAGED BY THE SCENEMANAGER. '''

class Scene:
    def __init__(self):
        pass
    def on_Start(self):
        pass
    def on_Exit(self):
        pass
    def input(self,sm,inputstream):
        pass
    def update(self,sm,inputstream):
        pass
    def draw(self,sm,screen):
        pass

class StartGameScene(Scene):
    def __init__(self):
        self.enter=button.Button(globals.SCREEN_SIZE[0]/2-150,150,"Start")
        x,y=self.enter.position.rect.bottomleft
        self.quit=button.Button(x,y+40,"Quit")
        globals.Buttons=[self.enter,self.quit]
        self.buttonSystem=engine.ButtonSystem()
    def input(self,sm,inputstream):
        if self.enter.pressed:
            sm.push(FadeTransitionScene([self],[ClassChoiceScene()]))
        if self.quit.pressed:
            sm.pop()
    def update(self,sm,inputstream):
        self.buttonSystem.update()
    def draw(self,sm,screen):
        self.enter.draw(screen)
        self.quit.draw(screen)
        utl.drawText(screen,"Start",50,50,globals.WHITE)
    def on_Exit(self):
        self.enter.pressed=False
        self.enter.selected=False

class ClassChoiceScene(Scene):
    def __init__(self):
        globals.classDico=classes.ClassDatabase()
        self.buttons=[]
        length=len(globals.classDico.classes)
        index_x=0
        index_y=-1
        for archetype in globals.classDico.classes:
            x=150+(index_x%2)*450
            if index_x%2==0:
                index_y+=1
            y=globals.SCREEN_SIZE[1]//2+index_y*200
            index_x+=1
            button1=button.Button(x,y,archetype)
            self.buttons.append(button1)
        globals.Buttons=self.buttons
        self.buttonSystem=engine.ButtonSystem()

    def input(self,sm,inputstream):
        for button1 in self.buttons:
            if button1.pressed:
                if globals.classDico.classes[button1.name][3]==1:
                    globals.archetype=globals.classDico.classes[button1.name]
                    globals.Deck=card.Deck(globals.archetype[2],globals.archetype[0])
                    sm.push(FadeTransitionScene([],[LevelScene()]))
        if inputstream.keyboard.isKeyPressed(pg.K_ESCAPE):
            sm.pop()
            sm.push(FadeTransitionScene([self],[]))

    def update(self,sm,inputstream):
        self.buttonSystem.update()

    def draw(self,sm,screen):
        screen.fill(globals.PURPLE)
        for button1 in self.buttons:
            button1.draw(screen)
        utl.drawText(screen,"Main Menu",50,50,globals.WHITE)

    def on_Exit(self):
        for button1 in self.buttons:
            if button1.pressed:
                button1.pressed=False
            if button1.selected:
                button1.selected=False

class LevelScene(Scene):
    def __init__(self):
        self.inputStream=InputStream()
        self.physicSystem=engine.PhysicsSystem()
        self.cameraSystem=engine.CameraSystem()
        self.inputSystem=engine.InputSystem()
        self.animationSystem=engine.AnimationSystem()
        self.battleSystem=engine.EnterOnBattleSystem()
        Niveau=lg.WorldGenerator(5,3,8,6,16*3,16*3,0,0)
        level1=level.Level(entities=[],plateforms=Niveau.rooms.plateforms)
        globals.world=level1
        globals.InFight=level.Level(entities=[],cards=globals.Deck.decklist,winFunctions=winFightFunc,loseFunctions=looseFightFunc)
        entityGen=eg.EntityGenerator()
        globals.position=entityGen.entities[0].position.rect.topleft
        globals.world.entities=entityGen.entities

    def input(self,sm,inputstream):
        keys=pg.key.get_pressed()
        if inputstream.keyboard.isKeyDown(pg.K_ESCAPE):
            sm.pop()
        self.inputStream.processInput()
        self.inputSystem.update(inputStream=inputstream)
        if inputstream.keyboard.isKeyPressed(pg.K_p):
            sm.push(FadeTransitionScene([self],[PauseScene()]))

    def update(self,sm,inputstream):
        self.physicSystem.update(inputStream=inputstream)
        self.animationSystem.update(inputStream=inputstream)
        self.battleSystem.update(inputStream=inputstream)
        for entity in globals.world.entities:
            if entity.battle:
                globals.InFight.entities.append(entity)
                if entity.type=='enemy':
                    globals.indice=globals.world.entities.index(entity)

        if len(globals.InFight.entities)>0:
            for entitie in globals.InFight.entities:
                if entitie.type=='player':
                    globals.position=entitie.position.rect.topleft
                    sm.push(FadeTransitionScene([],[FightScene()]))

    def draw(self,sm,screen):
        self.cameraSystem.update(screen=screen)

class PauseScene(Scene):
    def __init__(self):
        self.surface=pg.Surface((globals.SCREEN_SIZE))
        self.ResumeButton=button.Button(globals.SCREEN_SIZE[0]//2-150,150,"Resume")
        self.OptionButton=button.Button(globals.SCREEN_SIZE[0]//2-150,300,"Option")
        self.QuitButton=button.Button(globals.SCREEN_SIZE[0]//2-150,450,"Quit")
        self.buttons=[self.ResumeButton,self.OptionButton,self.QuitButton]
        globals.Buttons=self.buttons
        self.buttonSystem=engine.ButtonSystem()
    def input(self,sm,inputstream):
        if self.ResumeButton.pressed:
            sm.pop()
            sm.push(FadeTransitionScene([self],[]))
        elif self.QuitButton.pressed:
            sm.pop()
            sm.set(StartGameScene())
    def update(self,sm,inputstream):
        self.buttonSystem.update()
        for entity in self.buttons:
            x,y=pg.mouse.get_pos()
            rect=pg.Rect(x,y,5,5)

            if rect.colliderect(entity.position.rect) and not pg.mouse.get_pressed()[0]:
                entity.selected=True
                entity.state='selected'
            elif not rect.colliderect(entity.position.rect) and not pg.mouse.get_pressed()[0]:
                entity.selected=False
                entity.state='idle'
            if rect.colliderect(entity.position.rect) and pg.mouse.get_pressed()[0]:
                entity.selected=False
                entity.pressed=True
                entity.state='pressed'

    def draw(self,sm,screen):
        self.surface.fill((250,250,0))
        self.surface.set_alpha(100)
        if len(sm.scenes)>0:
            sm.scenes[-2].draw(sm=sm,screen=screen)
        screen.blit(self.surface,(0,0))
        for button1 in self.buttons:
            button1.draw(screen)


    def on_Exit(self):
        for button1 in self.buttons:
            button1.selected=False
            button1.pressed=False

    def on_Start(self):
        pass

class BaseScene(Scene):
    pass

class OptionScene(Scene):
    def input(self,sm,inputstream):
        pass
    def update(self,sm,inputstream):
        pass
    def draw(self,sm,screen):
        pass

class FightScene(Scene):
    def __init__(self):
        self.hub1=hub.Hub()
        for card1 in globals.InFight.cards:
            card1.position=engine.Position(300,150,300,430)
        random.shuffle(globals.InFight.cards)
        self.turnManager=turn.TurnManager()
        self.endTurn=button.Button(globals.SCREEN_SIZE[0]-200,globals.SCREEN_SIZE[1]-300,"End Turn")
        globals.Buttons=[self.endTurn]
        self.buttonSystem=engine.ButtonSystem()
        self.turnManager.push(turn.PlayerTurn(),self.hub1)
        random.shuffle(self.hub1.deck.Cards)

    def update(self,sm,inputstream):
        self.buttonSystem.update()

        if self.endTurn.pressed:
            #self.turnManager.pop(self.hub1)
            self.endTurn.pressed=False
            self.endTurn.selected=False
            self.turnManager.push(turn.EnemyTurn(),self.hub1)

        self.turnManager.update(self.hub1)

        if len(self.turnManager.turns)>1:
            #self.turnManager.turns[-1].MainPhase(self.hub1)
            self.turnManager.pop(self.hub1)

        for entity in globals.InFight.entities:
            if entity.type=='enemy' and entity.life.life==0:
                globals.InFight.entities.remove(entity)
        if globals.InFight.isWon():
            globals.world.entities.pop(globals.indice)
            for entity in globals.world.entities:
                if entity.battle:
                    entity.battle=False
                if entity.type=='player':
                    globals.world.entities.remove(entity)
                    globals.world.entities.append(globals.InFight.entities[0])
                    globals.InFight.entities[0].battle=False
            globals.InFight.entities=[]
            sm.pop()
            sm.push(FadeTransitionScene([self],[WinFightScene()]))
        if globals.InFight.isLost():
            globals.world.entities.pop(globals.indice)
            for entity in globals.world.entities:
                if entity.battle:
                    entity.battle=False
                if entity.type=='player':
                    globals.world.entities.remove(entity)
                    globals.world.entities.append(globals.InFight.entities[0])
                    globals.InFight.entities[0].battle=False
            globals.InFight.entities=[]
            sm.pop()
            sm.push(FadeTransitionScene([self],[LooseFightScene()]))

    def draw(self,sm,screen):
        screen.fill(globals.BROWN)
        self.hub1.draw(screen)
        self.endTurn.draw(screen)
        utl.drawText(screen,"Fight Scene",50,50,globals.WHITE)

class WinFightScene(Scene):
    def __init__(self):
        self.choices=[]
        for i in range (0,3):
            cardName=random.choice(list(globals.CardsDico.keys()))
            card1=card.createCardFromStr(globals.CardsDico[cardName])()
            card1.scaling=0.55
            card1.position=engine.Position(200+int(200*i),150,300,430)
            self.choices.append(card1)
        self.test=[]

    def update(self,sm,inputstream):
        self.test=[]
        x,y=pg.mouse.get_pos()
        new_rect=pg.Rect(x,y,2,2)
        for card1 in self.choices:
            rect_entity=pg.Rect(card1.position.rect.x,
                card1.position.rect.y,
                int(card1.position.rect.w*card1.scaling),
                int(card1.position.rect.h*card1.scaling)
                )

            if rect_entity.colliderect(new_rect):
                card1.scan=True
            else:
                card1.scan=False

            if card1.scan and pg.mouse.get_pressed()[0]:
                card1.selected=True
                card1.scan=False
                self.test.append(card1)
                break
            elif card1.scan and not pg.mouse.get_pressed()[0]:
                selected=False
        if len(self.test)!=0:
            sm.pop()
            sm.push(FadeTransitionScene([self],[]))


    def draw(self,sm,screen):
        for card1 in self.choices:
            card1.draw(screen)
            if card1.scan:
                pg.draw.circle(screen,globals.BLUE,card1.position.rect.topleft,30)
    def on_Exit(self):
        globals.world.entities[-1].position.rect.topleft=globals.position
        for card1 in self.test:
            globals.Deck.decklist.append(card1)

class LooseFightScene(Scene):
    def __init__(self):
        self.test=[]
    def update(self,sm,inputstream):
        if inputstream.keyboard.isKeyPressed(pg.K_RETURN):
            sm.set(ClassChoiceScene())
    def draw(self,sm,screen):
        utl.drawText(screen,"You loose!",screen.get_rect().midtop[0]-150,screen.get_rect().midtop[1]+80,globals.PURPLE)
    def on_Exit(self):
        pass

class TransitionScene(Scene):
    def __init__(self,fromScenes,toScenes):
        self.currentPercentage = 0
        self.fromScenes = fromScenes
        self.toScenes = toScenes
    def update(self,sm,inputstream):
        self.currentPercentage += 1
        if self.currentPercentage >= 100:
            sm.pop()
            for s in  self.toScenes:
                sm.push(s)
            if len(self.toScenes)==0:
                sm.scenes[-1].on_Start()
        for scene in self.fromScenes:
            scene.update(sm,inputstream)
        if len(self.toScenes)>0:
            for scene in self.toScenes:
                scene.update(sm,inputstream)
        else:
            if len(sm.scenes)>1:
                sm.scenes[-2].update(sm,inputstream)

class FadeTransitionScene(TransitionScene):
    def draw(self, sm, screen):
        if self.currentPercentage<50:
            for scene in self.fromScenes:
                scene.draw(sm,screen)
        else:
            if len(self.toScenes)==0:
                if len(sm.scenes)>1:
                    sm.scenes[-2].draw(sm,screen)
            else:
                for scene in self.toScenes:
                    scene.draw(sm,screen)
        #fade overlay
        overlay=pg.Surface(globals.SCREEN_SIZE)

        alpha=int(abs((255-((255/50)*self.currentPercentage))))

        overlay.set_alpha(255 - alpha)
        overlay.fill(globals.WHITE)
        screen.blit(overlay,(0,0))

class GlissTransitionScene(TransitionScene):
    def draw(self,sm,screen):

        #gliss overlay
        overlay=pg.Surface(globals.SCREEN_SIZE)
        overlay.fill(globals.WHITE)
        if self.currentPercentage<99:
            for scene in self.fromScenes:
                scene.draw(sm,screen)
        else:
            if len(self.toScenes)==0:
                if len(sm.scenes)>1:
                    sm.scenes[-2].draw(sm,overlay)
            else:
                for scene in self.toScenes:
                    scene.draw(sm,overlay)

        x=globals.SCREEN_SIZE[1]-(globals.SCREEN_SIZE[1]//100)*self.currentPercentage

        screen.blit(overlay,(x,0))

class SceneManager:
    def __init__(self):
        self.scenes=[]

    def isEmpty(self):
        if len(self.scenes)==0:
            return True
        return False

    def input(self, inputstream):
        if len(self.scenes)>0:
            self.scenes[-1].input(self,inputstream)

    def update(self,inputstream):
        if len(self.scenes)>0:
            self.scenes[-1].update(self,inputstream)

    def draw(self,screen):
        screen.fill(globals.BLACK)
        if len(self.scenes)>0:
            self.scenes[-1].draw(self,screen)
        pg.display.flip()

    def push(self,scene):
        if len(self.scenes)>0:
            self.scenes[-1].on_Exit()
        self.scenes.append(scene)
        if len(self.scenes)>0:
            self.scenes[-1].on_Start()

    def pop(self):
        if len(self.scenes)>0:
            self.scenes[-1].on_Exit()
        self.scenes.pop()

    def set(self,scene):
        while len(self.scenes)>0:
            self.scenes.pop()
        #for s in scenes:
        self.scenes=[scene]

if __name__ == '__main__':
    scene=LooseFightScene()
    clock=pg.time.Clock()
    pg.init()
    sm,inputStream=[],InputStream()
    screen=pg.display.set_mode(globals.SCREEN_SIZE)
    running=True
    while running:
        inputStream.processInput()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running=False
        scene.input(sm,inputStream)
        scene.update(sm,inputStream)
        screen.fill((0,120,150))
        scene.draw(sm,screen)
        pg.display.flip()
        clock.tick(60)
    pg.quit()
