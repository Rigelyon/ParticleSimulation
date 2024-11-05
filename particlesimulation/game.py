import sys

import pygame

from particlesimulation.ui import UI
from particlesimulation.particles.particles_manager import ParticlesManager
from particlesimulation.constants import *


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.max_frame_rate = 60

        self.particles = ParticlesManager()
        self.ui = UI()

    def update(self):
        self.window.fill(BG_COLOR)
        self.dt = self.clock.tick(self.max_frame_rate) / 1000

        particle_count = len(self.particles.groups)
        self.ui.draw_screen()
        self.ui.draw_text(
            self.window,
            f"Particle(s) count: {particle_count}",
            (SCREEN_MARGIN, SCREENY_BOTTOM + SCREEN_MARGIN),
            "midleft",
            self.ui.font_normal,
            BASE_COLOR,
        )
        self.ui.draw_text(
            self.window,
            f"Frame: 0/0",
            (SCREEN_MARGIN, SCREENY_BOTTOM + SCREEN_MARGIN + 22),
            "midleft",
            self.ui.font_normal,
            BASE_COLOR,
        )
        self.ui.draw_text(
            self.window,
            f"Frame rate: {round(self.clock.get_fps(), 2)}",
            (SCREENX_RIGHT, SCREENY_BOTTOM + SCREEN_MARGIN),
            "midright",
            self.ui.font_normal,
            BASE_COLOR,
        )
        self.ui.draw_text(
            self.window,
            f"Amount: {self.ui.size_slider.get_current_value()}",
            (SCREENX_RIGHT + SCREEN_MARGIN, SCREENY_TOP + 20 + PARTICLE_BT_SIZE[1] * 2),
            "midleft",
            self.ui.font_normal,
            BASE_COLOR,
        )

        self.particles.groups.draw(self.ui.screen_surf)
        self.particles.groups.update(self.dt)

        # Kill particles when reach the threshold and offscreen
        self.particles.check_max_particles()
        self.particles.kill_off_screen()

        self.ui.update(self.dt)
        self.ui.surface_blit(self.window)
        self.ui.draw_ui(self.window)

        pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                self.quit()

            self.ui.process_events(event)

    def quit(self):
        pygame.quit()
        sys.exit()

    def loop(self):
        while self.is_running:
            self.handle_events()
            self.update()

            print(self.ui.size_slider.get_current_value())

            # self.particles.spawn_particle('snow', 1,1,1,1,1,1)
