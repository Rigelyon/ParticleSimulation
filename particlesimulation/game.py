import os
import sys
import time
from random import sample

import pygame
from pygame_gui import UIManager

from particlesimulation.constants import *
from particlesimulation.particles_manager import ParticlesManager
from particlesimulation.ui import UI
from particlesimulation.video_manager import VideoManager


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.is_paused = False
        self.is_video_running = False
        self.max_frame_rate = 120
        self.current_frame = 0

        script_dir = os.path.dirname(os.path.abspath(__file__))
        theme_path = os.path.join(script_dir, "styles", "theme.json")
        self.ui_manager = UIManager((WINDOW_WIDTH, WINDOW_HEIGHT), theme_path)

        self.video_manager = VideoManager()
        self.particles = ParticlesManager()
        self.ui = UI(self.ui_manager)

        self.last_frame_time = pygame.time.get_ticks()

    def update(self):
        self.window.fill(self.ui_manager.ui_theme.get_colour("dark_bg"))
        self.dt = self.clock.tick(self.max_frame_rate) / 1000

        self.get_frames_count = self.video_manager.files_count
        self.get_amount = len(self.particles.groups)
        self.get_fps = round(self.clock.get_fps(), 2)
        self.get_types = self.ui.current_type
        self.get_color = self.ui.current_color
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
        self.ui.frame_label.set_text(
            f"Frame: {self.current_frame}/{self.get_frames_count}"
        )

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    # TODO: Create progress bar for loading the frames
                    self.video_manager.delete_existing_frames()
                    self.video_manager.make_dir()
                    self.video_manager.video_to_images()
                    self.video_manager.save_coords()
                if event.key == pygame.K_p:
                    self.is_video_running = not self.is_video_running
                    if self.is_video_running:
                        self.video_manager.music.play()
                        self.ui.enforce_value_video_mode()
                    elif not self.is_video_running:
                        self.video_manager.music.stop()
                if event.key == pygame.K_r:
                    self.current_frame = 0

            self.ui_manager.process_events(event)

    def quit(self):
        pygame.quit()
        sys.exit()

    def loop(self):
        self.current_frame = 0
        target_frame_duration = 1 / 30

        while self.is_running:
            start_time = time.time()
            self.handle_events()
            self.update()

            file_name = f"ba-{str(self.current_frame).zfill(4)}.json"
            if self.is_video_running and self.current_frame < self.get_frames_count:
                dark_pixels = self.video_manager.load_coords(self.current_frame)

                if len(dark_pixels) > 300:
                    for y, x in sample(dark_pixels, 300):
                        scaled_x = int(x * SCALE_VIDEO_WIDTH + 1)
                        scaled_y = int(y * SCALE_VIDEO_HEIGHT + 1)
                        self.particles.spawn_particle(
                            self.get_types,
                            self.get_multiplier,
                            self.get_color,
                            self.get_min_speed,
                            self.get_max_speed,
                            self.get_min_size,
                            self.get_max_size,
                            self.get_min_fade,
                            self.get_max_fade,
                            True,
                            (scaled_x, scaled_y),
                        )
                    self.current_frame += 1
                    print(f"Load {file_name} frame number: {self.current_frame-1}")
                else:
                    self.current_frame += 1
                    print(f"Load {file_name} frame number: {self.current_frame-1}")

                elapsed = time.time() - start_time
                if elapsed < target_frame_duration:
                    time.sleep(target_frame_duration - elapsed)
            else:
                # TODO: Switching particles
                self.particles.spawn_particle(
                    self.get_types,
                    self.get_multiplier,
                    self.get_color,
                    self.get_min_speed,
                    self.get_max_speed,
                    self.get_min_size,
                    self.get_max_size,
                    self.get_min_fade,
                    self.get_max_fade,
                )
