import random
from random import randint

import pygame.sprite

from particlesimulation.constants import *


class Particle(pygame.sprite.Sprite):
    def __init__(
        self,
        groups: pygame.sprite.Group = None,
        pos: list[int] = None,
        color: str = None,
        speed: int = None,
        size: int = 8,
        fade_speed: int = 240,
    ):
        super().__init__(groups)
        self.pos = pos
        self.color = color
        self.size = size
        self.speed = speed
        self.alpha = 255
        self.fade_speed = fade_speed

        self.create_surf()

    def create_surf(self):
        self.image = pygame.Surface((self.size, self.size)).convert_alpha()
        self.image.set_colorkey(BG_COLOR)
        pygame.draw.circle(
            surface=self.image,
            color=self.color,
            center=(self.size / 2, self.size / 2),
            radius=self.size / 2,
        )
        self.rect = self.image.get_rect(center=self.pos)

    def move(self, dt):
        direction = pygame.math.Vector2(0, 0)
        self.pos += direction * self.speed * dt
        self.rect.center = self.pos

    def check_alpha(self):
        if self.alpha < 0:
            self.kill()

    def fade(self, dt):
        self.alpha -= self.fade_speed * dt
        self.image.set_alpha(self.alpha)

    def update(self, dt):
        self.move(dt)
        self.fade(dt)
        self.check_alpha()


class SnowParticle(Particle):
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
        self.pos = pos
        self.color = color
        self.size = size
        self.speed = speed
        self.fade_speed = fade_speed

        self.create_surf()

    def move(self, dt):
        move_side = pygame.math.Vector2(-1, 0) * self.speed * dt
        move_down = pygame.math.Vector2(0, 1) * self.speed * dt
        self.pos += move_side + move_down

        self.rect.center = self.pos
