import pygame
from entity import *
import random


class Card(Entity):
    def __init__(self, image_path, x_y, scale_size, value):
        super().__init__(image_path, x_y, scale_size)

        # Direção do vetor
        self.value = value


class Deck(Entity):
    def __init__(self, card_path):
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
                card = Card(card_path + card_name, (0, 0), (150, 100), value=(x, y))
                self.cards.append(card)

                __card_count += 1

        # Embaralha as cartas
        self.shuffle_deck()

    def shuffle_deck(self):
        # Se o deck estiver vazio, randomiza drawn_cards
        if not self.cards:
            random.shuffle(self.drawn_cards)
            self.cards = self.drawn_cards

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

