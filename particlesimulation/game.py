import sys
from random import uniform, randint

import pygame

from particlesimulation.particles.particle import Particle
from particlesimulation.settings import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.max_frame_rate = 60
        self.particle_groups = pygame.sprite.Group()

    def update(self):
        self.screen.fill(BG_COLOR)
        self.dt = self.clock.tick(self.max_frame_rate) / 1000

        self.particle_groups.draw(self.screen)
        self.particle_groups.update(self.dt)

        while len(self.particle_groups) > 5000:
            self.particle_groups.sprites()[0].kill()

        pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                self.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed(3)[2]:
                    for _ in range(1010):
                        pos = pygame.mouse.get_pos()
                        direction = pygame.math.Vector2(uniform(-1, 1), uniform(-1, 1)).normalize()
                        speed = randint(10, 100)
                        Particle(groups=self.particle_groups, pos=pos, color=BASE_COLOR, direction=direction,
                                 speed=speed)

    def quit(self):
        pygame.quit()
        sys.exit()

    def loop(self):
        while self.is_running:
            self.handle_events()
            self.update()

            print(f'Particle count: {len(self.particle_groups)}')
