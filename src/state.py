import pygame

import menu
import game
from config import *


class Vectrun:

    def __init__(self):
        # Cria a tela do jogo
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Vectrun")
        pygame.display.set_icon(pygame.image.load(TEXTURE_PATH + "icon.png"))

        # Cria o relógio interno do FPS
        self.fps_clock = pygame.time.Clock()

        # Define a tela inicial
        self.curr_menu = menu.MainMenu(
            (TEXTURE_MENU_PATH + "vectrun_logo.png"),
            (WIDTH / 2, HEIGHT / 5),
            (LOGO_X, LOGO_Y),
        )

        # Carrega a música pra memória
        self.volume = VOLUME_START
        self.__change_music("title.ogg", self.volume)
        pygame.mixer.music.play(-1, 0, 2)

        # TODO
        self.winner = 0
        self.running = True

    def play(self):
        # Loop principal
        while self.running:
            # Preenche a tela
            self.screen.fill(BLACK)

            # Atualiza e exibe o jogo na tela
            self.__next_menu = self.curr_menu.update()
            self.curr_menu.draw(self.screen)

            # Enfim mostra o diplay
            pygame.display.update()
            self.fps_clock.tick(30)

            # Verifica se mudou de menu
            self.change_menu()

        return

    def change_menu(self):
        # A depender do código retornado por update(), muda de menu
        match self.__next_menu:
            # Sair do jogo
            case -1:
                self.running = False
                return
            # Não muda
            case 0:
                return
            # Menu principal
            case 1:
                if isinstance(self.curr_menu, game.GridGame):
                    self.__change_music("title.ogg", self.volume)
                    pygame.mixer.music.play(-1, 0, 2)

                self.curr_menu = menu.MainMenu(
                    (TEXTURE_MENU_PATH + "vectrun_logo.png"),
                    (WIDTH / 2, HEIGHT / 5),
                    (LOGO_X, LOGO_Y),
                )
                return
            # Tutorial
            case 2:
                self.curr_menu = menu.TutorialScreen(
                    (TEXTURE_MENU_PATH + "tutorial_button.png"),
                    (WIDTH / 2, HEIGHT / 6 - 50),
                    (2 * BUTTON_X, 2 * BUTTON_Y),
                )
                return
            # Opções
            case 3:
                self.curr_menu = menu.OptionsMenu(
                    (TEXTURE_MENU_PATH + "options_button.png"),
                    (WIDTH / 2, (HEIGHT / 6 - 50)),
                    (2 * BUTTON_X, 2 * BUTTON_Y),
                    self,
                )
                return
            # Grid
            case 4:
                self.__change_music("grid_1.ogg", self.volume)
                pygame.mixer.music.play(-1, 0, 2)

                self.curr_menu = game.GridGame(
                    TEXTURE_PATH + "grid.png",
                    (0, 0),
                    (GRID_X, GRID_Y),
                    3,
                    self.volume,
                )
                return
            # Win
            case 5:
                self.curr_menu = menu.ResultScreen(
                    (TEXTURE_MENU_PATH + "you_win.png"),
                    (WIDTH / 2, HEIGHT / 5),
                    (LOGO_X, LOGO_Y),
                )
            # Lose
            case 6:
                self.curr_menu = menu.ResultScreen(
                    (TEXTURE_MENU_PATH + "you_lose.png"),
                    (WIDTH / 2, HEIGHT / 5),
                    (LOGO_X, LOGO_Y),
                )
            # Credits
            case 8:
                self.curr_menu = menu.CreditsMenu(
                    (TEXTURE_MENU_PATH + "credits_button.png"),
                    (WIDTH / 2, (HEIGHT / 6 - 50)),
                    (2 * BUTTON_X, 2 * BUTTON_Y),
                )
            # TODO

    @staticmethod
    def __change_music(title, volume):
        pygame.mixer.music.load(MUSIC_PATH + title)
        pygame.mixer.music.set_volume(volume)
