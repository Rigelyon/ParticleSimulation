from random import randint

import pygame

from particlesimulation.particles.particle import Particle
from particlesimulation.constants import *


class ParticlesManager:
    def __init__(self):
        self.groups = pygame.sprite.Group()

    def kill_off_screen(self):
        for particle in self.groups:
            if (particle.pos[0] < 0 or particle.pos[0] > SCREEN_WIDTH or
                    particle.pos[1] < 0 + 5 or particle.pos[1] > SCREEN_HEIGHT):
                particle.kill()

    def check_max_particles(self):
        while len(self.groups) > MAX_PARTICLES - 100:
            self.groups.sprites()[0].kill()

    def spawn_particle(self):
        pos = (randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT))
        direction = pygame.math.Vector2(0, -1)
        speed = randint(50, 100)
        size = randint(5, 10)
        Particle(groups=self.groups, pos=pos, color=BASE_COLOR, direction=direction,
                 speed=speed, size=size)

    def kill_on_cursor(self):
        for event in pygame.event.get():
            if pygame.mouse.get_pressed()[0]:
                # if (event.pos[0])
                pass