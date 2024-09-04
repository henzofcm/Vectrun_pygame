import pygame

from config import *

import texts as txt
import entity
import textwrap


class Button(entity.Entity):
    """
    Represents a menu button.
    
    Attributes
    ----------
    label : str
        The label for the menu.
    rect : Rect
        The rectangle that represents the menu's position and size.
    selected : bool
        Indicates whether the menu is selected or not.
        
    Methods
    -------
    __init__(self, image_path, x_y, scale_size, label)
        Initializes a Menu object.
    update(self)
        Update the state of the menu.
    """

    def __init__(self, image_path, x_y, scale_size, value):
        """
        Initializes a Menu object.

        Parameters
        ----------
        image_path : str
            The path to the image file for the menu.
        x_y : tuple
            The x and y coordinates of the menu.
        scale_size : float
            The scale size of the menu.
        label : str
            The label for the menu.
            
        Returns
        -------
        None
        """
        # Caso for carregar uma imagem da memória
        if '\\' in image_path:
            super().__init__(image_path, x_y, scale_size)
        # Ou caso precise criar com texto
        else:
            super().__init__(TEXTURE_MENU_PATH + "square_full.png", x_y, scale_size)
            font = pygame.font.Font(FONTS_PATH + "DOSVGA2.ttf", 50)

            self.image = font.render(image_path, True, WHITE)
        
        self.rect = self.image.get_rect(center=x_y)
        self.value = value

    def update(self):
        """
        Update the state of the menu.

        Check for collision with the mouse and return True if there is a collision,
        otherwise return False.

        Returns
        -------
        bool
            True if there is a collision with the mouse, False otherwise.
        """
        # Testa se houve colisão com o mouse
        mouse_pos = pygame.mouse.get_pos()

        # Se houver, retorna True
        if self.rect.collidepoint(mouse_pos):
            return True
        else:
            return False


class Menu(entity.Entity):

    def __init__(self, image_path, x_y, scale_size):
        """
        Initializes a Menu object.
        
        Parameters
        ----------
        game : Game
            The game object that controls the menu.
        image_path : str
            The path to the image file for the menu.
        x_y : tuple
            The x and y coordinates of the menu.
        scale_size : float
            The scale size of the menu.
        
        Returns
        -------
        None
        """
        super().__init__(image_path, x_y, scale_size)
        self.rect = self.image.get_rect(center=x_y)

        # Define a fonte a ser usada
        self.font_name = pygame.font.get_default_font()

        # Cria um grupo para os sprites
        self.buttons_group = pygame.sprite.Group()
        self.options_group = pygame.sprite.Group()

    def draw_text(self, text, size, x, y, screen):
        """
        Draw text on the screen.
        
        Parameters
        ----------
        text : str
            The text to draw.
        size : int
            The size of the text.
        x : int
            The x coordinate of the text.
        y : int
            The y coordinate of the text.
        
        Returns
        -------
        None
        """
        font = pygame.font.Font(FONTS_PATH + "terminator.otf", size)

        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)

        screen.blit(text_surface, text_rect)

    def choice_preview(self, screen):
        """
        Preview the selected choice.
        
        Parameters
        ----------
        screen : Surface
            The screen to preview the selected choice.
        
        Returns
        -------
        None
        """
        # Verifica se o mouse está em cima do botão
        for button in self.buttons_group:
            if button.update():
                # Desenha o contorno
                self._preview_selected_button(button, screen)

    @staticmethod
    def _preview_selected_button(button, screen):
        """
        Preview the selected button.
        
        Parameters
        ----------
        button : Button
            The button to preview.
        screen : Surface
            The screen to preview the button.
        
        Returns
        -------
        None        
        """
        # Desenha o contorno do botão selecionado
        rect_pos = (button.rect.left - BUTTON_SELECTED_WIDTH, button.rect.top - BUTTON_SELECTED_WIDTH)
        rect_size = (button.rect.width + 2 * BUTTON_SELECTED_WIDTH, button.rect.height + 2 * BUTTON_SELECTED_WIDTH)

        rectangle = pygame.Rect(rect_pos, rect_size)

        pygame.draw.rect(screen, RED, rectangle, width=2 * BUTTON_SELECTED_WIDTH)

    def _validate_click(self):
        # Verifica em qual botão clicou
        for button in self.buttons_group:
            if button.update():
                return button.value


class MainMenu(Menu):

    def __init__(self, image_path, x_y, scale_size):
        super().__init__(image_path, x_y, scale_size)

        # Adiciona o background
        self.background = entity.Entity(TEXTURE_MENU_PATH + "background.png", (0, 0), (WIDTH, HEIGHT))

        # Define os botões dessa tela
        pos_x = WIDTH*0.27 + BUTTON_X / 2
        pos_y =  HEIGHT*0.8 + BUTTON_Y / 2
        buff = 0.0243 * WIDTH

        btn_the_grid = Button(
            TEXTURE_MENU_PATH + "jogar_logo.png",
            (pos_x, pos_y),
            (BUTTON_X, BUTTON_Y),
            4,
        )
        btn_tutorial = Button(
            TEXTURE_MENU_PATH + "tutorial_logo.png",
            (btn_the_grid.rect.right + CARD_X + buff, pos_y),
            (BUTTON_X, BUTTON_Y),
            2,
        )
        btn_options = Button(
            TEXTURE_MENU_PATH + "opcoes_logo.png",
            (btn_tutorial.rect.right + CARD_X + buff, pos_y),
            (BUTTON_X, BUTTON_Y),
            3,
        )
        btn_credits = Button(
            TEXTURE_MENU_PATH + "creditos_logo.png",
            (WIDTH*0.817 + CARD_X / 2, HEIGHT*0.037 + CARD_Y / 2),
            (BUTTON_X, BUTTON_Y),
            8,
        )

        # Adiciona os botões a um grupo
        self.buttons_group = pygame.sprite.Group(
            btn_the_grid, btn_options, btn_credits, btn_tutorial
        )

    def draw(self, screen):
        # Exibe o background e a logo do jogo
        screen.blit(self.background.image, self.background.rect)
        screen.blit(self.image, self.rect)

        # Insere os botões na tela
        self.buttons_group.draw(screen)

    def update(self):
        # Loop dos eventos principais
        for event in pygame.event.get():
            # Valida o fechamento
            if event.type == pygame.QUIT:
                return -1

            if event.type == pygame.KEYDOWN:
                # ESC
                if event.key == pygame.K_ESCAPE:
                    return -1

            # Clique dos botões
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    return self._validate_click()


class OptionsMenu(Menu):
    def __init__(self, image_path, x_y, scale_size, state):
        super().__init__(image_path, x_y, scale_size)
        self.state = state

        # Define variáveis com valores recorrentes no menu
        self.button_size = (75, 75)
        vol_space = self.button_size[0] + 0.025*WIDTH
        vol_y = HEIGHT * 0.395
        vol_x = WIDTH / 2
        vol_position = tuple((vol_x + x * vol_space, vol_y) for x in range(0, 5))

        # Define os botões dessa tela
        self.btn_back = Button(
            TEXTURE_MENU_PATH + "back_button.png",
            (WIDTH / 2, HEIGHT - BUTTON_Y / 2),
            (BUTTON_Y * 2.6742, BUTTON_Y),
            1,
        )
        self.btn_vol_1 = Button(
            TEXTURE_MENU_PATH + "square_empty.png",
            vol_position[0],
            self.button_size,
            1,
        )
        self.btn_vol_2 = Button(
            TEXTURE_MENU_PATH + "square_empty.png",
            vol_position[1],
            self.button_size,
            2,
        )
        self.btn_vol_3 = Button(
            TEXTURE_MENU_PATH + "square_full.png",
            vol_position[2],
            self.button_size,
            3,
        )
        self.btn_vol_4 = Button(
            TEXTURE_MENU_PATH + "square_empty.png",
            vol_position[3],
            self.button_size,
            4,
        )
        self.btn_vol_5 = Button(
            TEXTURE_MENU_PATH + "square_empty.png",
            vol_position[4],
            self.button_size,
            5,
        )

        # Mais botões
        vol_y = HEIGHT * 0.5833
        self.more_buttons_group = pygame.sprite.Group()
        self.btn_fs = Button(TEXTURE_MENU_PATH + "square_full.png", (vol_position[2][0], vol_y), self.button_size, FULLSCREEN)

        vol_y = HEIGHT * 0.7777
        self.bot_buttons_group = pygame.sprite.Group()
        btn_bot_2 = Button("2", (vol_position[1][0], vol_y), self.button_size, 1)
        btn_bot_3 = Button("3", (vol_position[2][0], vol_y), self.button_size, 2)
        btn_bot_4 = Button("4", (vol_position[3][0], vol_y), self.button_size, 3)
        self.btn_select = Button(TEXTURE_MENU_PATH + "square_empty.png", btn_bot_4.rect.center, self.button_size, 1)

        # Adiciona os botões a um grupo
        self.buttons_group.add(self.btn_back)
        self.bot_buttons_group.add(btn_bot_2, btn_bot_3, btn_bot_4)
        self.more_buttons_group.add(self.btn_fs, self.btn_select)

        self.volume_group = pygame.sprite.Group()
        self.volume_group.add(
            self.btn_vol_1,
            self.btn_vol_2,
            self.btn_vol_3,
            self.btn_vol_4,
            self.btn_vol_5,
        )

    def draw(self, screen):
        # Exibe o menu
        screen.blit(self.image, self.rect)

        # Exibe a imagem das opções
        self.options_group.draw(screen)
        self.buttons_group.draw(screen)

        # O nº de jogadores
        self.draw_text("2", 35, self.bot_buttons_group.sprites()[0].rect.centerx, self.bot_buttons_group.sprites()[0].rect.centery, screen)
        self.draw_text("3", 35, self.bot_buttons_group.sprites()[1].rect.centerx, self.bot_buttons_group.sprites()[0].rect.centery, screen)
        self.draw_text("4", 35, self.bot_buttons_group.sprites()[2].rect.centerx, self.bot_buttons_group.sprites()[0].rect.centery, screen)
        self.more_buttons_group.draw(screen)

        # E os volumes
        self.volume_group.draw(screen)

        # Desenha o contorno
        self.choice_preview(screen)

    def update(self):
        # Loop dos eventos principais
        for event in pygame.event.get():
            # Valida o fechamento
            if event.type == pygame.QUIT:
                return -1

            if event.type == pygame.KEYDOWN:
                # ESC
                if event.key == pygame.K_ESCAPE:
                    return 1

            # Clique dos botões
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    return self._validate_click()

    def _validate_click(self):
        # Verifica em qual volume clicou
        for button in self.volume_group:
            if button.update():
                self.change_volume(button.value)
                return 0

        # Ou em qual botao de saida clicou
        for button in self.buttons_group:
            if button.update():
                return button.value
        
        # Ou se mudou a tela
        if self.btn_fs.update():
            self.change_fullscreen()
            return 0
        
        # Ou se mudou os bots
        for button in self.bot_buttons_group:
            if button.update():
                self.btn_select.rect.center = button.rect.center
                self.state.bot_num = button.value

    def choice_preview(self, screen):
        # Verifica se o mouse está em cima do botão
        for button in self.buttons_group:
            if button.update():
                # Desenha o contorno
                self._preview_selected_button(button, screen)

        # E verifica outros botões
        for button in self.volume_group:
            if button.update():
                # Desenha o contorno
                self._preview_selected_button(button, screen)

        # Mais alguns
        if self.btn_fs.update():
            # Desenha o contorno
            self._preview_selected_button(self.btn_fs, screen)

    def change_volume(self, vol):
        # Volume antigo e novo
        temp_vol = int(self.state.volume / 0.15)

        # Muda as imagens
        self.__change_button_image(temp_vol + 1, False)
        self.__change_button_image(vol)

        # Muda o volume
        pygame.mixer.music.set_volume(0.15 * (vol - 1))
        self.state.volume = 0.15 * (vol - 1)

    def __change_button_image(self, num, clicked=True):
        # Decide se vai preencher ou esvaziar
        click = "empty.png"
        if clicked:
            click = "full.png"

        # Cria a imagem
        img = pygame.image.load(TEXTURE_MENU_PATH + "square_" + click).convert_alpha()
        img = pygame.transform.smoothscale(img, self.button_size)

        # E altera
        exec("self.btn_vol_" + str(num) + ".image = img", None, locals())

    def change_fullscreen(self):
        # Muda o botão
        click = "full.png"
        if self.btn_fs.value:
            click = "empty.png"

        self.btn_fs.image = pygame.image.load(TEXTURE_MENU_PATH + "square_" + click).convert_alpha()
        self.btn_fs.image = pygame.transform.smoothscale(self.btn_fs.image, self.button_size)
        
        self.btn_fs.value = not self.btn_fs.value
        pygame.display.toggle_fullscreen()


class TutorialScreen(Menu):

    def __init__(self, image_path, x_y, scale_size):
        super().__init__(image_path, x_y, scale_size)

        # Atributos de interesse
        self._page = 1
        self.__page_num = 2

        # Carrega as imagens que serão usadas
        self.page_1 = entity.Entity(TEXTURE_MENU_PATH + "tutorial_1.png", (0, 0), (WIDTH, HEIGHT))
        self.page_2 = entity.Entity(TEXTURE_MENU_PATH + "tutorial_2.png", (0, 0), (WIDTH, HEIGHT))

        # Define os botões dessa tela
        self.btn_right = Button(
            TEXTURE_MENU_PATH + "right_arrow.png",
            (WIDTH * 9 / 10, HEIGHT / 2),
            (WIDTH / 5, HEIGHT),
            21,
        )
        self.btn_left = Button(
            TEXTURE_MENU_PATH + "left_arrow.png",
            (WIDTH / 10, HEIGHT / 2),
            (WIDTH / 5, HEIGHT),
            20,
        )

        # Adiciona os botões a um grupo
        self.buttons_group.add(self.btn_left, self.btn_right)

    def draw(self, screen):
        # Botões
        self.buttons_group.draw(screen)

        # Telas de tutorial
        if self._page == 1:
            screen.blit(self.page_1.image, self.page_1.rect)
        elif self._page == 2:
            screen.blit(self.page_2.image, self.page_2.rect)

        # Exibe o número da página
        self.__draw_text(str(self._page), 40, WIDTH - 100, HEIGHT - 65, 20,screen)

    def update(self):
        # Loop dos eventos principais
        for event in pygame.event.get():
            # Valida o fechamento
            if event.type == pygame.QUIT:
                return -1

            if event.type == pygame.KEYDOWN:
                # ESC
                if event.key == pygame.K_ESCAPE:
                    return 1
                
                # Verifica se saiu do menu
                if event.key == pygame.K_RIGHT and self._page == self.__page_num:
                    return 1
                
                if event.key == pygame.K_LEFT and self._page == 1:
                    return 1
                
                # RIGHT
                if event.key == pygame.K_RIGHT and self._page < self.__page_num:
                    self.__change_page(True)

                # LEFT
                if event.key == pygame.K_LEFT and self._page > 1:
                    self.__change_page(False)

            # Clique dos botões
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    return self._validate_click()
                
        return 0

    def _validate_click(self):
        # Verifica em qual direção clicou
        for button in self.buttons_group:
            if button.update():
                # Se clicar para a direita
                if button.value == 21:
                    return self.__change_page(True)

                # Se clicar para a esquerda
                if button.value == 20:
                    return self.__change_page(False)

    def __change_page(self, right=True):
        # Clique para a direita
        if self._page < self.__page_num and right:
            # Muda de página
            self._page += 1
            return 0

        # Clique para a esquerda
        if self._page >= 2 and not right:
            # Muda a página
            self._page -= 1
            return 0

        # Caso saia do menu pela direita
        if self._page == self.__page_num and right:
            return 1
        
        # Caso saia do menu pela esquerda
        if self._page == 1 and not right:
            return 1

    def __draw_text(self, text, size, x, y, max_line_length, screen):
        # Cria o texto separado em linhas de uma lista
        lines = textwrap.wrap(text, width=max_line_length)

        # Carrega a fonte e cria um buff para offset
        font = pygame.font.Font(FONTS_PATH + "terminator.otf", size)
        y_offset = 0

        # Laceia cada linha, criando sua surface e fazendo blit
        for line in lines:
            text_surface = font.render(line, True, WHITE)
            text_rect = text_surface.get_rect()
            text_rect.center = (x, y + y_offset)

            screen.blit(text_surface, text_rect)
            y_offset += text_rect.height + 10


class ResultScreen(Menu):

    def __init__(self, image_path, x_y, scale_size):
        super().__init__(image_path, x_y, scale_size)

        # Define a fonte a ser usada
        self.font_name = FONTS_PATH + "tron.ttf"

        # Define os botões dessa tela
        self.btn_menu = Button(
            TEXTURE_MENU_PATH + "to_menu_button.png",
            (WIDTH / 2, HEIGHT - 200),
            (BUTTON_X, BUTTON_Y),
            1,
        )
        self.btn_exit = Button(
            TEXTURE_MENU_PATH + "exit_button.png",
            (WIDTH / 2, HEIGHT - 100),
            (BUTTON_X, BUTTON_Y),
            -1,
        )

        # Adiciona os botões a um grupo
        self.buttons_group.add(self.btn_menu, self.btn_exit)

    def draw(self, screen):
        # Mostra a logo desta tela
        screen.blit(self.image, self.rect)

        # Desenha o texto
        self.draw_text("Select your", 40, WIDTH / 2, HEIGHT / 2 - 40, screen)
        self.draw_text("next action :", 40, WIDTH / 2, HEIGHT / 2 + 40, screen)

        # Insere os botões na tela:
        self.buttons_group.draw(screen)

        # Desenha o contorno
        self.choice_preview(screen)

    def update(self):
        # Loop dos eventos principais
        for event in pygame.event.get():
            # Valida o fechamento
            if event.type == pygame.QUIT:
                return -1

            if event.type == pygame.KEYDOWN:
                # ESC
                if event.key == pygame.K_ESCAPE:
                    return 1

            # Clique dos botões
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    return self._validate_click()


class CreditsMenu(Menu):

    def __init__(self, image_path, x_y, scale_size):
        super().__init__(image_path, x_y, scale_size)

        # Define os botões dessa tela
        btn_back = Button(
            TEXTURE_MENU_PATH + "back_button.png",
            (WIDTH / 2, HEIGHT - BUTTON_Y / 2),
            (BUTTON_Y * 2.6742, BUTTON_Y),
            1,
        )

        # Adiciona os botões a um grupo
        self.buttons_group.add(btn_back)

    def draw(self, screen):
        # Exibe a imagem "credits"
        screen.blit(self.image, self.rect)

        # Insere os botões na tela:
        self.buttons_group.draw(screen)

        # Desenha o contorno
        self.choice_preview(screen)

    def update(self):
        # Loop dos eventos principais
        for event in pygame.event.get():
            # Valida o fechamento
            if event.type == pygame.QUIT:
                return -1

            if event.type == pygame.KEYDOWN:
                # ESC
                if event.key == pygame.K_ESCAPE:
                    return 1

            # Clique dos botões
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    return self._validate_click()


class LoadingScreen(Menu):

    def __init__(self, image_path, x_y, scale_size, state):
        super().__init__(image_path, x_y, scale_size)
        self.__state = state

        # Configura a fonte e o texto inicial
        self.__font = pygame.font.Font(FONTS_PATH + "zig.ttf", 40)
        self.__text = "Carregando"

        # Cria um evento para a animação
        self.__clock = pygame.event.custom_type()
        pygame.time.set_timer(self.__clock, 500, 5)
    
    def draw(self, screen):
        # Mostra a logo desta tela
        screen.fill((0, 0, 0))

        # Desenha o texto
        self.draw_text(self.__text, WIDTH * 0.05, HEIGHT * 0.9, screen)

    def update(self):
        # Loop dos eventos principais
        for event in pygame.event.get():
            # Valida o fechamento
            if event.type == pygame.QUIT:
                return -1
            
            # Atualiza o texto
            if event.type == self.__clock:
                self.__text += "."

        # Quando tiver acabado a animação, carrega o jogo
        if self.__text.endswith("....."):
            self.__state._load()
            return 1

        return 0
    
    def draw_text(self, text, x, y, screen):
        # Cria uma superficie com o texto nela
        text_surface = self.__font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)

        # Põe na tela
        screen.blit(text_surface, text_rect)
