from dataclasses import dataclass

import pygame

from particlesimulation.constants import *


@dataclass
class GameFlag:
    is_running = True
    is_paused = False
    is_video_running = False
    is_video_loaded = True
    max_frame_rate = 120
    current_video_frame = 0
    video_loading_progress = 0


@dataclass
class UIFlag:
    spacing = 2
    bt_spacing = 5
    separator_spacing = 15
    particle_bt_width, particle_bt_height = PARTICLE_BT_SIZE
    mini_player_width = (particle_bt_width * 4) + (3 * bt_spacing)
    mini_player_height = mini_player_width * (3 / 4)
    start_x = 0
    start_y = 0
    current_type = "circle"
    current_color = pygame.Color(BASE_COLOR)
    default_min_fade = 100
    default_max_fade = 800
    default_max_size = 200
    default_max_speed = 500
