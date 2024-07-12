import pygame

import menu
import game
import deck

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
        self.curr_menu = menu.LoadingScreen(TEXTURE_MENU_PATH + "loading2.jpg", (0, 0), (WIDTH, HEIGHT), self)

        # Salva o volume
        self.volume = VOLUME_START

        # TODO
        self.running = True
        self.bot_num = 3

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
                if isinstance(self.curr_menu, game.GridGame) or isinstance(self.curr_menu, menu.LoadingScreen):
                    self.__change_music("title.ogg", self.volume)
                    pygame.mixer.music.play(-1, 0, 2)

                self.curr_menu = self.__menus[1]
                return
            # Tutorial
            case 2:
                self.curr_menu = self.__menus[2]
                return
            # Opções
            case 3:
                self.curr_menu = self.__menus[3]
                return
            # Grid
            case 4:
                self.__change_music("grid_1.ogg", self.volume)
                pygame.mixer.music.play(-1, 0, 2)

                self.__deck.reshuffle()
                self.__menus[4] = game.GridGame(
                    TEXTURE_PATH + "grid.png",
                    ((WIDTH - GRID_X) / 2, 0),
                    (GRID_X, GRID_Y),
                    self.bot_num,
                    self.volume,
                    self.__deck
                )
                self.curr_menu = self.__menus[4]
                return
            # Win
            case 5:
                self.curr_menu = self.__menus[5]
            # Lose
            case 6:
                self.curr_menu = self.__menus[6]
            # Credits
            case 8:
                self.curr_menu = self.__menus[8]
            # TODO

    @staticmethod
    def __change_music(title, volume):
        pygame.mixer.music.load(MUSIC_PATH + title)
        pygame.mixer.music.set_volume(volume)

    def _load(self):
        # Cria o deck (o mais lento)
        self.__load_deck()

        # Cria todos menus
        self.__menus = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.__menus[1] = menu.MainMenu(
                    (TEXTURE_MENU_PATH + "vectrun_logo.png"),
                    (WIDTH / 2, HEIGHT / 5),
                    (LOGO_X, LOGO_Y),
                )

        self.__menus[2] = menu.TutorialScreen(
                    (TEXTURE_MENU_PATH + "tutorial_button.png"),
                    (WIDTH / 2, HEIGHT / 6 - 50),
                    (2 * BUTTON_X, 2 * BUTTON_Y),
                )
        
        self.__menus[3] = menu.OptionsMenu(
                    (TEXTURE_MENU_PATH + "options_button.png"),
                    (WIDTH / 2, (HEIGHT / 6 - 50)),
                    (2 * BUTTON_X, 2 * BUTTON_Y),
                    self,
                )
        
        self.__menus[5] = menu.ResultScreen(
                    (TEXTURE_MENU_PATH + "you_win.png"),
                    (WIDTH / 2, HEIGHT / 5),
                    (LOGO_X, LOGO_Y),
                )
        
        self.__menus[6] = menu.ResultScreen(
                    (TEXTURE_MENU_PATH + "you_lose.png"),
                    (WIDTH / 2, HEIGHT / 5),
                    (LOGO_X, LOGO_Y),
                )
        
        self.__menus[8] = menu.CreditsMenu(
                    (TEXTURE_MENU_PATH + "credits_button.png"),
                    (WIDTH / 2, (HEIGHT / 6 - 50)),
                    (2 * BUTTON_X, 2 * BUTTON_Y),
                )
        

    def __load_deck(self):
        # Cria o deck
        self.__deck = deck.Deck(CARDS_PATH, (CARD_X, CARD_Y))