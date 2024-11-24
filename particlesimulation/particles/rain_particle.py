from random import randint

import pygame

from particlesimulation.constants import SCREEN_HEIGHT, SCREEN_MARGIN
from particlesimulation.particles.particle import Particle


class SplashParticle(Particle):
    def __init__(self, groups, pos, size, color):
        super().__init__(groups, pos, size, color)
        self.pos = pos
        self.size = size
        self.color = color
        self.random_down_multiplier = randint(1, 3)
        self.random_side_multiplier = randint(1, 5)
        self.lifetime = 20

    def move(self, dt):
        move_side = pygame.math.Vector2(randint(-1, 0), 0) * randint(50, 100) * dt
        move_up = pygame.math.Vector2(0, -1) * randint(50, 100) * dt
        self.pos += (
            move_side * self.random_side_multiplier
            + move_up * self.random_down_multiplier
        )
        self.rect.center = self.pos

        self.size -= 0.1 * randint(1, 6)

    def check_size(self, dt):
        self.lifetime -= 1
        if self.size <= 0 or self.lifetime <= 0:
            self.kill()

    def update(self, dt):
        self.move(dt)
        self.fade(dt)
        self.check_alpha()
        self.check_size(dt)


class Splash:
    def __init__(self, groups, pos, size, color):
        self.groups = groups
        self.x, self.y = pos
        self.size = size / 2
        self.color = color

        self.intensity = 2
        self.particles = []

        for i in range(self.intensity * 25):
            self.particles.append(
                SplashParticle(
                    self.groups,
                    (self.x + randint(-5, 5), self.y),
                    self.size,
                    self.color,
                )
            )

    def draw(self):
        for particle in self.particles:
            particle.create_surf()

    def update(self, pos):
        self.x, self.y = pos


class RainParticle(Particle):
    def __init__(
        self,
        groups: pygame.sprite.Group,
        pos: list[int],
        color: str,
        speed: int,
        size: int,
        fade_speed: int = 240,
    ):
        super().__init__(groups, pos, color, size, speed, fade_speed)
        self.groups = groups
        self.pos = pos
        self.color = color
        self.size = size
        self.speed = speed
        self.fade_speed = fade_speed

        self.create_surf()

    def move(self, dt):
        direction = pygame.math.Vector2(0, 1) * self.speed * dt
        self.pos += direction * randint(1, 5)
        self.rect.center = self.pos
        if self.pos[1] >= SCREEN_HEIGHT:
            self.spawn_splash(self.pos)
            self.splash.update(self.pos)

    def spawn_splash(self, pos):
        self.splash = Splash(self.groups, pos, self.size, self.color)
        self.splash.draw()

    def update(self, dt):
        self.move(dt)
