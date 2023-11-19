import pygame
from abc import ABCMeta


class Entity(pygame.sprite.Sprite, metaclass=ABCMeta):
    def __init__(self, image_path, x_y, scale_size):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, scale_size)
        
        self.rect = self.image.get_rect(topleft=x_y)

    def update(self):
        pass
