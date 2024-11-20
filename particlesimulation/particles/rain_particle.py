from random import randint

import pygame

from particlesimulation.particles.particle import Particle


class SplashParticle(Particle):
    def __init__(self, groups, pos, size):
        super().__init__(groups, pos, size)
        self.pos = pos
        self.size = size
        self.color = (255, 255, 255)
        self.random_down_multiplier = randint(1, 3)
        self.random_side_multiplier = randint(1, 5)

    def move(self, dt):
        move_side = pygame.math.Vector2(randint(-1, 0), 0) * randint(50, 100) * dt
        move_up = pygame.math.Vector2(0, -1) * randint(50, 100) * dt
        self.pos += (
            move_side * self.random_side_multiplier
            + move_up * self.random_down_multiplier
        )
        self.rect.center = self.pos

        self.size -= 0.1 * randint(1, 4)

    def check_size(self):
        if self.size <= 0:
            self.kill()

    def update(self, dt):
        self.move(dt)
        self.fade(dt)
        self.check_alpha()
        self.check_size()


class Splash:
    def __init__(self, groups, pos):
        self.groups = groups
        self.x, self.y = pos
        self.flame_intensity = 2
        self.particles = []

        for i in range(self.flame_intensity * 25):
            self.particles.append(
                SplashParticle(
                    self.groups, (self.x + randint(-5, 5), self.y), randint(1, 5)
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
        self.group = groups
        self.pos = pos
        self.color = color
        self.size = size
        self.speed = speed
        self.fade_speed = fade_speed

        self.random_down_multiplier = randint(1, 3)
        self.random_side_multiplier = randint(1, 2)

        self.create_surf()
        self.splash = Splash(groups, self.pos)
        self.splash.draw()

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
        self.splash.update(self.pos)
