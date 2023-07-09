import pygame as pg

class Touche:
    def __init__(self,name,keyCode):
        self.name=name
        self.keyCode=keyCode

class ControlKeys:
    def __init__(self,touches):
        self.controlDico={}
        for touche in touches:
            self.controlDico[touche.name]=touche.keyCode

class Input:
    def __init__(self,up,down,left,right,interaction):
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.interaction=interaction

class Intention:
    def __init__(self):
        self.moveLeft =False
        self.moveRight= False
        self.jump = False
        self.interaction=False
