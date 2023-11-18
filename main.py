import pygame
import sys
sys.path.append("src/")
from src import *

print(dir(menu))

# Sets all the Paths
ASSET_PATH = "assets/"
TEXTURE_PATH = "assets/textures/"
MUSIC_PATH = ASSET_PATH + "music/"
SOUNDS_PATH = ASSET_PATH + "sounds/"
FONTS_PATH = ASSET_PATH + "fonts/"

# Screen default size
WIDTH = 1280
HEIGHT = 720

# Initializes pygame
pygame.init()

# Defines the displayer configs    
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vectrun")
pygame.display.set_icon(pygame.image.load(TEXTURE_PATH + "icon.png"))

# Creates internal fps clock
fps_clock = pygame.time.Clock()

# Initializes everything
menu_1 = menu.Grid_Game(TEXTURE_PATH + "grid.png", (WIDTH / 2 - 300, 0), 600, 600)

# Game's loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    menu_1.update()
    screen.blit(menu_1._image, menu_1._rect)

    # Updates the displayer
    pygame.display.update()
    fps_clock.tick(30)
