import math

import pygame as p
import random

WIDTH = 500
HEIGHT = 500
FPS = 30

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
DARK_PURPLE = (70, 0, 150)
LIGHT_PURPLE = (220, 150, 255)
WHITE = (255, 255, 255)


class Player(p.sprite.Sprite):
    def __init__(self):
        p.sprite.Sprite.__init__(self)
        # self.step_x = 5
        # self.step_y = 3
        self.right_move = 0
        self.up_move = 0
        self.image = p.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (25, 25)

    def update(self):
        if self.right_move == 1:
            if self.rect.x + 50 < WIDTH:
                self.rect.x += 50
        elif self.right_move == -1:
            if self.rect.x - 50 >= 0:
                self.rect.x -= 50
        elif self.up_move == 1:
            if self.rect.y - 50 >= 0:
                self.rect.y -= 50
        elif self.up_move == -1:
            if self.rect.y + 50 < HEIGHT:
                self.rect.y += 50
        self.right_move = 0
        self.up_move = 0


class Enemy(p.sprite.Sprite):
    def __init__(self, x, y, timer):
        p.sprite.Sprite.__init__(self)
        self.image = p.Surface((50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x * 50 + 25, y * 50 + 25)
        self.step = 50
        self.timer = timer
        self.time_count = 0


class CommonEnemy(Enemy):
    def __init__(self, x, y, direction, timer):
        Enemy.__init__(self, x, y, timer)
        self.image.fill(RED)
        self.direction = direction

    def update(self):
        self.time_count += 1
        if self.time_count == self.timer:
            self.time_count = 0
            if self.direction == 'h':
                if self.rect.right >= WIDTH or self.rect.left <= 0:
                    self.step = -self.step
                self.rect.x += self.step
            if self.direction == 'v':
                if self.rect.bottom >= HEIGHT or self.rect.top <= 0:
                    self.step = -self.step
                self.rect.y += self.step


class Stalker(Enemy):
    def __init__(self, x, y, timer, player_obj, error_rate):
        Enemy.__init__(self, x, y, timer)
        self.timer *= 5
        self.image.fill(YELLOW)
        self.player = player_obj
        self.error_rate = error_rate

    def update(self):
        self.time_count += 1
        if self.time_count == self.timer:
            self.time_count = 0
            if random.random() >= self.error_rate:
                x_dist = player.rect.x - self.rect.x
                y_dist = player.rect.y - self.rect.y
                if abs(x_dist) >= abs(y_dist):
                    self.rect.x += math.copysign(1, x_dist) * self.step
                else:
                    self.rect.y += math.copysign(1, y_dist) * self.step
            else:
                direction = random.choice(['u', 'd', 'r', 'l'])
                if direction == 'r':
                    if self.rect.x + 50 < WIDTH:
                        self.rect.x += 50
                elif direction == 'l':
                    if self.rect.x - 50 >= 0:
                        self.rect.x -= 50
                elif direction == 'u':
                    if self.rect.y - 50 >= 0:
                        self.rect.y -= 50
                elif direction == 'd':
                    if self.rect.y + 50 < HEIGHT:
                        self.rect.y += 50


class Madman(Enemy):
    def __init__(self, x, y, timer, rest_time, madness_time):
        Enemy.__init__(self, x, y, timer)
        self.image.fill(LIGHT_PURPLE)
        self.rest_time = rest_time
        self.madness_time = madness_time
        self.timer = max(self.timer // 2, 1)
        self.status = 'rest'

    def update(self):
        self.time_count += 1
        if self.status == 'rest':
            if self.time_count == self.rest_time:
                self.time_count = 0
                self.image.fill(DARK_PURPLE)
                self.status = 'madness'
        if self.status == 'madness':
            if self.time_count % self.timer == 0:
                direction = random.choice(['u', 'd', 'r', 'l'])
                if direction == 'r':
                    if self.rect.x + 50 < WIDTH:
                        self.rect.x += 50
                elif direction == 'l':
                    if self.rect.x - 50 >= 0:
                        self.rect.x -= 50
                elif direction == 'u':
                    if self.rect.y - 50 >= 0:
                        self.rect.y -= 50
                elif direction == 'd':
                    if self.rect.y + 50 < HEIGHT:
                        self.rect.y += 50
            if self.time_count == self.madness_time:
                self.time_count = 0
                self.image.fill(LIGHT_PURPLE)
                self.status = 'rest'


class Target(p.sprite.Sprite):
    def __init__(self):
        p.sprite.Sprite.__init__(self)
        global goal_counter
        self.image = p.Surface((20, 20))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (50 * random.randint(1, 9) + 25, 50 * random.randint(1, 9) + 25)
        self.reached = 0

    def update(self):
        if self.rect.center == player.rect.center and self.reached == 0:
            self.reached = 1
        if self.reached == 1:
            self.image.fill(WHITE)
            global goal_counter
            goal_counter -= 1
            self.reached = -1


p.init()
p.mixer.init()
screen = p.display.set_mode((WIDTH, HEIGHT))
p.display.set_caption("Test")
clock = p.time.Clock()
all_sprites = p.sprite.Group()

# -----------------PARAMETERS-----------------
common_enemies_number = 3
stalkers_number = 2
madmen_number = 2

goal_counter = 3

stalkers_mistakes_rate = random.random()

madmen_rest_time_min = 50
madmen_rest_time_max = 200
madmen_madness_time_min = 50
madmen_madness_time_max = 200

frames_per_enemy_step = 5
# ----------------------------------------------


enemies = []
player = Player()

directions = ['h', 'v']

for i in range(goal_counter):
    goal = Target()
    all_sprites.add(goal)

for i in range(common_enemies_number):
    enemies.append(CommonEnemy(random.randint(1, 9),
                               random.randint(1, 9),
                               directions[random.randint(0, 1)],
                               frames_per_enemy_step))
    all_sprites.add(enemies[i])

for i in range(common_enemies_number, stalkers_number + common_enemies_number):
    enemies.append(Stalker(random.randint(3, 9),
                           random.randint(3, 9),
                           frames_per_enemy_step,
                           player,
                           stalkers_mistakes_rate))
    all_sprites.add(enemies[i])

for i in range(stalkers_number + common_enemies_number, stalkers_number + common_enemies_number + madmen_number):
    enemies.append(Madman(random.randint(3, 9),
                          random.randint(3, 9),
                          frames_per_enemy_step,
                          random.randint(madmen_rest_time_min, madmen_rest_time_max),
                          random.randint(madmen_madness_time_min, madmen_madness_time_max)))
    all_sprites.add(enemies[i])

all_sprites.add(player)

win = -1
running = True
while running:
    clock.tick(FPS)
    for i in p.event.get():
        if i.type == p.QUIT:
            running = False
        elif i.type == p.KEYDOWN:
            if i.key == p.K_RIGHT:
                player.right_move = 1
            elif i.key == p.K_LEFT:
                player.right_move = -1
            elif i.key == p.K_UP:
                player.up_move = 1
            elif i.key == p.K_DOWN:
                player.up_move = -1

    for enemy in enemies:
        if player.rect.center == enemy.rect.center:
            win = 0
            running = False

    if goal_counter == 0:
        win = 1
        running = False

    p.display.update()
    all_sprites.update()

    screen.fill(WHITE)
    for i in range(1, WIDTH // 50):
        p.draw.line(screen, BLACK, (i * 50, 0), (i * 50, HEIGHT))
    for i in range(1, HEIGHT // 50):
        p.draw.line(screen, BLACK, (0, i * 50), (WIDTH, i * 50))
    all_sprites.draw(screen)

if win == 1:
    screen.fill(GREEN)
elif win == 0:
    screen.fill(RED)

p.display.update()
if win != -1:
    running = True
    while running:
        for i in p.event.get():
            if i.type == p.QUIT:
                running = False

p.quit()
