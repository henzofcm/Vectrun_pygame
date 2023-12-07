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

current_state = game_state.Game_State()

while current_state.running:
    current_state.curr_menu.display_menu()
    current_state.game_loop()

    # Enfim atualiza o display
    pygame.display.update()
    fps_clock.tick(30)

    screen.fill("#000000")

pygame.quit()
sys.exit()