import pygame
import sys

# Adiciona a pasta /src/ pro PYTHONPATH
sys.path.append("src/")

# Importa todo o pacote de src/
from src import state_control

# Inicializa
pygame.init()

# Cria o jogo
game = state_control.StateControl()

# Começa o jogo
game.start()

# Quando retornar, fecha tudo
pygame.quit()
sys.exit()
