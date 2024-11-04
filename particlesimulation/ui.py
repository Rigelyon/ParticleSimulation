import pygame
from pygame_gui import UIManager
from pygame_gui.elements import UIHorizontalSlider, UILabel, UIButton

from particlesimulation.constants import *


class UI(UIManager):
    def __init__(self):
        super().__init__((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.font_normal = pygame.font.SysFont(None, 22)

        self.circle_particle_bt = UIButton(pygame.Rect((SCREENX_RIGHT + SCREEN_MARGIN, SCREENY_TOP), PARTICLE_BT_SIZE),
                                           'Circle', self)
        self.particle_bt2 = UIButton(
            pygame.Rect((SCREENX_RIGHT + SCREEN_MARGIN + PARTICLE_BT_SIZE[0], SCREENY_TOP), PARTICLE_BT_SIZE),
            'Circle', self)
        self.particle_bt3 = UIButton(
            pygame.Rect((SCREENX_RIGHT + SCREEN_MARGIN + PARTICLE_BT_SIZE[0] * 2, SCREENY_TOP), PARTICLE_BT_SIZE),
            'Circle', self)
        self.particle_bt4 = UIButton(
            pygame.Rect((SCREENX_RIGHT + SCREEN_MARGIN + PARTICLE_BT_SIZE[0] * 3, SCREENY_TOP), PARTICLE_BT_SIZE),
            'Circle', self)
        self.particle_bt5 = UIButton(
            pygame.Rect((SCREENX_RIGHT + SCREEN_MARGIN, SCREENY_TOP + PARTICLE_BT_SIZE[1]), PARTICLE_BT_SIZE),
            'Circle', self)
        self.particle_bt6 = UIButton(
            pygame.Rect((SCREENX_RIGHT + SCREEN_MARGIN + PARTICLE_BT_SIZE[0], SCREENY_TOP + PARTICLE_BT_SIZE[1]),
                        PARTICLE_BT_SIZE),
            'Circle', self)
        self.particle_bt7 = UIButton(
            pygame.Rect((SCREENX_RIGHT + SCREEN_MARGIN + PARTICLE_BT_SIZE[0] * 2, SCREENY_TOP + PARTICLE_BT_SIZE[1]),
                        PARTICLE_BT_SIZE),
            'Circle', self)
        self.particle_bt8 = UIButton(
            pygame.Rect((SCREENX_RIGHT + SCREEN_MARGIN + PARTICLE_BT_SIZE[0] * 3, SCREENY_TOP + PARTICLE_BT_SIZE[1]),
                        PARTICLE_BT_SIZE),
            'Circle', self)

        self.size_slider = UIHorizontalSlider(
            pygame.Rect((SCREENX_RIGHT + SCREEN_MARGIN, SCREENY_TOP + 30 + PARTICLE_BT_SIZE[1] * 2), (230, 25)), 1,
            (1, 100), self, anchors={'left': 'left', 'right': 'right'})

    def draw_button(self, surface, text, pos, size, color, color_hover, font, rect):
        button_rect = pygame.Rect(pos, size)
        mouse_pos = pygame.mouse.get_pos()

        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, color, button_rect)
        else:
            pygame.draw.rect(surface, color_hover, button_rect)

        text = font.render(text, 1, color)
        text_rect = text.get_rect()
        surface.blit(text, text_rect)

        # icon_rect = icon.get_rect(center=rect.center)
        # surface.blit(icon, icon_rect)

    def draw_text(self, surface, text, pos, justification: ('midleft', 'midright'), font, color):
        text = font.render(text, 1, color)
        text_rect = text.get_rect()
        match justification:
            case 'midleft':
                text_rect.midleft = pos
            case 'midright':
                text_rect.midright = pos
        surface.blit(text, text_rect)

    def draw_screen(self):
        self.screen_surf = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        pygame.draw.rect(self.screen_surf, BASE_COLOR, screen_rect, width=2)

    def handle_events(self):
        pass

    def surface_blit(self, surface):
        surface.blit(self.screen_surf, (SCREENX_LEFT, SCREENY_TOP))
