import pygame as pg
import sys
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 600
HEIGHT = 450
FPS = 100

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Создаем игру и окно
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Ping Pong")
clock = pg.time.Clock()
pg.mouse.set_visible(False)

cursor_img = pg.image.load(path.join(img_dir, "cursor1.png")).convert()
cursor_img.set_colorkey(BLACK)
cursor_rect = cursor_img.get_rect()




font_name = pg.font.match_font('arial')
def draw_text(surf, text, size, x, y, color):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def mouse_handler():
    mouse_k = pg.mouse.get_pos()
    if not (mouse_k[0]+2>=WIDTH or mouse_k[1]+2>=HEIGHT or mouse_k[0]<=0 or mouse_k[1]<=0)and not delay:
            cursor_rect.center = mouse_k
            screen.blit(cursor_img, cursor_rect)

def show_go_screen():
    screen.fill(BLACK)
    draw_text(screen, "PING PONG!", 64, WIDTH / 2, HEIGHT / 4, BLUE)
    solo_but = create_button(screen,WIDTH//2,HEIGHT//2,   BLACK,"solo_but.png")
    duo_but = create_button( screen,WIDTH//2,HEIGHT//2+60,BLACK,"duo_but.png")
    pg.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.MOUSEBUTTONUP and solo_but.collidepoint(pg.mouse.get_pos()):
                waiting = False
                return 2
            if event.type == pg.MOUSEBUTTONUP and duo_but.collidepoint(pg.mouse.get_pos()):
                waiting = False
                return 0
        screen.fill(BLACK)
        draw_text(screen, "PING PONG!", 64, WIDTH / 2, HEIGHT / 4, BLUE)
        solo_but = create_button(screen,WIDTH//2,HEIGHT//2,   BLACK,"solo_but.png")
        duo_but = create_button( screen,WIDTH//2,HEIGHT//2+60,BLACK,"duo_but.png")

        mouse_handler()

        pg.display.flip()
def create_button(surface,x,y,colorkey,img):
    but_img = pg.image.load(path.join(img_dir, img)).convert()
    but_img.set_colorkey(colorkey)
    but_rect = but_img.get_rect()
    but_rect.midtop = (x , y)
    surface.blit(but_img,but_rect)
    return but_rect


class Paddle(pg.sprite.Sprite):
    def __init__(self, x,y,vector, state):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((15,60))
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.vector = vector
        self.state = state

    def update(self):
        self.speedy = 0
        keystate = pg.key.get_pressed()
        condition = [0,0]

        if self.state == 1:
            condition[0] = keystate[pg.K_UP]
            condition[1] = keystate[pg.K_DOWN]
        elif self.state == 0:
            condition[0] = keystate[pg.K_w]
            condition[1] = keystate[pg.K_s]

        if condition[0]:
            self.speedy -= 5
        if condition[1]:
            self.speedy += 5
        self.rect.y += self.speedy
        if self.state == 2:
            if ball.rect.centery - 10 > self.rect.centery:
                self.rect.y += 10
            elif ball.rect.centery + 10 < self.rect.centery:
                self.rect.y -= 10

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.y < 0:
            self.rect.y = 0

        self.hit_speed = abs(ball.speedx) * self.vector

        hit = pg.sprite.collide_rect(self, ball)
        if hit:
            ball.speedx = self.hit_speed
            bounce_snd.play()

class Ball(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(path.join(img_dir, "ball.png")).convert()
        self.image.set_colorkey(BLACK)
        self.image =  pg.transform.scale(self.image, (40,40))

        self.respawn()
        while -0.9 < self.speedy < 0.9:
            self.speedy = random.randrange(-10,10)

        self.score_f = 0
        self.score_s = 0

    def update(self):
        global running, goal
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speedy = -self.speedy
            bounce_snd.play()
        if self.rect.centerx >= WIDTH:
            self.score_f += 1
            self.respawn()
            goal = True
        if self.rect.centerx <= 0:
            self.score_s += 1
            self.respawn()
            goal = True
        if abs(self.speedx) < 25:
            self.speedx *= 1.0005

    def respawn(self):
        global delay, time_delay
        time_delay = 0.8

        for i in Paddles:
            i.rect.centery = HEIGHT // 2
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH//2,HEIGHT//2)

        self.speedx = random.choice([-1.75,1.75])
        self.speedy = random.randrange(-5,5)

        delay = True

bounce_snd = pg.mixer.Sound(path.join(snd_dir, 'bounce.mp3'))
game_won_snd = pg.mixer.Sound(path.join(snd_dir, 'game_won.mp3'))

goal_img = pg.image.load(path.join(img_dir, "goal.png")).convert()
goal_img.set_colorkey(RED)

win_img = []
for i in ['game_win1.png','game_win2.png']:
    img = pg.image.load(path.join(img_dir, i)).convert()
    img.set_colorkey(RED)
    win_img.append(img)

pg.mixer.music.load(path.join(snd_dir, 'music.mp3'))
pg.mixer.music.set_volume(0.09)
pg.mixer.music.play(loops=-1)

time_delay = 0.8
delay = False
goal = False

game_over = True
running = True
while running:
    if game_over:
        mode = show_go_screen()
        Border = pg.Surface((3,HEIGHT))
        Border.fill(WHITE)

        all_sprites = pg.sprite.Group()
        Paddles = pg.sprite.Group()

        player_f = Paddle(5,HEIGHT//2 - 35, 1 , 1)
        all_sprites.add(player_f)
        Paddles.add(player_f)

        player_s = Paddle(WIDTH-15-5,HEIGHT//2 - 35,-1 , mode)
        all_sprites.add(player_s)
        Paddles.add(player_s)

        ball = Ball()
        all_sprites.add(ball)
        game_over = False
        goal = False
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pg.event.get():
        # check for closing window
        if event.type == pg.QUIT:
            running = False
    # Обновление
    all_sprites.update()


    # Рендеринг
    screen.fill(BLACK)
    screen.blit(Border, (WIDTH//2,0))

    draw_text(screen, f'Score: {ball.score_f}', 20, WIDTH//4, 10, WHITE)
    draw_text(screen, f'Score: {ball.score_s}', 20, WIDTH - WIDTH//4, 10, WHITE)

    all_sprites.draw(screen)
    if goal and not(ball.score_f >= 5 or ball.score_s >= 5):
        screen.blit(goal_img,(0,0))
        game_won_snd.play()
        goal = False
    if ball.score_f >= 5:
        screen.blit(win_img[0],(0,0))
        game_won_snd.play()
        game_over = True
        time_delay = 0.5
    elif ball.score_s >= 5:
        screen.blit(win_img[1],(0,0))
        game_won_snd.play()
        game_over = True
        time_delay = 0.5

    mouse_handler()
    # После отрисовки всего, переворачиваем экран
    pg.display.flip()
    if delay:
        clock.tick(time_delay)
        delay = False

pg.quit()
