import pygame

class Input:
    def __init__(self):
        self.mouse_x = 0
        self.mouse_y = 0

    def get_mouse_pos(self) -> tuple:
        pos = pygame.mouse.get_pos()
        return pos

