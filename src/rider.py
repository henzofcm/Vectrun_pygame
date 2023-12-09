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
        super().__init__(RIDER_PATH + archive, x_y, scale_size)
        self.rect = self.image.get_rect(center=x_y)

        # Atributos adicionais
        self._number = number
        self._path = [x_y, x_y]
        self.__velocity = 1 / 2
        self.__flipped = False

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
        self.clock = None

        # Máscaras para colisões mais precisas
        self.mask = pygame.rect.Rect(x_y, (RIDER_X / 5 - 2, RIDER_Y / 5 - 1))

        self.line_mask = self._get_line_mask(self._color, (-10, -10), (-10, -10))
        self._last_line_mask = self.line_mask

    def update(self):
        # Muda a imagem do rider dependendo do estágio da animação
        archive = "rider_dead_" + str(self.__death_stage) + ".png"

        self.last_image = pygame.image.load(RIDER_PATH + archive).convert_alpha()
        self.last_image = pygame.transform.scale(self.last_image, (RIDER_X, RIDER_Y))

        # Se estiver virada, atualiza de acordo
        if self.__flipped:
            self.last_image = pygame.transform.flip(self.last_image, True, False)

        self.__death_stage += 1

    def move_rider(self, deck, backward=False):
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
            # Se for retrógrado, reseta de maneira diferente
            if not backward:
                self.__reset_movement(deck)
            else:
                self.__reset_backward()
                del self._path[-1]
            
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
        self.__temp_x = self.__temp_x + time * delta_x / self.__velocity
        self.__temp_y = self.__temp_y - time * delta_y / self.__velocity

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

        # Cria uma mascára para a linha e a adiciona em line_mask
        temp_mask = self._get_line_mask(self._color, self._path[-2], self._path[-1])

        self._last_line_mask = self.line_mask.copy()
        self.line_mask.draw(temp_mask, (0, 0))

    @staticmethod
    def _get_line_mask(color,start, end):
        # Cria uma superfície em preto
        temp_surf = pygame.Surface((GRID_X, GRID_Y))
        temp_surf.set_colorkey((0, 0, 0))

        # Desenha a linha e retorna a máscara
        pygame.draw.line(temp_surf, color, start, end, width=6)
        return pygame.mask.from_surface(temp_surf)

    def select_card(self, card):
        # Seleciona a carta passada e define parametros internos do movimento
        self.clicked_card = card

        self.__player_target = self.rect.center
        self.__player_target = (card[0] * DISTANCE + self.__player_target[0], -card[1] * DISTANCE + self.__player_target[1])

        # Se a carta for contraria a anterior, gira o rider
        if self.clicked_card[0] * self._last_card[0] < 0:
            self.image = pygame.transform.flip(self.image, True, False)
            self.__flipped = not self.__flipped
        # No caso de ser o primeiro movimento, age de acordo
        elif self._last_card == (0, 0) and self.clicked_card[0] < 0:
            self.image = pygame.transform.flip(self.image, True, False)
            self.__flipped = not self.__flipped
            
    def update_death(self):
        # TODO: Quando acabar os eventos de clock, apaga a imagem do rider
        if self.__death_stage == 8:
            self.__remove_rider()

        # Remove parte da linha
        self.__remove_line()

        # Se tiver acabado as linhas, apaga o sprite
        if len(self._path) == 1:
            self.kill()
            return True
        
        return False

    def __remove_rider(self):
        # Esconde a imagem da animação
        self.last_image = pygame.Surface((1, 1))
        self.last_image.set_colorkey((0, 0, 0))

        self.__death_stage += 1

    def __remove_line(self):
        # Se não tiver uma carta, pega uma contrária à ultima linha
        if self.clicked_card is None:
            self.__get_last_vector()

        # E então a linha vai retroceder
        self.move_rider(self._hand, backward=True)

    def __get_last_vector(self):
        # Cria uma carta da diferença dos últimos pontos
        card = (self.rect.center[0] - self._path[-1][0], self.rect.center[1] - self._path[-1][1])
        card = (- card[0] / DISTANCE, card[1] / DISTANCE)

        # E a seleciona
        self.select_card(card)

    def __reset_backward(self):
        # Recomeça o tempo e a carta
        self.__timer = 0
        self.clicked_card = None

    def kill_rider(self):
        self.__reset_backward()

        # Muda o estado do rider
        self.state_alive = False
        self.clicked_card = None
        self.__death_stage = 0

        # Muda sua imagem na animação
        self.update()
        self.last_rect = self.rect.copy()

        # Esconde sua imagem atual
        self.image = pygame.Surface((1, 1))
        self.image.set_colorkey((0, 0, 0))

        # Cria um clock interno
        self.clock = pygame.USEREVENT + self._number
        pygame.time.set_timer(self.clock, 100, 7)


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

        # Cria uma máscara para testar colisões futuras desta linha
        line_mask = self._get_line_mask(self._color, start, end)

        # Se for colidir com as linhas de outrem retorna
        if utilities.check_line_cross(all_riders, self, line_mask, card):
            return False
        
        # Se for colidir com alguém também retorna
        temp_group = all_riders.copy()
        temp_group.remove(self)

        for enemy in temp_group:
            if utilities.check_riders_collision(self, enemy) and len(self._path) != 2:
                return False

        # Se não colidir com nada, a carta é válida
        return True

