import pygame
from pygame import Event
from pygame_gui.elements import (
    UIHorizontalSlider,
    UILabel,
    UIButton,
    UIScrollingContainer,
)
from pygame_gui.core import ObjectID

from particlesimulation.constants import *


class UI:
    def __init__(self, ui_manager):
        self.font_normal = pygame.font.SysFont(None, 22)

        self.spacing = 2
        self.bt_spacing = 5
        self.separator_spacing = 15
        self.start_x = 0
        self.start_y = 0
        self.size_x, self.size_y = PARTICLE_BT_SIZE
        self.max_size = 200
        self.max_speed = 500

        self.draw_container(ui_manager)
        self.draw_components(ui_manager, self.scroll_container)

        # TODO:
        #   - Color picker
        #   - Play button
        #   - Pause button
        #   - Clear button
        #   - Apple button
        #   - Use dropdown instead of buttons(?)
        #   - Try to use horizontal scroll container

    def enforce_slider_limit(self):
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

    def draw_container(self, ui_manager):
        self.scroll_container = UIScrollingContainer(
            pygame.Rect(
                (SCREENX_RIGHT + SCREEN_SPACING, SCREENY_TOP), (265, SCREEN_HEIGHT)
            ),
            manager=ui_manager,
            allow_scroll_x=False,
        )

    def draw_components(self, ui_manager, container):
        self.particle_count_label = UILabel(
            pygame.Rect((SCREENX_LEFT, SCREENY_BOTTOM + SCREEN_SPACING), (300, 20)),
            "Particle(s) count:",
            ui_manager,
            object_id=ObjectID(class_id="@debug_text"),
        )

        self.frame_label = UILabel(
            pygame.Rect((SCREENX_LEFT, self.spacing), (300, 20)),
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
            pygame.Rect((self.start_x, self.start_y), PARTICLE_BT_SIZE),
            "Circle",
            ui_manager,
            container,
            object_id=ObjectID(class_id="@particle_button"),
        )
        self.snow_bt = UIButton(
            pygame.Rect((self.bt_spacing, self.start_y), PARTICLE_BT_SIZE),
            "Snow",
            ui_manager,
            container,
            anchors={"left": "left", "left_target": self.circle_bt},
            object_id=ObjectID(class_id="@particle_button"),
        )
        self.leaves_bt = UIButton(
            pygame.Rect((self.bt_spacing, self.start_y), PARTICLE_BT_SIZE),
            "Leaves",
            ui_manager,
            container,
            anchors={"left": "left", "left_target": self.snow_bt},
            object_id=ObjectID(class_id="@particle_button"),
        )
        self.meteor_bt = UIButton(
            pygame.Rect((self.bt_spacing, self.start_y), PARTICLE_BT_SIZE),
            "Meteor",
            ui_manager,
            container,
            anchors={"left": "left", "left_target": self.leaves_bt},
            object_id=ObjectID(class_id="@particle_button"),
        )
        self.firefly_bt = UIButton(
            pygame.Rect((self.start_x, self.bt_spacing), PARTICLE_BT_SIZE),
            "Firefly",
            ui_manager,
            container,
            anchors={"top": "top", "top_target": self.circle_bt},
            object_id=ObjectID(class_id="@particle_button"),
        )
        self.rain_bt = UIButton(
            pygame.Rect((self.bt_spacing, self.bt_spacing), PARTICLE_BT_SIZE),
            "Rain",
            ui_manager,
            container,
            anchors={
                "top": "top",
                "left": "left",
                "top_target": self.snow_bt,
                "left_target": self.firefly_bt,
            },
            object_id=ObjectID(class_id="@particle_button"),
        )
        self.sakura_bt = UIButton(
            pygame.Rect((self.bt_spacing, self.bt_spacing), PARTICLE_BT_SIZE),
            "Sakura",
            ui_manager,
            container,
            anchors={
                "top": "top",
                "left": "left",
                "top_target": self.leaves_bt,
                "left_target": self.rain_bt,
            },
            object_id=ObjectID(class_id="@particle_button"),
        )
        self.stars_bt = UIButton(
            pygame.Rect((self.bt_spacing, self.bt_spacing), PARTICLE_BT_SIZE),
            "Stars",
            ui_manager,
            container,
            anchors={
                "top": "top",
                "left": "left",
                "top_target": self.meteor_bt,
                "left_target": self.sakura_bt,
            },
            object_id=ObjectID(class_id="@particle_button"),
        )
        self.multiplier_label = UILabel(
            pygame.Rect((self.start_x, self.separator_spacing), (200, 20)),
            "Multiplier:",
            ui_manager,
            container,
            anchors={"top": "top", "top_target": self.firefly_bt},
            object_id=ObjectID(class_id="@setting_indicator"),
        )

        self.multiplier_slider = UIHorizontalSlider(
            pygame.Rect((self.start_x, self.spacing), (235, 25)),
            1,
            (1, 100),
            ui_manager,
            container,
            anchors={"top": "top", "top_target": self.multiplier_label},
        )

        self.lifetime_label = UILabel(
            pygame.Rect((self.start_x, self.spacing), (200, 20)),
            "Lifetime:",
            ui_manager,
            container,
            anchors={"top": "top", "top_target": self.multiplier_slider},
            object_id=ObjectID(class_id="@setting_indicator"),
        )

        self.lifetime_slider = UIHorizontalSlider(
            pygame.Rect((self.start_x, self.spacing), (235, 25)),
            1,
            (1, 100),
            ui_manager,
            container,
            anchors={"top": "top", "top_target": self.lifetime_label},
        )

        self.min_size_label = UILabel(
            pygame.Rect((self.start_x, self.separator_spacing), (200, 20)),
            "Min Size:",
            ui_manager,
            container,
            anchors={"top": "top", "top_target": self.lifetime_slider},
            object_id=ObjectID(class_id="@setting_indicator"),
        )

        self.min_size_slider = UIHorizontalSlider(
            pygame.Rect((self.start_x, self.spacing), (235, 25)),
            1,
            (1, self.max_size - 1),
            ui_manager,
            container,
            anchors={"top": "top", "top_target": self.min_size_label},
        )

        self.max_size_label = UILabel(
            pygame.Rect((self.start_x, self.spacing), (200, 20)),
            "Max Size:",
            ui_manager,
            container,
            anchors={"top": "top", "top_target": self.min_size_slider},
            object_id=ObjectID(class_id="@setting_indicator"),
        )

        self.max_size_slider = UIHorizontalSlider(
            pygame.Rect((self.start_x, self.spacing), (235, 25)),
            10,
            (2, self.max_size),
            ui_manager,
            container,
            anchors={"top": "top", "top_target": self.max_size_label},
        )

        self.min_speed_label = UILabel(
            pygame.Rect((self.start_x, self.separator_spacing), (200, 20)),
            "Min Speed:",
            ui_manager,
            container,
            anchors={"top": "top", "top_target": self.max_size_slider},
            object_id=ObjectID(class_id="@setting_indicator"),
        )

        self.min_speed_slider = UIHorizontalSlider(
            pygame.Rect((self.start_x, self.spacing), (235, 25)),
            1,
            (1, self.max_speed - 1),
            ui_manager,
            container,
            anchors={"top": "top", "top_target": self.min_speed_label},
        )

        self.max_speed_label = UILabel(
            pygame.Rect((self.start_x, self.spacing), (200, 20)),
            "Max Speed:",
            ui_manager,
            container,
            anchors={"top": "top", "top_target": self.min_speed_slider},
            object_id=ObjectID(class_id="@setting_indicator"),
        )

        self.max_speed_slider = UIHorizontalSlider(
            pygame.Rect((self.start_x, self.spacing), (235, 25)),
            20,
            (2, self.max_speed),
            ui_manager,
            container,
            anchors={"top": "top", "top_target": self.max_speed_label},
        )

    def draw_screen(self):
        self.screen_surf = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        pygame.draw.rect(self.screen_surf, BASE_COLOR, screen_rect, width=2)

    def surface_blit(self, surface):
        surface.blit(self.screen_surf, (SCREENX_LEFT, SCREENY_TOP))
