import os
import sys
from random import uniform

import pygame

from particlesimulation.particles.particle import Particle

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
        print(f"Resolved path: {os.path.join(base_path, relative_path)}")
    return os.path.join(base_path, relative_path)

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

    def create_surf(self):
        this_dir = resource_path("")
        sprite_dir = os.path.join(this_dir, "assets", "particles", "snow.png")

        print(f"Sprite directory: {sprite_dir}")  # Debug output
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
        self.pos += move_side + move_down

        self.rect.center = self.pos
