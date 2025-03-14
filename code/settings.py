"""
Module contenant les constantes et paramètres globaux du jeu.
Ce module définit les dimensions de la fenêtre, les couleurs, et d'autres
paramètres généraux utilisés dans tout le jeu.
"""

import pygame
import sys
from os.path import join
from os import walk

# Dimensions de la hauteur de la fenêtre
WINDOW_HEIGHT = 720 * 1.3
# Dimensions de la largeur de la fenêtre
WINDOW_WIDTH = WINDOW_HEIGHT * (9 / 16)
# Fréquence d'images par seconde
FPS = 60
# Temps de sommeil entre les mouvements
SLEEP_TIME = 100
# Couleurs de base
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
WHITE = (255, 255, 255)

# Fréuence d'apparition d'un Shop
FREQUENCY_SPAWN_SHOP = 0.2
# Nombre de niveaux
NB_LEVEL = 10

# Variable globale pour gérer les inputs utilisateur
global is_input_active
can_receive_input = True

# Taille d'une tuile (initiale)
TILE_SIZE = int((WINDOW_WIDTH / 15))
# Taille de l'interface utilisateur
UI_SIZE = int(WINDOW_WIDTH / 15)


def get_tile_size():
    """
    Récupère la taille actuelle d'une tuile.

    Returns:
        int: La taille d'une tuile en pixels
    """
    global TILE_SIZE
    return TILE_SIZE


def set_tile_size(new_tile_size):
    """
    Modifie la taille des tuiles.

    Args:
        new_tile_size (int): La nouvelle taille de tuile en pixels
    """
    global TILE_SIZE
    TILE_SIZE = int(new_tile_size)
