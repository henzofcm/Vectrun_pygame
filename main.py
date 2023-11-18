import pygame
import sys

# Adiciona a pasta /src/ pro PYTHONPATH
sys.path.append("src/")

# Importa todo o pacote de src/
from src import *


# Define caminho de todas as pastas que usaremos
ASSET_PATH = "assets/"
TEXTURE_PATH = ASSET_PATH + "textures/"
MUSIC_PATH = ASSET_PATH + "music/"
SOUNDS_PATH = ASSET_PATH + "sounds/"
FONTS_PATH = ASSET_PATH + "fonts/"

# Tamanho da tela
WIDTH = 1280
HEIGHT = 720

# Inicializa
pygame.init()

# Cria algumas configurações do display   
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vectrun")
pygame.display.set_icon(pygame.image.load(TEXTURE_PATH + "icon.png"))

# Cria o relógio interno do FPS
fps_clock = pygame.time.Clock()

# Aqui vai ser criado todos os objetos (jogadores, deck, menus)
menu_1 = menu.Grid_Game(TEXTURE_PATH + "grid.png", (WIDTH / 2 - 300, 0), 600, 600)

# Loop do jogo
while True:
    # Loop dos eventos principal (mexeremos no futuro)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Aqui vão ser atualizados todos objetos (cada um com seu update())
    menu_1.update()


    # Aqui vão ser mostrado tudo o que foi atualizado
    screen.blit(menu_1._image, menu_1._rect)


    # Enfim atualiza o display
    pygame.display.update()
    fps_clock.tick(30)
