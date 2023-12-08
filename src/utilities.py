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

def check_line_collision(players_group, rider, card=None):
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

    # E então compara com o último vetor usado: se for múltiplo e contrário
    # Ao anterior deve haver colisão
    if __last_vector_collision(card, rider._last_card):
        return True

    return False

def __last_vector_collision(card, last_card):
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
    # Cria um grupo com todos jogadores menos o rider atual
    temp_group = players_group.copy()
    temp_group.remove(player)

    # Se a linha colidir com o caminho de outro rider retorna True
    for rider in temp_group.sprites():
        if line.overlap(rider.line_mask, (0, 0)):
            print("Enemy", end=' ')
            print(line.overlap_area(rider.line_mask, (0, 0)))
            return True
        
    # Se a linha colidir com alguma das próprias retorna True
    if line.overlap(player._last_line_mask, (0, 0)):
        print("Self", end=' ')
        print(line.overlap_area(player.line_mask, (0, 0)))
        return True
    
    # Se não passou card usa a que estiver salva
    if not card:
        card = player.clicked_card
    
    # E verifica se elas não são contrárias
    if __last_vector_collision(card, player._last_card):
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
    