import pygame
import sys
from src import *

# Screen size
WIDTH = 1280
HEIGHT = 720

# Sets the assets Path
ASSET_PATH = "assets/"

pygame.init()

# Defines the displayer configs    
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vectrun")
pygame.display.set_icon(pygame.image.load(ASSET_PATH + "textures/icon.png"))

# Creates internal fps clock
fps_clock = pygame.time.Clock()

# Game's loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Updates the displayer
    pygame.display.update()
    fps_clock.tick(30)