import sys
import time
from random import uniform, randint

import pygame

from particlesimulation.particles.particle import Particle
from particlesimulation.menu import Menu
from particlesimulation.settings import *


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.max_frame_rate = 60
        self.particle_groups = pygame.sprite.Group()

        self.menu = Menu()

    def update(self):
        self.window.fill(BG_COLOR)
        self.dt = self.clock.tick(self.max_frame_rate) / 1000

        particle_count = len(self.particle_groups)
        self.menu.draw_menu(self.window)
        self.menu.draw_text(self.window, f'Particle(s) count: {particle_count}', (20, SCREEN_HEIGHT + 20 + 15),
                            'midleft',
                            self.menu.font_normal, BASE_COLOR)
        self.menu.draw_text(self.window, f'Frame: 0/0', (20, SCREEN_HEIGHT + 20 + 35),
                            'midleft',
                            self.menu.font_normal, BASE_COLOR)
        self.menu.draw_text(self.window, f'Frame rate: {round(self.clock.get_fps(), 2)}',
                            (SCREEN_WIDTH + 20, SCREEN_HEIGHT + 20 + 15), 'midright',
                            self.menu.font_normal, BASE_COLOR)

        self.particle_groups.draw(self.window)
        self.particle_groups.update(self.dt)

        # Kill particles when reach the threshold
        while len(self.particle_groups) > MAX_PARTICLES:
            self.particle_groups.sprites()[0].kill()

        pygame.display.update()

    def spawn_particle(self):
        pos = (randint(30, SCREEN_WIDTH + 15), randint(25, SCREEN_HEIGHT + 20))
        direction = pygame.math.Vector2(0, -1)
        speed = randint(50, 100)
        size = randint(5, 10)
        Particle(groups=self.particle_groups, pos=pos, color=BASE_COLOR, direction=direction,
                 speed=speed, size=size)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                self.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

    def quit(self):
        pygame.quit()
        sys.exit()

    def loop(self):
        while self.is_running:
            self.handle_events()
            self.update()
            for _ in range(100):
                self.spawn_particle()
