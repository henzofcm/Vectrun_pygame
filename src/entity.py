import pygame
from abc import ABCMeta


class Entity(pygame.sprite.Sprite, metaclass=ABCMeta):
    def __init__(self, image_path, x_0, y_0):
        super().__init__(self)
        self._image = pygame.image.load(image_path).convert_alpha()
        self._rect = self._image.get_rect()

    def update(self):
        pygame.blit(self._image)
