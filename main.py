import pygame as pg
import sys
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'assets')

class Bird():
    def __init__(self):
        self.sc = pg.display.set_mode((400,700))
        self.bird = pg.Rect(65,50,50,40)

        self.bg = pg.image.load(path.join(img_dir, "Background.png"))
        self.bg = pg.transform.scale(self.bg, (400,700))

        self.birds = pg.image.load(path.join(img_dir, "Bird1.png")).convert()
        self.birds.set_colorkey((255,0,255))
        self.birds =  pg.transform.scale(self.birds, (50,40))

        self.wallUp =  pg.image.load(path.join(img_dir, "Column1.png")).convert()
        self.wallDown =  pg.image.load(path.join(img_dir, "Column1.png")).convert()

        self.wallUp.set_colorkey((255,255,255))
        self.wallUp =  pg.transform.scale(self.wallUp, (80,420))
        self.wallDown.set_colorkey((255,255,255))
        self.wallDown =  pg.transform.scale(self.wallDown, (80,420))


        self.gap = 135
        self.wallX = 400
        self.birdY = 350
        self.jump = 0
        self.jumpSpeed = 10
        self.gravity = 5
        self.dead = False
        self.sprite = 0
        self.counter = 0
        self.offset = random.randint(-110,110)

    def updateWalls(self):
        self.wallX -= 2
        if self.wallX < -80:
            self.wallX = 400
            self.counter += 1
            self.offset = random.randint(-110,110)
    def updateBird(self):
        if self.jump:
            self.jumpSpeed -= 1
            self.birdY -= self.jumpSpeed
            self.jump -= 1
        else:
            self.birdY += self.gravity
            self.gravity += 0.2
        self.bird[1] = self.birdY
        upRect = pg.Rect(self.wallX,
                        360 + self.gap - self.offset + 10,
                        self.wallUp.get_width()-10,
                        self.wallUp.get_height()
                        )
        downRect = pg.Rect(self.wallX,
                        0 - self.gap - self.offset - 10,
                        self.wallDown.get_width() - 10,
                        self.wallDown.get_height()
                        )
        if upRect.colliderect(self.bird) or downRect.colliderect(self.bird):
            self.dead = True
            self.gravity = 5

        if not 0 < self.bird[1] < 720:
            self.bird[1] = 50
            self.birdY = 50
            self.dead = False
            self.counter = 0
            self.wallX = 400
            self.offset = random.randint(-135,135)



    def run(self):
        clock = pg.time.Clock()
        pg.font.init()
        font = pg.font.SysFont('Arial', 50)
        while 1:
            clock.tick(60)
            for i in pg.event.get():
                if i.type == pg.QUIT:
                    sys.exit()
                if (i.type == pg.KEYDOWN or i.type == pg.MOUSEBUTTONUP) and not self.dead:
                    self.jump = 200
                    self.gravity = 5
                    self.jumpSpeed = 15
                elif self.dead:
                    self.gravity = 5

            self.sc.blit(self.bg, (0,0))

            self.sc.blit(self.wallUp,
                         (self.wallX, 360 + self.gap - self.offset))
            self.sc.blit(self.wallDown,
                         (self.wallX, 0 - self.gap - self.offset))
            self.sc.blit(font.render(str(self.counter), -1, (255,0,0)), (200,50))
            self.sc.blit(self.birds, (65 , self.birdY ))


            self.updateWalls()
            self.updateBird()
            pg.display.update()

ex = Bird()
ex.run()
