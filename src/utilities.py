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
        if enemy.line.collidepoint(rider.rect.center):
            return True
            
    return False

def check_riders_collision(group_1, group_2):
     # Mata ambos sprites se colidirem
        pygame.sprite.groupcollide(group_1, group_2, True, True)
        
