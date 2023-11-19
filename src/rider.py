import pygame
from entity import *

class Rider(Entity):
    def __init__(self, number, x_0, y_0):
        # Carrega texturas diferentes dependendo do nº do jogador
        archive = "rider_" + str(number) + ".png"

        # Cria o rider, diminui a imagem e centraliza sua possição
        super().__init__("assets/textures/" + archive, (x_0, y_0))
        self._image = pygame.transform.scale(self._image, (50, 25))
        self._rect = self._image.get_rect(center=(x_0, y_0)) 

        # Atributos adicionais
        self._number = number
        self._path = [(0, 0)]

class Player(Rider):
    def __init___(self, number, x_0, y_0):
        super().__init__(number, x_0, y_0)

class Bot(Rider):
    pass
