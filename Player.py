import pygame
from pygame.locals import *
import math


class Player(pygame.sprite.Sprite):

    orange_x = 0
    orange_y = 0

    def __init__(self, type):
        pygame.sprite.Sprite.__init__(self)
        self.x_pos = 1080 / 2
        self.y_pos = 720 / 2
        self.mouse_x = pygame.mouse.get_pos()[0]
        self.mouse_y = pygame.mouse.get_pos()[1]
        self.screen = pygame.display.get_surface()
        self.type = type

        if self.type == 0:
            self.image = pygame.image.load("Assets/OrangeBlob.png")
        elif self.type == 1:
            self.image = pygame.image.load("Assets/BlueBlob.png")
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):

        self.position()
        #self.screen.blit(self.mask.to_surface(), (self.x_pos, self.y_pos))
        self.screen.blit(self.image, (self.x_pos - self.image.get_width()/2, self.y_pos - self.image.get_width()/2))

    def position(self):
        self.mouse_x = pygame.mouse.get_pos()[0]
        self.mouse_y = pygame.mouse.get_pos()[1]
        move_x = self.distance_to_mouse('x') * .20
        move_y = self.distance_to_mouse('y') * .20

        if self.type == 0:
            Player.orange_x = self.x_pos
            Player.orange_y = self.y_pos
            if self.x_pos < self.mouse_x - 2:
                self.x_pos += move_x
            elif self.x_pos > self.mouse_x + 2:
                self.x_pos -= move_x
            if self.y_pos > self.mouse_y + 2:
                self.y_pos -= move_y
            elif self.y_pos < self.mouse_y - 2:
                self.y_pos += move_y
        elif self.type == 1:
            self.x_pos = -(Player.orange_x - self.screen.get_width())
            self.y_pos = -(Player.orange_y - self.screen.get_height())

    def transform_image(self, image):
        image_copy = pygame.transform.scale(image, (int(self.distance_to_mouse()), self.image.get_height()))
        image_copy = pygame.transform.rotate(image_copy, self.get_angle(self.get_loc()) + 90)
        return image_copy

    def get_angle(self, loc):
        try:
            angle = math.atan((loc[1] - self.mouse_x) / (loc[0] - self.mouse_y))
        except:
            angle = math.pi / 2
        if self.mouse_y < loc[1] and self.mouse_x > loc[0]:
            angle = abs(angle)
        elif self.mouse_y < loc[1] and self.mouse_x < loc[0]:
            angle = math.pi - angle
        elif self.mouse_y > loc[1] and self.mouse_x < loc[0]:
            angle = math.pi + abs(angle)
        elif self.mouse_y > loc[1] and self.mouse_x > loc[0]:
            angle = (math.pi * 2) - angle
        angle = angle * (180 / math.pi)
        if self.type == 0:
            return angle
        else:
            return -angle

    def distance_to_mouse(self, coord='both'):
        if coord == 'x':
            distance = abs(self.mouse_x - self.x_pos)
        elif coord == 'y':
            distance = abs(self.mouse_y - self.y_pos)
        else:
            distance = math.sqrt(math.pow(self.x_pos - self.mouse_x, 2) + math.pow(self.y_pos - self.mouse_y, 2))
        return distance

    def get_loc(self):
        return self.x_pos, self.y_pos

    def get_center_loc(self):
        return self.x_pos - self.rect.width / 2, self.y_pos - self.rect.height / 2