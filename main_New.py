import pygame as pg
import sys
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'assets')

WIDTH = 400
HEIGHT = 700
FPS = 60
COUNTER = 0

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255,0,255)

pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Flappy Bird!")
clock = pg.time.Clock()

font_name = pg.font.match_font('arial')

def draw_text(surf, text, size, x, y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, RED)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

class Bird(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load(path.join(img_dir, "Bird1.png")).convert()
        self.image.set_colorkey(PURPLE)
        self.image =  pg.transform.scale(self.image, (50,40))

        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 40

        self.dead = False
        self.birdY = 350
        self.jump = 0
        self.jumpSpeed = 15
        self.gravity = 5
        self.gravity_k = 0.2

    def jump_set(self):
        bird.jump = 200
        bird.gravity = 5
        bird.jumpSpeed = 15
    def dead_act(self):
        self.rect.y = 50
        self.birdY = 50
        self.gravity = 5
        self.dead = False
        for i in columns:
            i.start()
            i.score = 0

    def update(self):
        if self.jump:
            self.jumpSpeed -= 1
            self.birdY -= self.jumpSpeed
            self.jump -= 1
        else:
            self.birdY += self.gravity
            self.gravity += self.gravity_k
        self.rect.y = self.birdY

        if self.rect.y > 700 or self.rect.y < 0:
            self.dead_act()

class Column(pg.sprite.Sprite):
    def __init__(self, side):
        pg.sprite.Sprite.__init__(self)

        self.score = 0

        self.side = side
        self.gap = 135
        self.offset = random.randint(65,110)
        self.wallx_start = 400

        self.image = pg.image.load(path.join(img_dir, "Column1.png")).convert()
        self.image.set_colorkey(WHITE)
        self.image =  pg.transform.scale(self.image, (80,420))

        self.rect = self.image.get_rect()

        self.start()

    def update(self):
        self.rect.x -= 2
        if self.rect.x < -80:
            self.score += 1
            self.start()
    def start(self):
        self.offset = random.randint(65,110)
        if self.side == "top":
            self.rect.y = 360 + self.gap - self.offset + 10
        elif self.side == "bot":
            self.rect.y = 0 - self.gap - self.offset - 1

        self.rect.x = self.wallx_start


background = pg.image.load(path.join(img_dir, "Background.png")).convert()
background = pg.transform.scale(background, (400,700))
background_rect = background.get_rect()

all_sprites = pg.sprite.Group()
columns = pg.sprite.Group()

for i in ["top","bot"]:
    column = Column(i)
    all_sprites.add(column)
    columns.add(column)

bird = Bird()
all_sprites.add(bird)

running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pg.event.get():
        # check for closing window
        if event.type == pg.QUIT:
            running = False
        if (event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONUP) and not bird.dead:
            bird.jump_set()
    # Обновление
    all_sprites.update()

    hits = pg.sprite.spritecollide(bird , columns, False)
    if hits:
        bird.dead = True

    # Рендеринг
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(column.score),  45, WIDTH / 2, 10)
    # После отрисовки всего, переворачиваем экран
    pg.display.flip()

pg.quit()
