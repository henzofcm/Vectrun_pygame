import pygame
import sys
from entity import *
from rider import *

# Define caminho de todas as pastas que usaremos
ASSET_PATH = "assets/"
TEXTURE_PATH = ASSET_PATH + "textures/"
MUSIC_PATH = ASSET_PATH + "music/"
SOUNDS_PATH = ASSET_PATH + "sounds/"
FONTS_PATH = ASSET_PATH + "fonts/"

# Tamanho do tabuleiro
GRID_X = 750
GRID_Y = 750

# Tamanho da moto
RIDER_X = 50
RIDER_Y = 25

# Tamanho da carta
CARD_X = 150
CARD_Y = 100

class Grid_Game(Entity):
    def __init__(self, image_path, x_y, scale_size, bot_number):
        super().__init__(image_path, x_y, scale_size)

        # Timer interno, eventualmente útil
        self._timer = 0

        # Se o jogador clicar nas cartas, será true
        self._clicked = False

        # Cria o jogador
        self._player = Player(1, (GRID_X / 2, GRID_Y / 2), (RIDER_X, RIDER_Y))
        self._player = pygame.sprite.GroupSingle(self._player)

        # Cria os bots
        __bot_list = []
        for bot in range(bot_number):
            __bot_list.append(Player(bot + 2, (GRID_X / 2 - 45, GRID_Y / 2 - 45), (RIDER_X, RIDER_Y)))

        self._bots = pygame.sprite.Group(__bot_list)

       # Cria as cartas do jogador e o deck
        for card in range(3):
            pass


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
                self._player.update(vector, self._timer)
            
                self._timer += 0.05
            else:
                self._timer = 0
                self._clicked = False