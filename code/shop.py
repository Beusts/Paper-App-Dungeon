import csv

from settings import *
from utils import draw_text
from random import randint

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
                elif row[0] == 'Scroll of Mulligan':
                    self.items.append(Scroll_of_Mulligan((1, col)))
                elif row[0] == 'Gambler':
                    self.items.append(Gambler((1, col)))
                elif row[0] == 'Light Snack':
                    self.items.append(Light_Snack((1, col)))
                elif row[0] == 'Coin Rush':
                    self.items.append(Coin_Rush((1, col)))
                elif row[0] == 'Break on Through':
                    self.items.append(Break_on_Trought((1, col)))
                elif row[0] == 'Hearty Snack':
                    self.items.append(Hearty_Snack((1, col)))
                elif row[0] == 'Teleport Scroll':
                    self.items.append(Teleport_Scroll((1, col)))
                elif row[0] == 'Magic Shield':
                    self.items.append(Magic_Shield((1, col)))
                if row[0] == 'Medium Snack':
                    self.items.append(Medium_Snack((1, col)))
                if row[0] == 'Weaklings':
                    self.items.append(Weaklings((1, col)))
                col += 4

    def run(self, dt):
        self.display_surface.fill('white')
        self.draw_shop()

    def draw_shop(self):
        """
        Dessine le shop
        """
        pygame.draw.rect(self.display_surface, GRAY,
                         (0, 0, TILE_SIZE * 15, TILE_SIZE * 2))

        round_radius = int(TILE_SIZE)
        for i in range(15):
            pygame.draw.rect(self.display_surface, GRAY,
                             (i * TILE_SIZE, TILE_SIZE * 2, TILE_SIZE, TILE_SIZE), border_bottom_left_radius=round_radius, border_bottom_right_radius=round_radius)

        draw_text(self.display_surface, "Shop",
                  (TILE_SIZE * 7.5, TILE_SIZE * 1.5), FONT, BLACK, center=True)

        for item in self.items:
            item.draw()

    def purchase_item(self, game, item):

        if coins > item.price :
            item.buy()
            game.final_coins -= item.price
            game.inventory.append(item)

        return game

class Item:
    def __init__(self, name, description, price, position, use_once = False):
        self.name = name
        self.description = description
        self.price = price
        self.is_bought = False
        self.position = position
        self.display_surface = pygame.display.get_surface()
        self.use_once = use_once

    def buy(self):
        self.is_bought = True

    def use(self, player):
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


"""
    Items that have a direct impact on the player
"""

class Gambler(Item):
    def __init__(self, position):
        super().__init__("Gambler",
                         "Roll: If you roll 4+, gain 10¢. Otherwise, gain 0¢.", 5, position)

    def use(self, player):
        roll = randint(1, 6)

        if roll > 4 :
            player.winning_coins += 4

        return player

class Light_Snack(Item):
    def __init__(self, position):
        super().__init__("Light Snack",
                         "Gain 3 HP.", 2, position)

    def use(self, player):
        player.winning_hp += 3

        return player

class Medium_Snack(Item):
    def __init__(self, position):
        super().__init__("Meduim Snack",
                         "Gain 6 HP.", 9, position)

    def use(self, player):
        player.winning_hp += 6

        return player

class Hearty_Snack(Item):
    def __init__(self, position):
        super().__init__("Hearty Snack",
                         "Gain 9 HP", 13, position)

    def use(self, player):
        player.winning_hp += 9

        return player


"""
    Particular items
"""
class Doubling_Potion(Item):
    def __init__(self, position):
        super().__init__("Doubling Potion",
                         "Double the number of a dice roll (use once).", 6, position, True)

    def use(self, level):
        pass

class Scroll_of_Mulligan(Item):
    def __init__(self, position):
        super().__init__("Scroll of Mulligan",
                         "re-roll your dice (use once).", 10, position, True)

    def use(self, level):
        pass

class Coin_Rush(Item):
    def __init__(self, position):
        super().__init__("Coin Rush",
                         "All coins and treasure chests are worth 2x on next floor only.", 11, position)

    def use(self, level):
        pass

class Break_on_Trought(Item):
    def __init__(self, position):
        super().__init__("Break on Through",
                         "Traver through a wall (use once).", 9, position, True)

    def use(self, level):
        pass


class Teleport_Scroll(Item):
    def __init__(self, position):
        super().__init__("Teleport Scroll",
                         "Teleport to anywhere on the map (use once).", 11, position, True)

    def use(self, level):
        pass

class Magic_Shield(Item):
    def __init__(self, position):
        super().__init__("Magic Shield",
                         "Provides invinicibility on the next floor only. Enjoy!", 18, position)

    def use(self, level):
        pass


class Weaklings(Item):
    def __init__(self, position):
        super().__init__("Weaklings",
                         "Act as if all monsters on the next floor have only 1 HP.", 15, position)

    def use(self, level):
        pass
