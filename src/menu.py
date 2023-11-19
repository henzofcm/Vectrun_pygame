import pygame
from entity import *

class Menu(Entity):
    def __init__(self, image_path, x_y, scale_size):
        super().__init__(image_path, x_y, scale_size)
        
