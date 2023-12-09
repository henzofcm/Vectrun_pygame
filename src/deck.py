import pygame
from entity import *
import random


class Deck(Entity):
    """
    Represents a deck of cards.

    This deck of cards contains a collection of cards and allows shuffling
    and drawing cards from the deck.

    Attributes
    ----------
    cards : list of Card
        A list of Card objects representing the cards in the deck.
    drawn_cards : list of Card
        A list of Card objects representing the cards that have been drawn
        from the deck and are in play.

    Methods
    -------
    __init__(card_path, scale_size)
        Initialize a Deck object with the specified cards and settings.
    shuffle_deck()
        Shuffle the cards in the deck.
    draw_card()
        Draw a card from the deck and return it.

    Notes
    -----
    This class inherits from the Entity class and uses a list of Card objects
    to represent the cards in the deck. It allows shuffling the deck and
    drawing cards for use in a game.
    """

    def __init__(self, card_path, scale_size):
        """
        Initialize a Deck object with the specified cards and settings.

        Parameters
        ----------
        card_path : str
            The path to the image file for the card backs.
        scale_size : float
            The scale size of the cards.

        Returns
        -------
        None
        """
        super().__init__(card_path + "card_back.png", (0, 0), (0, 0))

        self.cards = []
        self.drawn_cards = []  # Cards that have been drawn from the deck and are in play

        # Load all the cards into memory
        __card_count = 1
        for y in range(-4, 5):
            for x in range(-4, 5):
                # Skip if it's the origin (this vector card doesn't exist)
                if (x, y) == (0, 0):
                    continue

                # Card file name
                card_name = "card_" + str(__card_count) + ".png"

                # Create the card itself
                card = Card(card_path + card_name, (0, 0), scale_size, value=(x, y))
                self.cards.append(card)

                __card_count += 1

        # Shuffle the cards
        self.shuffle_deck()

    def shuffle_deck(self):
        """
        Shuffle the cards in the deck.

        If the deck is empty, the previously drawn cards are shuffled and reused.

        Returns
        -------
        None
        """
        # If the deck is empty, shuffle drawn_cards
        if not self.cards:
            random.shuffle(self.drawn_cards)
            self.cards = self.drawn_cards.copy()

            # Clear the drawn cards
            self.drawn_cards.clear()

        # Otherwise, shuffle the deck itself
        else:
            random.shuffle(self.cards)

    def draw_card(self):
        """
        Draw a card from the deck and return it.

        If the deck is empty, the cards are shuffled again before drawing a card.

        Returns
        -------
        Card
            A Card object representing the drawn card from the deck.
        """
        if not self.cards:  # If the deck is empty, shuffle it again
            self.shuffle_deck()

        card = self.cards.pop(0)  # Remove the first card from the deck
        self.drawn_cards.append(card)  # Add the card to the drawn cards

        return card


class Deck(Entity):
    """
    Represents a deck of cards.

    This deck of cards contains a collection of cards and allows shuffling
    and drawing cards from the deck.

    Attributes
    ----------
    cards : list of Card
        A list of Card objects representing the cards in the deck.
    drawn_cards : list of Card
        A list of Card objects representing the cards that have been drawn
        from the deck and are in play.

    Methods
    -------
    __init__(card_path, scale_size)
        Initialize a Deck object with the specified cards and settings.
    shuffle_deck()
        Shuffle the cards in the deck.
    draw_card()
        Draw a card from the deck and return it.

    Notes
    -----
    This class inherits from the Entity class and uses a list of Card objects
    to represent the cards in the deck. It allows shuffling the deck and
    drawing cards for use in a game.
    """

    def __init__(self, card_path, scale_size):
        """
        Initialize a Deck object with the specified cards and settings.

        Parameters
        ----------
        card_path : str
            The path to the image file for the card backs.
        scale_size : float
            The scale size of the cards.

        Returns
        -------
        None
        """
        super().__init__(card_path + "card_back.png", (0, 0), (0, 0))

        self.cards = []
        self.drawn_cards = []  # Cards that have been drawn from the deck and are in play

        # Load all the cards into memory
        __card_count = 1
        for y in range(-4, 5):
            for x in range(-4, 5):
                # Skip if it's the origin (this vector card doesn't exist)
                if (x, y) == (0, 0):
                    continue

                # Card file name
                card_name = "card_" + str(__card_count) + ".png"

                # Create the card itself
                card = Card(card_path + card_name, (0, 0), scale_size, value=(x, y))
                self.cards.append(card)

                __card_count += 1

        # Shuffle the cards
        self.shuffle_deck()

    def shuffle_deck(self):
        """
        Shuffle the cards in the deck.

        If the deck is empty, the previously drawn cards are shuffled and reused.

        Returns
        -------
        None
        """
        # If the deck is empty, shuffle drawn_cards
        if not self.cards:
            random.shuffle(self.drawn_cards)
            self.cards = self.drawn_cards.copy()

            # Clear the drawn cards
            self.drawn_cards.clear()

        # Otherwise, shuffle the deck itself
        else:
            random.shuffle(self.cards)

    def draw_card(self):
        """
        Draw a card from the deck and return it.

        If the deck is empty, the cards are shuffled again before drawing a card.

        Returns
        -------
        Card
            A Card object representing the drawn card from the deck.
        """
        if not self.cards:  # If the deck is empty, shuffle it again
            self.shuffle_deck()

        card = self.cards.pop(0)  # Remove the first card from the deck
        self.drawn_cards.append(card)  # Add the card to the drawn cards

        return card


