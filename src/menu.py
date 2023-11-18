import pygame
from entity import *

class Menu(Entity):
    def __init__(self, image_path, x_y, WIDTH, HEIGHT):
        super().__init__(image_path, x_y)

        # Transforms it so it fills the screen
        self._image = pygame.transform.scale(self._image, (WIDTH, HEIGHT))

class Grid_Game(Menu):
        def __init__(self, image_path, x_y, WIDTH, HEIGHT):
            super().__init__(image_path, x_y, WIDTH, HEIGHT)
        
        
