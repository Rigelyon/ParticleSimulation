import os
import sys

import cv2
import pygame
import pygame_gui
from pygame_gui import UIManager

from particlesimulation.constants import *
from particlesimulation.dataclass import GameFlag, ParticleFlag
from particlesimulation.particles.particles_manager import ParticlesManager
from particlesimulation.ui import UI
from particlesimulation.video_manager import VideoManager


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()

        self.this_dir = os.path.dirname(os.path.abspath(__file__))
        theme_path = os.path.join(self.this_dir, "styles", "theme.json")
        self.ui_manager = UIManager((WINDOW_WIDTH, WINDOW_HEIGHT), theme_path)

        self.video_manager = VideoManager()
        self.particles = ParticlesManager()
        self.ui = UI(self.ui_manager)
        self.first_run_init()

    def first_run_init(self):
        self.ui.set_particle_types("circle")
        self.check_video_availability()
        self.ui.change_bt_status(ParticleFlag.current_type)

    def process_video_mode(self):
        if GameFlag.current_video_frame < self.get_frames_count:
            dark_pixels = self.video_manager.load_coords(
                GameFlag.current_video_frame
            ).tolist()
            threshold = self.get_pixels_threshold_video(dark_pixels)

            if threshold is not None:
                self.spawn_particles_with_threshold(dark_pixels, threshold)

            GameFlag.current_video_frame += 1
        else:
            self.stop_video_playback()

    def handle_user_events(self, event=None):
        self.ui.enforce_slider_limit()
        if event.user_type == pygame_gui.UI_WINDOW_CLOSE:
            if hasattr(self.ui, "loading_window"):
                if event.ui_element == self.ui.loading_window:
                    self.ui.on_close_loading_window()
            if hasattr(self.ui, "load_video_dialog_window"):
                if event.ui_element == self.ui.load_video_dialog_window:
                    self.ui.on_close_dialog_window()
            if hasattr(self.ui, "restart_dialog_window"):
                if event.ui_element == self.ui.restart_dialog_window:
                    self.ui.on_close_restart_dialog_window()
        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.ui.clear_particle_bt:
                self.particles.kill_all()
        if event.user_type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
            if event.ui_element == self.ui.color_picker:
                self.ui.on_picked_colour_picker()

    def handle_keydown_events(self, event=None):
        if event.key == pygame.K_SPACE:
            self.toggle_video_playback()
        if event.key == pygame.K_c:
            self.particles.kill_all()
        if event.key == pygame.K_9:
            GameFlag.current_video_frame = 5500
            self.video_manager.cap.set(cv2.CAP_PROP_POS_FRAMES, 5500)

    def start_video_playback(self):
        self.particles.kill_all()
        self.ui.set_particle_types("circle")
        self.video_manager.music.play()
        self.ui.ui_state_enabled_video()
        self.video_manager.init_capture()

    def stop_video_playback(self):
        self.video_manager.music.stop()
        self.ui.ui_state_disabled_video()
        GameFlag.current_video_frame = 0
        GameFlag.is_video_running = False
        self.video_manager.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def toggle_video_playback(self):
        self.check_video_availability()
        if GameFlag.is_video_loaded:
            GameFlag.is_video_running = not GameFlag.is_video_running
            if GameFlag.is_video_running:
                self.start_video_playback()
            else:
                self.stop_video_playback()
        else:
            if not GameFlag.is_dialog_opened:
                GameFlag.is_dialog_opened = True
                self.ui.draw_load_video_confirmation_dialog_window(self.ui_manager)

    def get_pixels_threshold_video(self, dark_pixels):
        dark_pixels_threshold = [
            # 450,
            # 400,
            # 350,
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
                return threshold
        return None

    def spawn_particles_with_threshold(self, dark_pixels, threshold):
        self.particles.call_particles_video_mode(
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

    def spawn_default_particles(self):
        self.particles.call_particles(
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

    def refresh_screen(self):
        self.window.fill(self.ui_manager.ui_theme.get_colour("dark_bg"))

    def update_mini_player(self):
        if GameFlag.is_video_running:
            self.ui.draw_mini_player(self.window, self.video_manager.play_mini_player())

    def set_frame_rate(self):
        if GameFlag.is_video_running:
            GameFlag.max_frame_rate = self.video_manager.get_fps
        else:
            GameFlag.max_frame_rate = 120

    def update_time_delta(self):
        self.dt = self.clock.tick(GameFlag.max_frame_rate) / 1000

    def check_video_availability(self):
        coords_dir = os.path.join(self.this_dir, "coordinates")
        if os.path.isdir(coords_dir):
            files = os.listdir(coords_dir)
            if len(files) >= self.video_manager.get_max_frames - 1:
                GameFlag.is_video_loaded = True
                print("Video is loaded")
            else:
                GameFlag.is_video_loaded = False
                print(
                    f"Video not loaded (folder empty or files less than {self.video_manager.get_max_frames-1})"
                )
        else:
            GameFlag.is_video_loaded = False
            print("Video not loaded")

    def fetch_info(self):
        self.get_frames_count = self.video_manager.coords_files_count
        self.get_amount = len(self.particles.groups)
        self.get_fps = round(self.clock.get_fps(), 2)

        self.get_types = ParticleFlag.current_type
        self.get_color = ParticleFlag.current_color
        self.get_multiplier = self.ui.multiplier_slider.get_current_value()
        self.get_min_fade = self.ui.min_fade_slider.get_current_value()
        self.get_max_fade = self.ui.max_fade_slider.get_current_value()
        self.get_min_size = self.ui.min_size_slider.get_current_value()
        self.get_max_size = self.ui.max_size_slider.get_current_value()
        self.get_min_speed = self.ui.min_speed_slider.get_current_value()
        self.get_max_speed = self.ui.max_speed_slider.get_current_value()

    def update_ui_elements(self):
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

        if GameFlag.is_video_loading_in_progress:
            self.ui.loading_bar.percent_full = (
                self.video_manager.calculate_total_progress()
            )
            if self.ui.loading_bar.percent_full >= 0.99:
                self.ui.on_finished_loading(self.ui_manager)
                self.check_video_availability()

    def update_particles(self):
        self.particles.groups.draw(self.ui.screen_surf)
        self.particles.groups.update(self.dt)

    def check_particles(self):
        # Kill particles when reach the threshold and offscreen
        self.particles.check_max_particles()
        self.particles.kill_off_screen()

    def finalize_display(self):
        self.ui_manager.update(self.dt)
        self.ui.surface_blit(self.window)
        self.ui.enforce_slider_limit()
        self.ui_manager.draw_ui(self.window)
        pygame.display.update()

    def update(self):
        self.refresh_screen()
        self.set_frame_rate()
        self.update_time_delta()

        self.fetch_info()
        self.update_ui_elements()
        self.update_mini_player()

        self.update_particles()
        self.check_particles()
        self.finalize_display()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GameFlag.is_running = False
            if event.type == pygame.USEREVENT:
                self.handle_user_events(event)
            if event.type == pygame.KEYDOWN:
                self.handle_keydown_events(event)
            if pygame.mouse.get_pressed()[0]:
                try:
                    self.particles.kill_at_cursor(event.pos)
                except AttributeError:
                    pass

            self.ui_manager.process_events(event)

    def quit(self):
        pygame.quit()
        sys.exit()

    def loop(self):
        GameFlag.current_video_frame = 0
        while GameFlag.is_running:
            self.handle_events()
            self.update()

            if GameFlag.is_video_running:
                self.process_video_mode()
            else:
                self.spawn_default_particles()

        self.quit()
