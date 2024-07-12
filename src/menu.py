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
            font = pygame.font.Font(FONTS_PATH + "DOSVGA2.ttf", 30)

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

        # Cria o "botão" de seleção
        font = pygame.font.Font(FONTS_PATH + "DOSVGA2.ttf", 30)
        self.__selected = font.render("> ", True, WHITE)

        # Muda o titulo
        self.image = font.render("SolarOS 4.0.1 Generic_50203-02 sun4m i386 Unknown.Unknown", True, WHITE)
        self.rect.left = 50

        # E extras
        self.__pretitle = font.render("Vectrun:\> dir", True, WHITE)

        # Define os botões dessa tela
        btn_the_grid = Button(
            "grid.exe",
            (100, HEIGHT / 2),
            (BUTTON_X, BUTTON_Y),
            4,
        )
        btn_tutorial = Button(
            "tutorial.txt",
            (100, HEIGHT / 2 + 100),
            (BUTTON_X, BUTTON_Y),
            2,
        )
        btn_options = Button(
            "options.txt",
            (100, HEIGHT / 2 + 200),
            (BUTTON_X, BUTTON_Y),
            3,
        )
        btn_credits = Button(
            "credits.txt",
            (100, HEIGHT / 2 + 300),
            (BUTTON_X, BUTTON_Y),
            8,
        )

        btn_credits.rect.left = 80
        btn_options.rect.left = 80
        btn_tutorial.rect.left = 80
        btn_the_grid.rect.left = 80

        # Adiciona os botões a um grupo
        self.buttons_group = pygame.sprite.Group(
            btn_the_grid, btn_options, btn_credits, btn_tutorial
        )

    def draw(self, screen):
        # Exibe o logo do jogo
        screen.blit(self.image, self.rect)
        screen.blit(self.__pretitle, (50, HEIGHT/2 - 100))

        # Insere os botões na tela
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
                    return -1

            # Clique dos botões
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    return self._validate_click()

    def _preview_selected_button(self, button, screen):
        # Desenha > atrás da seleção
        screen.blit(self.__selected, (button.rect.left - 35, button.rect.top))


class OptionsMenu(Menu):
    def __init__(self, image_path, x_y, scale_size, state):
        super().__init__(image_path, x_y, scale_size)
        self.state = state

        # Define variáveis com valores recorrentes no menu
        vol_space = 80
        vol_y = HEIGHT / 3 + 30
        vol_x = WIDTH / 3 + 5
        vol_position = tuple((vol_x + x * vol_space, vol_y) for x in range(2, 7))

        # Carrega as imagens a exibir
        volume_logo = Button(
            TEXTURE_MENU_PATH + "volume_text.png",
            (vol_x - 30, vol_y),
            (BUTTON_X, BUTTON_Y),
            0,
        )
        volume_logo.rect = volume_logo.image.get_rect(center=(vol_x - 30, vol_y))

        # Define os botões dessa tela
        self.btn_back = Button(
            TEXTURE_MENU_PATH + "back_button.png",
            (WIDTH / 2, (HEIGHT - 100)),
            (BUTTON_X, BUTTON_Y),
            1,
        )
        self.btn_vol_1 = Button(
            TEXTURE_MENU_PATH + "square_empty.png",
            vol_position[0],
            (50, 50),
            1,
        )
        self.btn_vol_2 = Button(
            TEXTURE_MENU_PATH + "square_empty.png",
            vol_position[1],
            (50, 50),
            2,
        )
        self.btn_vol_3 = Button(
            TEXTURE_MENU_PATH + "square_full.png",
            vol_position[2],
            (50, 50),
            3,
        )
        self.btn_vol_4 = Button(
            TEXTURE_MENU_PATH + "square_empty.png",
            vol_position[3],
            (50, 50),
            4,
        )
        self.btn_vol_5 = Button(
            TEXTURE_MENU_PATH + "square_empty.png",
            vol_position[4],
            (50, 50),
            5,
        )

        # Mais botões
        self.more_buttons_group = pygame.sprite.Group()
        self.btn_fs = Button(TEXTURE_MENU_PATH + "square_full.png", (vol_position[2][0], vol_y + vol_space), (50, 50), 0)

        self.bot_buttons_group = pygame.sprite.Group()
        btn_bot_1 = Button("1", (vol_position[0][0], vol_y + 2 * vol_space), (50, 50), 1)
        btn_bot_2 = Button("2", (vol_position[1][0], vol_y + 2 * vol_space), (50, 50), 2)
        btn_bot_3 = Button("3", (vol_position[2][0], vol_y + 2 * vol_space), (50, 50), 3)
        self.btn_select = Button(TEXTURE_MENU_PATH + "square_empty.png", btn_bot_3.rect.center, (50, 50), 1)

        # Adiciona os botões a um grupo
        self.options_group.add(volume_logo)
        self.buttons_group.add(self.btn_back)
        self.bot_buttons_group.add(btn_bot_1, btn_bot_2, btn_bot_3)
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
        # Exibe a imagem "Options"
        screen.blit(self.image, self.rect)

        # Exibe a imagem das opções
        self.options_group.draw(screen)
        self.buttons_group.draw(screen)

        self.bot_buttons_group.draw(screen)
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
        img = pygame.transform.smoothscale(img, (50, 50))

        # E altera
        exec("self.btn_vol_" + str(num) + ".image = img", None, locals())

    def change_fullscreen(self):
        # Muda o botão
        click = "full.png"
        if self.btn_fs.value:
            click = "empty.png"

        self.btn_fs.image = pygame.image.load(TEXTURE_MENU_PATH + "square_" + click).convert_alpha()
        self.btn_fs.image = pygame.transform.smoothscale(self.btn_fs.image, (50, 50))
        
        self.btn_fs.value = not self.btn_fs.value
        pygame.display.toggle_fullscreen()


class TutorialScreen(Menu):

    def __init__(self, image_path, x_y, scale_size):
        super().__init__(image_path, x_y, scale_size)

        # Atributos de interesse
        self.__page = 1
        self.__page_num = 3
        self.__font_size = 19

        # Variáveis de posicionamento
        self.__size = 200
        self.__img_x = WIDTH / 2 - self.__size / 2
        self.__img_y = 360
        self.__space = 120

        # Define a fonte a ser usada
        self.font_name = FONTS_PATH + "tron.ttf"

        # Carrega as imagens que serão usadas
        img_wall = entity.Entity(
            IMG_MANUAL_PATH + "collision_with_side_walls.png",
            (self.__img_x - self.__size - self.__space, self.__img_y),
            (self.__size, self.__size),
        )
        img_moto = entity.Entity(
            IMG_MANUAL_PATH + "intersection_with_motorcycle.png",
            (self.__img_x, self.__img_y),
            (self.__size, self.__size),
        )
        img_line = entity.Entity(
            IMG_MANUAL_PATH + "intersection_with_the_line.png",
            (self.__img_x + self.__size + self.__space, self.__img_y),
            (self.__size, self.__size),
        )

        self.__imgs = pygame.sprite.Group(img_moto, img_line, img_wall)

        # Define os botões dessa tela
        self.btn_right = Button(
            TEXTURE_MENU_PATH + "right_arrow.png",
            (WIDTH - 70, HEIGHT / 2),
            (60, 60),
            21,
        )
        self.btn_left = Button(
            TEXTURE_MENU_PATH + "left_arrow.png",
            (70, HEIGHT / 2),
            (60, 60),
            20,
        )

        self.btn_back = Button(
            TEXTURE_MENU_PATH + "back_button.png",
            (WIDTH / 2, HEIGHT - 80),
            (BUTTON_X, BUTTON_Y),
            1,
        )

        # Adiciona os botões a um grupo
        self.buttons_group.add(self.btn_back, self.btn_right)

    def draw(self, screen):
        # Exibe a logo e os botões principais
        screen.blit(self.image, self.rect)
        self.buttons_group.draw(screen)

        # Telas de tutorial
        if self.__page == 1:
            self.__draw_text(
                txt.txt_regra_1, self.__font_size, WIDTH / 2, 210, 55, screen
            )
            self.__draw_text(
                txt.txt_regra_2, self.__font_size, WIDTH / 2, 440, 55, screen
            )
        elif self.__page == 2:
            self.__draw_text(
                txt.txt_regra_3, self.__font_size, WIDTH / 2, 210, 55, screen
            )
            self.__draw_text(
                txt.txt_regra_4, self.__font_size, WIDTH / 2, 440, 55, screen
            )
        else:
            new_y = self.__img_y - 60
            new_x = self.__img_x + self.__size / 2
            new_space = self.__space + self.__size

            self.__draw_text(
                txt.txt_regra_5, self.__font_size, WIDTH / 2, 210, 55, screen
            )
            self.__draw_text(
                txt.txt_collision_1, self.__font_size, new_x - new_space, new_y, 12, screen
            )
            self.__draw_text(txt.txt_collision_2, self.__font_size, new_x, new_y, 12, screen)
            self.__draw_text(
                txt.txt_collision_3, self.__font_size, new_x + new_space, new_y, 12, screen
            )

            # Imagens de colisões
            self.__imgs.draw(screen)

        # Exibe o número da página
        self.__draw_text(str(self.__page), 30, WIDTH - 100, HEIGHT - 75, 20,screen)

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
                
                # RIGHT
                if event.key == pygame.K_RIGHT and self.__page < self.__page_num:
                    self.__change_page(True)

                # LEFT
                if event.key == pygame.K_LEFT and self.__page > 1:
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
                    self.__change_page(True)
                    return 0

                # Se clicar para a esquerda
                if button.value == 20:
                    self.__change_page(False)
                    return 0

                # Se tiver sido nenhum, retorna
                return button.value

    def __change_page(self, right=True):
        # Adiciona o botão esquerdo para exibi-lo se necessário
        if self.__page == 1:
            self.buttons_group.add(self.btn_left)

        # Adiciona o botão direito para exibi-lo se necessário
        if self.__page == self.__page_num:
            self.buttons_group.add(self.btn_right)

        # Clique para a direita
        if self.__page < self.__page_num and right:
            # Muda de página
            self.__page += 1

            # Remove o botão direito para deixar de exibi-lo se atingir a última página
            if self.__page == self.__page_num:
                self.buttons_group.remove(self.btn_right)

        # Clique para a esquerda
        if self.__page >= 2 and not right:
            # Muda a página
            self.__page -= 1

            # Remove o botão esquerdo para deixar de exibi-lo
            if self.__page == 1:
                self.buttons_group.remove(self.btn_left)

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
            (WIDTH / 2, (HEIGHT - 100)),
            (BUTTON_X, BUTTON_Y),
            1,
        )

        # Adiciona os botões a um grupo
        self.buttons_group.add(btn_back)

    def draw(self, screen):
        # Exibe a imagem "credits"
        screen.blit(self.image, self.rect)

        # Insere os botões na tela:
        self.buttons_group.draw(screen)

        # Define variáveis com valores recorrentes no menu
        font_size = [20, 24, 30]
        space_size = [40, 30]
        txt_x = WIDTH / 2
        txt_y = HEIGHT / 4 + 20

        # Desenha os textos na tela
        self.draw_text("VECTRUN", font_size[2], txt_x, txt_y, screen)
        self.draw_text(
            "Art, concept and design",
            font_size[1],
            txt_x,
            (txt_y + 2 * space_size[0]), screen
        )
        self.draw_text(
            "Tulio Konecny",
            font_size[0],
            txt_x,
            (txt_y + 3 * space_size[0]), screen
        )
        self.draw_text(
            "Programming",
            font_size[1],
            txt_x,
            (txt_y + 5 * space_size[0]), screen
        )
        self.draw_text(
            "Beatriz Miranda Bezerra",
            font_size[0],
            txt_x,
            (txt_y + 6 * space_size[0]), screen
        )
        self.draw_text(
            "Gustavo Murilo Cavalcante Carvalho",
            font_size[0],
            txt_x,
            (txt_y + 7 * space_size[0]), screen
        )
        self.draw_text(
            "Henzo Felipe Carvalho de Mattos",
            font_size[0],
            txt_x,
            (txt_y + 8 * space_size[0]), screen
        )

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
        self.rect = self.image.get_rect(topleft=x_y)
        self.__state = state

        # Configura a fonte e o texto inicial
        self.__font = pygame.font.Font(FONTS_PATH + "zig.ttf", 40)
        self.__text = "Loading"

        # Cria um evento para a animação
        self.__clock = pygame.USEREVENT + 5
        pygame.time.set_timer(self.__clock, 8, 125)

        # Carrega o rider
        self.__rider = entity.Entity(RIDER_PATH + "rider_1.png", (0, 0), (RIDER_X * 0.6, RIDER_Y * 0.6))
        self.__rider.rect.center = (-30, HEIGHT * 0.9 - RIDER_Y * 0.6)
    
    def draw(self, screen):
        # Mostra a logo desta tela
        screen.blit(self.image, self.rect)

        # Desenha o texto
        self.draw_text(self.__text, WIDTH * 0.72, HEIGHT * 0.9, screen)

        # Desenha o rider e sua linha
        pygame.draw.line(screen, "#258dc2", (-30, HEIGHT * 0.9 - RIDER_Y * 0.6), self.__rider.rect.center, 3)
        screen.blit(self.__rider.image, self.__rider.rect)

    def update(self):
        # Loop dos eventos principais
        for event in pygame.event.get():
            # Valida o fechamento
            if event.type == pygame.QUIT:
                return -1
            
            # Atualiza a animação
            if event.type == self.__clock:
                self.__rider.rect.centerx += 2

        # Quando tiver acabado a animação, carrega o jogo
        if self.__rider.rect.centerx == 220:
            self.__state._load()
            self.__rider.rect.centerx += 2

        # Quando acabar o loading, termina a animação
        if self.__rider.rect.centerx == 222:
            pygame.time.set_timer(self.__clock, 5, 800)

        # Quando acabar a animação, troca de tela
        if self.__rider.rect.left > WIDTH + 10:
            return 1

        return 0
    
    def draw_text(self, text, x, y, screen):
        # Cria uma superficie com o texto nela
        text_surface = self.__font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)

        # Põe na tela
        screen.blit(text_surface, text_rect)