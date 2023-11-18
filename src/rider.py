import pygame
from entity import *

class Rider(Entity):
    def __init__(self, number):
        super().__init__(self)
        self._number = number
        self._path = [(0, 0)]

class Player(Rider):
    pass

class Bot(Rider):
    pass
