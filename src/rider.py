import pygame
from entity import *


class Rider(Entity):
    def __init__(self, number, x_y, scale_size):
        # Carrega texturas diferentes dependendo do nº do jogador
        archive = "rider_" + str(number) + ".png"

        # Cria o rider, diminui a imagem e centraliza sua possição
        super().__init__("assets/textures/" + archive, x_y, scale_size)
        self.rect = self.image.get_rect(center=x_y)

        # Atributos adicionais
        self._number = number
        self._path = [x_y, x_y]
        self._velocity = 1

        # Salva a cor da moto
        if number == 1:
            self._color = "#258dc2"
        elif number == 2:
            self._color = "#ec6716"
        elif number == 3:
            self._color = "#cb101a"
        elif number == 4:
            self._color = "#ffb001"


class Player(Rider):
    def __init___(self, number, x_y, scale_size):
        super().__init__(number, x_y, scale_size)

    def update(self, vector, time):
        # Calcula a posição inicial e final no tabuleiro
        start = self._path[-1]
        end = (start[0] + vector[0], start[1] + vector[1])

        # Diferença que a moto deverá andar
        delta_x = end[0] - start[0]
        delta_y = end[1] - start[1]

        # Atualiza a posição
        self.rect.centerx = self.rect.centerx + delta_x * time / self._velocity
        self.rect.centery = self.rect.centery + delta_y * time / self._velocity

        self._path.append(self.rect.center)
        
        # Debugger
        print(f"Choice updated for {self._color}: {self.rect.center}")


class Bot(Rider):
    pass
