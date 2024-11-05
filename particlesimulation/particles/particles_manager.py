from random import randint, choice

import pygame

from particlesimulation.particles.particle import Particle
from particlesimulation.ui import UI
from particlesimulation.constants import *


class ParticlesManager:
    def __init__(self):
        self.groups = pygame.sprite.Group()

    def spawn_particle(
        self,
        types: str,
        multiplier: int,
        color: int,
        min_speed: int,
        max_speed: int,
        min_size: int,
        max_size: int,
    ):
        match types:
            case "normal":
                self.draw_particle(
                    multiplier, color, min_speed, max_speed, min_size, max_size
                )
            case "snow":
                self.draw_snow_particle(
                    multiplier, color, min_speed, max_speed, min_size, max_size
                )

    def kill_off_screen(self):
        for particle in self.groups:
            if (
                particle.pos[0] < 0
                or particle.pos[0] > SCREEN_WIDTH
                or particle.pos[1] < -20 + 5
                or particle.pos[1] > SCREEN_HEIGHT + 20
            ):
                particle.kill()

    def check_max_particles(self):
        while len(self.groups) > MAX_PARTICLES - 50:
            self.groups.sprites()[0].kill()

    def draw_particle(
        self,
        amount=1,
        color=BASE_COLOR,
        min_speed=50,
        max_speed=100,
        min_size=5,
        max_size=10,
    ):
        for i in range(amount):
            pos = (randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT))
            direction = pygame.math.Vector2(0, 0)
            speed = randint(min_speed, max_speed)
            size = randint(min_size, max_size)
            Particle(
                groups=self.groups,
                pos=pos,
                color=color,
                direction=direction,
                speed=speed,
                size=size,
                fade_speed=100,
            )

    def draw_snow_particle(
        self,
        amount=1,
        color=BASE_COLOR,
        min_speed=50,
        max_speed=100,
        min_size=5,
        max_size=10,
    ):
        for i in range(amount):
            pos = (randint(0, SCREEN_WIDTH), randint(-20, SCREEN_HEIGHT - 20))
            direction = pygame.math.Vector2(0, 1)
            speed = randint(min_speed, max_speed)
            size = randint(min_size, max_size)
            Particle(
                groups=self.groups,
                pos=pos,
                color=color,
                direction=direction,
                speed=speed,
                size=size,
            )

    def kill_on_cursor(self):
        for event in pygame.event.get():
            if pygame.mouse.get_pressed()[0]:
                # if (event.pos[0])
                pass
