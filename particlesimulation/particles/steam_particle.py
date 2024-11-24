from random import randint, choice

import pygame

from particlesimulation.particles.particle import Particle


class SteamParticle(Particle):
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
        self.group = groups
        self.pos = pos
        self.color = color
        self.size = size
        self.speed = speed
        self.fade_speed = fade_speed
        self.max_size = 200
        self.growth_rate = randint(10, 20)

        self.create_surf()

    def grow(self, dt):
        if self.size < self.max_size:
            self.size += self.growth_rate * dt
            self.size = min(self.size, self.max_size)
            self.create_surf()

    def move(self, dt):
        direction = pygame.math.Vector2(0, -1)
        if not self.pos[1] >= choice(range(20, 100)):
            direction = pygame.math.Vector2(0, 0)
        self.pos += direction * self.speed * dt
        self.rect.center = self.pos

    def update(self, dt):
        self.move(dt)
        self.grow(dt)
        self.fade(dt)
        self.check_alpha()
