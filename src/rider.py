import pygame
from entity import *


class Rider(Entity):
    def __init__(self, number, x_y, scale_size):
        # Carrega texturas diferentes dependendo do nº do jogador
        archive = "rider_" + str(number) + ".png"

        # Cria o rider, diminui a imagem e centraliza sua possição
        super().__init__("assets/textures/" + archive, x_y, scale_size)
        self._rect = self._image.get_rect(center=x_y)

        # Atributos adicionais
        self._number = number
        self._path = [(0, 0)]
        self._velocity = 1

        # Salva a cor da moto
        if number == 1:
            self._color = "blue"
        elif number == 2:
            self._color = "orange"
        elif number == 3:
            self._color = "red"
        elif number == 4:
            self._color = "yellow"


class Player(Rider):
    def __init___(self, number, x_y, scale_size):
        super().__init__(number, x_y, scale_size)

    def choice_preview(self, vector, screen):
        # Calcula posição inicial e final no tabuleiro
        start = self._path[-1]
        end = (start[0] + vector[0], start[1] + vector[1])

        # Desenha a linha ligando esses pontos
        pygame.draw.line(screen, self._color, start, end, width=2)

    def choice_update(self, vector):
        # Calcula a posição inicial e final no tabuleiro
        start = self._path[-1]
        end = (start[0] + vector[0], start[1] + vector[1])

        # Diferença que a moto deverá andar
        delta_x = end[0] - start[0]
        delta_y = end[1] - start[1]

        # Gerador que pausa a cada tempo (dt = 0.05)
        for time in range(0, delta_x / self._velocity, 0.05):
            self._rect.centerx = self._rect.centerx + delta_x * time / self._velocity
            self._rect.centery = self._rect.centery + delta_y * time / self._velocity

            yield self._rect.center

    def update(self, choice, vector):
        # Quando o jogador clicar na carta, choice será True
        if choice:
            self.choice_update(vector)
            self._path.append(self._rect.center)


class Bot(Rider):
    pass
