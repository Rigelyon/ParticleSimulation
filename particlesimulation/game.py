import sys

import pygame

from settings import *


class Game:
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.is_running = True

    def update(self, dt):
        pass

    def quit(self):
        pygame.quit()
        sys.exit()

    def loop(self):
        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                    self.quit()
