import pygame
from config import *

def check_border_collision(rider_position):
    # Morre se colidir com as barras verticais
    if rider_position[0] > GRID_X - BORDER or rider_position[0] < BORDER:
        return True

    # E também se colidir com as horizontais
    if rider_position[1] > GRID_Y - BORDER or rider_position[1] < BORDER:
        return True
        
    return False

def check_line_cross(players_group, rider, card=None):
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

        # Caso clicked_card for None, usa uma carta inexistente
        if not card:
            card = (10, 10)

    # E então compara com o último vetor usado (para quando voltar no mesmo caminho)
    if (card[0], card[1]) == (-rider._last_card[0], -rider._last_card[1]):
        return True

    return False

def check_riders_collision(group_1, group_2):
    # Mata ambos sprites se colidirem
    pygame.sprite.groupcollide(group_1, group_2, True, True)
        
class Singleton():
    def __init__(self, cls):
        # Salva a classe original
        self.aClass = cls
        self.instance = None

    def __call__(self, *args, **kwargs):
        # Usa o mesmo objeto em todas chamadas
        if self.instance is None:
            self.instance = self.aClass(*args, **kwargs)

        return self.instance
    