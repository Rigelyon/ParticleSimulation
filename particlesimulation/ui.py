import threading

import pygame
from pygame_gui.elements import (
    UIHorizontalSlider,
    UILabel,
    UIButton,
    UIScrollingContainer,
    UIWindow,
    UITextBox,
    UIStatusBar,
)
from pygame_gui.core import ObjectID
from pygame_gui.windows import UIColourPickerDialog

from particlesimulation.constants import *
from particlesimulation.dataclass import UIFlag, GameFlag, ParticleFlag
from particlesimulation.particles.particles_manager import ParticlesManager
from particlesimulation.video_manager import VideoManager


class UI:
    def __init__(self, ui_manager):
        self.font_normal = pygame.font.SysFont(None, 22)

        self.draw_container(ui_manager)
        self.draw_components(ui_manager, self.scroll_container)

        self.video_manager = VideoManager()
        self.particle_manager = ParticlesManager()

    def set_particle_types(self, types):
        match types:
            case "circle":
                self.change_bt_status("circle")
                ParticleFlag.current_type = "circle"
                ParticleFlag.current_color = pygame.Color(255, 255, 255)
                if not GameFlag.is_video_running:
                    self.multiplier_slider.set_current_value(1)
                    self.min_fade_slider.set_current_value(
                        ParticleFlag.default_max_fade - 1
                    )
                    self.max_fade_slider.set_current_value(
                        ParticleFlag.default_max_fade
                    )
                    self.min_size_slider.set_current_value(1)
                    self.max_size_slider.set_current_value(15)
                    self.min_speed_slider.set_current_value(1)
                    self.max_speed_slider.set_current_value(2)
            case "snow":
                self.change_bt_status("snow")
                ParticleFlag.current_type = "snow"
                ParticleFlag.current_color = pygame.Color(168, 235, 255)
                if not GameFlag.is_video_running:
                    self.multiplier_slider.set_current_value(1)
                    self.min_fade_slider.set_current_value(50)
                    self.max_fade_slider.set_current_value(100)
                    self.min_size_slider.set_current_value(1)
                    self.max_size_slider.set_current_value(10)
                    self.min_speed_slider.set_current_value(100)
                    self.max_speed_slider.set_current_value(300)
            case "leaves":
                self.change_bt_status("leaves")
                ParticleFlag.current_type = "leaves"
                ParticleFlag.current_color = pygame.Color(219, 114, 7)
                if not GameFlag.is_video_running:
                    self.multiplier_slider.set_current_value(1)
                    self.min_fade_slider.set_current_value(50)
                    self.max_fade_slider.set_current_value(100)
                    self.min_size_slider.set_current_value(10)
                    self.max_size_slider.set_current_value(25)
                    self.min_speed_slider.set_current_value(50)
                    self.max_speed_slider.set_current_value(60)
            case "steam":
                self.change_bt_status("steam")
                ParticleFlag.current_type = "steam"
                ParticleFlag.current_color = pygame.Color(225, 245, 254)
                if not GameFlag.is_video_running:
                    self.multiplier_slider.set_current_value(1)
                    self.min_fade_slider.set_current_value(
                        ParticleFlag.default_min_fade
                    )
                    self.max_fade_slider.set_current_value(
                        ParticleFlag.default_min_fade + 1
                    )
                    self.min_size_slider.set_current_value(3)
                    self.max_size_slider.set_current_value(10)
                    self.min_speed_slider.set_current_value(50)
                    self.max_speed_slider.set_current_value(80)
            case "firefly":
                self.change_bt_status("firefly")
                ParticleFlag.current_type = "firefly"
                ParticleFlag.current_color = pygame.Color(255, 241, 118)
                if not GameFlag.is_video_running:
                    self.multiplier_slider.set_current_value(1)
                    self.min_fade_slider.set_current_value(
                        ParticleFlag.default_min_fade
                    )
                    self.max_fade_slider.set_current_value(
                        ParticleFlag.default_min_fade + 1
                    )
                    self.min_size_slider.set_current_value(3)
                    self.max_size_slider.set_current_value(10)
                    self.min_speed_slider.set_current_value(50)
                    self.max_speed_slider.set_current_value(80)
            case "rain":
                self.change_bt_status("rain")
                ParticleFlag.current_type = "rain"
                ParticleFlag.current_color = pygame.Color(129, 212, 250)
                if not GameFlag.is_video_running:
                    self.multiplier_slider.set_current_value(1)
                    self.min_fade_slider.set_current_value(
                        ParticleFlag.default_min_fade
                    )
                    self.max_fade_slider.set_current_value(
                        ParticleFlag.default_min_fade + 1
                    )
                    self.min_size_slider.set_current_value(3)
                    self.max_size_slider.set_current_value(10)
                    self.min_speed_slider.set_current_value(
                        ParticleFlag.default_max_speed - 10
                    )
                    self.max_speed_slider.set_current_value(
                        ParticleFlag.default_max_speed
                    )
            case "sakura":
                self.change_bt_status("sakura")
                ParticleFlag.current_type = "sakura"
                ParticleFlag.current_color = pygame.Color(255, 182, 193)
                if not GameFlag.is_video_running:
                    self.multiplier_slider.set_current_value(1)
                    self.min_fade_slider.set_current_value(
                        ParticleFlag.default_min_fade
                    )
                    self.max_fade_slider.set_current_value(
                        ParticleFlag.default_min_fade + 1
                    )
                    self.min_size_slider.set_current_value(10)
                    self.max_size_slider.set_current_value(20)
                    self.min_speed_slider.set_current_value(20)
                    self.max_speed_slider.set_current_value(80)
            case "vortex":
                self.change_bt_status("vortex")
                ParticleFlag.current_type = "vortex"
                ParticleFlag.current_color = pygame.Color(129, 212, 250)
                if not GameFlag.is_video_running:
                    self.multiplier_slider.set_current_value(1)
                    self.min_fade_slider.set_current_value(
                        ParticleFlag.default_min_fade
                    )
                    self.max_fade_slider.set_current_value(
                        ParticleFlag.default_min_fade + 1
                    )
                    self.min_size_slider.set_current_value(1)
                    self.max_size_slider.set_current_value(10)
                    self.min_speed_slider.set_current_value(20)
                    self.max_speed_slider.set_current_value(80)

    def change_bt_status(self, types):
        self.circle_bt.unselect()
        self.snow_bt.unselect()
        self.leaves_bt.unselect()
        self.steam_bt.unselect()
        self.firefly_bt.unselect()
        self.rain_bt.unselect()
        self.sakura_bt.unselect()
        self.vortex_bt.unselect()

        match types:
            case "circle":
                self.circle_bt.select()
            case "snow":
                self.snow_bt.select()
            case "leaves":
                self.leaves_bt.select()
            case "steam":
                self.steam_bt.select()
            case "firefly":
                self.firefly_bt.select()
            case "rain":
                self.rain_bt.select()
            case "sakura":
                self.sakura_bt.select()
            case "vortex":
                self.vortex_bt.select()

    def enforce_slider_limit(self):
        min_fade = self.min_fade_slider.get_current_value()
        max_fade = self.max_fade_slider.get_current_value()
        min_size = self.min_size_slider.get_current_value()
        max_size = self.max_size_slider.get_current_value()
        min_speed = self.min_speed_slider.get_current_value()
        max_speed = self.max_speed_slider.get_current_value()

        if min_size > max_size:
            self.min_size_slider.set_current_value(max_size - 1)
        if max_size < min_size:
            self.max_size_slider.set_current_value(min_size + 1)

        if min_speed > max_speed:
            self.min_speed_slider.set_current_value(max_speed - 1)
        if max_speed < min_speed:
            self.max_speed_slider.set_current_value(min_speed + 1)

        if min_fade > max_fade:
            self.min_fade_slider.set_current_value(max_fade - 1)
        if max_fade < min_fade:
            self.max_fade_slider.set_current_value(min_fade + 1)

    def ui_state_enabled_video(self):
        self.circle_bt.disable()
        self.snow_bt.disable()
        self.leaves_bt.disable()
        self.steam_bt.disable()
        self.firefly_bt.disable()
        self.rain_bt.disable()
        self.sakura_bt.disable()
        self.vortex_bt.disable()
        self.multiplier_slider.set_current_value(1)
        self.multiplier_slider.disable()
        self.multiplier_label.disable()
        self.min_fade_slider.set_current_value(ParticleFlag.default_max_fade - 1)
        self.min_fade_slider.disable()
        self.min_fade_label.disable()
        self.max_fade_slider.set_current_value(ParticleFlag.default_max_fade)
        self.max_fade_slider.disable()
        self.max_fade_label.disable()
        self.min_size_slider.set_current_value(1)
        self.min_size_slider.disable()
        self.min_size_label.disable()
        self.max_size_slider.set_current_value(6)
        self.max_size_slider.disable()
        self.max_size_label.disable()
        self.min_speed_slider.set_current_value(1)
        self.min_speed_slider.disable()
        self.min_speed_label.disable()
        self.max_speed_slider.set_current_value(2)
        self.max_speed_slider.disable()
        self.max_speed_label.disable()
        self.scroll_container.set_relative_position(
            (
                SCREENX_RIGHT + SCREEN_SPACING,
                SCREENY_TOP + UIFlag.mini_player_height + UIFlag.separator_spacing,
            )
        )
        self.scroll_container.set_dimensions(
            (
                265,
                SCREEN_HEIGHT - (UIFlag.mini_player_height + UIFlag.separator_spacing),
            )
        )

    def ui_state_disabled_video(self):
        self.circle_bt.enable()
        self.snow_bt.enable()
        self.leaves_bt.enable()
        self.steam_bt.enable()
        self.firefly_bt.enable()
        self.rain_bt.enable()
        self.sakura_bt.enable()
        self.vortex_bt.enable()
        self.multiplier_slider.enable()
        self.multiplier_label.enable()
        self.min_fade_slider.enable()
        self.min_fade_label.enable()
        self.max_fade_slider.enable()
        self.max_fade_label.enable()
        self.min_size_slider.enable()
        self.min_size_label.enable()
        self.max_size_slider.enable()
        self.max_size_label.enable()
        self.min_speed_slider.enable()
        self.min_speed_label.enable()
        self.max_speed_slider.enable()
        self.max_speed_label.enable()
        self.scroll_container.set_position(
            (SCREENX_RIGHT + SCREEN_SPACING, SCREENY_TOP)
        )
        self.scroll_container.set_dimensions(
            (
                265,
                SCREEN_HEIGHT,
            ),
            False,
        )

    def draw_mini_player(self, surface, video):
        surface.blit(video, (SCREENX_RIGHT + SCREEN_SPACING, SCREEN_MARGIN))
        screen_rect = pygame.Rect(
            (SCREENX_RIGHT + SCREEN_SPACING, SCREEN_MARGIN),
            (UIFlag.mini_player_width, UIFlag.mini_player_height),
        )
        pygame.draw.rect(surface, pygame.Color("#8C89B2"), screen_rect, width=2)

    def draw_screen(self):
        self.screen_surf = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        pygame.draw.rect(
            self.screen_surf, pygame.Color("#8C89B2"), screen_rect, width=2
        )

    def surface_blit(self, surface):
        surface.blit(self.screen_surf, (SCREENX_LEFT, SCREENY_TOP))

    def draw_color_picker_dialog(self, ui_manager):
        self.color_picker = UIColourPickerDialog(
            pygame.Rect((WINDOW_WIDTH / 4, WINDOW_HEIGHT / 4), (500, 300)),
            ui_manager,
            window_title="Choose Color",
        )

    def draw_container(self, ui_manager):
        self.scroll_container = UIScrollingContainer(
            pygame.Rect(
                (SCREENX_RIGHT + SCREEN_SPACING, SCREENY_TOP), (265, SCREEN_HEIGHT)
            ),
            manager=ui_manager,
            allow_scroll_x=False,
        )

    def on_picked_colour_picker(self):
        ParticleFlag.current_color = self.color_picker.get_colour()

    def on_close_restart_dialog_window(self):
        self.restart_dialog_window.kill()
        GameFlag.is_dialog_opened = False

    def on_yes_restart_dialog_window(self, ui_manager):
        GameFlag.is_dialog_opened = False
        GameFlag.is_running = False

    def on_close_dialog_window(self):
        self.load_video_dialog_window.kill()
        GameFlag.is_dialog_opened = False

    def on_yes_dialog_window(self, ui_manager):
        self.draw_loading_window(ui_manager)
        self.thread = threading.Thread(
            target=self.video_manager.start_loading_operation
        )
        self.thread.start()
        GameFlag.is_dialog_opened = False

    def on_close_loading_window(self):
        self.loading_window.kill()
        self.video_manager.stop_loading_operation()
        self.thread.join()

    def on_finished_loading(self, ui_manager):
        self.loading_window.kill()
        self.thread.join()
        GameFlag.is_video_loading_in_progress = False
        self.draw_restart_confirmation_dialog_window(ui_manager)

    def draw_loading_window(self, ui_manager):
        self.load_video_dialog_window.kill()
        self.loading_window = UIWindow(
            pygame.Rect((WINDOW_WIDTH / 4, WINDOW_HEIGHT / 4), (500, 200)),
            ui_manager,
            window_display_title="Loading Video!",
        )
        self.loading_label = UILabel(
            pygame.Rect((500 / 2 - 200 / 2, 20), (200, 80)),
            "Please wait..",
            manager=ui_manager,
            container=self.loading_window,
            object_id=ObjectID(class_id="@loading_text"),
        )
        self.loading_bar = UIStatusBar(
            pygame.Rect((10, 60), (480, 30)),
            manager=ui_manager,
            container=self.loading_window,
            object_id=ObjectID(class_id="@loading_bar"),
        )

        self.cancel_bt = UIButton(
            pygame.Rect((500 / 2 - 100 / 2, 20), (100, 40)),
            "Cancel",
            ui_manager,
            container=self.loading_window,
            command=lambda: self.on_close_loading_window(),
            anchors={"top": "top", "top_target": self.loading_bar},
        )

    def draw_load_video_confirmation_dialog_window(self, ui_manager):
        self.load_video_dialog_window = UIWindow(
            pygame.Rect((WINDOW_WIDTH / 4, WINDOW_HEIGHT / 4), (500, 200)),
            ui_manager,
            window_display_title="Alert!",
        )
        self.alert_label = UITextBox(
            "Pressing Space Bar will actually plays the video sequence, but you haven't load the video. Do you want to load the video now?",
            pygame.Rect((10, 20), (480, 80)),
            manager=ui_manager,
            container=self.load_video_dialog_window,
            anchors={
                "top": "top",
                "bottom": "bottom",
                "left": "left",
                "right": "right",
            },
            object_id=ObjectID(class_id="@alert_text"),
        )
        self.yes_bt = UIButton(
            pygame.Rect((500 / 2 - 210 / 2, 10), (100, 40)),
            "Yes",
            ui_manager,
            self.load_video_dialog_window,
            command=lambda: self.on_yes_dialog_window(ui_manager),
            anchors={"top": "top", "top_target": self.alert_label},
        )

        self.no_bt = UIButton(
            pygame.Rect((10, 10), (100, 40)),
            "No",
            ui_manager,
            self.load_video_dialog_window,
            command=lambda: self.load_video_dialog_window.kill(),
            anchors={
                "left": "left",
                "top": "top",
                "top_target": self.alert_label,
                "left_target": self.yes_bt,
            },
        )

    def draw_restart_confirmation_dialog_window(self, ui_manager):
        self.restart_dialog_window = UIWindow(
            pygame.Rect((WINDOW_WIDTH / 4, WINDOW_HEIGHT / 4), (500, 200)),
            ui_manager,
            window_display_title="Alert!",
        )
        self.alert_label = UITextBox(
            "Video is loaded, restart the program to start playing video sequence. You can play by pressing the space bar",
            pygame.Rect((10, 20), (480, 80)),
            manager=ui_manager,
            container=self.restart_dialog_window,
            anchors={
                "top": "top",
                "bottom": "bottom",
                "left": "left",
                "right": "right",
            },
            object_id=ObjectID(class_id="@alert_text"),
        )
        self.yes_bt = UIButton(
            pygame.Rect((500 / 2 - 210 / 2, 10), (100, 40)),
            "Quit Program",
            ui_manager,
            self.restart_dialog_window,
            command=lambda: self.on_yes_restart_dialog_window(ui_manager),
            anchors={"top": "top", "top_target": self.alert_label},
        )

        self.no_bt = UIButton(
            pygame.Rect((10, 10), (100, 40)),
            "Later",
            ui_manager,
            self.restart_dialog_window,
            command=lambda: self.restart_dialog_window.kill(),
            anchors={
                "left": "left",
                "top": "top",
                "top_target": self.alert_label,
                "left_target": self.yes_bt,
            },
        )

    def draw_components(self, ui_manager, container):
        self.particle_count_label = UILabel(
            pygame.Rect((SCREENX_LEFT, SCREENY_BOTTOM + SCREEN_SPACING), (300, 20)),
            "Particle(s) count:",
            ui_manager,
            object_id=ObjectID(class_id="@debug_text"),
        )
        self.frame_label = UILabel(
            pygame.Rect((SCREENX_LEFT, UIFlag.spacing), (300, 20)),
            "Frame: 0/0",
            ui_manager,
            anchors={"top": "top", "top_target": self.particle_count_label},
            object_id=ObjectID(class_id="@debug_text"),
        )
        self.fps_label = UILabel(
            pygame.Rect(
                (SCREENX_RIGHT - 150, SCREENY_BOTTOM + SCREEN_SPACING), (150, 20)
            ),
            "FPS:",
            ui_manager,
            object_id=ObjectID(class_id="#fps_counter"),
        )

        self.circle_bt = UIButton(
            pygame.Rect((UIFlag.start_x, UIFlag.start_y), PARTICLE_BT_SIZE),
            "Circle",
            ui_manager,
            container,
            command=lambda: self.set_particle_types("circle"),
            object_id=ObjectID(class_id="@particle_button"),
        )
        self.snow_bt = UIButton(
            pygame.Rect((UIFlag.bt_spacing, UIFlag.start_y), PARTICLE_BT_SIZE),
            "Snow",
            ui_manager,
            container,
            command=lambda: self.set_particle_types("snow"),
            anchors={"left": "left", "left_target": self.circle_bt},
            object_id=ObjectID(class_id="@particle_button"),
        )
        self.leaves_bt = UIButton(
            pygame.Rect((UIFlag.bt_spacing, UIFlag.start_y), PARTICLE_BT_SIZE),
            "Leaves",
            ui_manager,
            container,
            command=lambda: self.set_particle_types("leaves"),
            anchors={"left": "left", "left_target": self.snow_bt},
            object_id=ObjectID(class_id="@particle_button"),
        )
        self.steam_bt = UIButton(
            pygame.Rect((UIFlag.bt_spacing, UIFlag.start_y), PARTICLE_BT_SIZE),
            "Steam",
            ui_manager,
            container,
            command=lambda: self.set_particle_types("steam"),
            anchors={"left": "left", "left_target": self.leaves_bt},
            object_id=ObjectID(class_id="@particle_button"),
        )
        self.firefly_bt = UIButton(
            pygame.Rect((UIFlag.start_x, UIFlag.bt_spacing), PARTICLE_BT_SIZE),
            "Firefly",
            ui_manager,
            container,
            command=lambda: self.set_particle_types("firefly"),
            anchors={"top": "top", "top_target": self.circle_bt},
            object_id=ObjectID(class_id="@particle_button"),
        )
        self.rain_bt = UIButton(
            pygame.Rect((UIFlag.bt_spacing, UIFlag.bt_spacing), PARTICLE_BT_SIZE),
            "Rain",
            ui_manager,
            container,
            command=lambda: self.set_particle_types("rain"),
            anchors={
                "top": "top",
                "left": "left",
                "top_target": self.snow_bt,
                "left_target": self.firefly_bt,
            },
            object_id=ObjectID(class_id="@particle_button"),
        )
        self.sakura_bt = UIButton(
            pygame.Rect((UIFlag.bt_spacing, UIFlag.bt_spacing), PARTICLE_BT_SIZE),
            "Sakura",
            ui_manager,
            container,
            command=lambda: self.set_particle_types("sakura"),
            anchors={
                "top": "top",
                "left": "left",
                "top_target": self.leaves_bt,
                "left_target": self.rain_bt,
            },
            object_id=ObjectID(class_id="@particle_button"),
        )
        self.vortex_bt = UIButton(
            pygame.Rect((UIFlag.bt_spacing, UIFlag.bt_spacing), PARTICLE_BT_SIZE),
            "Vortex",
            ui_manager,
            container,
            command=lambda: self.set_particle_types("vortex"),
            anchors={
                "top": "top",
                "left": "left",
                "top_target": self.steam_bt,
                "left_target": self.sakura_bt,
            },
            object_id=ObjectID(class_id="@particle_button"),
        )

        self.chose_color_bt = UIButton(
            pygame.Rect(
                (UIFlag.start_x, UIFlag.separator_spacing),
                (PARTICLE_BT_SIZE[0] * 2 + UIFlag.bt_spacing, 35),
            ),
            "Choose Color",
            ui_manager,
            container,
            command=lambda: self.draw_color_picker_dialog(ui_manager),
            anchors={"top": "top", "top_target": self.firefly_bt},
            object_id=ObjectID(class_id="@button"),
        )

        self.clear_particle_bt = UIButton(
            pygame.Rect(
                (UIFlag.bt_spacing, UIFlag.separator_spacing),
                (PARTICLE_BT_SIZE[0] * 2 + UIFlag.bt_spacing, 35),
            ),
            "Clear",
            ui_manager,
            container,
            anchors={
                "left": "left",
                "top": "top",
                "left_target": self.chose_color_bt,
                "top_target": self.firefly_bt,
            },
            object_id=ObjectID(class_id="@button"),
        )

        self.multiplier_label = UILabel(
            pygame.Rect((UIFlag.start_x, UIFlag.separator_spacing), (200, 20)),
            "Multiplier:",
            ui_manager,
            container,
            anchors={"top": "top", "top_target": self.chose_color_bt},
            object_id=ObjectID(class_id="@setting_indicator"),
        )
        self.multiplier_slider = UIHorizontalSlider(
            pygame.Rect((UIFlag.start_x, UIFlag.spacing), (235, 25)),
            1,
            (1, 100),
            ui_manager,
            container,
            anchors={"top": "top", "top_target": self.multiplier_label},
        )

        self.min_fade_label = UILabel(
            pygame.Rect((UIFlag.start_x, UIFlag.separator_spacing), (200, 20)),
            "Min Fade Speed:",
            ui_manager,
            container,
            anchors={"top": "top", "top_target": self.multiplier_slider},
            object_id=ObjectID(class_id="@setting_indicator"),
        )
        self.min_fade_slider = UIHorizontalSlider(
            pygame.Rect((UIFlag.start_x, UIFlag.spacing), (235, 25)),
            ParticleFlag.default_min_fade,
            (ParticleFlag.default_min_fade, ParticleFlag.default_max_fade - 1),
            ui_manager,
            container,
            anchors={"top": "top", "top_target": self.min_fade_label},
        )

        self.max_fade_label = UILabel(
            pygame.Rect((UIFlag.start_x, UIFlag.spacing), (200, 20)),
            "Max Fade Speed:",
            ui_manager,
            container,
            anchors={"top": "top", "top_target": self.min_fade_slider},
            object_id=ObjectID(class_id="@setting_indicator"),
        )
        self.max_fade_slider = UIHorizontalSlider(
            pygame.Rect((UIFlag.start_x, UIFlag.spacing), (235, 25)),
            ParticleFlag.default_min_fade + 1,
            (ParticleFlag.default_min_fade + 1, ParticleFlag.default_max_fade),
            ui_manager,
            container,
            anchors={"top": "top", "top_target": self.max_fade_label},
        )

        self.min_size_label = UILabel(
            pygame.Rect((UIFlag.start_x, UIFlag.separator_spacing), (200, 20)),
            "Min Size:",
            ui_manager,
            container,
            anchors={"top": "top", "top_target": self.max_fade_slider},
            object_id=ObjectID(class_id="@setting_indicator"),
        )
        self.min_size_slider = UIHorizontalSlider(
            pygame.Rect((UIFlag.start_x, UIFlag.spacing), (235, 25)),
            1,
            (1, ParticleFlag.default_max_size - 1),
            ui_manager,
            container,
            anchors={"top": "top", "top_target": self.min_size_label},
        )

        self.max_size_label = UILabel(
            pygame.Rect((UIFlag.start_x, UIFlag.spacing), (200, 20)),
            "Max Size:",
            ui_manager,
            container,
            anchors={"top": "top", "top_target": self.min_size_slider},
            object_id=ObjectID(class_id="@setting_indicator"),
        )

        self.max_size_slider = UIHorizontalSlider(
            pygame.Rect((UIFlag.start_x, UIFlag.spacing), (235, 25)),
            10,
            (2, ParticleFlag.default_max_size),
            ui_manager,
            container,
            anchors={"top": "top", "top_target": self.max_size_label},
        )

        self.min_speed_label = UILabel(
            pygame.Rect((UIFlag.start_x, UIFlag.separator_spacing), (200, 20)),
            "Min Speed:",
            ui_manager,
            container,
            anchors={"top": "top", "top_target": self.max_size_slider},
            object_id=ObjectID(class_id="@setting_indicator"),
        )

        self.min_speed_slider = UIHorizontalSlider(
            pygame.Rect((UIFlag.start_x, UIFlag.spacing), (235, 25)),
            1,
            (1, ParticleFlag.default_max_speed - 1),
            ui_manager,
            container,
            anchors={"top": "top", "top_target": self.min_speed_label},
        )

        self.max_speed_label = UILabel(
            pygame.Rect((UIFlag.start_x, UIFlag.spacing), (200, 20)),
            "Max Speed:",
            ui_manager,
            container,
            anchors={"top": "top", "top_target": self.min_speed_slider},
            object_id=ObjectID(class_id="@setting_indicator"),
        )

        self.max_speed_slider = UIHorizontalSlider(
            pygame.Rect((UIFlag.start_x, UIFlag.spacing), (235, 25)),
            20,
            (2, ParticleFlag.default_max_speed),
            ui_manager,
            container,
            anchors={"top": "top", "top_target": self.max_speed_label},
        )
