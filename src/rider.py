import pygame
import math
from abc import ABCMeta
from entity import *
from config import *

class Rider(Entity, metaclass=ABCMeta):
    def __init__(self, number, x_y, scale_size, deck):
        # Carrega texturas diferentes dependendo do nº do jogador
        archive = "rider_" + str(number) + ".png"

        # Cria o rider e centraliza sua possição
        super().__init__("assets/textures/" + archive, x_y, scale_size)
        self.rect = self.image.get_rect(center=x_y)

        # Atributos adicionais
        self._number = number
        self._path = [x_y, x_y]
        self._velocity = 1 / 2
        self._temp_x = self.rect.centerx
        self._temp_y = self.rect.centery

        # Salva a mão de cartas do jogador
        self._hand = pygame.sprite.Group()

        for foo in range(3):
            card = deck.draw_card()
            card.rect.topleft = (GRID_X + 50, GRID_Y / 2- 55 + foo * 125)

            self._hand.add(card)

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

    def update(self):
        self._hand.update()

        return

    def update_choice(self, card, time):
        # Diferença que a moto deverá andar
        delta_x = card.value[0]
        delta_y = card.value[1]

        # Reinicia a posição em cada nova animação
        if time == 0:
            self._temp_x = self.rect.centerx
            self._temp_y = self.rect.centery

        # Valores temporários para não perder precisão no movimento
        self._temp_x = self._temp_x + time * delta_x / self._velocity
        self._temp_y = self._temp_y - time * delta_y / self._velocity

        # Atualiza a posição (e converte para inteiro)
        self.rect.centerx = round(self._temp_x)
        self.rect.centery = round(self._temp_y)

        #self._path.append(self.rect.center)


class Bot(Rider):
    pass
