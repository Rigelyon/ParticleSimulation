from random import randint

import pygame

from particlesimulation.particles.particle import Particle


class FlameParticle(pygame.sprite.Sprite):
    def __init__(self, groups, pos, radius):
        super().__init__(groups)
        self.pos = pos
        self.x, self.y = self.pos
        self.radius = 5
        self.original_radius = radius
        self.alpha_layers = 2
        self.alpha_glow = 2

        self.burn_rate = 0.1 * randint(1, 4)
        self.create_surf()

    def create_surf(self):
        max_surf_size = (
            2 * self.radius * self.alpha_layers * self.alpha_layers * self.alpha_glow
        )
        self.image = pygame.Surface((max_surf_size, max_surf_size)).convert_alpha()

        for i in range(self.alpha_layers, -1, -1):
            alpha = 255 - i * (255 // self.alpha_layers - 5)

            if alpha <= 0:
                alpha = 0
            radius = self.radius * i * i * self.alpha_glow

            if self.radius == 4 or self.radius == 3:
                r, g, b = (255, 0, 0)
            elif self.radius == 2:
                r, g, b = (255, 150, 0)
            else:
                r, g, b = (50, 50, 50)

            color = (r, g, b, alpha)
            pygame.draw.circle(
                self.image,
                color,
                (self.image.get_width() // 2, self.image.get_height() // 2),
                radius,
            )
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def move(self, dt):
        self.pos = (
            self.x + randint(-self.radius, self.radius) * dt,
            self.y - 7 - self.radius * dt,
        )
        self.original_radius -= self.burn_rate
        self.radius = int(self.original_radius)
        if self.radius <= 0:
            self.radius = 1

    def update(self, dt):
        self.move(dt)


class Flame:
    def __init__(self, groups, pos):
        self.groups = groups
        self.x, self.y = pos
        self.flame_intensity = 2
        self.flame_particles = []

        for i in range(self.flame_intensity * 25):
            self.flame_particles.append(
                FlameParticle(
                    self.groups, (self.x + randint(-5, 5), self.y), randint(1, 5)
                )
            )

    def draw(self, dt):
        for i in self.flame_particles:
            if i.original_radius <= 0:
                self.flame_particles.remove(i)
                self.flame_particles.append(
                    FlameParticle(
                        self.groups, (self.x + randint(-5, 5), self.y), randint(1, 5)
                    )
                )

                del i
                continue

            i.update(dt)
            i.create_surf()

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
        self.pos = pos
        self.color = color
        self.size = size
        self.speed = speed
        self.fade_speed = fade_speed

        self.random_down_multiplier = randint(1, 3)
        self.random_side_multiplier = randint(1, 2)

        self.create_surf()
        self.flame = Flame(groups, self.pos)

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
        self.flame.draw(dt)
        self.flame.update(self.pos)
