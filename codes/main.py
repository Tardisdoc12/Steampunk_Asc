import pygame as pg
import scene
import globals
from inputstream import InputStream

sceneManager=scene.SceneManager()
startMenu=scene.StartGameScene()
sceneManager.push(startMenu)

inputstream=InputStream()

clock=pg.time.Clock()
pg.init()
screen=pg.display.set_mode(globals.SCREEN_SIZE)
pg.display.set_caption("Steampunk ascension")
running=True
while running:
    inputstream.processInput()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running=False
    if sceneManager.isEmpty():
        running=False
    sceneManager.input(inputstream)
    sceneManager.update(inputstream)
    sceneManager.draw(screen)
    clock.tick(60)

pg.quit()
