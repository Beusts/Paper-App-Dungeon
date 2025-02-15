import pygame
import sys
from os.path import join
from os import walk

# Dimensions de la hauteur de la fenêtre
WINDOW_HEIGHT = 720 * 1.3
# Taille d'une tuile
# Dimensions de la largeur de la fenêtre
WINDOW_WIDTH = WINDOW_HEIGHT * (9 / 16)
# Fréquence d'images par seconde
FPS = 60
# Temps de sommeil entre les mouvements
SLEEP_TIME = 100
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Fréuence d'apparition d'un Shop
FREQUENCY_SPAWN_SHOP = 2

global is_input_active
can_receive_input = True

# Taille d'une tuile (initiale)
TILE_SIZE = int((WINDOW_WIDTH / 15))

UI_SIZE = int(WINDOW_WIDTH / 15)

def get_tile_size():
    global TILE_SIZE
    return TILE_SIZE


def set_tile_size(new_tile_size):
    global TILE_SIZE
    TILE_SIZE = int(new_tile_size)
