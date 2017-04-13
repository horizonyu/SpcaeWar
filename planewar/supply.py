import pygame
from random import *

#子弹补给
class BulletSupply(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("images/bullet_supply.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.width, self.rect.bottom = randint(0, self.width - self.rect.width), -10
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 5

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.active = False


    def reset(self):
        self.rect.width, self.rect.bottom = randint(0, self.width - self.rect.width), -10
        self.active = True

#炸弹补给
class BombSupply(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("images/bomb_supply.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.width, self.rect.bottom = randint(0, self.width - self.rect.width - 10), -10
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 4

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.active = False


    def reset(self):
        self.rect.width, self.rect.bottom = randint(0, self.width - self.rect.width - 10), -10
        self.active = True