import pygame
import sys

# Adiciona a pasta /src/ pro PYTHONPATH
sys.path.append("src/")

# Importa todo o pacote de src/
from src import state

# Inicializa
pygame.init()

# Cria o jogo
game = state.Vectrun()

# Começa o jogo
game.play()

# Quando retornar, fecha tudo
pygame.quit()
sys.exit()
