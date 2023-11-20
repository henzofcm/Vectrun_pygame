import pygame
from entity import *
import random

class Card(Entity):
    def __init__(self, image_path, x, y, value):
        super().__init__(image_path, (x, y))
        self.value = value

class Deck(Entity):
    def __init__(self, card_image_paths):
        super().__init__(None, (0, 0))
        self.cards = []
        self.drawn_cards = []  # Cartas que foram tiradas do deck e estão em jogo
        self.shuffle_deck(card_image_paths)  # Inicializa o deck com cartas e embaralha

    def shuffle_deck(self, card_image_paths):
        random.shuffle(card_image_paths)
        self.cards.clear()
        self.drawn_cards.clear()

        for x in range(-4, 5):
            for y in range(-4, 5):
                if card_image_paths:
                    card_image_path = card_image_paths.pop(0)
                    card = Card(card_image_path, x, y, value=None)
                    self.cards.append(card)

    def draw_card(self):
        if not self.cards:  # Se o deck estiver vazio, embaralhe-o novamente
            self.shuffle_deck(self.drawn_cards)

        if self.cards:
            card = self.cards.pop(0)  # Remove a primeira carta do deck
            self.drawn_cards.append(card)  # Adiciona a carta às cartas tiradas
            return card

