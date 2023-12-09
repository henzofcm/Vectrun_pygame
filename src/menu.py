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

        self.state_control = game
        self.rect = self.image.get_rect(center=x_y)

        # Define variáveis de controle
        self.run_display = True
        self.button_clicked = False
        self.selected_button = None

        # Cria um grupo para os sprites
        self.buttons_group = pygame.sprite.Group()

    def draw_text(self, text, size, x, y ):
        self.font_name = pygame.font.get_default_font()
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.state_control.screen.blit(text_surface, text_rect)

    def update(self):
        pygame.display.update()
        self.state_control.reset_keys()
    
    def verify(self):
        self.state_control.check_events()
        self.choice_preview(self.state_control.screen)
        self.check_input()
    
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
                    self.state_control.BUTTON_CLICKED = True
                    # Delay para evitar cliques indesejados
                    pygame.time.delay(170)
                    return None

    @staticmethod
    def __preview_selected_button(button, screen):
        # Desenha o contorno do botão selecionado
        rect_pos = (button.rect.left - BUTTON_SELECTED_WIDTH, button.rect.top - BUTTON_SELECTED_WIDTH)
        rect_size = (button.rect.width + 2 * BUTTON_SELECTED_WIDTH, button.rect.height + 2 * BUTTON_SELECTED_WIDTH)

        rectangle = pygame.Rect(rect_pos, rect_size)

        pygame.draw.rect(screen, RED, rectangle, width=2 * BUTTON_SELECTED_WIDTH)

    def check_input(self):
        pass


class MainMenu(Menu):
    def __init__(self, game, image_path, x_y, scale_size):
        super().__init__(game, image_path, x_y, scale_size)
        self.state = "the_grid"

        # Posições para os elementos na tela
        self.start_x, self.start_y = (WIDTH/2), (HEIGHT/2)
        self.options_x, self.options_y = (WIDTH/2), (HEIGHT/2 + 100)
        self.credits_x, self.credits_y = (WIDTH/2), (HEIGHT/2 + 200)

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
            self.verify()

            # Exibie o logo do jogo
            self.state_control.screen.blit(self.image, self.rect)

            # Insere os botões na tela:
            self.buttons_group.draw(self.state_control.screen)

            self.update()

    def check_input(self):
        if self.state_control.ESC_KEY:
            self.state_control.running = False
            self.state_control.curr_menu.run_display = False
        if self.state_control.START_KEY or self.state_control.BUTTON_CLICKED:
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
        self.state = "main_menu"

        # Define os botões dessa tela
        self.btn_back = Button(TEXTURE_PATH + "back_button.png", (WIDTH / 2, (HEIGHT - 100)),
                               (BUTTON_X, BUTTON_Y), "main_menu")

        # Adiciona os botões a um grupo
        self.buttons_group.add(self.btn_back)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.state_control.screen.fill(BLACK)
            
            # Verifica as entradas e interação com os botões
            self.verify()

            # Exibe a imagem "Options"
            self.state_control.screen.blit(self.image, self.rect)

            # Insere os botões na tela:
            self.buttons_group.draw(self.state_control.screen)

            self.update()

    def check_input(self):
        if self.state_control.ESC_KEY:
            self.state_control.curr_menu = self.state_control.main_menu
            self.run_display = False
        if self.state_control.BACK_KEY:
            self.state_control.curr_menu = self.state_control.main_menu
            self.run_display = False
        if self.state_control.START_KEY or self.state_control.BUTTON_CLICKED:
            if self.state == "main_menu":
                self.state_control.curr_menu = self.state_control.main_menu
            self.run_display = False


class CreditsMenu(Menu):
    def __init__(self, game, image_path, x_y, scale_size):
        super().__init__(game, image_path, x_y, scale_size)
        self.state = "main_menu"

        # Define variáveis com valores recorrentes no menu
        self.font_size = [25, 30, 40]
        self.space_size = [40, 27]
        self.txt_x = WIDTH / 2
        self.txt_y = HEIGHT / 4 + self.space_size[1]

        # Carrega a imagem da tela de fundo
        self.background_image = pygame.image.load(TEXTURE_PATH + "background_credits.png").convert()

        # Define os botões dessa tela
        self.btn_back = Button(TEXTURE_PATH + "back_button.png", (WIDTH/2, (HEIGHT - 100)),
                                   (BUTTON_X, BUTTON_Y), "main_menu")

        # Adiciona os botões a um grupo
        self.buttons_group.add(self.btn_back)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            # Exibe o plano de fundo da tela
            self.state_control.screen.fill(BLACK)

            #Verifica as entradas e interação com os botões
            self.verify()

            # Exibe a imagem "credits"
            self.state_control.screen.blit(self.image, self.rect)

            # Insere os botões na tela:
            self.buttons_group.draw(self.state_control.screen)

            # Desenha os textos na tela
            self.draw_text("A2 - LP - 2023", self.font_size[2], self.txt_x, self.txt_y)
            self.draw_text("- Code by:", self.font_size[1], self.txt_x, (self.txt_y + 2*self.space_size[0]))
            self.draw_text("Beatriz Miranda Bezerra", self.font_size[0], self.txt_x, (self.txt_y + 3*self.space_size[0]))
            self.draw_text("Gustavo Murilo Cavalcante Carvalho", self.font_size[0], self.txt_x, (self.txt_y + 4*self.space_size[0]))
            self.draw_text("Henzo Felipe Carvalho de Mattos", self.font_size[0], self.txt_x, (self.txt_y + 5*self.space_size[0]))
            self.draw_text("- Art and Concept granted by:", self.font_size[1], self.txt_x, (self.txt_y + 7*self.space_size[0]))
            self.draw_text("Tulio Koneçny", self.font_size[0], self.txt_x, (self.txt_y + 8*self.space_size[0]))

            self.update()

    def check_input(self):
        if self.state_control.ESC_KEY:
            self.state_control.curr_menu = self.state_control.main_menu
            self.run_display = False
        if self.state_control.BACK_KEY:
            self.state_control.curr_menu = self.state_control.main_menu
            self.run_display = False
        if self.state_control.START_KEY or self.state_control.BUTTON_CLICKED:
            if self.state == "main_menu":
                self.state_control.curr_menu = self.state_control.main_menu
            self.run_display = False


class ResultScreen(Menu):
    def __init__(self, game, image_path, x_y, scale_size):
        super().__init__(game, image_path, x_y, scale_size)
        self.state = "main_menu"

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.state_control.screen.fill(BLACK)

            # Verifica as entradas e interação com os botões
            self.verify()

            # CODE TO FINISH -->
            # Exibe a imagem "You Died" ou "You Win"
            self.state_control.screen.blit(self.image, self.rect)
            # <-- CODE TO FINISH

            # Insere os botões na tela:
            self.buttons_group.draw(self.state_control.screen)

            self.update()

    def check_input(self):
        pass
        # CODE TO FINISH -->
        # <-- CODE TO FINISH

class TutorialScreen(Menu):
    def __init__(self, game, image_path, x_y, scale_size):
        super().__init__(game, image_path, x_y, scale_size)
        self.state = ""

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.state_control.screen.fill(BLACK)

            # Verifica as entradas e interação com os botões
            self.verify()
            
            # CODE TO FINISH -->
            # <-- CODE TO FINISH

            self.update()

    def check_input(self):
        pass
        # CODE TO FINISH -->
        # <-- CODE TO FINISH