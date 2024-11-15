from random import randint

import pygame

from particlesimulation.particles.particle import Particle


class SakuraParticle(Particle):
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
