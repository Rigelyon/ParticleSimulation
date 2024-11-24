from random import randint, choice, uniform

import pygame

from particlesimulation.particles.particle import Particle


class FireflyParticle(Particle):
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

        self.alpha = randint(128, 255)
        self.glow_speed = 2
        self.alpha_direction = 1
        self.lifetime = 255 / self.fade_speed
        self.direction = self.random_direction()
        self.direction_time = uniform(0.5, 2.0)
        self.elapsed_direction_time = 0
        self.elapsed_time = 0

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

    def random_direction(self):
        angle = uniform(0, 360)
        vector = pygame.math.Vector2()
        vector.from_polar((1, angle))
        return vector

    def move(self, dt):
        self.elapsed_direction_time += dt
        if self.elapsed_direction_time >= self.direction_time:
            self.direction = self.random_direction()
            self.direction_time = uniform(0.5, 2.0)
            self.elapsed_direction_time = 0

        self.pos += self.direction * self.speed * dt
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
