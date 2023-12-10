import pygame
from config import *

def check_border_collision(rider_position: tuple) -> bool:
    """
    Checks if the rider's position collides with the grid borders.

    Parameters
    ----------
    rider_position : tuple
        The current position of the rider (x, y).

    Returns
    -------
    bool
        True if there is a collision with the borders, False otherwise.
    """
    if rider_position[0] > GRID_X - BORDER or rider_position[0] < BORDER:
        return True

    if rider_position[1] > GRID_Y - BORDER or rider_position[1] < BORDER:
        return True

    return False


def check_line_collision(players_group, rider, card=None):
    """
    Check if there is a collision between the rider's line and the lines of other players.

    Parameters
    ----------
    players_group : Group
        Group containing all the players.
    rider : Player
        Current player.
    card : Card, optional
        Selected card. Defaults to None.

    Returns
    -------
    bool
        True if there is a collision, False otherwise.
    """
    # Cria um grupo com todos jogadores menos o rider atual
    temp_group = players_group.copy()
    temp_group.remove(rider)

    # Testa se ele colide com a linha de cada um dos outros
    for enemy in temp_group:
        for index in range(2, len(enemy._path)):
            temp_coord = rider.mask.clipline(enemy._path[index - 1], enemy._path[index])

            # Se a linha colidir, desenpacota a tupla que clipline retorna
            if temp_coord:
                return True

    # No caso de colidir com as próprias linhas
    for index in range(2, len(rider._path[:-1])):
        temp_coord = rider.mask.clipline(rider._path[index - 1], rider._path[index])

        # Desenpacota a tupla que clipline retorna
        if temp_coord:
            return True

    # Se não passou card usa a que estiver salva
    if not card:
        card = rider.clicked_card

    # E então compara com o último vetor usado: se for múltiplo e contrário ao anterior deve haver colisão
    if __last_vector_collision(card, rider._last_card):
        return True

    return False


def __last_vector_collision(card, last_card):
    """
    Check if the last vector collision occurred between two vectors.

    Parameters
    ----------
    card : tuple
        The current vector represented as a tuple (x, y).
    last_card : tuple
        The previous vector represented as a tuple (x, y).

    Returns
    -------
    bool
        True if the last vector collision occurred, False otherwise.

    Notes
    -----
    The function checks if the last vector collision occurred by comparing the x and y components of the current and previous vectors.
    If any component is zero, it only checks the other component.
    If both components are non-zero, it checks if the vectors are proportional.
    If the vectors are proportional and have opposite signs, it considers it as a collision.

    Examples
    --------
    >>> __last_vector_collision((1, 2), (-1, -2))
    True
    >>> __last_vector_collision((3, 4), (5, 6))
    False
    """
    # Se algum valor de (x, y) for 0 verifica apenas o outro valor
    if not card[0] and not last_card[0]:  
        if card[1] * last_card[1] < 0:
            return True
    elif not card[1] and not last_card[1]:
        if card[0] * last_card[0] < 0:
            return True
    # Se nenhum for, verifica se são proporcionais
    elif card[0] != 0 and card[1] != 0:
        if last_card[0] / card[0] == last_card[1] / card[1]:
            if last_card[0] / card[0] < 0:
                return True
    else:
        return False


def check_line_cross(players_group, player, line, card=None):
    """
    Check if a line crosses with other players' lines or with its own line.

    Parameters
    ----------
    players_group : pygame.sprite.Group
        A group containing all players except the current player.
    player : Player
        The current player.
    line : pygame.Surface
        The line to check for collisions.
    card : Card, optional
        The card used to draw the line. Defaults to None.

    Returns
    -------
    bool
        True if the line crosses with other players' lines or with its own line, False otherwise.
    """
    # Cria um grupo com todos jogadores menos o rider atual
    temp_group = players_group.copy()
    temp_group.remove(player)

    # Se a linha colidir com o caminho de outro rider retorna True
    for rider in temp_group.sprites():
        temp_line = rider.line_mask

        # No caso de ser o primeiro movimento do player é necessário esconder
        # A origem da linha do inimigo para que elas não colidam ali
        # Pois por ser o primeiro turno, todas sairão dali
        if not player.line_mask.get_at((GRID_X / 2 - 1, GRID_Y / 2 - 2)):
            temp_line = __hide_mask_origin(temp_line)

        # Verifica se houve overlap das linhas
        if line.overlap(temp_line, (0, 0)):
            return True

    # Se a linha colidir com alguma das próprias retorna True
    if line.overlap(player._last_line_mask, (0, 0)):
        return True

    # Se não passou card usa a que estiver salva
    if not card:
        card = player.clicked_card

    # E verifica se elas não são contrárias
    if __last_vector_collision(card, player._last_card):
        return True

    return False


def __hide_mask_origin(line_mask):
    """
    Hide the origin of the line mask.

    Parameters
    ----------
    line_mask : pygame.mask.Mask
        The original line mask.

    Returns
    -------
    pygame.mask.Mask
        The new line mask with the origin hidden.
    """
    new_mask = line_mask.copy()

    # Cria uma pequena máscara entorno da origem
    origin_mask = pygame.mask.Mask((RIDER_X, RIDER_Y), fill=True)
    size = origin_mask.get_size()

    # Apaga de fato a origem de temp_mask
    new_mask.erase(origin_mask, (GRID_X / 2 - size[0] / 2, GRID_Y / 2 - size[1] / 2))

    return new_mask

def check_riders_collision(rider_1, rider_2):
    """
    Check collision between two sprite groups and remove collided sprites.

    Parameters
    ----------
    group_1 : pygame.sprite.Group
        The first sprite group to check collision with.
    group_2 : pygame.sprite.Group
        The second sprite group to check collision with.

    Returns
    -------
    None
        This function does not return any value. It modifies the sprite groups in-place.

    """
    # Retorna verdadeiro se colidirem
    if rider_1.mask.colliderect(rider_2.mask):
        return True
    
    return False
        
class Singleton():
    """
    This class is used to create a singleton object.
    
    Attributes
    ----------
    aClass : object
        The object to be initialized.
    instance : object
        The instance of the object.
        
    Methods
    -------
    __init__(self, cls)
        Initialize the Utilities class.
    __call__(self, *args, **kwargs)
        Execute the object call as a function.
    """
    def __init__(self, cls):
        """
        Initialize the Utilities class.

        Parameters
        ----------
        cls : object
            The object to be initialized.

        Returns
        -------
        None
        """
        # Salva a classe original
        self.aClass = cls
        self.instance = None

    def __call__(self, *args, **kwargs):
        """
        Execute the object call as a function.

        Parameters
        ----------
        *args : positional arguments
            Positional arguments passed to the function.
        **kwargs : keyword arguments
            Keyword arguments passed to the function.

        Returns
        -------
        object
            The result of the function call.
        """
        # Usa o mesmo objeto em todas chamadas
        if self.instance is None:
            self.instance = self.aClass(*args, **kwargs)

        return self.instance
    
    def __del__(self):
        # Apaga a instancia original
        del self.instance
        self.instance = None
