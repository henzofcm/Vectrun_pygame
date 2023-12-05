import pygame
import sys

# Adiciona a pasta /src/ pro PYTHONPATH
sys.path.append("src/")

# Importa todo o pacote de src/
from src import *
from config import *

# Inicializa
pygame.init()

# Cria algumas configurações do display   
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vectrun")
pygame.display.set_icon(pygame.image.load(TEXTURE_PATH + "icon.png"))

# Cria o relógio interno do FPS
fps_clock = pygame.time.Clock()

# Grid_Game já cria todos objetos internamente (jogador, bots, cartas)
grid_game = game.Grid_Game(TEXTURE_PATH + "grid.png", (0, 0), (GRID_X, GRID_Y), 0)

# Loop do jogo
while True:
    # Faz blit no tabuleiro
    screen.blit(grid_game.image, grid_game.rect)

    # Aqui vão ser atualizados os menus (que atualizam tudo)
    grid_game.update(screen)

    # Desenha as linhas dos jogadores
    for bot in grid_game._bots.sprites():
        pygame.draw.lines(screen, bot._color, False, bot._path + [bot.rect.center], width=6)

    if grid_game._player.sprite:
        pygame.draw.lines(screen, grid_game._player.sprite._color, False, grid_game._player.sprite._path + [grid_game._player.sprite.rect.center], width=6)

        grid_game._player.sprite._hand.draw(screen)

    # Faz blit no jogador e nos bots
    grid_game._player.draw(screen)
    grid_game._bots.draw(screen)

    # Enfim atualiza o display
    pygame.display.update()
    fps_clock.tick(30)

    screen.fill("#000000")
