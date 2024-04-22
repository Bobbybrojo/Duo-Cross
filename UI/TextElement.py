import pygame.freetype


class TextElement():
    def __init__(self, text, pos, color=(0, 0, 0), dropshadow=False, sway=False, size=65):
        self.text = text
        self.font = pygame.freetype.Font("Duo-Cross/Assets/Fonts/NivoSB.otf", size)
        self.rect = self.font.get_rect(self.text)
        self.pos = [pos[0] - self.rect.width / 2, pos[1] - self.rect.height / 2]  # - self.rect.height / 2
        self.screen = pygame.display.get_surface()
        self.color = color
        self.dropshadow = dropshadow
        #  movement
        self.sway_amount = 10

    def render(self):
        if self.dropshadow:
            self.font.render_to(self.screen, self.pos_offset(self.pos, 2), self.text, (217, 189, 200))
        self.font.render_to(self.screen, self.pos, self.text, self.color)
        self.sway()

    def pos_offset(self, pos, offset):
        pos = list(pos)
        pos[0] += offset
        pos[1] += offset
        pos = tuple(pos)
        return pos

    def sway(self):
        pass

