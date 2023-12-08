import pygame
import random

from entity import *
import utilities
from config import *

class Rider(Entity):
    def __init__(self, number, x_y, scale_size, deck):
        # Carrega texturas diferentes dependendo do nº do jogador
        archive = "rider_" + str(number) + ".png"

        # Cria o rider e centraliza sua posição
        super().__init__("assets/textures/" + archive, x_y, scale_size)
        self.rect = self.image.get_rect(center=x_y)

        # Máscara para ter colisões mais precisas
        self.mask = pygame.rect.Rect(x_y, (RIDER_X / 5 - 2, RIDER_Y / 5 - 1))

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

        # Atributos de estado
        self.__timer = 0
        self.state_alive = True
        self.clicked_card = None
        self._last_card = (0, 0)

    def update(self, deck):
        # Roda animação de movimento se estiver vivo
        if self.state_alive:
            return self.move_rider(deck)
        # E animação de morte caso contrário
        else:
            pass

    def move_rider(self, deck):
        self.__set_temp_variables()

        # Move o jogador de acordo com essa desigualdade (quase sempre satisfeita)
        if self.__temp_player_center[0] + 2 < self.__temp_player_target[0]:
            self.__change_move(self.clicked_card, self.__timer)
        
            self.__timer += 0.05
        # No caso não-tão-raro de vetores (0, y), move o jogador de acordo
        elif self.clicked_card[0] == 0 and self.__temp_player_center[1] + 2 < self.__temp_player_target[1]:
            self.__change_move(self.clicked_card, self.__timer)
        
            self.__timer += 0.05
        # Se ficou parado, reseta o movimento
        else:
            self.__reset_movement(deck)
            return False
        
        return True

    def __change_move(self, card, time):
        # Diferença que a moto deverá andar
        delta_x = card[0]
        delta_y = card[1]

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
        self.mask.center = self.rect.center

    def __set_temp_variables(self):
        # Variáveis temporárias que poupam código no movimento
        self.__temp_player_center = self.rect.center
        self.__temp_player_target = self.__player_target

        # Dependendo do valor da carta, muda a coordenada relativa
        if self.clicked_card[0] < 0:
            self.__temp_player_center = (-self.__temp_player_center[0], self.__temp_player_center[1])
            self.__temp_player_target = (-self.__temp_player_target[0], self.__temp_player_target[1])

        if self.clicked_card[1] > 0:
            self.__temp_player_center = (self.__temp_player_center[0], -self.__temp_player_center[1])
            self.__temp_player_target = (self.__temp_player_target[0], -self.__temp_player_target[1])

    def __reset_movement(self, deck):
        # Retorna _timer para 0
        self.__timer = 0

        # Pesca uma nova carta e adiciona à mão
        card = deck.draw_card()
        card.rect.topleft = self.clicked_card.rect.topleft

        self._hand.add(card)

        # Remove a carta usada e limpa _clicked_card
        self._hand.remove(self.clicked_card)
        self._last_card = self.clicked_card
        self.clicked_card = (0, 0)

        # Salva a posição final do jogador no seu _path
        self._path.append(self.rect.center)

    def select_card(self, card):
        self.clicked_card = card

        self.__player_target = self._path[-1]
        self.__player_target = (card[0] * DISTANCE + self.__player_target[0], -card[1] * DISTANCE + self.__player_target[1])

@utilities.Singleton
class Player():
    def __init__(self, number, x_y, scale_size, deck):
        # Cria um envoltório entorno de um Rider
        self.__wrapper = Rider(number, x_y, scale_size, deck)
        self.__wrapper = pygame.sprite.GroupSingle(self.__wrapper)

    def __getattr__(self, attrvalue):
        # Pega o atributo do sprite e não do grupo
        return getattr(self.__wrapper.sprite, attrvalue)
    
    def __bool__(self):
        # Retorna o booleano do SingleGroup
        return bool(self.__wrapper)
    
    def sprite(self):
        # Retorna o sprite do SingleGroup
        return self.__wrapper.sprite
        
    def update(self):
        # Atualiza o SingleGroup
        return self.__wrapper.update()

    def draw(self, screen):
        # Desenha o SingleGroup
        return self.__wrapper.draw(screen)

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
        end = (start[0] + card[0] * DISTANCE, start[1] - card[1] * DISTANCE)

        # Se for colidir com as fronteiras retorna
        if utilities.check_border_collision(end):
            return False
        
        # Sprite temporário na posição futura
        future_self = pygame.sprite.Sprite()
        future_self.rect = pygame.rect.Rect((0, 0), self.rect.size)
        future_self.rect.center = end
        future_self._path = self._path
        future_self._last_card = self._last_card
        future_self.mask = self.mask

        # Se for colidir com as linhas de outrem retorna
        if utilities.check_line_cross(all_riders, future_self, card):
            return False
        
        # Se não colidir com nada, a carta é válida
        return True

