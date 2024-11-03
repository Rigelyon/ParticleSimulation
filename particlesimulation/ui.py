import pygame

from particlesimulation.constants import *


class UI:
    def __init__(self):
        self.font_normal = pygame.font.SysFont(None, 22)

    def draw_button(self, surface, text, pos):
        pass

    def draw_text(self, surface, text, pos, justification: ('midleft', 'midright'), font, color):
        text = font.render(text, 1, color)
        text_rect = (text.get_rect())
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

    def blit(self, surface):
        surface.blit(self.screen_surf, (SCREENX_LEFT, SCREENY_TOP))
