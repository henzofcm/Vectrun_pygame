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
        self._where_to_go = (0, 0)

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

        # Desenha o contorno das cartas
        self.choice_preview(screen)

        # Se o jogador clicar na carta, _clicked = True
        if pygame.mouse.get_pressed()[0] and not self._clicked:
            for card in self._player.sprite._hand.sprites():
                if card.rect.collidepoint(pygame.mouse.get_pos()):
                    self._clicked = True
                    self._clicked_card = card

                    # CÓDIGO RUIM, MUDAR PRO PLAYER DEPOIS
                    self._where_to_go = self._player.sprite._path[-1]
                    self._where_to_go = (card.value[0] * DISTANCE + self._where_to_go[0], -card.value[1] * DISTANCE + self._where_to_go[1])

                    if self._clicked_card.value[0] < 0:
                        self._where_to_go = (-self._where_to_go[0], -self._where_to_go[1])

        # Se tiver clicado, roda a animação
        if self._clicked:
            if self._player.sprite.rect.center <= self._where_to_go:
                self._player.sprite.update_choice(self._clicked_card, self._timer, DISTANCE)
            
                self._timer += 0.05
            else:
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

    def choice_preview(self, screen):
        # Verifica se o mouse está em cima da carta
        for card in self._player.sprite._hand.sprites():
            if card.update(screen) and not self._clicked:
                # Pega o ponto inicial e final da reta
                start = self._player.sprite._path[-1]
                end = (start[0] + card.value[0] * DISTANCE, start[1] - card.value[1] * DISTANCE)

                # Desenha a linha
                pygame.draw.line(screen, self._player.sprite._color, start, end, width = 6)