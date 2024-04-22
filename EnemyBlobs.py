

import pygame
import random
from pygame.locals import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed, x_pos=random.randint(-50, -5), angle=random.randint(0, 0), size=25):
        pygame.sprite.Sprite.__init__(self)
        self.screen = pygame.display.get_surface()
        self.speed = speed
        self.angle = angle
        self.x_pos = random.randint(-200, -5)
        self.y_pos = random.randint(10, 700)
        self.type = 0
        self.set_type()
        self.size = size
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.x_pos += self.speed
        self.screen.blit(self.image, (self.x_pos, self.y_pos))
        if self.x_pos > self.screen.get_size()[0] + 50:
            self.set_random_spawn()
            self.set_random_speed()
            self.set_type()

    def set_type(self):
        self.type = random.randint(0, 2)
        if self.type == 0:
            self.image = pygame.image.load("Duo-Cross/Assets/EnemyBlob.png")
        elif self.type == 1:
            self.image = pygame.image.load("Duo-Cross/Assets/BlueBlob.png")
        elif self.type == 2:
            self.image = pygame.image.load("Duo-Cross/Assets/OrangeBlob.png")

        self.image = pygame.transform.scale(self.image, (25, 25))

    def get_loc(self):
        return self.x_pos, self.y_pos

    def set_random_spawn(self):
        self.x_pos = random.randint(-50, -5)
        self.y_pos = random.randint(10, 700)

    def set_random_speed(self):
        self.speed = random.randint(5, 12)