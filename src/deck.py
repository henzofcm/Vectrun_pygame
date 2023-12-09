import pygame
from entity import *
import random


class Card(Entity):
    """
    Represents a card object.

    Parameters
    ----------
    image_path : str
        The path to the image file for the card.
    x_y : tuple
        The x and y coordinates of the card's position.
    scale_size : float
        The scale size of the card.
    value : int
        The value of the card.

    Attributes
    ----------
    value : int
        The value of the card.

    Methods
    -------
    __getitem__(key)
        Get the value of the card at the specified index.
    update()
        Update the card's state.

    """

    def __init__(self, image_path, x_y, scale_size, value):
        """
        Initialize a Card object.

        Parameters
        ----------
        image_path : str
            The path to the image file for the card.
        x_y : tuple
            The x and y coordinates of the card's position.
        scale_size : float
            The scale size of the card.
        value : int
            The value of the card.

        Returns
        -------
        None
        """
        super().__init__(image_path, x_y, scale_size)

        # Direção do vetor
        self.value = value

    def __getitem__(self, key):
        """
        Get the value of the card at the specified index.

        Parameters
        ----------
        key : int
            The index of the value to retrieve.

        Returns
        -------
        int
            The value of the card at the specified index.
        """
        return self.value[key]

    def update(self):
        """
        Update the card's state.

        Returns
        -------
        bool
            True if the card collides with the mouse position, False otherwise.
        """
        # Testa se houve colisão com o mouse
        mouse_pos = pygame.mouse.get_pos()

        # Se houver, retorna True
        if self.rect.collidepoint(mouse_pos):
            return True
        else:
            return False


class Deck(Entity):
    def __init__(self, card_path, scale_size):
        super().__init__(card_path + "card_back.png", (0, 0), (0, 0))

        self.cards = []
        self.drawn_cards = []  # Cartas que foram tiradas do deck e estão em jogo

        # Carrega todas as cartas pra memória
        __card_count = 1
        for y in range(-4, 5):
            for x in range(-4, 5):
                # Se for a origem, pula (esta carta-vetor não existe)
                if (x, y) == (0, 0):
                    continue

                # Nome do arquivo da carta
                card_name = "card_" + str(__card_count) + ".png"

                # Cria a carta em si
                card = Card(card_path + card_name, (0, 0), scale_size, value=(x, y))
                self.cards.append(card)

                __card_count += 1

        # Embaralha as cartas
        self.shuffle_deck()

    def shuffle_deck(self):
        # Se o deck estiver vazio, randomiza drawn_cards
        if not self.cards:
            random.shuffle(self.drawn_cards)
            self.cards = self.drawn_cards.copy()

            # Limpa as cartas tiradas
            self.drawn_cards.clear()

        # Caso contrário, randomiza o próprio deck
        else:
            random.shuffle(self.cards)


    def draw_card(self):
        if not self.cards:  # Se o deck estiver vazio, embaralhe-o novamente
            self.shuffle_deck()

        card = self.cards.pop(0)  # Remove a primeira carta do deck
        self.drawn_cards.append(card)  # Adiciona a carta às cartas tiradas

        return card

