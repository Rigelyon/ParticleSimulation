from random import randint, choice

import pygame

from particlesimulation.particles.particle import Particle
from particlesimulation.constants import *


class ParticlesManager:
    def __init__(self):
        self.groups = pygame.sprite.Group()

    def spawn_particle(self, particles: dict):
        types = choice([key for key in particles])
        match types:
            case 'normal':
                self.draw_particle(particles.get('normal'))
            case 'snow':
                self.draw_snow_particle(particles.get('snow'))

    def kill_off_screen(self):
        for particle in self.groups:
            if (particle.pos[0] < 0 or particle.pos[0] > SCREEN_WIDTH or
                    particle.pos[1] < -20 + 5 or particle.pos[1] > SCREEN_HEIGHT + 20):
                particle.kill()

    def check_max_particles(self):
        while len(self.groups) > MAX_PARTICLES - 50:
            self.groups.sprites()[0].kill()

    def draw_particle(self, n=1):
        for i in range(n):
            pos = (randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT))
            direction = pygame.math.Vector2(0, 0)
            speed = randint(50, 100)
            size = randint(5, 10)
            Particle(groups=self.groups, pos=pos, color=(153, 255, 255), direction=direction,
                     speed=speed, size=size, fade_speed=100)

    def draw_snow_particle(self, n=1):
        for i in range(n):
            pos = (randint(0, SCREEN_WIDTH), randint(-20, SCREEN_HEIGHT - 20))
            direction = pygame.math.Vector2(0, 1)
            speed = randint(50, 100)
            size = randint(5, 10)
            Particle(groups=self.groups, pos=pos, color=BASE_COLOR, direction=direction,
                     speed=speed, size=size)

    def kill_on_cursor(self):
        for event in pygame.event.get():
            if pygame.mouse.get_pressed()[0]:
                # if (event.pos[0])
                pass
