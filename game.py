import pygame
import sys
from pygame.constants import K_LEFT, K_RIGHT, QUIT
import random
import time

# Initialize game
pygame.init()

FPS = 60
clock = pygame.time.Clock()

# Some colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Screen info
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Speeds
PLAYER_SPEED = 5
ENEMY_SPEED = 10

# Score
SCORE = 0

# Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)

game_over = font.render("Game Over", True, BLACK)
background = pygame.image.load("AnimatedStreet.png")

display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
display.fill(WHITE)

pygame.display.set_caption("Game")


class Enemy(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (
            random.randint(self.rect.width, SCREEN_WIDTH - self.rect.width),
            0,
        )

    def move(self):
        global SCORE
        self.rect.move_ip(0, ENEMY_SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.center = (
                random.randint(self.rect.width, SCREEN_WIDTH - self.rect.width),
                0,
            )
            self.rect.top = 0


class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, 0)
        self.rect.bottom = SCREEN_HEIGHT

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-PLAYER_SPEED, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(PLAYER_SPEED, 0)


# Setting up sprites
player = Player()
e1 = Enemy()

# Creating Sprite groups
enemies = pygame.sprite.Group()
enemies.add(e1)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(*enemies)

# User events
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            ENEMY_SPEED += 2
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    display.blit(background, (0, 0))
    scores = font_small.render(str(SCORE), True, BLACK)
    display.blit(scores, (10, 10))

    # Moves and re-dreaws all sprites
    for entity in all_sprites:
        display.blit(entity.image, entity.rect)
        entity.move()

    # Test collisions
    if pygame.sprite.spritecollideany(player, enemies):
        pygame.mixer.Sound("crash.mp3").play()
        time.sleep(0.5)

        display.fill(RED)
        display.blit(game_over, (30, 250))

        pygame.display.update()

        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    clock.tick(FPS)
