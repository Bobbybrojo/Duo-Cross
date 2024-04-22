import pygame
import pygame.gfxdraw
import random
import math


class Particle:
    def __init__(self, loc, timer, velocity=None,  size=23, image="Duo-Cross/Assets/OrangeBlob.png"):
        self.image = pygame.image.load(image)
        self.loc = [loc[0] - size / 2, loc[1] - size / 2]
        self.velocity = velocity
        self.size = size
        self.timer = timer
        self.screen = pygame.display.get_surface()
        self.image_og = image
        self.surface = pygame.Surface((self.image.get_rect().width, self.image.get_rect().height))
        self.surface.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()

    def update(self):
        self.loc[0] += self.velocity[0]
        self.loc[1] += self.velocity[1]
        self.velocity[1] += 0.1
        if self.size > 0:
            self.image = pygame.transform.scale(self.image, (int(self.size), int(self.size)))
        self.surface.blit(self.image, (0, 0))
        self.screen.blit(self.surface, self.loc)
        self.image = pygame.image.load(self.image_og)
        self.size -= 1
        self.timer -= 0.4


class ParticleCluster:
    def __init__(self, loc, image="Duo-Cross/Assets/OrangeBlob.png"):

        self.particles = []
        self.loc = loc
        self.image = image

    def update(self):
        particles_to_delete = []
        for x in range(3):
            self.particles.append(Particle([self.loc[0], self.loc[1]], random.randint(2, 4)/2, velocity=[random.randint(0, 40)/20 - 1, random.randint(0, 40)/20 - 1], image=self.image))
        for particle in self.particles:
            particle.update()
            if particle.timer <= 0.1:
                particles_to_delete.append(particle)
        for particle in particles_to_delete:
            self.particles.remove(particle)
            particles_to_delete.remove(particle)


# Wave class is a an expanding circle from a point of collision
# can use draw
class Wave:
    def __init__(self, loc, thickness, color):
        self.loc = int(loc[0]), int(loc[1])
        self.thickness = thickness
        self.color = color
        self.radius = 0
        self.screen = pygame.display.get_surface()
        self.speed = 7
        self.width = 1

    def update(self):
        pygame.draw.circle(self.screen, self.color, self.loc, self.radius, self.width)
        self.radius = int((1/2) * math.pow(self.speed, 2))
        self.speed += 1
        self.width = int((1/18) * math.pow(0.5 * self.speed, 2))

    def get_radius(self):
        return self.radius


class TextParticle:
    def __init__(self, loc, text, size=39):
        self.loc = loc
        self.text = text
        self.size = size
        self.font = pygame.freetype.Font("Duo-Cross/Assets/Fonts/NivoSB.otf", self.size)
        self.screen = pygame.display.get_surface()
        self.alpha = 255
        self.color = (255, 255, 255, 255)
        self.ay = 1

    def update(self):
        self.render()

    def render(self):
        self.loc[1] -= self.ay
        self.ay += 2
        self.size += 2
        if self.size < 90 and self.loc[1] > 1:
            self.font.render_to(self.screen, self.loc, self.text, self.color)
        self.font = pygame.freetype.Font("Duo-Cross/Assets/Fonts/NivoSB.otf", self.size)

    def get_size(self):
        return self.size
