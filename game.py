import pygame
from pygame.constants import K_LEFT, K_RIGHT, QUIT
import random

# Init game
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

display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
display.fill(WHITE)

pygame.display.set_caption("Game")


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (
            random.randint(self.rect.width, SCREEN_WIDTH - self.rect.width),
            0,
        )

    def move(self):
        self.rect.move_ip(0, ENEMY_SPEED)
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.center = (
                random.randint(self.rect.width, SCREEN_WIDTH - self.rect.width),
                0,
            )
            self.rect.top = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, 0)
        self.rect.bottom = SCREEN_HEIGHT

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-PLAYER_SPEED, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(PLAYER_SPEED, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


player = Player()
e1 = Enemy()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
    player.update()
    e1.move()

    display.fill(WHITE)
    player.draw(display)
    e1.draw(display)

    pygame.display.update()
    clock.tick(FPS)
