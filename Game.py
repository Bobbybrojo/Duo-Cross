
import pygame
from pygame import gfxdraw
from pygame import freetype
import sys
from pygame.locals import *
import math
import random
from EnemyBlobs import Enemy
from Player import Player
from Particles import ParticleCluster, Wave, TextParticle
from UI.TextElement import TextElement
from UI.Label import Label, Button
import os

pygame.init()
pygame.freetype.init()

# creating display
DISP_WIDTH = 1080
DISP_HEIGHT = 720
screen = pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT), pygame.SCALED, pygame.OPENGL, vsync=1)
pygame.display.set_caption("Duo Cross")
pygame.mouse.set_visible(False)

colors = {
    "Black": (0, 0, 0),
    "White": (255, 255, 255),
    "Teal": (179, 227, 218),
    "Orange": (248, 196, 138),
    "Blue": (144, 186, 250),
    "Grey": (217, 189, 200),
    "Red": (236, 141, 137)

}

# Fill background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(colors["Teal"])

# Font and Score
font = pygame.freetype.Font("Duo-Cross/Assets/Fonts/NivoSB.otf", 65)

score = 0
lives = 3
life_surface = pygame.Surface((200, 100))
life_surface.set_colorkey(colors["Black"])
life_surface.set_alpha(40)


# Slanted BG Sprite
background_image = pygame.image.load("Duo-Cross/Assets/SlantBG.png").convert_alpha()
background_image = pygame.transform.scale2x(background_image)
background_image.set_colorkey((0, 0, 0))
background_image.set_alpha(45)
bg_y = 0


def reset_y(y):
    if y > 715:
        y = 0
    return y


def scroll_background(y):
    screen.blit(background_image, (0, y))
    screen.blit(background_image, (0, y - 720))
    reset_y(y)


# creating player objects
orange_ball = Player(0)
blue_ball = Player(1)

# Particles
orange_particles = ParticleCluster(orange_ball.get_loc(), image="Duo-Cross/Assets/OrangeBlob.png")
blue_particles = ParticleCluster(blue_ball.get_loc(), image="Duo-Cross/Assets/BlueBlob.png")

waves = []

text_particles = []


def spawn_wave(loc, thickness, color):
    waves.append(Wave(loc, thickness, color))


def spawn_text(loc, text):
    text_particles.append(TextParticle(loc, text))


# enemy generation
enemies = []
for x in range(10):
    enemies.append(Enemy(random.randint(5, 8)))


def distance_between(x1, y1, x2, y2):
    return math.sqrt(math.pow(x1-x2, 2) + math.pow(y1-y2, 2))


clock = pygame.time.Clock()
running = True
menu = True
game = False
options = False
game_over = False


while running:
    # ============================================================================================= GAME LOOP
    score = 0
    lives = 3
    waves = []
    enemies = []
    text_particles = []
    for x in range(10):
        enemies.append(Enemy(random.randint(4, 6)))
    while game:
        clock.tick(30)
        screen.blit(background, (0, 0))

        # scrolling background
        scroll_background(bg_y)
        bg_y += 5
        bg_y = reset_y(bg_y)

        pygame.mouse.set_visible(False)
        mx, my = pygame.mouse.get_pos()

        DISP_WIDTH, DISP_HEIGHT = pygame.display.get_window_size()
        center_x = DISP_WIDTH / 2
        center_y = DISP_WIDTH / 2

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game = False
                menu = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    lives -= 1
                    print(lives)

        # ------------------------------------------------------------------------------ enemy player collision
        for enemy in enemies:
            offset_orange = (int(orange_ball.get_center_loc()[0] - enemy.get_loc()[0]), int(orange_ball.get_center_loc()[1] - enemy.get_loc()[1]))
            offset_blue = (int(blue_ball.get_center_loc()[0] - enemy.get_loc()[0]), int(blue_ball.get_center_loc()[1] - enemy.get_loc()[1]))
            if enemy.mask.overlap(orange_ball.mask, offset_orange):
                if enemy.type == 0:
                    score -= 5
                    spawn_wave(orange_ball.get_loc(), 5, colors["Red"])
                    spawn_text(list(orange_ball.get_loc()), "-5")
                    spawn_wave((20 + lives * 40, 20, 18), 5, colors["Black"])
                    lives -= 1
                    if lives <= 0:
                        game = False
                        game_over = True
                elif enemy.type == 1:
                    score -= 1
                    spawn_text(list(orange_ball.get_loc()), "-1")
                elif enemy.type == 2:
                    score += 1
                    spawn_wave(orange_ball.get_loc(), 5, colors["Orange"])
                    spawn_text(list(orange_ball.get_loc()), "+1")
                enemies.remove(enemy)
                enemies.append(Enemy(random.randint(5, 12)))
            elif enemy.mask.overlap(blue_ball.mask, offset_blue):
                if enemy.type == 0:
                    score -= 5
                    spawn_text(list(blue_ball.get_loc()), "-5")
                    spawn_wave(blue_ball.get_loc(), 5, colors["Red"])
                    spawn_wave((20 + lives * 40, 20, 18), 5, colors["Black"])
                    lives -= 1
                    if lives <= 0:
                        game = False
                        game_over = True
                elif enemy.type == 1:
                    score += 1
                    spawn_text(list(blue_ball.get_loc()), "+1")
                    spawn_wave(blue_ball.get_loc(), 5, colors["Blue"])
                elif enemy.type == 2:
                    score -= 1
                    spawn_text(list(blue_ball.get_loc()), "-1")
                enemies.remove(enemy)
                enemies.append(Enemy(random.randint(5, 12)))

        # movement for player positive
        move_x, move_y = pygame.mouse.get_pos()

        # movement for anti player
        opp_x = -(move_x - DISP_WIDTH)
        opp_y = -(move_y - DISP_HEIGHT)

        # UPDATE OBJECTS
        for enemy in enemies:
            enemy.update()

        # update particles and players

        for wave in waves:
            wave.update()
            if wave.get_radius() > 1440:
                waves.remove(wave)

        orange_particles.loc = orange_ball.get_loc()
        orange_particles.update()
        orange_ball.update()
        pygame.draw.circle(screen, (255, 165, 0), (move_x, move_y), 5)

        blue_particles.loc = blue_ball.get_loc()
        blue_particles.update()
        blue_ball.update()
        pygame.draw.circle(screen, (253, 253, 253), (opp_x, opp_y), 5)

        for particle in text_particles:
            particle.update()
            if particle.get_size() > 80:
                text_particles.remove(particle)

        life_surface.fill(colors["Black"])
        for i in range(lives):
            # pygame.draw.circle(life_surface, (0, 2, 0), (20 + i * 40, 20), 18)
            pygame.gfxdraw.filled_circle(life_surface, 20 + i * 40, 20, 18, (0, 2, 0))
            pygame.gfxdraw.aacircle(life_surface, 20 + i * 40, 20, 18, (0, 2, 0))

        #life_surface.set_colorkey((0, 1 ,0))
        screen.blit(life_surface, (10,  10))




        # FONT RENDERING
        score_text = TextElement(str(score), [DISP_WIDTH / 2, 35], (255, 255, 255), True)
        score_text.render()

        # DISPLAY FLIP
        pygame.display.flip()

    # ============================================================================================= MAIN MENU LOOP
    dynamic_bop = 80
    scale_up = True
    start_button = Button((DISP_WIDTH / 2, DISP_HEIGHT / 2), (300, 80), colors["Black"], 20)
    options_button = Button((DISP_WIDTH / 2, DISP_HEIGHT / 2 + 100), (300, 80), colors["Black"], 20)
    while menu:
        clock.tick(30)
        screen.blit(background, (0, 0))
        pygame.mouse.set_visible(True)

        # scrolling background
        scroll_background(bg_y)
        bg_y += 5
        bg_y = reset_y(bg_y)

        title = Label((DISP_WIDTH / 2, 65), (DISP_WIDTH, 80), colors["Black"], 20)
        title.render()

        # draw menu

        title_text = TextElement("~CROSS~", [DISP_WIDTH / 2, title.get_rect().centery], colors["White"], True, size=95)
        title_text.render()

        start_button.render()
        start_text = TextElement("~START~", [start_button.get_rect().centerx, start_button.get_rect().centery], colors["White"], True)
        start_text.render()

        options_button.render()
        options_text = TextElement("~HOW TO~", [options_button.get_rect().centerx, options_button.get_rect().centery], colors["White"], True)
        options_text.render()

        for event in pygame.event.get():
            if event.type == QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu = False
                    game = True
                if event.key == pygame.K_g:     #  DEBUG GAME OVER
                    menu = False
                    game_over = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.hover():
                    menu = False
                    game = True
                if options_button.hover():
                    menu = False
                    options = True

        pygame.display.flip()

    back_button = Button((DISP_WIDTH / 2, 640), (300, 80), colors["Black"], 20)
    while options:
        clock.tick(30)
        screen.blit(background, (0, 0))
        pygame.mouse.set_visible(True)

        # scrolling background
        scroll_background(bg_y)
        bg_y += 5
        bg_y = reset_y(bg_y)

        title = Label((DISP_WIDTH / 2, 65), (DISP_WIDTH, 80), colors["Black"], 20)
        title.render()

        text_bg = Label((DISP_WIDTH / 2, DISP_HEIGHT / 2), (950, 420), colors["Black"], 20)
        text_bg.render()

        text = [                                                        # 215
            TextElement("~HOW TO~", [DISP_WIDTH / 2, text_bg.get_rect().centery - 165], colors["White"], True, size=65),
            TextElement("Control the ORANGE ball with the mouse", [DISP_WIDTH / 2, text_bg.get_rect().centery - 85], colors["White"], True, size=55),
            TextElement("The BLUE ball follows the opposite position", [DISP_WIDTH / 2, text_bg.get_rect().centery - 10], colors["White"], True, size=55),
            TextElement("Collect ORBS with the same colored ball", [DISP_WIDTH / 2, text_bg.get_rect().centery + 65], colors["White"], True, size=55),
            TextElement("Avoid RED orbs or lose LIFE", [DISP_WIDTH / 2, text_bg.get_rect().centery + 140], colors["White"], True, size=55)
        ]
        for line in text:
            line.render()

        # draw menu

        title_text = TextElement("~CROSS~", [DISP_WIDTH / 2, title.get_rect().centery], colors["White"], True, size=95)
        title_text.render()

        back_button.render()
        back_text = TextElement("~BACK~", [DISP_WIDTH / 2, back_button.get_rect().centery], colors["White"], True)
        back_text.render()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    options = False
                    menu = True
            if event.type == pygame.MOUSEBUTTONDOWN:  # use TextElement.hover() to detect mouse collision
                if back_button.hover():
                    options = False
                    menu = True

        pygame.display.flip()

    while game_over:
        clock.tick(30)
        screen.blit(background, (0, 0))
        pygame.mouse.set_visible(True)

        # scroll bg
        scroll_background(bg_y)
        bg_y += 5
        bg_y = reset_y(bg_y)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = False
                    menu = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.hover():
                    game_over = False
                    menu = True

        title_label = Label((DISP_WIDTH / 2, 65), (DISP_WIDTH, 80), colors["Black"], 20)
        title_label.render()
        game_over_text = TextElement("~GAME OVER~", [DISP_WIDTH / 2, title_label.get_rect().centery], colors["White"], True, size=95)
        game_over_text.render()

        back_button.render()
        back_text = TextElement("~BACK~", [DISP_WIDTH / 2, back_button.get_rect().centery], colors["White"], True)
        back_text.render()

        # render score
        score_text = TextElement(str(score), [DISP_WIDTH / 2, DISP_HEIGHT / 2], (255, 255, 255), True, size=200)
        score_text.render()

        score_text_label = TextElement("~SCORE~", [DISP_WIDTH / 2, DISP_HEIGHT / 2 - 110], (255, 255, 255), True, size=60)
        score_text_label.render()

        pygame.display.flip()
