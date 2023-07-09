import pygame as pg
import utilities as util
import globals
import inputstream 
class ButtonUI:
    def __init__(self,keycode,text,x,y):
        self.keyCode=keycode
        self.text=text
        self.x=x
        self.y=y
        self.pressed=False
        self.on=False
        self.timer=20

    def update(self,inputstream):
        self.pressed=inputstream.keyboard.isKeyPressed(self.keyCode)
        if self.pressed:
            self.on=True
        if self.on:
            self.timer-=1
            if self.timer<=0:
                self.on=False
                self.timer=20

    def draw(self,screen):
        if self.on:
            colour=globals.WHITE
        else:
            colour=globals.GREEN
        util.drawText(screen, self.text, self.x,self.y,colour)
