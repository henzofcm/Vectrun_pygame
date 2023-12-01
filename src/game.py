import pygame
import sys

from entity import *
from rider import *
from deck import *
from config import *


class Grid_Game(Entity):
    def __init__(self, image_path, x_y, scale_size, bot_number):
        super().__init__(image_path, x_y, scale_size)

        # Timer interno e um holder pra quando o jogador clicar na carta
        self._timer = 0
        self._clicked = False
        self._clicked_card = None
        self._player_target = (0, 0)

        # Cria o deck
        self._deck = Deck(TEXTURE_PATH + "cards/", (CARD_X, CARD_Y))

        # Cria o jogador
        self._player = Player(1, (GRID_X / 2, GRID_Y / 2), (RIDER_X, RIDER_Y), self._deck)
        self._player = pygame.sprite.GroupSingle(self._player)

        # Cria os bots
        __bot_list = []

        for bot in range(bot_number):
            __bot_list.append(Player(bot + 2, (GRID_X / 2 - 45, GRID_Y / 2 - 45), (RIDER_X, RIDER_Y), self._deck))

        self._bots = pygame.sprite.Group(__bot_list)

    def update(self, screen):
        # Eventos principais deste menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self._clicked:
                    self.__card_clicked()

        # Desenha o contorno das cartas
        self.choice_preview(screen)

        # Se tiver clicado, roda o movimento do jogador
        if self._clicked:
            self.move_player()

    def choice_preview(self, screen):
        # Verifica se o mouse está em cima da carta
        for card in self._player.sprite._hand.sprites():
            if card.update():
                # Desenha o contorno
                self.__preview_selected_card(card, screen)
                
                # Se não houver clicado antes, mostra a trajetória da carta
                if not self._clicked:
                    self.__preview_selected_path(card, screen)

    @staticmethod
    def __preview_selected_card(card, screen):
        # Desenha o contorno da carta selecionada
        rect_pos = (card.rect.left - CARD_SELECTED_WIDTH, card.rect.top - CARD_SELECTED_WIDTH)
        rect_size = (card.rect.width + 2 * CARD_SELECTED_WIDTH, card.rect.height + 2 * CARD_SELECTED_WIDTH)

        rectangle = pygame.Rect(rect_pos, rect_size)

        pygame.draw.rect(screen, "#258dc2", rectangle, width=2 * CARD_SELECTED_WIDTH)

    def __preview_selected_path(self, card, screen):
        # Pega o ponto inicial e final da reta
        start = self._player.sprite._path[-1]
        end = (start[0] + card.value[0] * DISTANCE, start[1] - card.value[1] * DISTANCE)

        # Desenha a linha
        pygame.draw.line(screen, self._player.sprite._color, start, end, width = 6)

    def __card_clicked(self):
        # Se o jogador clicar na carta, _clicked = True
        for card in self._player.sprite._hand.sprites():
            if card.update():
                self._clicked = True
                self._clicked_card = card

                # CÓDIGO RUIM, MUDAR PRO PLAYER DEPOIS (ou não)
                self._player_target = self._player.sprite._path[-1]
                self._player_target = (card.value[0] * DISTANCE + self._player_target[0], -card.value[1] * DISTANCE + self._player_target[1])

    def __set_temp_variables(self):
            # Variáveis temporárias para não duplicar o código depois
            self.__temp_player_center = self._player.sprite.rect.center
            self.__temp_player_target = self._player_target

            # Dependendo do valor da carta, muda a coordenada relativa
            if self._clicked_card.value[0] < 0:
                self.__temp_player_center = (-self.__temp_player_center[0], self.__temp_player_center[1])
                self.__temp_player_target = (-self.__temp_player_target[0], self.__temp_player_target[1])

            if self._clicked_card.value[1] > 0:
                self.__temp_player_center = (self.__temp_player_center[0], -self.__temp_player_center[1])
                self.__temp_player_target = (self.__temp_player_target[0], -self.__temp_player_target[1])

    def move_player(self):
        # Atualiza as variáveis __temp_player
        self.__set_temp_variables()

        # Move o jogador de acordo com essa desigualdade (quase sempre satisfeita)
        if self.__temp_player_center[0] < self.__temp_player_target[0]:
            self._player.sprite.update_choice(self._clicked_card, self._timer)
        
            self._timer += 0.05

        # No caso não-tão-raro de vetores (0, y), move o jogador de acordo
        elif self._clicked_card.value[0] == 0 and self.__temp_player_center[1] < self.__temp_player_target[1]:
            self._player.sprite.update_choice(self._clicked_card, self._timer)
        
            self._timer += 0.05
        
        # Se ficou parado, reseta o movimento
        else:
            self.__reset_player_movement()

    def __reset_player_movement(self):
         # Retorna _timer e _clicked pra 0
        self._timer = 0
        self._clicked = False

        # Pesca uma nova carta e adiciona à mão do player
        card = self._deck.draw_card()
        card.rect.topleft = self._clicked_card.rect.topleft

        self._player.sprite._hand.add(card)

        # Remove a carta usada do player e limpa _clicked_card
        self._player.sprite._hand.remove(self._clicked_card)
        self._clicked_card = None