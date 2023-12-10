import pygame
import random

from entity import *
import utilities
from config import *

class Rider(Entity):
    """
    Represents a rider object.
    """
    def __init__(self, number, x_y, scale_size, deck):
        """
        Initialize a Rider object.

        Parameters
        ----------
        number : int
            The number of the player.
        x_y : tuple
            The initial position of the rider.
        scale_size : float
            The scale size of the rider.
        deck : Deck
            The deck object that represents the game deck.

        Returns
        -------
        None
        """
        # Carrega texturas diferentes dependendo do nº do jogador
        archive = "rider_" + str(number) + ".png"

        # Cria o rider e centraliza sua posição
        super().__init__("assets/textures/" + archive, x_y, scale_size)
        self.rect = self.image.get_rect(center=x_y)

        # Atributos adicionais
        self._number = number
        self._path = [x_y, x_y]
        self._velocity = 1 / 2

        # Salva a mão de cartas do jogador
        self._hand = pygame.sprite.Group()

        for foo in range(3):
            card = deck.draw_card()
            card.rect.topleft = (GRID_X + 50, GRID_Y / 2- 55 + foo * 125)

            self._hand.add(card)

        # Salva a cor da moto
        if number == 1:
            self._color = "#258dc2"
        elif number == 2:
            self._color = "#ec6716"
        elif number == 3:
            self._color = "#cb101a"
        elif number == 4:
            self._color = "#ffb001"

        # Atributos de estado
        self.__timer = 0
        self.state_alive = True
        self.clicked_card = None
        self._last_card = (0, 0)

        # Máscaras para colisões mais precisas
        self.mask = pygame.rect.Rect(x_y, (RIDER_X / 5 - 2, RIDER_Y / 5 - 1))

        self.line_mask = self._get_line_mask(self._color, (-10, -10), (-10, -10))
        self._last_line_mask = self.line_mask

    def update(self, deck):
        """
        Update the rider's state based on the given deck.

        Parameters
        ----------
        deck : Deck
            The deck object that represents the game deck.

        Returns
        -------
        None
        """
        # Roda animação de movimento se estiver vivo
        if self.state_alive:
            return self.move_rider(deck)
        # E animação de morte caso contrário
        else:
            pass

    def move_rider(self, deck):
        """
        Move the rider according to the card it clicked.

        Parameters
        ----------
        deck : Deck
            The deck object.

        Returns
        -------
        bool
            True if the rider is moved, False otherwise.
        """
        self.__set_temp_variables()

        # Move o jogador de acordo com essa desigualdade (quase sempre satisfeita)
        if self.__temp_player_center[0] + 2 < self.__temp_player_target[0]:
            self.__change_move(self.clicked_card, self.__timer)
        
            self.__timer += 0.05
        # No caso não-tão-raro de vetores (0, y), move o jogador de acordo
        elif self.clicked_card[0] == 0 and self.__temp_player_center[1] + 2 < self.__temp_player_target[1]:
            self.__change_move(self.clicked_card, self.__timer)
        
            self.__timer += 0.05
        # Se ficou parado, reseta o movimento
        else:
            self.__reset_movement(deck)
            return False
        
        return True

    def __change_move(self, card, time):
        """
        Move the rider's position based on the given card and time.

        Parameters
        ----------
        card : tuple
            The difference that the rider should move in the x and y directions.
        time : int
            The time duration of the movement.

        Notes
        -----
        This method updates the rider's position by calculating the temporary positions
        based on the card and time values. The rider's position is then rounded to the
        nearest integer and updated accordingly.

        """
        # Diferença que a moto deverá andar
        delta_x = card[0]
        delta_y = card[1]

        # Reinicia a posição em cada nova animação
        if time == 0:
            self.__temp_x = self.rect.centerx
            self.__temp_y = self.rect.centery

        # Valores temporários para não perder precisão no movimento
        self.__temp_x = self.__temp_x + time * delta_x / self._velocity
        self.__temp_y = self.__temp_y - time * delta_y / self._velocity

        # Atualiza a posição (e converte para inteiro)
        self.rect.centerx = round(self.__temp_x)
        self.rect.centery = round(self.__temp_y)
        self.mask.center = self.rect.center

    def __set_temp_variables(self):
        """
        Set temporary variables that save code in movement.

        Parameters
        ----------
        self : Rider
            The Rider object.

        Returns
        -------
        None
        """
        # Variáveis temporárias que poupam código no movimento
        self.__temp_player_center = self.rect.center
        self.__temp_player_target = self.__player_target

        # Dependendo do valor da carta, muda a coordenada relativa
        if self.clicked_card[0] < 0:
            self.__temp_player_center = (-self.__temp_player_center[0], self.__temp_player_center[1])
            self.__temp_player_target = (-self.__temp_player_target[0], self.__temp_player_target[1])

        if self.clicked_card[1] > 0:
            self.__temp_player_center = (self.__temp_player_center[0], -self.__temp_player_center[1])
            self.__temp_player_target = (self.__temp_player_target[0], -self.__temp_player_target[1])

    def __reset_movement(self, deck):
        """
        Resets the movement of the rider.

        Parameters
        ----------
        deck : Deck
            The deck of cards.

        Returns
        -------
        None
        """
        # Retorna _timer para 0
        self.__timer = 0

        # Pesca uma nova carta e adiciona à mão
        card = deck.draw_card()
        card.rect.topleft = self.clicked_card.rect.topleft

        self._hand.add(card)

        # Remove a carta usada e limpa _clicked_card
        self._hand.remove(self.clicked_card)
        self._last_card = self.clicked_card
        self.clicked_card = (0, 0)

        # Salva a posição final do jogador no seu _path
        self._path.append(self.rect.center)

        # Cria uma mascára para a linha e a adiciona em line_mask
        temp_mask = self._get_line_mask(self._color, self._path[-2], self._path[-1])

        self._last_line_mask = self.line_mask.copy()
        self.line_mask.draw(temp_mask, (0, 0))

    @staticmethod
    def _get_line_mask(color,start, end):
        """
        Create a line mask based on the given color, start, and end points.

        Parameters
        ----------
        color : str
            The color of the line.
        start : tuple
            The starting point of the line.
        end : tuple
            The ending point of the line.

        Returns
        -------
        pygame.mask.Mask
            The line mask.

        """
        # Cria uma superfície em preto
        temp_surf = pygame.Surface((GRID_X, GRID_Y))
        temp_surf.set_colorkey((0, 0, 0))

        # Desenha a linha e retorna a máscara
        pygame.draw.line(temp_surf, color, start, end, width=6)
        return pygame.mask.from_surface(temp_surf)

    def select_card(self, card):
        """
        Select a card for the rider.

        Parameters
        ----------
        card : tuple
            The card that the rider clicked.

        Returns
        -------
        None
        """
        self.clicked_card = card

        self.__player_target = self._path[-1]
        self.__player_target = (card[0] * DISTANCE + self.__player_target[0], -card[1] * DISTANCE + self.__player_target[1])

@utilities.Singleton
class Player():
    """
    Class representing a player in the game.

    Parameters
    ----------
    number : int
        The player's number.
    x_y : tuple
        The initial position of the player.
    scale_size : int
        The scale size of the player.
    deck : Deck
        The player's deck.

    Attributes
    ----------
    __wrapper : pygame.sprite.GroupSingle
        The wrapper around the Rider sprite.

    Methods
    -------
    sprite()
        Returns the sprite of the SingleGroup.
    update()
        Updates the SingleGroup.
    draw(screen)
        Draws the SingleGroup.
    """

    def __init__(self, number, x_y, scale_size, deck):
        """
        Initialize a Player object.

        Parameters
        ----------
        number : int
            The player's number.
        x_y : tuple
            The initial position of the player.
        scale_size : int
            The scale size of the player.
        deck : Deck
            The player's deck.

        Retorns
        -------
        None
        """
        # Cria um envoltório entorno de um Rider
        self.__wrapper = Rider(number, x_y, scale_size, deck)
        self.__wrapper = pygame.sprite.GroupSingle(self.__wrapper)

    def __getattr__(self, attrvalue):
        """
        Get the attribute from the sprite and not from the group.

        Parameters
        ----------
        attrvalue : str
            The name of the attribute to retrieve.

        Returns
        -------
        Any
            The value of the requested attribute.

        Notes
        -----
        This method is called when an attribute is accessed on the `Rider` object
        that is not defined directly in the class. It delegates the attribute
        retrieval to the underlying sprite object.

        """
        return getattr(self.__wrapper.sprite, attrvalue)
    
    def __getattr__(self, attrvalue):
        """
        Get the attribute from the sprite and not from the group.

        Parameters
        ----------
        attrvalue : str
            The name of the attribute to get.

        Returns
        -------
        Any
            The value of the requested attribute.

        Notes
        -----
        This method is called when an attribute is not found in the current object.
        It allows accessing attributes of the sprite directly instead of the group.

        Examples
        --------
        >>> rider = Rider()
        >>> rider.x
        100
        >>> rider.y
        200
        """
        # Pega o atributo do sprite e não do grupo
        return getattr(self.__wrapper.sprite, attrvalue)
    
    def __bool__(self):
        """
        Return the boolean value of the SingleGroup.

        Returns
        -------
        bool
            The boolean value of the SingleGroup.

        """
        return bool(self.__wrapper)
    
    def sprite(self):
        """
        Return the sprite of the SingleGroup.

        Returns
        -------
        sprite : object
            The sprite object representing the SingleGroup.

        """
        return self.__wrapper.sprite
        
    def update(self):
        """
        Update the SingleGroup.

        Returns
        -------
        updated : bool
            True if the update was successful, False otherwise.
        """
        # Atualiza o SingleGroup
        return self.__wrapper.update()

    def draw(self, screen):
            """
            Draw the SingleGroup on the screen.

            Parameters
            ----------
            screen : pygame.Surface
                The surface to draw on.

            Returns
            -------
            pygame.Rect
                The rectangle that represents the area of the drawn SingleGroup.
            """
            # Desenha o SingleGroup
            return self.__wrapper.draw(screen)

class Bot(Rider):
    """
    Represents a bot object.
    """
    def __init__(self, number, x_y, scale_size):
        """
        Initializes a Rider object.

        Parameters
        ----------
        number : int
            The rider's number.
        x_y : tuple
            The initial position of the rider as a tuple of (x, y) coordinates.
        scale_size : float
            The scale size of the rider.

        Returns
        -------
        None
        """
        super().__init__(number, x_y, scale_size)

    def choose_card(self, all_riders):
        """
        Choose a card from the rider's hand based on the preview movement.

        Parameters
        ----------
        all_riders : list
            A list of all riders in the game.

        Returns
        -------
        pygame.sprite.Sprite
            The chosen card from the rider's hand.

        Notes
        -----
        This method iterates through each card in the rider's hand and checks if the preview movement is valid or not.
        If a card's movement is valid, it is added to the choices list.
        If there are valid choices, a random card is returned from the choices list.
        If there are no valid choices, a random card from the rider's hand is returned.
        """
        choices = []

        # Laceia cada carta e decide se o movimento é válido ou não
        for card in self._hand.sprites():
            # Se for, adiciona à lista choices
            if self.__preview_movement(card, all_riders):
                choices.append(card)

        # Se algum for válido, retorna um entre eles
        if choices:
            return random.choice(choices)
        # Se não houver nenhum, qualquer carta da mão valerá
        else:
            return random.choice(self._hand.sprites())

    def __preview_movement(self, card, all_riders):
        """
        Calculate the preview movement of the rider based on the given card.

        Parameters
        ----------
        card : tuple
            A tuple representing the movement card (x, y).
        all_riders : list
            A list of all riders in the game.

        Returns
        -------
        bool
            True if the preview movement is valid, False otherwise.
        """
        # Pega o ponto inicial e final do vetor
        start = self._path[-1]
        end = (start[0] + card[0] * DISTANCE, start[1] - card[1] * DISTANCE)

        # Se for colidir com as fronteiras retorna
        if utilities.check_border_collision(end):
            return False

        # Cria uma máscara para testar colisões futuras desta linha
        line_mask = self._get_line_mask(self._color, start, end)

        # Se for colidir com as linhas de outrem retorna
        if utilities.check_line_cross(all_riders, self, line_mask, card):
            return False

        # Se não colidir com nada, a carta é válida
        return True

