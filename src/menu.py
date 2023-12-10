import pygame
from config import *
from entity import *

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
                self.next_state = button.label

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
        self.next_state = "the_grid"

        # Posições para os elementos na tela
        self.start_x, self.start_y = (WIDTH/2), (HEIGHT/2)
        self.options_x, self.options_y = (WIDTH/2), (HEIGHT/2 + 100)
        self.credits_x, self.credits_y = (WIDTH/2), (HEIGHT/2 + 200)

        # Define os botões dessa tela
        self.btn_the_grid = Button(TEXTURE_PATH + "grid_logo.png", (self.start_x, self.start_y),
                              (BUTTON_X, BUTTON_Y), "the_grid")
        self.btn_options = Button(TEXTURE_PATH + "options_button.png", (self.options_x, self.options_y),
                                   (BUTTON_X, BUTTON_Y), "options_menu")
        self.btn_credits = Button(TEXTURE_PATH + "credits_button.png", (self.credits_x, self.credits_y),
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
            if self.next_state == "the_grid":
                self.state_control.playing = True
            elif self.next_state == "options_menu":
                self.state_control.curr_menu = self.state_control.options_menu
            elif self.next_state == "credits_menu":
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
        self.next_state = "main_menu"

        # Define os botões dessa tela
        self.btn_back = Button(TEXTURE_PATH + "back_button.png", (WIDTH / 2, (HEIGHT - 100)),
                               (BUTTON_X, BUTTON_Y), "main_menu")

        # Adiciona os botões a um grupo
        self.buttons_group.add(self.btn_back)

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
            if self.next_state == "main_menu":
                self.state_control.curr_menu = self.state_control.main_menu
            self.run_display = False


class CreditsMenu(Menu):
    def __init__(self, game, image_path, x_y, scale_size):
        super().__init__(game, image_path, x_y, scale_size)
        self.next_state = "main_menu"

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
            self.state_control.screen.blit(self.background_image, (0,0))

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
            if self.next_state == "main_menu":
                self.state_control.curr_menu = self.state_control.main_menu
            self.run_display = False


class ResultScreen(Menu):
    def __init__(self, game, image_path, x_y, scale_size):
        super().__init__(game, image_path, x_y, scale_size)
        self.next_state = "main_menu"

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
        if self.state_control.ESC_KEY:
            self.state_control.curr_menu = self.state_control.main_menu
            self.run_display = False
        if self.state_control.BACK_KEY:
            self.state_control.curr_menu = self.state_control.main_menu
            self.run_display = False
        if self.state_control.START_KEY or self.state_control.BUTTON_CLICKED:
            if self.next_state == "main_menu":
                self.state_control.curr_menu = self.state_control.main_menu
            self.run_display = False


class TutorialScreen(Menu):
    def __init__(self, game, image_path, x_y, scale_size):
        super().__init__(game, image_path, x_y, scale_size)
        self.next_state = ""

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