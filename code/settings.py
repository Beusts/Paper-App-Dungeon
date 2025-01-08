import pygame
import sys
from os.path import join
from os import walk

# Dimensions de la hauteur de la fenêtre
WINDOW_HEIGHT = 720 * 1.6
# Taille d'une tuile
TILE_SIZE = int(WINDOW_HEIGHT * (9 / 16)) // 15
# Dimensions de la largeur de la fenêtre
WINDOW_WIDTH = TILE_SIZE * 15
# Fréquence d'images par seconde
FPS = 60
# Temps de sommeil entre les mouvements
SLEEP_TIME = 100
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
