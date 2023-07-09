import pygame as pg
import globals

class Position:
    def __init__(self, x, y, w, h):
        self.rect=pg.Rect(x,y,w,h)

class Animations:
    def __init__(self):
        self.animationList={}
    def add(self, state, animation):
        self.animationList[state] = animation

class Animation:
    ''' Class for all the animation that will be used for the game.'''
    def __init__(self,imagesList):
        self.imagesList = imagesList
        self.imageIndex = 0
        self.animationTimer = 0
        self.animationspeed = 15

    def update(self):
        self.animationTimer += 1
        if self.animationTimer >= self.animationspeed:
            self.animationTimer = 0
            self.imageIndex += 1
            if self.imageIndex > len(self.imagesList)-1:
                self.imageIndex = 0

    def draw(self,screen,x,y,flipX,flipY,w,h):
        surface=pg.transform.scale(self.imagesList[self.imageIndex],(w,h))
        screen.blit(pg.transform.flip(surface,flipX,flipY),(x,y))

class Entity:
    def __init__(self):
        self.position = None
        self.state = 'idle'
        self.type ='normal'
        self.animations = Animations()
        self.direction='left'
        self.camera=None
        self.speed=0
        self.force=0
        self.life=None
        self.defense=0
        self.battle=False
        self.scaling=1
        self.input=None
        self.intention=None
        self.selected=False
        self.on_ground=False
        self.acceleration=0.2

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
        a.draw(screen,x,y,self.direction=='right',False,self.position.rect.w,self.position.rect.h)

class Camera:
    def __init__(self,x,y,w,h):
        self.rect = pg.Rect(x,y,w,h)
        self.worldY,self.worldX=0,0
        self.entityToTrack=None
    def setWorldPos(self, x, y):
        self.worldX = x
        self.worldY = y
    def trackEntity(self,e):
        self.entityToTrack=e

class System:
    def __init__(self):
        pass
    def check(self,entity):
        return True
    def update(self,screen=None,inputStream=None):
        for entity in globals.world.entities:
            if self.check(entity):
                self.updateEntity(inputStream,screen,entity)
    def updateEntity(self,inputStream,screen,entity):
        pass

class InputSystem(System):
    def check(self,entity):
        return entity.input is not None and entity.intention is not None
    def updateEntity(self,inputStream,screen,entity):
            #left =moveLeft
            if inputStream.keyboard.isKeyDown(entity.input.left):
                entity.intention.moveLeft=True
            else:
                entity.intention.moveLeft=False
            #right=moveRight
            if inputStream.keyboard.isKeyDown(entity.input.right):
                entity.intention.moveRight=True
            else:
                entity.intention.moveRight=False
            #up=jump
            if inputStream.keyboard.isKeyDown(entity.input.up):
                entity.intention.jump=True
            else:
                entity.intention.jump=False

class ButtonSystem(System):
    def check (self,entity):
        return entity.type=='button'
    def updateEntity(self,inputStream,screen,entity):
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

    def update(self,screen=None,inputStream=None):
        for entity in globals.Buttons:
            if self.check(entity):
                self.updateEntity(inputStream,screen,entity)

class AnimationSystem(System):
    def check(self,entity):
        return entity.animations is not None
    def updateEntity(self,inputStream,screen,entity):
        entity.animations.animationList[entity.state].update()

class CameraSystem(System):
    def __init__(self):
        super().__init__()

    def check(self,entity):
        return entity.camera is not None

    def updateEntity(self,inputStream,screen,entity):

        #Clipping the camera
        RectCamera=entity.camera.rect
        screen.set_clip(RectCamera)
        screen.fill(globals.YELLOW)

        offsetY,offsetX=0,0

        #update camera if tracking an entity:
        if entity.camera.entityToTrack is not None:

            trackedEntity = entity.camera.entityToTrack

            currentY=entity.camera.worldY
            currentX=entity.camera.worldX

            targetX=trackedEntity.position.rect.x + trackedEntity.position.rect.w/2
            targetY=trackedEntity.position.rect.y + trackedEntity.position.rect.h/2

            entity.camera.worldX = (currentX*0.95)+(targetX*0.05)
            entity.camera.worldY = (currentY*0.95)+(targetY*0.05)

        #calculate the offset:
        offsetX = RectCamera.x + RectCamera.w/2 - entity.camera.worldX
        offsetY = RectCamera.y + RectCamera.h/2 - entity.camera.worldY

        #Render the plateforms:
        for plateform in globals.world.plateforms:
            x=plateform.position.rect.x+offsetX
            y=plateform.position.rect.y+offsetY
            plateform.draw(screen,x,y)

        #Render the entities
        for entity in globals.world.entities:
            entity.draw(screen,x,y,offsetX,offsetY)
        screen.set_clip(None)

class PhysicsSystem(System):
    def check(self,entity):
        return entity.position is not None

    def updateEntity(self,inputStream,screen,entity):
        new_x=entity.position.rect.x
        new_y=entity.position.rect.y

        if entity.intention is not None:
            if entity.intention.moveLeft:
                new_x-=2
                entity.direction='left'
                entity.state='run'
            if entity.intention.moveRight:
                new_x+=2
                entity.direction='right'
                entity.state='run'
            if not entity.intention.moveRight and not entity.intention.moveLeft:
                entity.state='idle'
            if entity.intention.jump and entity.on_ground:
                entity.speed=-5

            #horizontal movement
            new_x_rect=pg.Rect(int(new_x),
                int(entity.position.rect.y),
                entity.position.rect.width,
                entity.position.rect.height)

            x_collision=False

            for plateform in globals.world.plateforms:
                if plateform.type=='plateform':
                    if plateform.position.rect.colliderect(new_x_rect):
                        x_collision=True
                        break
            for enti in globals.world.entities:
                if enti is not entity:
                    if enti.position.rect.colliderect(new_x_rect):
                        x_collision=True
                        break

            if x_collision==False:
                entity.intention.interaction=False
                entity.position.rect.x=new_x

            #Vertical movement
            entity.speed+=entity.acceleration
            new_y+=entity.speed

            new_y_rect=pg.Rect(int(entity.position.rect.x),
                int(new_y),
                entity.position.rect.width,
                entity.position.rect.height)

            y_collision=False
            entity.on_ground=False



            for plateform in globals.world.plateforms:
                if plateform.type=='plateform':
                    if plateform.position.rect.colliderect(new_y_rect):
                        y_collision=True
                        entity.speed=0
                        #if the plateform is below the entity
                        if plateform.position.rect.y>new_y:
                            #stick the entity to the plateform
                            entity.position.rect.y=plateform.position.rect.y-entity.position.rect.height
                            entity.on_ground=True
                        break

            if y_collision==False:
                entity.position.rect.y=int(new_y)

            #reset the intentions
            if entity.intention is not None:
                entity.intention.moveLeft=False
                entity.intention.moveRight=False
                entity.intention.jump=False

        if entity.intention is None:
            #horizontal movement:
            if entity.direction=='right':
                x,y=entity.position.rect.bottomright
                x_old,y_old=entity.position.rect.topright
            else:
                x,y=entity.position.rect.bottomleft
                x_old,y_old=entity.position.rect.topleft
            new_rect_collision=pg.Rect(x,y,2,5)

            x_collision=False
            absolute_x_collision=False
            new_x_rect=pg.Rect(x_old,y_old,1,entity.position.rect.h)
            for plateform in globals.world.plateforms:
                if plateform.position.rect.colliderect(new_rect_collision):
                    if plateform.type=='fond':
                        x_collision=True
                        break
                if plateform.type=='plateform':
                    if plateform.position.rect.colliderect(new_x_rect):
                        x_collision=True
                        break
            if entity.balise<=0:
                x_collision=True
                entity.balise=entity.save_balise
            for entity1 in globals.world.entities:
                if entity1.type=='player' and entity1.position.rect.colliderect(new_x_rect):
                    absolute_x_collision=True
                    break

            if x_collision and not absolute_x_collision:
                if entity.direction=='right':
                    entity.direction='left'
                else:
                    entity.direction='right'
            elif not x_collision and not absolute_x_collision:
                if entity.direction=='right':
                    entity.state='run'
                    entity.position.rect.x+=2
                    entity.balise-=1
                else:
                    entity.balise-=1
                    entity.state='run'
                    entity.position.rect.x-=2

            #Vertical movement
            entity.speed+=entity.acceleration
            new_y+=entity.speed

            new_y_rect=pg.Rect(int(entity.position.rect.x),
                int(new_y),
                int(entity.position.rect.width),
                int(entity.position.rect.height))

            y_collision=False
            entity.on_ground=False

            for plateform in globals.world.plateforms:
                if plateform.type=='plateform':
                    if plateform.position.rect.colliderect(new_y_rect):
                        y_collision=True
                        entity.speed=0
                        #if the plateform is below the entity
                        if plateform.position.rect.y>new_y:
                            #stick the entity to the plateform
                            entity.position.rect.y=plateform.position.rect.y-entity.position.rect.h
                            entity.on_ground=True
                        break

            if y_collision==False:
                entity.position.rect.y=int(new_y)

def verification(card):
    for entity in globals.InFight.cards:
        if entity is not card and entity.selected:
            return False
        elif entity is not card and entity.scan:
            return False
    return True

class CardSystem(System):
    def check(self,entity):
        return entity.type=='card' and entity.location=='hand'

    def updateEntity(self,inputStream,screen,entity):
        if verification(entity):
            #implementation of card state possible
            '''Entity=Card here'''
            x,y=pg.mouse.get_pos()
            new_rect=pg.Rect(x,y,2,2)
            rect_entity=pg.Rect(entity.position.rect.x,
                entity.position.rect.y,
                int(entity.position.rect.w*entity.scaling),
                int(entity.position.rect.h*entity.scaling)
                )
            if new_rect.colliderect(rect_entity) and not pg.mouse.get_pressed()[0]:
                entity.scan=True
            elif not new_rect.colliderect(rect_entity) and not pg.mouse.get_pressed()[0]:
                entity.scan=False
            if rect_entity.colliderect(new_rect) and pg.mouse.get_pressed()[0]:
                entity.scan=False
                entity.selected=True
            elif rect_entity.colliderect(new_rect) and not pg.mouse.get_pressed()[0]:
                for fighter in globals.InFight.entities:
                    if new_rect.colliderect(fighter.position.rect) and entity.target==fighter.type:
                        if entity.effect(fighter):
                            entity.activated=True

                entity.selected=False
            else:
                entity.selected=False

            #implementation of what state do what:
            #if card.scan is True or not
            if entity.scan:
                entity.zoom=True
            else:
                entity.zoom=False
            #if card.selected is True or not:
            if entity.selected:
                entity.alpha=120
                entity.position.rect.x=pg.mouse.get_pos()[0]-int(entity.position.rect.w*entity.scaling)/2
                entity.position.rect.y=pg.mouse.get_pos()[1]-int(entity.position.rect.h*entity.scaling)/2
            else:
                entity.alpha=255

    def draw(self,screen):
        for entity in globals.world.cards:
            if entity.location=='hand':
                new_surface=pg.Surface((240,345))
                new_surface.fill(globals.BLACK)
                old_x=entity.position.rect.x
                old_y=entity.position.rect.y
                old_scaling=entity.scaling
                if entity.zoom:
                    entity.scaling=0.8
                    entity.position.rect.x=0
                    entity.position.rect.y=0
                    entity.draw(new_surface)
                    screen.blit(new_surface,(old_x-50,old_y-230,0,0))
                    entity.alpha=0
                entity.scaling=old_scaling
                entity.position.rect.x=old_x
                entity.position.rect.y=old_y
                entity.draw(screen)

    def update(self,screen=None,inputStream=None):
        for card in globals.InFight.cards:
            if self.check(card):
                self.updateEntity(inputStream,screen,card)

class EnterOnBattleSystem(System):
    def check(self,entity):
        return entity.type=='player'and not entity.battle

    def updateEntity(self,inputStream,screen,entity):
        for otherEntity in globals.world.entities:
            #BattleSystem
            if otherEntity is not entity and otherEntity.type=='enemy' and not otherEntity.battle:

                if entity.direction=='right':
                    x,y=entity.position.rect.topright
                else:
                    x,y=entity.position.rect.topleft
                    x-=entity.position.rect.w
                new_rect_player=pg.Rect(x,y,entity.position.rect.w,entity.position.rect.h)
                if new_rect_player.colliderect(otherEntity.position.rect) and inputStream.keyboard.isKeyDown(entity.input.interaction):
                    entity.intention.interaction=True
                else:
                    entity.intention.interaction=False

                if entity.intention.interaction:
                    entity.battle=True
                    otherEntity.battle=True
                    break
                else:
                    entity.battle=False
                    otherEntity.battle=False

if __name__ == '__main__':
    import utilities as utils
    import inputstream
    import player
    pg.init()
    screen=pg.display.set_mode((1000,800))
    running=True

    clock=pg.time.Clock()

    entities=[]
    plateforms=[]
    inputStream=inputstream.InputStream()
    inputManager=[]

    entities.append(utils.makeEnemy(0,0))
    entities.append(player.Player(10,10))
    entities[1].camera=Camera(250,250,300,300)
    entities[1].camera.trackEntity(entities[1])
    cameraSys=CameraSystem()

    #PLAY SCREEN
    while running:
        inputStream.processInput()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running=False
        entities[1].update(inputStream)
        screen.fill(globals.PURPLE)
        cameraSys.update(screen=screen)
        pg.display.flip()

        clock.tick(60)
    pg.quit()
