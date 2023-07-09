import pygame as pg

def drawText(screen,text,pos_x,pos_y,couleur):
    police=pg.font.SysFont("monospace",50)
    police.set_bold(True)
    image_texte=police.render(text,1,couleur)
    screen.blit(image_texte,(pos_x,pos_y))
