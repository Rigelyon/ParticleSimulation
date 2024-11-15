import random
from random import randint
import pygame

from particlesimulation.particles.meteor_particle import MeteorParticle
from particlesimulation.particles.sakura_particle import SakuraParticle
from particlesimulation.particles.snow_particle import SnowParticle
from particlesimulation.constants import *
from particlesimulation.dataclass import GameFlag
from particlesimulation.particles.particle import Particle


class ParticlesManager:
    def __init__(self):
        self.groups = pygame.sprite.Group()

    def call_particles(
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
        pixel_pos=None,
    ):
        draw_method = {
            "circle": self._create_particle,
            "snow": self._create_snow_particle,
            "sakura": self._create_sakura_particle,
            "meteor": self._create_meteor_particle,
        }.get(types)

        if draw_method:
            draw_method(
                multiplier,
                color,
                min_speed,
                max_speed,
                min_size,
                max_size,
                min_fade,
                max_fade,
                pixel_pos,
            )

    def call_particles_video_mode(
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
            scaled_pos = (
                int(x * SCALE_VIDEO_WIDTH + 1),
                int(y * SCALE_VIDEO_HEIGHT + 1),
            )
            self.call_particles(
                types,
                multiplier,
                color,
                min_speed,
                max_speed,
                min_size,
                max_size,
                min_fade,
                max_fade,
                pixel_pos=scaled_pos,
            )

    def kill_off_screen(self):
        for particle in self.groups:
            if not (
                0 <= particle.pos[0] <= SCREEN_WIDTH
                and -20 < particle.pos[1] < SCREEN_HEIGHT + 20
            ):
                particle.kill()

    def kill_all(self):
        self.groups.empty()

    def check_max_particles(self):
        while len(self.groups) > MAX_PARTICLES - 50:
            self.groups.sprites()[0].kill()

    def _create_particle(
        self,
        amount,
        color,
        min_speed,
        max_speed,
        min_size,
        max_size,
        min_fade,
        max_fade,
        pixel_pos=None,
    ):
        for _ in range(amount):
            if GameFlag.is_video_running:
                pos = pixel_pos
            else:
                pos = randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT)
            speed = randint(min_speed, max_speed)
            size = randint(min_size, max_size)
            fade_speed = randint(min_fade, max_fade)

            Particle(
                groups=self.groups,
                pos=pos,
                color=color,
                speed=speed,
                size=size,
                fade_speed=fade_speed,
            )

    def _create_snow_particle(
        self,
        amount,
        color,
        min_speed,
        max_speed,
        min_size,
        max_size,
        min_fade,
        max_fade,
        pixel_pos=None,
    ):
        for _ in range(amount):
            if GameFlag.is_video_running:
                pos = pixel_pos
            else:
                pos = randint(0, SCREEN_WIDTH), randint(-10, SCREEN_HEIGHT)
            speed = randint(min_speed, max_speed)
            size = randint(min_size, max_size)
            fade_speed = randint(min_fade, max_fade)

            SnowParticle(
                groups=self.groups,
                pos=pos,
                color=color,
                speed=speed,
                size=size,
                fade_speed=fade_speed,
            )

    def _create_sakura_particle(
        self,
        amount,
        color,
        min_speed,
        max_speed,
        min_size,
        max_size,
        min_fade,
        max_fade,
        pixel_pos=None,
    ):
        for _ in range(amount):
            if GameFlag.is_video_running:
                pos = pixel_pos
            else:
                pos = randint(0, SCREEN_WIDTH), randint(-10, SCREEN_HEIGHT)
            speed = randint(min_speed, max_speed)
            size = randint(min_size, max_size)
            fade_speed = randint(min_fade, max_fade)

            SakuraParticle(
                groups=self.groups,
                pos=pos,
                color=color,
                speed=speed,
                size=size,
                fade_speed=fade_speed,
            )

    def _create_meteor_particle(
        self,
        amount,
        color,
        min_speed,
        max_speed,
        min_size,
        max_size,
        min_fade,
        max_fade,
        pixel_pos=None,
    ):
        for _ in range(amount):
            if GameFlag.is_video_running:
                pos = pixel_pos
            else:
                pos = randint(0, SCREEN_WIDTH), randint(-10, SCREEN_HEIGHT)
            speed = randint(min_speed, max_speed)
            size = randint(min_size, max_size)
            fade_speed = randint(min_fade, max_fade)

            MeteorParticle(
                groups=self.groups,
                pos=pos,
                color=color,
                speed=speed,
                size=size,
                fade_speed=fade_speed,
            )
