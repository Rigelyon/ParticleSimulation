import random
from random import randint

import pygame

from particlesimulation.constants import *
from particlesimulation.particle import Particle


class ParticlesManager:
    def __init__(self):
        self.groups = pygame.sprite.Group()

    def spawn_particle(
        self,
        types: str,
        multiplier: int,
        color: int,
        min_speed: int,
        max_speed: int,
        min_size: int,
        max_size: int,
        min_fade: int,
        max_fade: int,
        is_video=False,
        pixel_pos=None,
    ):
        match types:
            case "circle":
                self.draw_particle(
                    multiplier,
                    color,
                    min_speed,
                    max_speed,
                    min_size,
                    max_size,
                    min_fade,
                    max_fade,
                    is_video,
                    pixel_pos,
                )
            case "snow":
                self.draw_snow_particle(
                    multiplier,
                    color,
                    min_speed,
                    max_speed,
                    min_size,
                    max_size,
                    min_fade,
                    max_fade,
                    is_video,
                    pixel_pos,
                )

    def spawn_particles_video_mode(
        self,
        types: str,
        multiplier: int,
        color: int,
        min_speed: int,
        max_speed: int,
        min_size: int,
        max_size: int,
        min_fade: int,
        max_fade: int,
        pixel_count: int,
        dark_pixels: [[int, int]],
    ):
        sample_count = min(pixel_count, 450)
        for y, x in random.sample(dark_pixels, sample_count):
            scaled_x = int(x * SCALE_VIDEO_WIDTH + 1)
            scaled_y = int(y * SCALE_VIDEO_HEIGHT + 1)
            self.spawn_particle(
                types,
                multiplier,
                color,
                min_speed,
                max_speed,
                min_size,
                max_size,
                min_fade,
                max_fade,
                True,
                (scaled_x, scaled_y),
            )

    def kill_off_screen(self):
        for particle in self.groups:
            if (
                particle.pos[0] < 0
                or particle.pos[0] > SCREEN_WIDTH
                or particle.pos[1] < -20 + 5
                or particle.pos[1] > SCREEN_HEIGHT + 20
            ):
                particle.kill()

    def check_max_particles(self):
        while len(self.groups) > MAX_PARTICLES - 50:
            self.groups.sprites()[0].kill()

    def draw_particle(
        self,
        amount=1,
        color=BASE_COLOR,
        min_speed=50,
        max_speed=100,
        min_size=5,
        max_size=10,
        min_fade=1,
        max_fade=10,
        is_video=False,
        pixel_pos=None,
    ):
        for _ in range(amount):
            if is_video:
                pos = pixel_pos
            else:
                pos = (randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT))
            direction = pygame.math.Vector2(0, 0)
            speed = randint(min_speed, max_speed)
            size = randint(min_size, max_size)
            fade_speed = randint(min_fade, max_fade)
            Particle(
                groups=self.groups,
                pos=pos,
                color=color,
                direction=direction,
                speed=speed,
                size=size,
                fade_speed=fade_speed,
            )

    def draw_snow_particle(
        self,
        amount=1,
        color=BASE_COLOR,
        min_speed=50,
        max_speed=100,
        min_size=5,
        max_size=10,
        min_fade=1,
        max_fade=10,
        is_video=False,
        pixel_pos=None,
    ):
        for _ in range(amount):
            if is_video:
                pos = pixel_pos
            else:
                pos = (randint(0, SCREEN_WIDTH), randint(-20, SCREEN_HEIGHT - 20))
            direction = pygame.math.Vector2(0, 1)
            speed = randint(min_speed, max_speed)
            size = randint(min_size, max_size)
            fade_speed = randint(min_fade, max_fade)
            Particle(
                groups=self.groups,
                pos=pos,
                color=color,
                direction=direction,
                speed=speed,
                size=size,
                fade_speed=fade_speed,
            )

    def kill_on_cursor(self):
        for event in pygame.event.get():
            if pygame.mouse.get_pressed()[0]:
                # if (event.pos[0])
                pass
