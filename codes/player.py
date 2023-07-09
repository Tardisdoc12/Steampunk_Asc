import engine
import inputmanager
import pygame as pg

class Player(engine.Entity):
    '''         Class for the Player.
    Using the animation for the control and the idle.'''
    def __init__(self):
        super().__init__()
        x=0
        y=0
        self.type='player'
        self.direction='right'
        self.battle=False
        self.pa=None
        self.archetype=None
        self.position=engine.Position(x,y,17,29)
        self.life=None
        self.input=inputmanager.Input(pg.K_UP,pg.K_DOWN,pg.K_LEFT,pg.K_RIGHT,pg.K_e)
        self.intention=inputmanager.Intention()

    def putAt(self,x,y):
        self.position.rect.x=x
        self.position.rect.y=y

if __name__ == '__main__':
    import globals
    import level
    import levelgenerator as lg

    pg.init()
    running=True
    clock=pg.time.Clock()

    entities,inputManager,plateforms=[],[],[]
    player=Player(x=20*3,y=112*3,life=90)
    entities.append(player)
    entities[0].camera=engine.Camera(0,0,700,700)
    entities[0].camera.trackEntity(entities[0])
    inputStream=inputstream.InputStream()
    physicsSystem=engine.PhysicsSystem()
    animationSystem=engine.AnimationSystem()
    Niveau=lg.WorldGenerator(5,3,8,6,16*3,16*3,0,0)

    level1=level.Level(entities=entities,plateforms=Niveau.rooms.plateforms)
    globals.world=level1
    screen=pg.display.set_mode(globals.SCREEN_SIZE)
    cameraSys=engine.CameraSystem()
    inputSystem=engine.InputSystem()

    while running:

        inputStream.processInput()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running=False
        inputSystem.update(inputStream=inputStream)
        physicsSystem.update(screen=screen,inputStream=inputStream)
        animationSystem.update()

        clock.tick(60)
        screen.fill(globals.BROWN)
        cameraSys.update(screen=screen)
        pg.display.flip()

    pg.quit()
