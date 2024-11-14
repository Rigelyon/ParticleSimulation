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
class ParticleFlag:
    # Default value
    default_min_fade = 50
    default_max_fade = 1000
    default_min_size = 1
    default_max_size = 200
    default_min_speed = 1
    default_max_speed = 500

    # Current Value
    current_type = "circle"
    current_multiplier = 1
    current_color = pygame.Color(BASE_COLOR)
    current_min_fade = default_min_fade
    current_max_fade = default_max_fade
    current_min_size = default_min_size
    current_max_size = default_max_size
    current_min_speed = default_min_speed
    current_max_speed = default_max_speed


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
