import csv
import re

from settings import *
from utils import draw_text, draw_center_text, draw_centery_text


class Shop:
    def __init__(self, shop_data):
        self.display_surface = pygame.display.get_surface()
        self.items = []
        self.setup(shop_data)

    def setup(self, shop_data):
        with open(join('data', 'shop', shop_data + '.csv'), newline='') as csvfile:
            shop_reader = csv.reader(csvfile, delimiter=',')
            for row in shop_reader:
                self.items.append([row[0], row[1], int(row[2])])

    def run(self, dt):
        self.display_surface.fill('white')
        self.draw_shop(self.items)

    def draw_shop(self, items):
        """
        Dessine le shop
        """
        def draw_iteam(name, description, price, position):
            pygame.draw.rect(self.display_surface, BLACK,
                             (position[0] * TILE_SIZE, position[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE), int(TILE_SIZE*0.15))
            draw_text(self.display_surface, name,
                      (position[0] * TILE_SIZE + (TILE_SIZE * 2), position[1] * TILE_SIZE), font, BLACK)
            draw_center_text(self.display_surface, f"{price}¢",
                             (position[0] * TILE_SIZE + TILE_SIZE / 2, position[1] * TILE_SIZE + (TILE_SIZE * 1.5)), small_font, BLACK)
            draw_centery_text(self.display_surface, description,
                              (position[0] * TILE_SIZE + (TILE_SIZE * 2), position[1] * TILE_SIZE + (TILE_SIZE * 1.5)), small_font, BLACK)

        font = pygame.font.Font(None, int(TILE_SIZE * 1.5))
        small_font = pygame.font.Font(None, int(TILE_SIZE * 0.7))
        pygame.draw.rect(self.display_surface, GRAY,
                         (0, 0, TILE_SIZE * 15, TILE_SIZE * 3))

        draw_center_text(self.display_surface, "Shop",
                         (TILE_SIZE * 7.5, TILE_SIZE), font, BLACK)

        draw_iteam(items[0][0], items[0][1], items[0][2], (1, 4))
        draw_iteam(items[1][0], items[1][1], items[1][2], (1, 8))
        draw_iteam(items[2][0], items[2][1], items[2][2], (1, 12))
