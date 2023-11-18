import pygame
from entity import *

class Menu(Entity):
    def __init__(self, image_path, x_y, width, height):
        super().__init__(image_path, x_y)

        # Transforma a imagem pro tamanho (width, height)
        self._image = pygame.transform.scale(self._image, (width, height))

class Grid_Game(Menu):
        def __init__(self, image_path, x_y, width, height):
            super().__init__(image_path, x_y, width, height)
        
        
