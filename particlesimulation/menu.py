import pygame

from particlesimulation.settings import *


class Menu:
    def __init__(self):
        self.screen = pygame.Rect(20, 20, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.font_normal = pygame.font.SysFont(None, 22)

    def draw_text(self, surface, text, pos, justification: ('midleft', 'midright'), font, color):
        text = font.render(text, 1, color)
        text_rect = (text.get_rect())
        match justification:
            case 'midleft':
                text_rect.midleft = pos
            case 'midright':
                text_rect.midright = pos
        surface.blit(text, text_rect)

    def draw_menu(self, surface):
        # Draw screen border
        pygame.draw.rect(surface, BASE_COLOR, self.screen, width=2)
