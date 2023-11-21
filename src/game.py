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
        print(len(self._deck.cards))

    def update(self):
        # Eventos principais deste menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_SPACE and not self._clicked:
                    self._clicked = 1

        vector = (10, 10)
        # Se selecionar a carta, roda a animação
        if self._clicked:
            if self._player.sprite.rect.center < (500, 500):
                self._player.sprite.update_choice(vector, self._timer)
                self._bots.sprite.update_choice(vector, self._timer)
            
                self._timer += 0.05
            else:
                self._timer = 0
                self._clicked = False

    def choice_preview(self, vector, screen):
        # Pega o ponto inicial e final da reta
        start = self._player.sprite._path[-1]
        end = (start[0] + vector[0], start[1] + vector[1])

        # Desenha a linha
        pygame.draw.line(screen, self._player.sprite._color, start, end, width = 6)