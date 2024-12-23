import pygame
import sys
from os.path import join
from os import walk

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 800
TILE_SIZE = WINDOW_WIDTH/16
FPS = 165
SLEEP_TIME = 700
Z_LAYERS = {
    'background': 0,
    'player': 1,
    'wall': 2
}
