import pygame
from config import *
from entity import *


class Button(Entity):
    def __init__(self, image_path, x_y, scale_size, label):
        super().__init__(image_path, x_y, scale_size)
        self.label = label
        self.rect = self.image.get_rect(center=x_y)
        self.selected = False

    def update(self):
        # Testa se houve colisão com o mouse
        mouse_pos = pygame.mouse.get_pos()
        is_over = self.rect.collidepoint(mouse_pos)

        if is_over:
            return True
        else:
            return False


class Menu(Entity):
    def __init__(self, game, image_path, x_y, scale_size):
        super().__init__(image_path, x_y, scale_size)
        self.rect = self.image.get_rect(center=x_y)
        self.button_clicked = False
        self.state_control = game
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.adjustment_x, self.adjustment_y = -150, 15
        self.selected_button = None

    def draw_text(self, text, size, x, y ):
        self.font_name = pygame.font.get_default_font()
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.state_control.screen.blit(text_surface, text_rect)

    def blit_screen(self):
        self.state_control.screen.blit(self.state_control.screen, (0, 0))
        pygame.display.update()
        self.state_control.reset_keys()


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
        self.buttons_group = pygame.sprite.Group(self.btn_the_grid, self.btn_options, self.btn_credits)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            # Preenche o fundo
            self.state_control.screen.fill(BLACK)

            #Verifica as entradas e interação com os botões
            self.state_control.check_events()
            self.choice_preview(self.state_control.screen)
            self.check_input()

            # Exibie o logo do jogo
            self.state_control.screen.blit(self.image, self.rect)

            # Insere os botões na tela:
            self.buttons_group.draw(self.state_control.screen)

            self.blit_screen()

    def choice_preview(self, screen):
        # Verifica se o mouse está em cima da carta
        for button in self.buttons_group:
            if button.update():
                # Seleciona a tela equivalente ao botão
                self.state = button.label

                # Desenha o contorno
                self.__preview_selected_button(button, screen)

                # Verifica se o botão esquerdo do mouse é pressionado
                mouse_clicked = pygame.mouse.get_pressed()[0]

                if mouse_clicked or self.state_control.START_KEY:
                    self.button_clicked = True
                else:
                    self.button_clicked = False

    @staticmethod
    def __preview_selected_button(button, screen):
        # Desenha o contorno do botão selecionado
        rect_pos = (button.rect.left - BUTTON_SELECTED_WIDTH, button.rect.top - BUTTON_SELECTED_WIDTH)
        rect_size = (button.rect.width + 2 * BUTTON_SELECTED_WIDTH, button.rect.height + 2 * BUTTON_SELECTED_WIDTH)

        rectangle = pygame.Rect(rect_pos, rect_size)

        pygame.draw.rect(screen, RED, rectangle, width=2 * BUTTON_SELECTED_WIDTH)

    def check_input(self):
        if self.state_control.ESC_KEY:
            self.state_control.running = False
            self.state_control.curr_menu.run_display = False
        if self.state_control.START_KEY or self.button_clicked:
            if self.state == "the_grid":
                self.state_control.playing = True
            elif self.state == "options":
                self.state_control.curr_menu = self.state_control.options
            elif self.state == "credits":
                self.state_control.curr_menu = self.state_control.credits

            self.run_display = False


class OptionsMenu(Menu):
    def __init__(self, game, image_path, x_y, scale_size):
        super().__init__(game, image_path, x_y, scale_size)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.state_control.check_events()
            self.check_input()

            self.state_control.screen.fill(BLACK)

            # Falta criar um menu de opções funcional (quando a música estiver implementada)

            # Excluir essa linha
            self.draw_text("Options", 20, WIDTH / 2, HEIGHT / 2 - 30)

            self.blit_screen()

    def check_input(self):
        if self.state_control.ESC_KEY:
            self.state_control.curr_menu = self.state_control.main_menu
            self.run_display = False
        if self.state_control.BACK_KEY:
            self.state_control.curr_menu = self.state_control.main_menu
            self.run_display = False


class CreditsMenu(Menu):
    def __init__(self, game, image_path, x_y, scale_size):
        super().__init__(game, image_path, x_y, scale_size)
        # Carrega a imagem da tela de fundo
        self.background_image = pygame.image.load(TEXTURE_PATH + "background_credits.png").convert()

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.state_control.check_events()
            self.check_input()

            # Define a cor de fundo da tela
            self.state_control.screen.fill(BLACK)

            # Exibe o plano de fundo da tela
            self.state_control.screen.blit(self.background_image, (0,0))

            # Exibe a imagem credits
            self.state_control.screen.blit(self.image, self.rect)

            # Lista com o tamanhos das fontes
            font_size = [25, 30, 40]
            # Lista com tamanho de espaçamentos
            space_size = [40]

            # Posição inicial
            txt_x = WIDTH/2
            txt_y = HEIGHT/4 + space_size[0]

            # Desenha os textos na tela
            self.draw_text("A2 - LP - 2023",   font_size[2], txt_x, txt_y)

            self.draw_text("- Code by:",         font_size[1], txt_x, (txt_y + 2*space_size[0]))
            self.draw_text("Beatriz Miranda Bezerra",
                                                    font_size[0], txt_x, (txt_y + 3*space_size[0]))
            self.draw_text("Gustavo Murilo Cavalcante Carvalho",
                                                    font_size[0], txt_x, (txt_y + 4*space_size[0]))
            self.draw_text("Henzo Felipe Carvalho de Mattos",
                                                    font_size[0], txt_x, (txt_y + 5*space_size[0]))

            self.draw_text("- Art and Concept granted by:",
                                                    font_size[1], txt_x, (txt_y + 7*space_size[0]))
            self.draw_text("Tulio Koneçny",    font_size[0], txt_x, (txt_y + 8*space_size[0]))

            self.blit_screen()

    def check_input(self):
        if self.state_control.ESC_KEY:
            self.state_control.curr_menu = self.state_control.main_menu
            self.run_display = False
        if self.state_control.BACK_KEY:
            self.state_control.curr_menu = self.state_control.main_menu
            self.run_display = False