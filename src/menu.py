import pygame
from config import *
from entity import *


class Button(Entity):
    def __init__(self, image_path, x_y, scale_size, label):
        super().__init__(image_path, x_y, scale_size)
        self.label = label
        self.rect = self.image.get_rect(center=x_y)

    def update(self):
        # Testa se houve colisão com o mouse
        mouse_pos = pygame.mouse.get_pos()
        is_clicked = pygame.mouse.get_pressed()[0]

        # Verifica se o mouse está sobre o botão
        if self.rect.collidepoint(mouse_pos):
            if is_clicked:
                return True
            return self.label
        else:
            return False


class Menu(Entity):
    def __init__(self, game, image_path, x_y, scale_size):
        super().__init__(image_path, x_y, scale_size)
        self.rect = self.image.get_rect(center=x_y)
        self.BUTTON_CLICKED = False
        self.game_state = game
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.adjustment_x, self.adjustment_y = -150, 15

    def draw_cursor(self):
        self.draw_text('*', 50, self.cursor_rect.x, self.cursor_rect.y)

    def draw_text(self, text, size, x, y ):
        self.font_name = pygame.font.get_default_font()
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.game_state.screen.blit(text_surface, text_rect)

    def blit_screen(self):
        self.game_state.screen.blit(self.game_state.screen, (0, 0))
        pygame.display.update()
        self.game_state.reset_keys()


class MainMenu(Menu):
    def __init__(self, game, image_path, x_y, scale_size):
        super().__init__(game, image_path, x_y, scale_size)
        self.state = "the_grid"

        # Posições para os elementos na tela
        self.start_x, self.start_y = (WIDTH/2), (HEIGHT/2)
        self.options_x, self.options_y = (WIDTH/2), (HEIGHT/2 + 100)
        self.credits_x, self.credits_y = (WIDTH/2), (HEIGHT/2 + 200)
        self.cursor_rect.midtop = (self.start_x + self.adjustment_x, self.start_y + self.adjustment_y)

        # Define os botões dessa tela
        self.btn_the_grid = Button(TEXTURE_PATH + "grid_logo.png", (self.start_x, self.start_y),
                              (BUTTON_X, BUTTON_Y), "the_grid")
        self.btn_options = Button(TEXTURE_PATH + "options_button.png", (self.options_x, self.options_y),
                                   (BUTTON_X, BUTTON_Y), "options")
        self.btn_credits = Button(TEXTURE_PATH + "credits_button.png", (self.credits_x, self.credits_y),
                                   (BUTTON_X, BUTTON_Y), "credits")

        # Adiciona os botões a um grupo
        self.buttons_group = pygame.sprite.Group()
        self.buttons_group.add(self.btn_the_grid)
        self.buttons_group.add(self.btn_options)
        self.buttons_group.add(self.btn_credits)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game_state.check_events()
            self.check_input()

            self.game_state.screen.fill(BLACK)

            # Exibie o logo do jogo
            self.game_state.screen.blit(self.image, self.rect)

            # Insere os botões na tela:
            # botão 1 - código:
            self.game_state.screen.blit(self.btn_the_grid.image, self.btn_the_grid.rect)
            self.game_state.screen.blit(self.btn_options.image, self.btn_options.rect)
            self.game_state.screen.blit(self.btn_credits.image, self.btn_credits.rect)

            # Insere o cursor
            self.draw_cursor()

            # Verifica os botoes
            self.choice_preview(self.game_state.screen)

            self.blit_screen()

    def choice_preview(self, screen):
        # Verifica se o mouse está em cima da carta
        for button in self.buttons_group:
            if button.update():
                # Desenha o contorno
                self.__preview_selected_button(button, screen)

    @staticmethod
    def __preview_selected_button(button, screen):
        # Desenha o contorno do botão selecionado
        rect_pos = (button.rect.left - BUTTON_SELECTED_WIDTH, button.rect.top - BUTTON_SELECTED_WIDTH)
        rect_size = (button.rect.width + 2 * BUTTON_SELECTED_WIDTH, button.rect.height + 2 * BUTTON_SELECTED_WIDTH)

        rectangle = pygame.Rect(rect_pos, rect_size)

        pygame.draw.rect(screen, RED, rectangle, width=2 * BUTTON_SELECTED_WIDTH)

    def move_cursor(self):
        if self.game_state.DOWN_KEY:
            if self.state == 'the_grid':
                self.cursor_rect.midtop = (self.options_x + self.adjustment_x, self.options_y)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.credits_x + self.adjustment_x, self.credits_y)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.start_x + self.adjustment_x, self.start_y)
                self.state = 'the_grid'
        elif self.game_state.UP_KEY:
            if self.state == 'the_grid':
                self.cursor_rect.midtop = (self.credits_x + self.adjustment_x, self.credits_y)
                self.state = 'Credits'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.start_x + self.adjustment_x, self.start_y)
                self.state = 'the_grid'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.options_x + self.adjustment_x, self.options_y)
                self.state = 'Options'

    def check_input(self):
        self.move_cursor()

        if self.game_state.ESC_KEY:
            self.game_state.running = False
            self.game_state.curr_menu.run_display = False
        if self.game_state.START_KEY or self.BUTTON_CLICKED:
            if self.state == 'the_grid':
                self.game_state.playing = True
            elif self.state == 'Options':
                self.game_state.curr_menu = self.game_state.options
            elif self.state == 'Credits':
                self.game_state.curr_menu = self.game_state.credits
            self.run_display = False


class OptionsMenu(Menu):
    def __init__(self, game, image_path, x_y, scale_size):
        super().__init__(game, image_path, x_y, scale_size)
        self.state = 'Volume'
        self.volx, self.voly = (WIDTH/2), (HEIGHT/2 + 20)
        self.controlsx, self.controlsy = (WIDTH/2), (HEIGHT/2 + 40)
        self.cursor_rect.midtop = (self.volx + self.adjustment_x, self.voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game_state.check_events()
            self.check_input()

            self.game_state.screen.fill((0, 0, 0))

            self.game_state.screen.blit(self.image, self.rect)
            self.draw_text('Options', 20, WIDTH / 2, HEIGHT / 2 - 30)

            self.blit_screen()

    def check_input(self):
        if self.game_state.ESC_KEY:
            self.game_state.curr_menu = self.game_state.main_menu
            self.run_display = False
        if self.game_state.BACK_KEY:
            self.game_state.curr_menu = self.game_state.main_menu
            self.run_display = False


class CreditsMenu(Menu):
    def __init__(self, game, image_path, x_y, scale_size):
        super().__init__(game, image_path, x_y, scale_size)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game_state.check_events()
            self.check_input()

            # Define a cor de fundo da tela
            self.game_state.screen.fill(RED)

            # Insere a imagem "Credits" na tela
            self.game_state.screen.blit(self.image, self.rect)

            # Lista com o tamanhos das fontes
            font_size = [40, 30, 25]
            # Lista com os espaçamentos
            space_size = [60, 35]
            # Posição inicial
            txt_x = WIDTH / 2
            txt_y = HEIGHT / 5

            # Desenha os textos na tela
            self.draw_text('A2 - LP - 2023',   font_size[0], txt_x, HEIGHT / 5)
            self.draw_text('Credits',          font_size[0], txt_x, HEIGHT / 5 + 50)

            self.draw_text('- Code by:',         font_size[1], txt_x, HEIGHT / 3 + 20)
            self.draw_text('Beatriz Miranda Bezerra',
                                                    font_size[2], txt_x, HEIGHT / 3 + 60)
            self.draw_text('Gustavo Murilo Cavalcante Carvalho',
                                                    font_size[2], txt_x, HEIGHT / 3 + 95)
            self.draw_text('Henzo Felipe Carvalho de Mattos',
                                                    font_size[2], txt_x, HEIGHT / 3 + 130)

            self.draw_text('- Art and Concept granted by:',
                                                    font_size[1], txt_x, HEIGHT / 2 + 80)
            self.draw_text('Tulio Coutinho Koneçny',    font_size[2], txt_x, HEIGHT / 2 + 120)

            self.blit_screen()

    def check_input(self):
        if self.game_state.ESC_KEY:
            self.game_state.curr_menu = self.game_state.main_menu
            self.run_display = False
        if self.game_state.BACK_KEY:
            self.game_state.curr_menu = self.game_state.main_menu
            self.run_display = False