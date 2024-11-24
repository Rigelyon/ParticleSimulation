import os
from random import randint, uniform

import pygame

from particlesimulation.particles.particle import Particle


class LeavesParticle(Particle):
    def __init__(self, groups, pos, color, size, speed, fade_speed):
        super().__init__(groups, pos, color, size, speed, fade_speed)
        self.pos = pos
        self.color = color
        self.size = size
        self.speed = speed
        self.fade_speed = fade_speed

        self.timer = 3000
        self.random_down_multiplier = randint(1, 3)
        self.random_side_multiplier = randint(1, 5)
        self.spin_angle = 0
        self.spin_radius = 3

        self.create_surf()

    def create_surf(self):
        this_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(this_dir)
        sprite_dir = os.path.join(parent_dir, "assets", "particles", "maple_leaf.png")

        sprite = pygame.image.load(sprite_dir).convert_alpha()
        scaled_sprite = pygame.transform.scale(sprite, (self.size, self.size))
        tinted_sprite = self.tint_image(scaled_sprite, self.color)

        angle = uniform(0, 360)
        self.image = pygame.transform.rotate(tinted_sprite, angle)

        self.rect = self.image.get_rect(center=self.pos)

    def tint_image(self, image, color):
        tinted_sprite = image.copy()
        tinted_sprite.fill(color, special_flags=pygame.BLEND_RGBA_MULT)
        return tinted_sprite

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
