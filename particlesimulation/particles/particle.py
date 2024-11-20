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
