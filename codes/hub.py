import pygame as pg
import globals
import random
import button

def verification(card):
    for entity in globals.InFight.cards:
        if entity is not card and entity.selected:
            return False
        elif entity is not card and entity.scan:
            return False
    return True

def drawDeck(cardDico,surface):
    width=surface.get_rect().w
    step_x=(width-10)//3
    step_y=-1
    i=0
    for key in cardDico.keys():
        index=i%3
        if index == 0:
            step_y+=1
        card=cardDico[key][0]
        card.scaling=0.2
        card.position.rect.x=10+step_x*index
        card.position.rect.y=10+step_y*150
        card.draw(surface)
        pg.draw.circle(surface,(0,120,120),(card.position.rect.x+55,card.position.rect.y+5),10)
        police=pg.font.SysFont("monospace",16)
        image_texte=police.render(str(cardDico[key][1]),1,globals.BLACK)
        surface.blit(image_texte,(card.position.rect.x+50,card.position.rect.y-3))
        i+=1

def creaDico(cards):
    dico={}
    if len(cards)==0:
        return dico
    for card in cards:
        if not card.Name in dico:
            ''' On regarde si la carte existe déjà dans le dictionnaire.
            Si oui on incrémente le nombre de carte de ce nom là dans le deck de 1.
            Sinon c'est qu'il n'y a qu'une carte dans le deck.'''
            dico[card.Name]=(card,1)
        else:
            dico[card.Name]=(dico[card.Name][0],dico[card.Name][1]+1)
    return dico

def DrawCircleWritting(screen,x,y,radius,color,fontSize,text):
    image=pg.Surface((int(radius*2),int(radius*2)))
    image.fill((0,0,100,0))
    pg.draw.circle(image,color,image.get_rect().center,radius)

    police=pg.font.SysFont("monospace",fontSize)
    image_texte=police.render(text,1,globals.BLACK)
    image.blit(image_texte,(image.get_rect().w//2-image_texte.get_rect().w//2,image.get_rect().h//2-image_texte.get_rect().h//2))
    screen.blit(image,(x,y))

class Zone:
    def __init__(self):
        self.Zone=None
        self.Cards=[]
        self.open=False

    def draw(self,screen):
        pass

    def check(self,card):
        pass

    def update(self):
        for card in self.Cards:
            if self.check(card):
                self.updateCard(card)

    def updateCard(self,card):
        pass

class Hand(Zone):
    def __init__(self):
        super().__init__()
        self.Zone=pg.Surface((globals.SCREEN_SIZE[0]-300,200))

    def check(self,card):
        return self.Cards!=0

    def updateCard(self,card):
        if verification(card):
            #implementation of card state possible
            x,y=pg.mouse.get_pos()
            new_rect=pg.Rect(x,y,2,2)
            rect_card=pg.Rect(card.position.rect.x,
                card.position.rect.y,
                int(card.position.rect.w*card.scaling),
                int(card.position.rect.h*card.scaling)
                )
            if new_rect.colliderect(rect_card) and not pg.mouse.get_pressed()[0]:
                card.scan=True
            elif not new_rect.colliderect(rect_card) and not pg.mouse.get_pressed()[0]:
                card.scan=False
            if rect_card.colliderect(new_rect) and pg.mouse.get_pressed()[0]:
                card.scan=False
                card.selected=True
            elif rect_card.colliderect(new_rect) and not pg.mouse.get_pressed()[0]:
                for fighter in globals.InFight.entities:
                    if new_rect.colliderect(fighter.position.rect) and card.target==fighter.type:
                        card.activated=True
                card.selected=False
            else:
                card.selected=False
            #implementation of what state do what:
            #if card.scan is True or not
            if card.scan:
                card.zoom=True
            else:
                card.zoom=False
            #if card.selected is True or not:
            if card.selected:
                card.alpha=120
                card.position.rect.x=pg.mouse.get_pos()[0]-int(card.position.rect.w*card.scaling)//2
                card.position.rect.y=pg.mouse.get_pos()[1]-int(card.position.rect.h*card.scaling)//2
            else:
                card.alpha=255

    def draw(self,screen):
        #Zone for hand
        self.Zone.fill(globals.PURPLE)
        self.Zone.set_alpha(10)
        screen.blit(self.Zone,(150,screen.get_height()-200))
        #Cards in hands:
        if len(self.Cards)!=0:
            step=self.Zone.get_width()//(len(self.Cards)+1)
            for index in range (len(self.Cards)):
                if not self.Cards[index].selected:
                    card=self.Cards[index]

                    #card.position.rect.x=150+index*step
                    card.position.rect.x=150+(index+1)*step-int(card.position.rect.w*card.scaling)//2
                    card.position.rect.y=globals.SCREEN_SIZE[1]-200

            for entity in self.Cards:
                new_surface=pg.Surface((240,345))
                new_surface.fill(globals.BLACK)
                old_x=entity.position.rect.x
                old_y=entity.position.rect.y
                old_scaling=0.55#entity.scaling
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

class Deck(Zone):
    def __init__(self):
        super().__init__()
        self.image=pg.Surface((60,60))
        self.Zone=pg.Surface((300,globals.SCREEN_SIZE[1]-200))
        self.target=False
        self.dico={}

    def check(self,card):
        return True

    def updateCard(self,card):
        #the deck is not open yet but we may have the intention to do it
        x,y=pg.mouse.get_pos()
        new_rect=pg.Rect(x,y,5,5)
        rect=pg.Rect(globals.SCREEN_SIZE[0]-75,globals.SCREEN_SIZE[1]-100,60,60)
        if new_rect.colliderect(rect):
            self.target=True
        else:
            self.target=False

        #the deck can be open and we can see all the cards inside it
        if self.target and pg.mouse.get_pressed()[0]:
            self.open=True
        else:
            self.open=False

    def update(self):
        self.dico=creaDico(self.Cards)
        if len(self.Cards)==0:
            self.open=False
        for card in self.Cards:
            if self.check(card):
                self.updateCard(card)

    def draw(self,screen):
        self.image.fill((0,0,100,0))
        pg.draw.circle(self.image,globals.YELLOW,self.image.get_rect().center,30)
        screen.blit(self.image,(globals.SCREEN_SIZE[0]-75,globals.SCREEN_SIZE[1]-100))
        police=pg.font.SysFont("monospace",40)
        image_texte=police.render(str(len(self.Cards)),1,globals.BLACK)
        screen.blit(image_texte,(globals.SCREEN_SIZE[0]-55,globals.SCREEN_SIZE[1]-90))
        if self.open:
            self.Zone.fill(globals.BLACK)
            drawDeck(self.dico,self.Zone)
            screen.blit(self.Zone,(globals.SCREEN_SIZE[0]-300,0))

class Graveyard(Zone):
    def __init__(self):
        super().__init__()
        self.image=pg.Surface((60,60))
        self.Zone=pg.Surface((300,globals.SCREEN_SIZE[1]-200))
        self.target=False
        self.dico={}

    def check(self,card):
        return True

    def updateCard(self,card):
        #the deck is not open yet but we may have the intention to do it
        x,y=pg.mouse.get_pos()
        new_rect=pg.Rect(x,y,5,5)
        rect=pg.Rect(10,globals.SCREEN_SIZE[1]-160,60,60)
        if new_rect.colliderect(rect):
            self.target=True
        else:
            self.target=False

        #the deck can be open and we can see all the cards inside it
        if self.target and pg.mouse.get_pressed()[0]:
            self.open=True
        else:
            self.open=False

    def update(self):
        self.dico=creaDico(self.Cards)
        if len(self.Cards)==0:
            self.open=False
        for card in self.Cards:
            if self.check(card):
                self.updateCard(card)

    def draw(self,screen):
        self.image.fill((0,0,100,0))
        pg.draw.circle(self.image,globals.BROWN,self.image.get_rect().center,30)
        screen.blit(self.image,(10,globals.SCREEN_SIZE[1]-160))
        police=pg.font.SysFont("monospace",40)
        image_texte=police.render(str(len(self.Cards)),1,globals.BLACK)
        screen.blit(image_texte,(28,globals.SCREEN_SIZE[1]-148))
        if self.open:
            self.Zone.fill(globals.BROWN)
            drawDeck(self.dico,self.Zone)
            screen.blit(self.Zone,(0,0))

class Remove(Zone):
    def __init__(self):
        super().__init__()
        self.image=pg.Surface((60,60))
        self.Zone=pg.Surface((300,globals.SCREEN_SIZE[1]-200))
        self.target=False
        self.dico={}

    def check(self,card):
        return True

    def updateCard(self,card):
        #the deck is not open yet but we may have the intention to do it
        x,y=pg.mouse.get_pos()
        new_rect=pg.Rect(x,y,5,5)
        rect=pg.Rect(10,globals.SCREEN_SIZE[1]-80,60,60)
        if new_rect.colliderect(rect):
            self.target=True
        else:
            self.target=False

        #the deck can be open and we can see all the cards inside it
        if self.target and pg.mouse.get_pressed()[0]:
            self.open=True
        else:
            self.open=False

    def update(self):
        self.dico=creaDico(self.Cards)
        if len(self.Cards)==0:
            self.open=False
        for card in self.Cards:
            if self.check(card):
                self.updateCard(card)

    def draw(self,screen):
        self.image.fill((0,0,100,0))
        pg.draw.circle(self.image,globals.PURPLE,self.image.get_rect().center,30)
        screen.blit(self.image,(10,globals.SCREEN_SIZE[1]-80))
        police=pg.font.SysFont("monospace",40)
        image_texte=police.render(str(len(self.Cards)),1,globals.BLACK)
        screen.blit(image_texte,(28,globals.SCREEN_SIZE[1]-68))
        if self.open:
            self.Zone.fill(globals.PURPLE)
            drawDeck(self.dico,self.Zone)
            screen.blit(self.Zone,(0,0))

class EntityZone(Zone):
    def __init__(self,type,x,y,w,h,direction):
        self.surface=pg.Surface((w,h))
        self.entities_temp=[]
        self.x=x
        self.y=y
        for entity in globals.InFight.entities:
            if entity.type==type:
                self.entities_temp.append(entity)
        step_x=self.surface.get_rect().w//(len(self.entities_temp)+1)
        for index in range(len(self.entities_temp)):
            entity=self.entities_temp[index]
            entity.direction=direction
            entity.position.rect.x=step_x*(index+1)-entity.position.rect.w//2
            entity.position.rect.y=y+self.surface.get_rect().h-entity.position.rect.h

    def draw(self,screen):
        step_x=self.surface.get_rect().w//(len(self.entities_temp)+1)
        for index in range(len(self.entities_temp)):
            entity=self.entities_temp[index]
            entity.position.rect.x=self.x+step_x*(index+1)-entity.position.rect.w//2
            entity.position.rect.y=self.y+self.surface.get_rect().h-entity.position.rect.h
            entity.draw(screen,entity.position.rect.x,entity.position.rect.y,0,0)

class Hub:
    def __init__(self):
        self.hand=Hand()
        self.deck=Deck()
        self.graveyard=Graveyard()
        self.remove=Remove()
        self.playerZone=EntityZone('player',100,200,300,200,'right')
        self.enemyZone=EntityZone('enemy',globals.SCREEN_SIZE[0]//2+100,200,300,200,'left')
        self.notDraw=False
        for entity in globals.InFight.entities:
            if entity.type=='player':
                self.pa=entity.pa
        for card in globals.InFight.cards:
            self.deck.Cards.append(card)


    def sendGY(self,card):
        try:
            index=self.hand.Cards.index(card)
            self.hand.Cards[index].location='graveyard'
            card_temp=self.hand.Cards[index]
            self.hand.Cards.pop(index)
            self.graveyard.Cards.append(card_temp)
        except:
            print('Vous ne pouvez pas la discard!')

    def activate(self):
        for card in self.hand.Cards:
            if card.activated and (self.pa>0 or card.Cost==0):
                for entity in globals.InFight.entities:
                    if card.effect(entity,self):
                        self.pa-=card.Cost
                        card.activated=False
                        card.scan=False
                        self.sendGY(card)

    #For cards :
    #Draw card
    def Draw(self,numberCards=1):
        for index in range(1,numberCards+1):
            try:
                self.deck.Cards[-1*index].location='hand'
                card_temp=self.deck.Cards[-1*index]
                card_temp.scaling=0.55
                self.deck.Cards.pop()
                self.hand.Cards.append(card_temp)
            except:
                self.notDraw=True

    def DrawMultiple(self,numberCards=2):
        for nbrCard in range(numberCards):
            self.Draw()

    def update(self):
        self.hand.update()
        self.deck.update()
        self.remove.update()
        self.graveyard.update()
        self.activate()

    #send card from hand to graveyard
    def Discard(self):
        for index in range(1,2):
            try:
                self.hand.Cards[-1*index].location='graveyard'
                card_temp=self.hand.Cards[-1*index]
                self.hand.Cards.pop()
                self.graveyard.Cards.append(card_temp)
            except:
                print('Vous ne pouvez plus Discard!')

    def DiscardMultiple(self,numberCards=2):
        for i in range(1,numberCards+1):
            self.Discard()

    #banish a card
    def Banish(self,numberCards=1,fromZone=None):
        try:
            for index in range (1,numberCards+1):
                self.hand.Cards[-1*index].location='remove'
                card_temp=self.hand.Cards[-1*index]
                self.hand.Cards.pop()
                self.remove.Cards.append(card_temp)
        except:
            print('Vous ne pouvez plus Bannir!')

    #Shuffle graveyard into Deck
    def Shuffle(self):
        if len(self.deck.Cards) == 0:
            index=len(self.graveyard.Cards)-1
            random.shuffle(self.graveyard.Cards)
            while index!=-1:
                self.graveyard.Cards[index].location='deck'
                card_temp=self.graveyard.Cards[index]
                self.graveyard.Cards.pop()
                self.deck.Cards.append(card_temp)
                index-=1

    #draw all the zones.
    def draw(self,screen):
        self.playerZone.draw(screen)
        self.enemyZone.draw(screen)
        self.hand.draw(screen)
        self.deck.draw(screen)
        self.remove.draw(screen)
        self.graveyard.draw(screen)
        DrawCircleWritting(screen,globals.SCREEN_SIZE[0]-100,globals.SCREEN_SIZE[0]-400,30,globals.GREEN,40,str(self.pa))
        if self.notDraw:
            police=pg.font.SysFont("monospace",50)
            image_texte=police.render("You can not draw any card!",1,globals.BLACK)
            screen.blit(image_texte,(globals.SCREEN_SIZE[0]//2-image_texte.get_rect().w//2,globals.SCREEN_SIZE[1]//2-image_texte.get_rect().h//2))

if __name__ == '__main__':
    import card
    import level
    import engine
    import player
    pg.init()
    database=card.CardsDatabase()
    database.createDatabase()
    database.createDico()
    screen=pg.display.set_mode((1000,800))
    cards=[]
    scaling=0.55
    cardInfo=database.cardsDico['Griffe']
    card2=card.Card((1,'Test',1,'Ceci est plus un test qu\'autre chose!','Neutre','player',-3,0,0))
    card2.position=engine.Position(0,0,300,430)
    card2.scaling=scaling
    for card_index in range(0,4):
        card1=card.Card(cardInfo)
        card1.scaling=scaling
        card1.position=engine.Position(300+card_index*30,150,300,430)
        card1.target='player'
        cards.append(card1)
    cards.append(card2)
    joueur=player.Player(500,400,90,'Scientific')
    joueur.battle=True
    level1=level.Level(cards=cards,entities=[joueur])
    globals.InFight=level1
    hub=Hub()
    running=True

    cardSystem=engine.CardSystem()

    while running:
        for event in pg.event.get():
            if event.type==pg.QUIT:
                running=False
            if event.type==pg.KEYDOWN:
                if event.key==pg.K_a:
                    hub.Draw()
                if event.key==pg.K_e:
                    hub.Discard()
                if event.key==pg.K_p:
                    hub.DrawMultiple(2)
                if event.key==pg.K_s:
                    hub.Banish()
        #cardSystem.update()
        hub.update()
        hub.Shuffle()

        screen.fill((0,0,100))
        hub.draw(screen)
        pg.display.flip()
    pg.quit()
