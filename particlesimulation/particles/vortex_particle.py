import math
from random import randint, uniform

import pygame

from particlesimulation.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from particlesimulation.particles.particle import Particle


class VortexParticle(Particle):
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
        self.pos = list(pos)
        self.color = color
        self.size = size
        self.speed = speed
        self.fade_speed = fade_speed
        self.spawn_delay = 10

        self.alpha = 0
        self.glow_speed = 2
        self.alpha_direction = 1
        self.lifetime = 255 / self.fade_speed
        self.elapsed_time = 0
        self.angle = uniform(0, 360)
        self.radius = uniform(10, SCREEN_HEIGHT / 2)

        self.create_surf()

    def create_surf(self):
        self.image = pygame.Surface((self.size, self.size)).convert_alpha()
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.circle(
            surface=self.image,
            color=self.color,
            center=(self.size / 2, self.size / 2),
            radius=self.size / 2,
        )
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect(center=self.pos)

    def move(self, dt):
        self.angle += self.speed * dt

        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2

        self.pos[0] = center_x + int(self.radius * math.cos(math.radians(self.angle)))
        self.pos[1] = center_y + int(self.radius * math.sin(math.radians(self.angle)))

        self.rect.center = self.pos

    def glow(self, dt):
        self.alpha += self.alpha_direction * self.glow_speed * dt * 255
        if self.alpha >= 255:
            self.alpha = 255
            self.alpha_direction = -1
        elif self.alpha <= 128:
            self.alpha = 128
            self.alpha_direction = 1
        self.image.set_alpha(self.alpha)

    def update_lifetime(self, dt):
        self.elapsed_time += dt
        if self.elapsed_time >= self.lifetime:
            self.kill()

    def update(self, dt):
        self.move(dt)
        self.glow(dt)
        self.update_lifetime(dt)
