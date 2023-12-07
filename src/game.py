import pygame
import sys

from entity import *
from rider import *
from deck import *
import utilities
from config import *


class Grid_Game(Entity):
    def __init__(self, image_path, x_y, scale_size, bot_number):
        super().__init__(image_path, x_y, scale_size)

        # Atributos para o estado do jogo
        self.next_menu = "none"
        self._game_turn = 0
        self._mov_stage = -1

        # Timer interno e holders pra quando o jogador clicar na carta
        self._timer = 0
        self._clicked = False
        self._clicked_card = None
        self._player_target = (0, 0)

        # Cria o deck
        self._deck = Deck(TEXTURE_PATH + "cards/", (CARD_X, CARD_Y))

        # Cria o jogador
        self._player = Player(1, (GRID_X / 2 - 2, GRID_Y / 2 - 2), (RIDER_X, RIDER_Y), self._deck)
        self._player = pygame.sprite.GroupSingle(self._player)

        # Cria os bots
        __bot_list = []

        for bot in range(bot_number):
            __bot_list.append(Bot(bot + 2, (GRID_X / 2 - 45, GRID_Y / 2 - 45), (RIDER_X, RIDER_Y), self._deck))

        self._bots = pygame.sprite.Group(__bot_list)

        # Grupo com todos personagens animados (bots e player)
        self._all_riders = pygame.sprite.Group((self._player.sprite), self._bots.sprites())

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
                    self.__validate_click()

        # Desenha o tabuleiro no layer mais baixo
        screen.blit(self.image, self.rect)

        # Desenha o contorno e as cartas
        if self._player.sprite:
            self.choice_preview(screen)
            self._player.sprite._hand.draw(screen)

        # Se tiver clicado, roda o movimento do jogador ou dos bots
        if self._clicked and self._all_riders:
            self.move_player(self._all_riders.sprites()[self._mov_stage])

        # Desenha as linhas dos riders
        for rider in self._all_riders.sprites():
            rider.line = pygame.draw.lines(screen, rider._color, False, rider._path + [rider.rect.center], width=6)

        # Verifica colisões
        if self._all_riders:
            self.check_collision()

        return False

    def draw(self, screen):
        # Faz blit no jogador e nos bots
        self._player.draw(screen)
        self._bots.draw(screen)

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
        pygame.draw.line(screen, self._player.sprite._color, start, end, width = 4)

    def __validate_click(self):
        # Verifica em qual carta clicou
        player_card = self.__card_clicked()

        # Se tiver clicado, prepara o movimento do player
        if player_card:
            self._clicked = True
            self.__next_player_movement(player_card)

    def __card_clicked(self):
        # Se o jogador clicar na carta, _clicked = True
        for card in self._player.sprite._hand.sprites():
            if card.update():
                return card
            
        return None
            
    def move_player(self, rider):
        # Atualiza as variáveis __temp_player
        self.__set_temp_variables(rider)

        # Move o jogador de acordo com essa desigualdade (quase sempre satisfeita)
        if self.__temp_player_center[0] + 2 < self.__temp_player_target[0]:
            rider.update_choice(self._clicked_card, self._timer)
        
            self._timer += 0.05

        # No caso não-tão-raro de vetores (0, y), move o jogador de acordo
        elif self._clicked_card.value[0] == 0 and self.__temp_player_center[1] + 2 < self.__temp_player_target[1]:
            rider.update_choice(self._clicked_card, self._timer)
        
            self._timer += 0.05
        
        # Se ficou parado, reseta o movimento
        else:
            self.__reset_player_movement(rider)
            self.__next_player_movement()

    def __set_temp_variables(self, rider):
        # Variáveis temporárias para não duplicar o código depois
        self.__temp_player_center = rider.rect.center
        self.__temp_player_target = self._player_target

        # Dependendo do valor da carta, muda a coordenada relativa
        if self._clicked_card.value[0] < 0:
            self.__temp_player_center = (-self.__temp_player_center[0], self.__temp_player_center[1])
            self.__temp_player_target = (-self.__temp_player_target[0], self.__temp_player_target[1])

        if self._clicked_card.value[1] > 0:
            self.__temp_player_center = (self.__temp_player_center[0], -self.__temp_player_center[1])
            self.__temp_player_target = (self.__temp_player_target[0], -self.__temp_player_target[1])

    def __reset_player_movement(self, rider):
        # Retorna _timer para 0
        self._timer = 0

        # Pesca uma nova carta e adiciona à mão do rider
        card = self._deck.draw_card()
        card.rect.topleft = self._clicked_card.rect.topleft

        rider._hand.add(card)

        # Remove a carta usada do rider e limpa _clicked_card
        rider._hand.remove(self._clicked_card)
        self._clicked_card = None

        # Salva a posição final do jogador no seu _path
        rider._path.append(rider.rect.center)

    def __next_player_movement(self, card=None):
        self._mov_stage += 1

        # Se todos jogadores tiverem se movimentado, acaba o turno
        if self._mov_stage == len(self._all_riders):
            self._game_turn += 1
            self._mov_stage = -1
            self._clicked = False

            return

        # Caso contrário, prepara o jogo para rodar mais uma animação
        next_player = self._all_riders.sprites()[self._mov_stage]

        # Se não tiver passado uma carta, faz o rider escolher (em geral um bot)
        if not card:
            card = next_player.choose_card(self._all_riders)

        self._clicked_card = card

        self._player_target = next_player._path[-1]
        self._player_target = (card.value[0] * DISTANCE + self._player_target[0], -card.value[1] * DISTANCE + self._player_target[1])

    def check_collision(self):
        # Laceia todos jogadores
        for rider in self._all_riders.sprites():
            # Morrem se colidirem com a fronteira
            if utilities.check_border_collision(rider.rect.center):
                rider.kill()

            # Morrem se alguém passar na linha dos outros
            if utilities.check_line_cross(self._all_riders, rider):
                rider.kill()

        # Verifica se colidiram entre si
        #utilities.check_riders_collision(self._player, self._bots)

