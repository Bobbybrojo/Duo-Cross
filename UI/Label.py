import pygame

# pygame.init()


class Label:
    def __init__(self, pos, size, color, alpha, text=None):
        self.pos = pos[0] - size[0] / 2, pos[1] - size[1] / 2
        self.color = color
        self.alpha = alpha
        self.screen = pygame.display.get_surface()
        # create label surface
        self.label = pygame.Surface(size)
        self.label.set_alpha(alpha)
        self.label.fill(color)
        self.rect = self.label.get_rect(center=pos)

        if text:
            self.text = text
        else:
            self.text = None

    def render(self):
        self.screen.blit(self.label, self.pos)
        if self.text:
            self.text.render()

    def get_rect(self):
        return self.rect


class Button:
    def __init__(self, pos, size, color, alpha):
        self.pos = pos[0] - size[0] / 2, pos[1] - size[1] / 2
        self.size = size
        self.color = color
        self.alpha = alpha
        self.screen = pygame.display.get_surface()
        # create label surface
        self.label = pygame.Surface(size).convert()
        self.label.set_alpha(alpha)
        self.label.fill(color)
        self.rect = self.label.get_rect(center=pos)

    def render(self):
        self.screen.blit(self.label, self.pos)
        if self.hover():
            if self.alpha < 60:
                self.alpha += 2
                self.label.set_alpha(self.alpha)
        elif not self.hover():
            if self.alpha > 20:
                self.alpha -= 2
                self.label.set_alpha(self.alpha)

    def get_rect(self):
        return self.rect

    def hover(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
