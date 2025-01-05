import pygame
import sys
from os.path import join
from os import walk

# Dimensions de la fenêtre
WINDOW_HEIGHT = 720
WINDOW_WIDTH = int(WINDOW_HEIGHT * (9 / 16))
# Taille d'une tuile
TILE_SIZE = WINDOW_WIDTH // 15
# Fréquence d'images par seconde
FPS = 60
# Temps de sommeil entre les mouvements
SLEEP_TIME = 100
# Couches Z pour les différents éléments
Z_LAYERS = {
    'background': 0,
    'player': 1,
    'wall': 2
}
