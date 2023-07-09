import pygame as pg
import globals
import time
class Turn:
    def __init__(self):
        pass
    def drawPhase(self,hub):
        pass
    def MainPhase(self,hub):
        pass
    def endPhase(self,hub):
        pass

class PlayerTurn(Turn):
    def drawPhase(self,hub):
        for entity in globals.InFight.entities:
            if entity.type=='player':
                hub.pa=entity.pa
                if entity.defense>0:
                    entity.defense=0
        if len(hub.deck.Cards)>=3:
            hub.DrawMultiple(3)
        else:
            hub.DrawMultiple(len(hub.deck.Cards))
            hub.Shuffle()
            hub.DrawMultiple(3-len(hub.hand.Cards))
    def MainPhase(self,hub):
        hub.update()
        hub.Shuffle()
    def endPhase(self,hub):
        hub.DiscardMultiple(len(hub.hand.Cards))

class EnemyTurn(Turn):
    def drawPhase(self,hub):
        for enemy in globals.InFight.entities:
            if enemy.type=='enemy':
                enemy.defense=0
                if enemy.force>0:
                    enemy.nbrTurn+=1
                if enemy.nbrTurn>2:
                    enemy.force=0
    def MainPhase(self,hub):
        time.sleep(0.5)
        for enemy in globals.InFight.entities:
            if enemy.type=='enemy':
                enemy.attack()
        return 3

    def endPhase(self,hub):
        pass

class TurnManager:
    def __init__(self):
        self.turns=[]

    def isEmpty(self):
        if len(self.turns)==0:
            return True
        return False

    def update(self,hub):
        if len(self.turns)>0:
            self.turns[-1].MainPhase(hub)

    def push(self,turn,hub):
        if len(self.turns)>0:
            self.turns[-1].endPhase(hub)
        self.turns.append(turn)
        if len(self.turns)>0:
            self.turns[-1].drawPhase(hub)

    def pop(self,hub):
        if len(self.turns)>0:
            self.turns[-1].endPhase(hub)
        self.turns.pop()
        if len(self.turns)>0:
            self.turns[-1].drawPhase(hub)

    def set(self,turn):
        while len(self.turns)>0:
            self.turns.pop()
        self.turns=[turn]
