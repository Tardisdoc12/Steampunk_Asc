import pygame as pg
import engine
import random as rd
import rooms as rg

class WorldGenerator:
    def __init__(self,worldSizeW,worldSizeH,roomSizeW,roomSizeH,tuileSizeW,tuileSizeH,xInitial,yInitial):
        self.middleRoom=['middle','cross','T_down','T_up']
        #création du monde qui va être le niveau :
        #création de la ligne principale:
        world_middle=['right']
        up_occurence=[]
        low_occurence=[]
        for i in range (worldSizeW-2):
            world_middle.append(rd.choice(self.middleRoom))
            if world_middle[-1]=='cross' or world_middle[-1]=='T_up':
                up_occurence.append(len(world_middle)-1)
            if world_middle[-1]=='cross' or world_middle[-1]=='T_down':
                low_occurence.append(len(world_middle)-1)
        if len(up_occurence)<2 and len(up_occurence)!=0:
            if up_occurence[-1]==len(world_middle)-1:
                if world_middle[-1]=='cross':
                    world_middle[-1]='T_down'
                    up_occurence.pop()
                elif world_middle[-1]=='T_up':
                    world_middle[-1]='middle'
                    up_occurence.pop()
            elif world_middle[-1]=='T_down':
                world_middle[-1]='cross'
                up_occurence.append(len(world_middle)-1)
            else:
                world_middle[-1]='T_up'
                up_occurence.append(len(world_middle)-1)

        if len(low_occurence)<2 and len(low_occurence)!=0:
            if low_occurence[-1]==len(world_middle)-1:
                if world_middle[-1]=='T_down':
                    world_middle[-1]='middle'
                    low_occurence.pop()
                elif world_middle[-1]=='cross':
                    world_middle[-1]='T_up'
                    low_occurence.pop()
            elif world_middle[-1]=='T_up':
                world_middle[-1]='cross'
                low_occurence.append(len(world_middle)-1)
            else:
                world_middle[-1]='T_down'
                low_occurence.append(len(world_middle)-1)


        world_middle.append('left')

        #création du upper and lower world:
        world_upper=[]
        world_lower=[]

        for index in range (len(world_middle)):
            if up_occurence!=[]:
                if index==up_occurence[0]:
                    world_upper.append('G_right')
                elif index==up_occurence[-1]:
                    world_upper.append('G_left')
                elif index<up_occurence[-1] and index>up_occurence[0]:
                    if index in up_occurence:
                        world_upper.append('T_down')
                    else:
                        world_upper.append('middle')
                else:
                    world_upper.append('wall')
            else:
                world_upper.append('wall')
            if low_occurence!=[]:
                if index==low_occurence[0]:
                    world_lower.append('L_right')
                elif index==low_occurence[-1]:
                    world_lower.append('L_left')
                elif index<low_occurence[-1] and index>low_occurence[0]:
                    if index in low_occurence:
                        world_lower.append('T_up')
                    else:
                        world_lower.append('middle')
                else:
                    world_lower.append('wall')
            else:
                world_lower.append('wall')

        world_temporary=world_upper+world_middle+world_lower
        world=[]
        for i in world_temporary:
            world.append(rg.roomDico[i])
        self.rooms=Rooms(world,roomSizeW,roomSizeH,tuileSizeW,tuileSizeH,xInitial,yInitial,worldSizeW,worldSizeH)

class Rooms:
    def __init__(self,roomsList,roomSizeW,roomSizeH,tuileSizeW,tuileSizeH,xInitial,yInitial,worldSizeW,worldSizeH):
        self.roomsList=[]
        self.plateforms=[]
        for roomIndex in range (len(roomsList)):
            x=xInitial+(roomSizeW*tuileSizeW)*(roomIndex%worldSizeW)
            y=yInitial+(roomSizeH*tuileSizeH)*int(roomIndex/worldSizeW)
            room=roomsList[roomIndex]
            room1=Room(room,tuileSizeW,tuileSizeH,roomSizeW,roomSizeH,x,y)
            self.plateforms+=room1.tuileList
            self.roomsList.append(room1)

    def draw(self,screen):
        for room in self.roomsList:
            room.draw(screen)

class Room:
    def __init__(self,tuileList,tuileSizeW,tuileSizeH,roomSizeW,roomSizeH,xInitial,yInitial):
        self.tuileList = []
        for tuileIndex in range (len(tuileList)):
            #calcul de la position de la tuile:
            x=xInitial+(tuileIndex%roomSizeW)*tuileSizeW
            y=yInitial+int(tuileIndex/roomSizeW)*tuileSizeH

            #Creation de la tuile:
            tuile=Tuile(x,y,tuileList[tuileIndex])
            self.tuileList.append(tuile)

    def draw(self,screen):
        for tuile in self.tuileList:
            tuile.draw(screen)

class Tuile(engine.Entity):
    def __init__(self,x,y,numberTuile=466):
        if numberTuile!=466 and numberTuile!=4:
            self.image=pg.image.load('../Sprites/Room/tuile_'+str(numberTuile)+'.png')
            self.position=engine.Position(x,y,16*3,16*3)
            self.type='plateform'
        else:
            self.image=pg.image.load('../Sprites/Room/tuile_'+str(numberTuile)+'.png')
            self.position=engine.Position(x,y,16*3,16*3)
            self.type='fond'
    def draw(self,screen,x,y):
        screen.blit(pg.transform.scale(self.image,(16*3,16*3)),(x,y))

if __name__ == '__main__':
    import globals


    pg.init()
    screen=pg.display.set_mode(globals.SCREEN_SIZE,pg.RESIZABLE)
    running=True


    world1=WorldGenerator(5,3,8,6,16,16,100,50)


    clock=pg.time.Clock()

    fullscreen=False
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running=False
            if event.type == pg.VIDEORESIZE:
                    screen=pg.display.set_mode((event.w,event.h),pg.RESIZABLE)
            if event.type==pg.KEYDOWN:
                if event.key==pg.K_g:
                    world1=WorldGenerator(5,3,8,6,16,16,100,50)

        clock.tick(60)
        screen.fill(globals.PURPLE)
        world1.rooms.draw(screen)
        pg.display.flip()
    pg.quit()
