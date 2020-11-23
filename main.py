import pygame
import random
import math
from pygame import mixer

pygame.display.set_caption("Space Attack")

pygame.init()

WIDTH_GAME = 1150
HEIGHT_GAME = 1150
win = pygame.display.set_mode((WIDTH_GAME, HEIGHT_GAME))

clock = pygame.time.Clock()

FRAME = 25

player_img_array = ['PNG/playerShip1_blue.png', 'PNG/playerShip1_green.png', 'PNG/playerShip1_orange.png',
                    'PNG/playerShip1_red.png', 'PNG/playerShip2_blue.png', 'PNG/playerShip2_green.png',
                    'PNG/playerShip2_orange.png', 'PNG/playerShip2_red.png']

player_img = pygame.image.load(player_img_array[random.randint(0, 7)])
WIDTH = player_img.get_size()[0]
HEIGHT = player_img.get_size()[1]
xPlayer = (WIDTH_GAME - WIDTH) / 2
yPlayer = HEIGHT_GAME - FRAME - HEIGHT

SPEED = 15


background_array = ['Backgrounds/1.png', 'Backgrounds/2.png', 'Backgrounds/3.png',
                    'Backgrounds/4.png', 'Backgrounds/5.png', 'Backgrounds/6.png', 'Backgrounds/7.png',
                    'Backgrounds/8.png', 'Backgrounds/9.png']
# background_array = ['Backgrounds/10.png', 'Backgrounds/11.png']
background = pygame.image.load(background_array[random.randint(0, 8)])
# настройка бэкграунда
background_size = background.get_size()
background_rect = background.get_rect()
screen = pygame.display.set_mode(background_size)
wBackground, hBackground = background_size

xBackground = 0
yBackground = 0

x1Background = 0
y1Background = -hBackground

clock = pygame.time.Clock()
score_value = 0
font = pygame.font.Font('Bonus/kenvector_future.ttf', 32)

xText = 25
yText = 25


def show_score(xText, yText):
    score = font.render("Score: " + str(score_value), True, (255, 0, 0))
    win.blit(score, (xText, yText))


class fire():
    def __init__(self, xBullet, yBullet):
        self.xBullet = xBullet
        self.yBullet = yBullet
        self.vel = 10
        self.destruction = 100
        self.fire_img = pygame.image.load('PNG/Lasers/laserGreen05.png')
        self.fire_body_size_x = self.fire_img.get_size()[0] // 2
        self.fire_body_size_y = self.fire_img.get_size()[1] // 2

    def draw(self, win):
        win.blit(self.fire_img, (self.xBullet, self.yBullet))


enemy_array = ['PNG/Enemies/enemyBlack1.png', 'PNG/Enemies/enemyBlack2.png', 'PNG/Enemies/enemyBlack3.png',
               'PNG/Enemies/enemyBlack4.png']


class enemy():
    def __init__(self, xEnemy, yEnemy):
        self.xEnemy = xEnemy
        self.yEnemy = yEnemy
        self.vel = 10
        self.health = 100
        self.enemy_img = pygame.image.load(enemy_array[random.randint(0, 3)])
        self.enemy_body_size_x = self.enemy_img.get_size()[0] // 2
        self.enemy_body_size_y = self.enemy_img.get_size()[1] // 2

    def draw(self, win):
        win.blit(self.enemy_img, (self.xEnemy, self.yEnemy))


def isCollision(xEnemy, yEnemy, xBullet, yBullet):
    distance = math.sqrt((math.pow(xEnemy - xBullet, 2)) + (math.pow(yEnemy - yBullet, 2)))
    if distance < 30:
        return True
    else:
        return False


def drawWindow():
    for bullet in bullets:
        bullet.draw(win)

    for enemy in enemies:
        enemy.draw(win)

    show_score(xText, yText)

    win.blit(player_img, (xPlayer, yPlayer))

    pygame.display.update()


RUN = True
fight_boss = True
bullets = []
enemies = []
enemies_count = 5
while RUN:

    screen.blit(background, background_rect)

    y1Background += 1
    yBackground += 1
    screen.blit(background, (xBackground, yBackground))
    screen.blit(background, (x1Background, y1Background))
    if yBackground >= hBackground:
        yBackground = -hBackground
    if y1Background >= hBackground:
        y1Background = -hBackground

    clock.tick(45)

    if len(enemies) < 1:
        i = len(enemies)
        while i < 5:
            enemies.append(enemy(random.randint(25, 1045), random.randint(25, 75)))
            i = i + 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False

    for bullet in bullets:
        if bullet.yBullet > 20:
            bullet.yBullet -= bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    for enemy in enemies:
        enemy_goaway = random.randint(1, 30)
        if enemy_goaway == 1 and enemy.xEnemy > FRAME:
            enemy.xEnemy -= enemy.vel * random.randint(1, 4)
        elif enemy_goaway == 2 and enemy.xEnemy < WIDTH_GAME - WIDTH - FRAME - FRAME:
            enemy.xEnemy += enemy.vel * random.randint(1, 4)
        elif enemy_goaway == 3:
            enemy.yEnemy += 5
        elif enemy_goaway == 4:
            enemy.yEnemy += 5

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if len(bullets) < 50:
            fire_sound = mixer.Sound('Bonus/sfx_laser2.ogg')
            fire_sound.play()
            bullets.append(fire(round(14 + xPlayer + WIDTH // 2), round(yPlayer + HEIGHT // 2)))

    if keys[pygame.K_LEFT] and xPlayer > FRAME:
        xPlayer -= SPEED
    elif keys[pygame.K_RIGHT] and xPlayer < WIDTH_GAME - WIDTH - FRAME - FRAME:
        xPlayer += SPEED

    for bullet in bullets:
        for enemy in enemies:
            if isCollision(enemy.xEnemy + enemy.enemy_body_size_x, enemy.yEnemy + enemy.enemy_body_size_y,
                           bullet.xBullet + bullet.fire_body_size_x, bullet.yBullet):
                bullets.pop(bullets.index(bullet))
                enemies.pop(enemies.index(enemy))
                score_value += 1

    if keys[pygame.K_q]:
        RUN = False

    drawWindow()

pygame.quit()
