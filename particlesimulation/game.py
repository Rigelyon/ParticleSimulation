import os
import sys

import pygame
from pygame_gui import UIManager

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

        script_dir = os.path.dirname(os.path.abspath(__file__))
        theme_path = os.path.join(script_dir, "styles", "theme.json")
        self.ui_manager = UIManager((WINDOW_WIDTH, WINDOW_HEIGHT), theme_path)

        self.particles = ParticlesManager()
        self.ui = UI(self.ui_manager)

    def update(self):
        self.window.fill(self.ui_manager.ui_theme.get_colour("dark_bg"))
        self.dt = self.clock.tick(self.max_frame_rate) / 1000

        self.get_amount = len(self.particles.groups)
        self.get_fps = round(self.clock.get_fps(), 2)
        self.get_multiplier = self.ui.multiplier_slider.get_current_value()
        self.get_min_fade = self.ui.min_fade_slider.get_current_value()
        self.get_max_fade = self.ui.max_fade_slider.get_current_value()
        self.get_min_size = self.ui.min_size_slider.get_current_value()
        self.get_max_size = self.ui.max_size_slider.get_current_value()
        self.get_min_speed = self.ui.min_speed_slider.get_current_value()
        self.get_max_speed = self.ui.max_speed_slider.get_current_value()

        self.ui.draw_screen()
        self.ui.particle_count_label.set_text(f"Particle(s) amount: {self.get_amount}")
        self.ui.fps_label.set_text(f"FPS: {self.get_fps}")

        self.ui.multiplier_label.set_text(f"Multiplier: {self.get_multiplier}")
        self.ui.min_fade_label.set_text(f"Min Fade Speed: {self.get_min_fade}")
        self.ui.max_fade_label.set_text(f"Max Fade Speed: {self.get_max_fade}")
        self.ui.min_size_label.set_text(f"Min Size: {self.get_min_size}")
        self.ui.max_size_label.set_text(f"Max Size: {self.get_max_size}")
        self.ui.min_speed_label.set_text(f"Min Speed: {self.get_min_speed}")
        self.ui.max_speed_label.set_text(f"Max Speed: {self.get_max_speed}")

        self.particles.groups.draw(self.ui.screen_surf)
        self.particles.groups.update(self.dt)

        # Kill particles when reach the threshold and offscreen
        self.particles.check_max_particles()
        self.particles.kill_off_screen()

        self.ui_manager.update(self.dt)
        self.ui.surface_blit(self.window)
        self.ui.enforce_slider_limit()
        self.ui_manager.draw_ui(self.window)

        pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                self.quit()
            if event.type == pygame.USEREVENT:
                self.ui.enforce_slider_limit()

            self.ui_manager.process_events(event)

    def quit(self):
        pygame.quit()
        sys.exit()

    def loop(self):
        while self.is_running:
            self.handle_events()
            self.update()

            # TODO: Switching particles
            self.particles.spawn_particle(
                "snow",
                self.get_multiplier,
                BASE_COLOR,
                self.get_min_speed,
                self.get_max_speed,
                self.get_min_size,
                self.get_max_size,
                self.get_min_fade,
                self.get_max_fade,
            )
