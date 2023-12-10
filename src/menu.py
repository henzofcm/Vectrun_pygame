import pygame
from config import *
from entity import *
from texts import *
import textwrap

class Button(Entity):
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
    def __init__(self, image_path, x_y, scale_size, label):
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
        super().__init__(image_path, x_y, scale_size)
        self.label = label
        self.rect = self.image.get_rect(center=x_y)
        self.selected = False

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
        mouse_pos = pygame.mouse.get_pos()
        is_over = self.rect.collidepoint(mouse_pos)

        if is_over:
            return True
        else:
            return False


class Menu(Entity):
    """
    Represents a menu.
    
    Attributes
    ----------
    state_control : Game
        The game object that controls the menu.
    rect : Rect
        The rectangle that represents the menu's position and size.
    run_display : bool
        Indicates whether the menu is running or not.
    button_clicked : bool
        Indicates whether a button was clicked or not.
    selected_button : Button
        The button that was selected.
    buttons_group : Group
        The group of buttons for the menu.
    
    Methods
    -------
    __init__(self, game, image_path, x_y, scale_size)
        Initializes a Menu object.
    draw_text(self, text, size, x, y)
        Draw text on the screen.
    update(self)
        Update the state of the menu.
    verify(self)
        Verify the state of the menu.
    choice_preview(self, screen)
        Preview the selected choice.
    __preview_selected_button(self, button, screen)
        Preview the selected button.
    check_input(self)
        Check the input for the menu.
    """
    def __init__(self, game, image_path, x_y, scale_size):
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

        self.state_control = game
        self.rect = self.image.get_rect(center=x_y)

        # Define a fonte a ser usada
        self.font_name = pygame.font.get_default_font()

        # Define variáveis de controle
        self.run_display = True
        self.button_clicked = False
        self.selected_button = None

        # Cria um grupo para os sprites
        self.buttons_group = pygame.sprite.Group()

    def draw_text(self, text, size, x, y ):
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
        self.font_name = pygame.font.get_default_font()
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.state_control.screen.blit(text_surface, text_rect)

    def update(self):
        """
        Update the state of the menu.
        
        Returns
        -------
        None
        """
        pygame.display.update()
        self.state_control.reset_keys()
    
    def verify(self):
        """ 
        Verify the state of the menu.
        
        Returns
        -------
        None
        """
        self.state_control.check_events()
        self.choice_preview(self.state_control.screen)
        self.check_input()

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
        # Verifica se o mouse está em cima da carta
        for button in self.buttons_group:
            if button.update():
                # Seleciona a tela equivalente ao botão
                self.action = button.label

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

    def check_input(self):
        """
        Check the input for the menu.
        
        Returns
        -------
        None
        """
        pass


class MainMenu(Menu):
    """
    Represents the main menu.
    
    Attributes
    ----------
    next_state : str
        The next state to transition to.
    start_x : int
        The x coordinate of the start button.
    start_y : int
        The y coordinate of the start button.
    options_x : int
        The x coordinate of the options button.
    options_y : int
        The y coordinate of the options button.
    credits_x : int
        The x coordinate of the credits button.
    credits_y : int
        The y coordinate of the credits button.
    btn_the_grid : Button
        The button to transition to the grid.
    btn_options : Button
        The button to transition to the options menu.
    btn_credits : Button
        The button to transition to the credits menu.
    buttons_group : Group
        The group of buttons for the menu.
    
    Methods
    -------
    __init__(self, game, image_path, x_y, scale_size)
        Initializes a MainMenu object.
    display_menu(self)
        Display the main menu.
    check_input(self)
        Check the input for the menu.
    """
    def __init__(self, game, image_path, x_y, scale_size):
        """
        Initializes a MainMenu object.
        
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
        super().__init__(game, image_path, x_y, scale_size)
        self.action = "the_grid"

        # Posições para os elementos na tela
        self.start_x, self.start_y = (WIDTH/2), (HEIGHT/2)
        self.options_x, self.options_y = (WIDTH/2), (HEIGHT/2 + 100)
        self.credits_x, self.credits_y = (WIDTH/2), (HEIGHT/2 + 200)

        # Define os botões dessa tela
        self.btn_the_grid = Button(TEXTURE_MENU_PATH + "grid_logo.png", (self.start_x, self.start_y),
                              (BUTTON_X, BUTTON_Y), "the_grid")
        self.btn_options = Button(TEXTURE_MENU_PATH + "options_button.png", (self.options_x, self.options_y),
                                   (BUTTON_X, BUTTON_Y), "options_menu")
        self.btn_credits = Button(TEXTURE_MENU_PATH + "credits_button.png", (self.credits_x, self.credits_y),
                                   (BUTTON_X, BUTTON_Y), "credits_menu")

        # Adiciona os botões a um grupo
        self.buttons_group = pygame.sprite.Group(self.btn_the_grid, self.btn_options, self.btn_credits)

    def display_menu(self):
        """
        Display the main menu.
        
        Returns
        -------
        None
        """
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
        """
        Check the input for the menu.
        
        Returns
        -------
        None
        """
        if self.state_control.ESC_KEY:
            self.state_control.running = False
            self.state_control.curr_menu.run_display = False

        # Checa os cliques em botões
        if self.state_control.START_KEY or self.state_control.BUTTON_CLICKED:
            if self.action == "the_grid":
                if self.state_control.first_time:
                    # Abre o tutorial antes de iniciar a primeira partida
                    self.state_control.curr_menu = self.state_control.tutorial_screen
                else:
                    self.state_control.playing = True
            elif self.action == "options_menu":
                self.state_control.curr_menu = self.state_control.options_menu
            elif self.action == "credits_menu":
                self.state_control.curr_menu = self.state_control.credits_menu
            self.run_display = False


class OptionsMenu(Menu):
    """
    Represents the options menu.
    
    Attributes
    ----------
    next_state : str
        The next state to transition to.
    btn_back : Button
        The button to transition to the main menu.
    buttons_group : Group
        The group of buttons for the menu.
        
    Methods
    -------
    __init__(self, game, image_path, x_y, scale_size)
        Initializes a OptionsMenu object.
    display_menu(self)
        Display the options menu.
    check_input(self)
        Check the input for the menu.        
    """
    def __init__(self, game, image_path, x_y, scale_size):
        """
        Initializes a OptionsMenu object.
        
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
        super().__init__(game, image_path, x_y, scale_size)
        self.action = "main_menu"

        # Define variáveis com valores recorrentes no menu
        self.vol_space = 80
        self.vol_y = HEIGHT/3 + 30
        self.vol_x = WIDTH/3 + 5
        self.vol_position = (
        (self.vol_x + 2*self.vol_space, self.vol_y), (self.vol_x + 3*self.vol_space, self.vol_y), (self.vol_x + 4*self.vol_space, self.vol_y),
        (self.vol_x + 5*self.vol_space, self.vol_y), (self.vol_x + 6*self.vol_space, self.vol_y))
        self.vol_dict = {"vol_1": 0, "vol_2": 0.25, "vol_3": 0.5, "vol_4": 0.75, "vol_5": 1}

        # Carrega as imagens a exibir
        self.volume_image = Entity(TEXTURE_MENU_PATH + "volume_text.png", (self.vol_x - 30, self.vol_y), (BUTTON_X, BUTTON_Y))
        self.volume_image.rect = self.volume_image.image.get_rect(center=(self.vol_x - 30, self.vol_y))

        # Define os botões dessa tela
        self.btn_back = Button(TEXTURE_MENU_PATH + "back_button.png", (WIDTH / 2, (HEIGHT - 100)),
                               (BUTTON_X, BUTTON_Y), "main_menu")
        self.btn_vol_1 = Button(TEXTURE_MENU_PATH + "square_full.png", self.vol_position[0], (50,50), "vol_1")
        self.btn_vol_2 = Button(TEXTURE_MENU_PATH + "square_full.png", self.vol_position[1], (50, 50), "vol_2")
        self.btn_vol_3 = Button(TEXTURE_MENU_PATH + "square_full.png", self.vol_position[2], (50, 50), "vol_3")
        self.btn_vol_4 = Button(TEXTURE_MENU_PATH + "square_full.png", self.vol_position[3], (50, 50), "vol_4")
        self.btn_vol_5 = Button(TEXTURE_MENU_PATH + "square_full.png", self.vol_position[4], (50, 50), "vol_5")

        # Adiciona os botões a um grupo
        self.buttons_group.add(self.btn_back)
        self.buttons_group.add(self.btn_vol_1, self.btn_vol_2, self.btn_vol_3, self.btn_vol_4, self.btn_vol_5)

    def display_menu(self):
        """
        Display the options menu.
        
        Returns
        -------
        None
        """
        self.run_display = True
        while self.run_display:
            self.state_control.screen.fill(BLACK)
            
            # Verifica as entradas e interação com os botões
            self.verify()

            # Exibe a imagem "Options"
            self.state_control.screen.blit(self.image, self.rect)
            # Exibe a imagem "volume"
            self.state_control.screen.blit(self.volume_image.image, self.volume_image.rect)

            # Insere os botões na tela:
            self.buttons_group.draw(self.state_control.screen)

            self.update()

    def check_input(self):
        """
        Check the input for the menu.
        
        Returns
        -------
        None
        """
        if self.state_control.ESC_KEY:
            self.state_control.curr_menu = self.state_control.main_menu
            self.run_display = False
        if self.state_control.BACK_KEY:
            self.state_control.curr_menu = self.state_control.main_menu
            self.run_display = False
        if self.state_control.START_KEY or self.state_control.BUTTON_CLICKED:
            if self.action in ["vol_1", "vol_2", "vol_3", "vol_4", "vol_5"]:
               self.change_volume(self.action)
            elif self.action == "main_menu":
                self.state_control.curr_menu = self.state_control.main_menu
                self.run_display = False

    def change_volume(self, vol):
        sound = int(vol[-1])
        pygame.mixer.set_volume(0.15 * sound)


class CreditsMenu(Menu):
    """
    Represents the credits menu.
    
    Attributes
    ----------
    next_state : str
        The next state to transition to.
    font_size : list
        The font sizes for the menu.
    space_size : list
        The space sizes for the menu.
    txt_x : int
        The x coordinate of the text.
    txt_y : int
        The y coordinate of the text.
    background_image : Surface  
        The background image for the menu.
    btn_back : Button
        The button to transition to the main menu.
    buttons_group : Group
        The group of buttons for the menu.
        
    Methods
    -------
    __init__(self, game, image_path, x_y, scale_size)
        Initializes a CreditsMenu object.
    display_menu(self)
        Display the credits menu.
    check_input(self)
        Check the input for the menu.
    """
    def __init__(self, game, image_path, x_y, scale_size):
        """
        Initializes a CreditsMenu object.
        
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
        super().__init__(game, image_path, x_y, scale_size)
        self.action = "main_menu"

        # Define a fonte a ser usada
        self.font_name = FONTS_PATH + "tron.ttf"

        # Define variáveis com valores recorrentes no menu
        self.font_size = [17, 20, 25]
        self.space_size = [38, 30]
        self.txt_x = WIDTH / 2
        self.txt_y = HEIGHT / 4 + 20

        # Carrega a imagem da tela de fundo
        self.background_image = Entity(TEXTURE_MENU_PATH + "background_credits.png", (0,0), (1000,750))

        # Define os botões dessa tela
        self.btn_back = Button(TEXTURE_MENU_PATH + "back_button.png", (WIDTH/2, (HEIGHT - 100)),
                                   (BUTTON_X, BUTTON_Y), "main_menu")

        # Adiciona os botões a um grupo
        self.buttons_group.add(self.btn_back)

    def display_menu(self):
        """
        Display the credits menu.
        
        Returns
        -------
        None
        """
        self.run_display = True
        while self.run_display:
            # Exibe o plano de fundo da tela
            self.state_control.screen.blit(self.background_image.image, self.background_image.rect)

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
            self.draw_text("Tulio Konecny", self.font_size[0], self.txt_x, (self.txt_y + 8*self.space_size[0]))

            # Atualiza a tela
            self.update()

    def check_input(self):
        """
        Check the input for the menu.
        
        Returns
        -------
        None
        """
        if self.state_control.ESC_KEY:
            self.state_control.curr_menu = self.state_control.main_menu
            self.run_display = False
        if self.state_control.BACK_KEY:
            self.state_control.curr_menu = self.state_control.main_menu
            self.run_display = False
        if self.state_control.START_KEY or self.state_control.BUTTON_CLICKED:
            if self.action == "main_menu":
                self.state_control.curr_menu = self.state_control.main_menu
            elif self.action == "scree_1":
                pass
            elif self.action == "screen_2":
                pass
            else:
                self.state_control.curr_menu = self.state_control.main_menu
            self.run_display = False


class ResultScreen(Menu):
    """
    Represents the result screen.
    
    Attributes
    ----------
    next_state : str
        The next state to transition to.
    
    Methods
    -------
    __init__(self, game, image_path, x_y, scale_size)
        Initializes a ResultScreen object.
    display_menu(self)
        Display the result screen.
    check_input(self)
        Check the input for the menu.
    """
    def __init__(self, game, image_path, x_y, scale_size):
        """
        Initializes a ResultScreen object.
        
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
        super().__init__(game, image_path, x_y, scale_size)
        self.action = "main_menu"

        # Define a fonte a ser usada
        self.font_name = FONTS_PATH + "tron.ttf"

        # Define os botões dessa tela
        self.btn_menu = Button(TEXTURE_MENU_PATH + "to_menu_button.png", (WIDTH/2, HEIGHT-200),
                               (BUTTON_X, BUTTON_Y), "main_menu")
        self.btn_exit = Button(TEXTURE_MENU_PATH + "exit_button.png", (WIDTH/2, HEIGHT-100),
                               (BUTTON_X, BUTTON_Y), "exit")

        # Adiciona os botões a um grupo
        self.buttons_group.add(self.btn_menu, self.btn_exit)

    def display_menu(self):
        """
        Display the result screen.
        
        Returns
        -------
        None
        """
        self.run_display = True
        while self.run_display:
            self.state_control.screen.fill(BLACK)

            # Verifica as entradas e interação com os botões
            self.verify()

            self.state_control.screen.blit(self.image, self.rect)

            self.draw_text("Select your", 40, WIDTH/2, HEIGHT/2 - 40)
            self.draw_text("next action :", 40, WIDTH/2, HEIGHT/2 + 40)

            # Insere os botões na tela:
            self.buttons_group.draw(self.state_control.screen)

            self.update()

    def check_input(self):
        """
        Check the input for the menu.
        
        Returns
        -------
        None
        """
        if self.state_control.ESC_KEY:
            self.state_control.curr_menu = self.state_control.main_menu
            self.run_display = False
        if self.state_control.BACK_KEY:
            self.state_control.curr_menu = self.state_control.main_menu
            self.run_display = False
        if self.state_control.START_KEY or self.state_control.BUTTON_CLICKED:
            if self.action == "main_menu":
                self.state_control.curr_menu = self.state_control.main_menu
            if self.action == "exit":
                self.state_control.running = False
                self.state_control.curr_menu.run_display = False
            self.run_display = False


class TutorialScreen(Menu):
    """
    Represents the tutorial screen.
    
    Attributes
    ----------
    next_state : str
        The next state to transition to.
        
    Methods
    -------
    __init__(self, game, image_path, x_y, scale_size)
        Initializes a TutorialScreen object.
    display_menu(self)
        Display the tutorial screen.
    check_input(self)
        Check the input for the menu.
    """
    def __init__(self, game, image_path, x_y, scale_size):
        """
        Initializes a TutorialScreen object.
        
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
        super().__init__(game, image_path, x_y, scale_size)
        self.action = "right_arrow"
        self.page = 1
        self.num_of_pages = 3
        self.tutorial_read = False

        # Definição de variáveis
        self.font_size = 25
        self.img_x = 150
        self.img_y = 360
        self.space_img = 100

        # Define a fonte a ser usada
        self.font_name = FONTS_PATH + "tron.ttf"

        # Carrega as imagens que serão usadas
        self.img_wall = Entity(IMG_MANUAL_PATH + "collision_with_side_walls.png",
                               (self.img_x, self.img_y), (200, 200))
        self.img_moto = Entity(IMG_MANUAL_PATH + "intersection_with_motorcycle.png",
                               (2*self.img_x + self.space_img, self.img_y), (200, 200))
        self.img_line = Entity(IMG_MANUAL_PATH + "intersection_with_the_line.png",
                               (3*self.img_x + 2*self.space_img, self.img_y), (200, 200))

        # Define os botões dessa tela
        self.btn_play = Button(TEXTURE_MENU_PATH + "play_button.png", (WIDTH/2, HEIGHT-80),
                               (BUTTON_X, BUTTON_Y), "play")
        self.btn_right = Button(TEXTURE_MENU_PATH + "right_arrow.png", (WIDTH - 70, HEIGHT/2),
                               (60, 60), "right_arrow")
        self.btn_left = Button(TEXTURE_MENU_PATH + "left_arrow.png", (70, HEIGHT/2),
                                (60, 60), "left_arrow")

        # Adiciona os botões a um grupo
        self.buttons_group.add(self.btn_right)

    def display_menu(self):
        """
        Display the tutorial screen.
        
        Returns
        -------
        None
        """
        self.run_display = True
        while self.run_display:
            self.state_control.screen.fill(BLACK)

            # Verifica as entradas e interação com os botões
            self.verify()
            
            # Exibe a imagem "Tutorial"
            self.state_control.screen.blit(self.image, self.rect)

            self.buttons_group.draw(self.state_control.screen)


            # Telas de tutorial
            if self.page == 1:
                self.draw_large_text(txt_regra_1, self.font_size, WIDTH/2, 210, 55)
                self.draw_large_text(txt_regra_2, self.font_size, WIDTH/2, 410, 55)
            elif self.page == 2:
                self.draw_large_text(txt_regra_3, self.font_size, WIDTH/2, 210, 55)
                self.draw_large_text(txt_regra_4, self.font_size, WIDTH/2, 370, 55)
            else:
                self.draw_large_text(txt_regra_5, self.font_size, WIDTH/2, 210, 55)
                self.draw_large_text("Colisões com paredes",    self.font_size, 250, 300, 15)
                self.draw_large_text("Colisões diretas",        self.font_size, 500, 300, 15)
                self.draw_large_text("Colisões com as linhas",  self.font_size, 750, 300, 15)
                self.state_control.screen.blit(self.img_wall.image, self.img_wall.rect)
                self.state_control.screen.blit(self.img_moto.image, self.img_moto.rect)
                self.state_control.screen.blit(self.img_line.image, self.img_line.rect)

            # Exibe o núemro da página
            self.draw_text(str(self.page), 30, WIDTH-100, HEIGHT-75)

            self.update()

    def check_input(self):
        """
        Check the input for the menu.
        
        Returns
        -------
        None
        """
        if self.state_control.ESC_KEY:
            self.state_control.curr_menu = self.state_control.main_menu
            self.run_display = False
        if self.state_control.BACK_KEY:
            self.state_control.curr_menu = self.state_control.main_menu
            self.run_display = False
        if self.state_control.START_KEY or self.state_control.BUTTON_CLICKED:
            if self.action == "right_arrow":
                if self.page < self.num_of_pages:
                    # Adiciona o botão esquerdo para exibi-lo se necessário
                    if self.page == 1:
                        self.buttons_group.add(self.btn_left)
                    self.page += 1

                    # Remove o botão direito para deixar de exibi-lo se atingir a última página
                    if self.page == self.num_of_pages:
                        self.buttons_group.remove(self.btn_right)

                    # Permite que o jogador avance para o jogo após ler o tutorial
                    if not self.tutorial_read and self.page == self.num_of_pages:
                        self.buttons_group.add(self.btn_play)
                        self.tutorial_read = True

            elif self.action == "left_arrow":
                if self.page <= self.num_of_pages:
                    # Adiciona o botão direito para exibi-lo se necessário
                    if self.page == self.num_of_pages:
                        self.buttons_group.add(self.btn_right)
                    self.page -= 1

                    # Remove o botão esquerdo para deixar de exibi-lo
                    if self.page == 1:
                        self.buttons_group.remove(self.btn_left)

            if self.action == "play":
                self.state_control.playing = True
                self.run_display = False
                self.state_control.first_time = False

    def draw_large_text(self, text, size, x, y, max_line_length):
        lines = textwrap.wrap(text, width=max_line_length)
        y_offset = 0

        for line in lines:
            text_surface = (pygame.font.Font(pygame.font.get_default_font(), size).
                            render(line, True, WHITE))
            text_rect = text_surface.get_rect()
            text_rect.center = (x, y + y_offset)
            self.state_control.screen.blit(text_surface, text_rect)
            y_offset += text_rect.height + 10
