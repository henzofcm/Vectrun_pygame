import pygame
import random

from entity import *
import utilities
from config import *

class Rider(Entity):
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

    def update_choice(self, card, time):
        # Diferença que a moto deverá andar
        delta_x = card.value[0]
        delta_y = card.value[1]

        # Reinicia a posição em cada nova animação
        if time == 0:
            self.__temp_x = self.rect.centerx
            self.__temp_y = self.rect.centery

        # Valores temporários para não perder precisão no movimento
        self.__temp_x = self.__temp_x + time * delta_x / self._velocity
        self.__temp_y = self.__temp_y - time * delta_y / self._velocity

        # Atualiza a posição (e converte para inteiro)
        self.rect.centerx = round(self.__temp_x)
        self.rect.centery = round(self.__temp_y)


class Player(Rider):
    def __init___(self, number, x_y, scale_size):
        super().__init__(number, x_y, scale_size)

        # Cria um grupo para as cartas, que serão desenhadas no grid_game
        self._hand = pygame.sprite.Group(self._hand)

class Bot(Rider):
    def __init___(self, number, x_y, scale_size):
        super().__init__(number, x_y, scale_size)

    def choose_card(self, all_riders):
        choices = []

        # Laceia cada carda e decide se o movimento é válido ou não
        for card in self._hand.sprites():
            # Se for, adiciona à lista choices
            if self.__preview_movement(card, all_riders):
                choices.append(card)

        # Se algum for válido, retorna um entre eles
        if choices:
            return random.choice(choices)
        # Se não houver nenhum, qualquer carta da mão valerá
        else:
            return random.choice(self._hand.sprites())
        
    def __preview_movement(self, card, all_riders):
        # Pega o ponto inicial e final do vetor
        start = self._path[-1]
        end = (start[0] + card.value[0] * DISTANCE, start[1] - card.value[1] * DISTANCE)

        # Se for colidir com as fronteiras retorna
        if utilities.check_border_collision(end):
            return False
        
        # Sprite temporário na posição futura
        future_self = pygame.sprite.Sprite()
        future_self.rect = pygame.rect.Rect((0, 0), self.rect.size)
        future_self.rect.center = end
        future_self._path = self._path

        # Se for colidir com as linhas de outrem retorna
        if utilities.check_line_cross(all_riders, future_self):
            return False
        
        # Se não colidir com nada, a carta é válida
        return True

