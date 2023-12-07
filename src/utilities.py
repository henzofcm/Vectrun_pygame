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

def check_line_cross(players_group, rider):
    # Cria um grupo com todos jogadores menos o rider atual
    temp_group = players_group.copy()
    temp_group.remove(rider)

    # Testa se ele colide com a linha de cada um dos outros
    for enemy in temp_group:
        for index in range(2, len(enemy._path)):
            temp_coord = rider.rect.clipline(enemy._path[index - 1], enemy._path[index])

            # Se a linha colidir, desenpacota a tupla que clipline retorna
            if temp_coord:
                return True
            
    # No caso de colidir com as próprias linhas
    for index in range(2, len(rider._path[:-1])):
        temp_coord = rider.rect.clipline(rider._path[index - 1], rider._path[index])

        # Desenpacota a tupla que clipline retorna
        if temp_coord:
            return True
            
    return False

def check_riders_collision(group_1, group_2):
    # Mata ambos sprites se colidirem
    pygame.sprite.groupcollide(group_1, group_2, True, True)
        
