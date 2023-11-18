import pygame
from abc import ABCMeta


class Entity(pygame.sprite.Sprite, metaclass=ABCMeta):
    def __init__(self, image_path, x_y):
        super().__init__()
        self._image = pygame.image.load(image_path).convert_alpha()
        self._rect = self._image.get_rect(topleft=x_y)

    def update(self):
        pass
