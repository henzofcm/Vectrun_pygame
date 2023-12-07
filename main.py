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

# # Grid_Game já cria todos objetos internamente (jogador, bots, cartas)
# current_menu = game.Grid_Game(TEXTURE_PATH + "grid.png", (0, 0), (GRID_X, GRID_Y), 0)
#
# # PARA O TESTE DOS MENUS
# main_menu = menu.MainMenu(current_menu)
#
# # Loop do jogo
# while True:
    # # Se o jogador trocar de menu, current_menu muda de acordo
    # if current_menu.update(screen):
    #     if current_menu.next_menu == "start":
    #         current_menu = menu.Start_Menu()
    #     elif current_menu.next_menu == "config":
    #         current_menu = menu.Config_Menu(menu)
    #     elif current_menu.next_menu == "grid":
    #         # Mantém a partida se estiver voltando pro jogo do menu de configurações
    #         if isinstance(current_menu, menu.Config_Menu):
    #             current_menu = current_menu.last_menu
    #             continue
    #
    #         current_menu = game.Grid_Game(menu)
    #
    #
    # # Desenha tudo do menu
    # current_menu.draw(screen)
    #
    # main_menu.display_menu()


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