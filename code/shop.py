import csv
import re

from settings import *
from utils import draw_text

pygame.font.init()
FONT = pygame.font.Font(None, int(TILE_SIZE * 1.5))
DESC_FONT = pygame.font.Font(None, int(TILE_SIZE * 0.7))


class Shop:
    def __init__(self, shop_data):
        self.display_surface = pygame.display.get_surface()
        self.items = []
        self.setup(shop_data)

    def setup(self, shop_data):
        col = 4
        with open(join('data', 'shop', shop_data + '.csv'), newline='') as csvfile:
            shop_reader = csv.reader(csvfile, delimiter=',')
            for row in shop_reader:
                if row[0] == 'Doubling Potion':
                    self.items.append(Doubling_Potion((1, col)))
                col += 4

    def run(self, dt):
        self.display_surface.fill('white')
        self.draw_shop()

    def draw_shop(self):
        """
        Dessine le shop
        """
        pygame.draw.rect(self.display_surface, GRAY,
                         (0, 0, TILE_SIZE * 15, TILE_SIZE * 3))

        draw_text(self.display_surface, "Shop",
                  (TILE_SIZE * 7.5, TILE_SIZE), FONT, BLACK, center=True)

        for item in self.items:
            item.draw()


class Item:
    def __init__(self, name, description, price, position):
        self.name = name
        self.description = description
        self.price = price
        self.is_bought = False
        self.position = position
        self.display_surface = pygame.display.get_surface()

    def buy(self):
        self.is_bought = True

    def use(self):
        raise NotImplementedError(
            "This method must be redefined in a subclass")

    def draw(self):
        rect = pygame.Rect(
            self.position[0] * TILE_SIZE, self.position[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        if self.is_bought:
            pygame.draw.rect(self.display_surface, BLACK, rect)
        else:
            pygame.draw.rect(self.display_surface, BLACK,
                             rect, int(TILE_SIZE*0.15))

        # Check for mouse click on the item
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        if rect.collidepoint(mouse_pos) and mouse_click:
            self.buy()
        draw_text(self.display_surface, self.name,
                  (self.position[0] * TILE_SIZE + (TILE_SIZE * 2), self.position[1] * TILE_SIZE), FONT, BLACK)
        draw_text(self.display_surface, f"{self.price}¢",
                  (self.position[0] * TILE_SIZE + TILE_SIZE / 2, self.position[1] * TILE_SIZE + (TILE_SIZE * 1.5)), DESC_FONT, BLACK, center=True)
        draw_text(self.display_surface, self.description,
                  (self.position[0] * TILE_SIZE + (TILE_SIZE * 2), self.position[1] * TILE_SIZE + (TILE_SIZE * 1.5)), DESC_FONT, BLACK, center_y=True, line_width=TILE_SIZE * 10)


class Doubling_Potion(Item):
    def __init__(self, position):
        super().__init__("Doubling Potion",
                         "Double the number of a dice roll (use once).", 6, position)

    def use(self):
        pass
