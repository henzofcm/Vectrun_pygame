import pygame

from menu import *
from game import *
from deck import *
from config import *


class StateControl():
    def __init__(self):
        # Iniciação das variáveis de controle
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESC_KEY = False, False, False, False, False
        self.BUTTON_CLICKED = False

        # Cria a tela do jogo
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Vectrun")
        pygame.display.set_icon(pygame.image.load(TEXTURE_PATH + "icon.png"))
        
        # Cria o relógio interno do FPS
        self.fps_clock = pygame.time.Clock()

        # Cria um objeto para cada uma das telas
        self.main_menu = MainMenu(self, (TEXTURE_PATH + "vectrun_logo.png"), (WIDTH/2, HEIGHT/5), (LOGO_X, LOGO_Y))
        self.options_menu = OptionsMenu(self, (TEXTURE_PATH + "options_button.png"), (WIDTH / 2, (HEIGHT / 6 - 50)), (2 * BUTTON_X, 2 * BUTTON_Y))
        self.credits_menu = CreditsMenu(self, (TEXTURE_PATH + "credits_button.png"), (WIDTH / 2, (HEIGHT / 6 - 50)), (2 * BUTTON_X, 2 * BUTTON_Y))

        # EDIÇão FUtura para considerar ambos casos (derrrota e virtoria)
        self.result_screen = ResultScreen(self, (TEXTURE_PATH + "you_win.png"), (WIDTH/2, HEIGHT/2), (LOGO_X,LOGO_Y))

        # Define a tela inicial
        self.curr_menu = self.main_menu

        # Cria um objeto para o jogo
        self.game_run = GridGame(TEXTURE_PATH + "grid.png", (0, 0), (GRID_X, GRID_Y), 3)
        # Posteriormente, criar um a cada vez que o jogo for iniciado

    def game_loop(self):
        while self.playing:
            # Preenche a tela
            self.screen.fill(BLACK)

            # Atualiza e exibe o jogo na tela
            self.game_run.update()
            self.game_run.draw(self.screen)

            # Enfim mostra o diplay
            pygame.display.update()
            self.fps_clock.tick(30)

        # INSERIR AQUI
        # (DETECTAR DERROTA OU VITORIA)
        if False:
            self.curr_menu = self.result_screen


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
        self.BUTTON_CLICKED = False

    def start(self):
        while not self.playing:
            self.curr_menu.display_menu()

            if not self.running:
                return


        self.game_loop()