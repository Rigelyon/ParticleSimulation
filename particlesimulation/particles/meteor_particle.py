from random import randint

import pygame

from particlesimulation.constants import *
from particlesimulation.particles.particle import Particle


# class FlameParticle(Particle):
#     def __init__(self, groups, pos, radius):
#         super().__init__(groups)
#         self.pos = pos
#         self.x, self.y = self.pos
#         self.radius = 5
#         self.original_radius = radius
#         self.alpha_layers = 2
#         self.alpha_glow = 2
#
#         self.burn_rate = 0.1 * randint(1, 4)
#
#     def create_surf(self):
#         max_surf_size = (
#             2 * self.radius * self.alpha_layers * self.alpha_layers * self.alpha_glow
#         )
#         self.image = pygame.Surface((max_surf_size, max_surf_size)).convert_alpha()
#         self.image.set_colorkey(BG_COLOR)
#
#         for i in range(self.alpha_layers, -1, -1):
#             self._draw_alpha_layer(i)
#
#         self.rect = self.image.get_rect(center=(self.x, self.y))
#
#     def _draw_alpha_layer(self, layer_index):
#         alpha = max(255 - layer_index * (255 // self.alpha_layers - 5), 0)
#         layer_radius = self.radius * layer_index**2 * self.alpha_layers
#         color = (*self._get_color_for_radius(), alpha)  # Add alpha to the RGB color
#         pygame.draw.circle(
#             self.image,
#             color,
#             (self.image.get_width() // 2, self.image.get_height() // 2),
#             layer_radius,
#         )
#
#     def _get_color_for_radius(self):
#         if self.radius in (4, 3):
#             return 255, 0, 0
#         elif self.radius == 2:
#             return 255, 150, 0
#         else:
#             return 50, 50, 50
#
#     def move(self, dt):
#         self.pos = (
#             self.x + randint(-self.radius, self.radius) * dt,
#             self.y - 7 - self.radius * dt,
#         )
#         self.original_radius -= self.burn_rate
#         self.radius = max(int(self.original_radius), 1)
#         if self.radius <= 0:
#             self.radius = 1
#
#     def update(self, dt):
#         self.move(dt)


class FlameParticle(Particle):
    def __init__(self, groups, pos, size):
        super().__init__(groups)
        self.pos = pos
        self.size = size
        self.color = (255, 255, 255)
        self.random_down_multiplier = randint(1, 3)
        self.random_side_multiplier = randint(1, 5)

        self.burn_rate = 0.1 * randint(1, 4)

    def move(self, dt):
        move_side = pygame.math.Vector2(randint(-1, 0), 0) * randint(50, 100) * dt
        move_up = pygame.math.Vector2(0, -1) * randint(50, 100) * dt
        self.pos += (
            move_side * self.random_side_multiplier
            + move_up * self.random_down_multiplier
        )
        self.rect.center = self.pos

        self.size -= self.burn_rate

    def check_size(self):
        if self.size <= 0:
            self.kill()

    def update(self, dt):
        self.move(dt)
        self.fade(dt)
        self.check_alpha()
        self.check_size()


class Flame:
    def __init__(self, groups, pos):
        self.groups = groups
        self.x, self.y = pos
        self.flame_intensity = 2
        self.particles = []

        for i in range(self.flame_intensity * 25):
            self.particles.append(
                FlameParticle(
                    self.groups, (self.x + randint(-5, 5), self.y), randint(1, 5)
                )
            )

    def draw(self):
        for particle in self.particles:
            particle.create_surf()

    def update(self, pos):
        self.x, self.y = pos


class MeteorParticle(Particle):
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

        self.random_down_multiplier = randint(1, 3)
        self.random_side_multiplier = randint(1, 2)

        self.create_surf()
        self.flame = Flame(groups, self.pos)
        self.flame.draw()

    def move(self, dt):
        move_side = pygame.math.Vector2(-1, 0) * self.speed * dt
        move_down = pygame.math.Vector2(0, 1) * self.speed * dt
        self.pos += (
            move_side * self.random_side_multiplier
            + move_down * self.random_down_multiplier
        )
        self.rect.center = self.pos

    def update(self, dt):
        self.move(dt)
        self.flame.update(self.pos)
