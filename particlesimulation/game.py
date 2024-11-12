import os
import sys
import threading

import cv2
import pygame
from pygame_gui import UIManager

from particlesimulation.constants import *
from particlesimulation.dataclass import GameFlag, UIFlag
from particlesimulation.particles_manager import ParticlesManager
from particlesimulation.ui import UI
from particlesimulation.video_manager import VideoManager


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()

        script_dir = os.path.dirname(os.path.abspath(__file__))
        theme_path = os.path.join(script_dir, "styles", "theme.json")
        self.ui_manager = UIManager((WINDOW_WIDTH, WINDOW_HEIGHT), theme_path)

        self.video_manager = VideoManager()
        self.particles = ParticlesManager()
        self.ui = UI(self.ui_manager)

    def update(self):
        self.window.fill(self.ui_manager.ui_theme.get_colour("dark_bg"))
        if GameFlag.is_video_running:
            GameFlag.max_frame_rate = self.video_manager.get_fps
            self.ui.draw_mini_player(self.window, self.video_manager.play_mini_player())
        else:
            GameFlag.max_frame_rate = 120

        self.dt = self.clock.tick(GameFlag.max_frame_rate) / 1000

        self.get_frames_count = self.video_manager.files_count
        self.get_amount = len(self.particles.groups)
        self.get_fps = round(self.clock.get_fps(), 2)
        self.get_types = UIFlag.current_type
        self.get_color = UIFlag.current_color
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
            f"Frame: {GameFlag.current_video_frame}/{self.get_frames_count}"
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
                GameFlag.is_running = False
                self.quit()
            if event.type == pygame.USEREVENT:
                self.ui.enforce_slider_limit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if GameFlag.is_video_loaded:
                        GameFlag.is_video_running = not GameFlag.is_video_running
                        if GameFlag.is_video_running:
                            self.video_manager.music.play()
                            self.ui.ui_state_enabled_video()
                            self.video_manager.init_capture()
                        elif not GameFlag.is_video_running:
                            GameFlag.current_video_frame = 0
                            self.video_manager.music.stop()
                            self.ui.ui_state_disabled_video()
                            self.video_manager.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        # thread = threading.Thread(
                        #     target=self.video_manager.loading_operation
                        # )
                        # thread.start()
                    else:
                        self.ui.draw_dialog_window(self.ui_manager)

            self.ui_manager.process_events(event)

    def quit(self):
        pygame.quit()
        sys.exit()

    def loop(self):
        GameFlag.current_video_frame = 0

        while GameFlag.is_running:
            self.handle_events()
            self.update()

            if (
                GameFlag.is_video_running
                and GameFlag.current_video_frame < self.get_frames_count
            ):
                dark_pixels = self.video_manager.load_coords(
                    GameFlag.current_video_frame
                ).tolist()
                dark_pixels_threshold = [
                    450,
                    400,
                    350,
                    300,
                    250,
                    200,
                    150,
                    100,
                    50,
                    40,
                    30,
                    20,
                    10,
                    5,
                ]
                for threshold in dark_pixels_threshold:
                    if len(dark_pixels) > threshold:
                        self.particles.spawn_particles_video_mode(
                            self.get_types,
                            self.get_multiplier,
                            self.get_color,
                            self.get_min_speed,
                            self.get_max_speed,
                            self.get_min_size,
                            self.get_max_size,
                            self.get_min_fade,
                            self.get_max_fade,
                            threshold,
                            dark_pixels,
                        )
                        GameFlag.current_video_frame += 1
                        break
                else:
                    GameFlag.current_video_frame += 1

            elif GameFlag.current_video_frame >= self.get_frames_count:
                GameFlag.is_video_running = False
                self.video_manager.music.stop()
                self.ui.ui_state_disabled_video()
                GameFlag.current_video_frame = 0

            else:
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
