import pygame
from config import *
from menu import *
from game import *
from deck import *
from config import *


class StateControl():
    def __init__(self, screen):
        # Validação dos parâmetros
        if not isinstance(screen, pygame.Surface):
            raise ValueError(
                f"O objeto passado ao iniciar o jogo deve ser do tipo pygame.Suface, mas foi passado {type(screen)}")

        # Iniciação das variáveis de controle
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESC_KEY = False, False, False, False, False

        # Define a tela do jogo (pygame.display)
        self.screen = screen

        # Cria um objeto para cada uma das telas
        self.main_menu = MainMenu(self, (TEXTURE_PATH + "vectrun_logo.png"), (WIDTH / 2, HEIGHT / 5), (LOGO_X, LOGO_Y))
        self.options = OptionsMenu(self, (TEXTURE_PATH + "options_button.png"), (0, 0), (0, 0))
        self.credits = CreditsMenu(self, (TEXTURE_PATH + "credits_button.png"), (0, 0), (0, 0))
        self.game_run = Grid_Game(TEXTURE_PATH + "grid.png", (0, 0), (GRID_X, GRID_Y), 0)

        # Define a tela inicial
        self.curr_menu = self.main_menu

    def game_loop(self):
        while self.playing:
            self.check_events()

            # Preenche a tela escondendo o Menu
            self.screen.fill(BLACK)

            # Inicia uma partida
            self.game_run.update(self.screen)

            # Atualiza a tela
            pygame.display.update()
            self.reset_keys()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.ESC_KEY = True
                    self.playing = False
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESC_KEY = False, False, False, False, False
