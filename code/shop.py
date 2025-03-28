"""
Module définissant la classe Shop et les différents objets achetables dans le jeu.
Ce module gère l'affichage du magasin et les interactions avec les objets disponibles à l'achat.
"""

import csv
import random
from encodings import search_function

from settings import *
from utils import draw_text
from random import randint

pygame.font.init()
FONT = pygame.font.Font(None, int(UI_SIZE * 1.5))
DESC_FONT = pygame.font.Font(None, int(UI_SIZE * 0.7))


class Shop(pygame.sprite.Sprite):
    """
    Classe qui gère l'interface du magasin et les objets disponibles à l'achat.
    """

    def __init__(self, shop_data, player):
        """
        Initialise le magasin avec les données spécifiées.

        Args:
            shop_data (str): Le nom du fichier de données du magasin.
            player (Player): Le joueur qui visite ce magasin.
        """
        self.display_surface = pygame.display.get_surface()
        self.items = []
        self.player = player
        print(f"level hp start : {self.player.level.hp_start}")
        print(f"current hp : {self.player.level.hp_start}")

        self.setup(shop_data)
        self.completed = False

    def setup(self, shop_data):
        """
        Configure le magasin en chargeant les objets depuis un fichier CSV.

        Args:
            shop_data (str): Le nom du fichier de données du magasin.
        """
        col = 4
        with open(join('data', 'shop', shop_data + '.csv'), newline='') as csvfile:
            shop_reader = csv.reader(csvfile, delimiter=',')
            for row in shop_reader:
                if row[0] == 'Doubling Potion':
                    self.items.append(Doubling_Potion((1, col), self.player))
                elif row[0] == 'Scroll of Mulligan':
                    self.items.append(
                        Scroll_of_Mulligan((1, col), self.player))
                elif row[0] == 'Gambler':
                    self.items.append(Gambler((1, col), self.player))
                elif row[0] == 'Light Snack':
                    self.items.append(Light_Snack((1, col), self.player))
                elif row[0] == 'Coin Rush':
                    self.items.append(Coin_Rush((1, col), self.player))
                elif row[0] == 'Break on Through':
                    self.items.append(Break_on_Trought((1, col), self.player))
                elif row[0] == 'Hearty Snack':
                    self.items.append(Hearty_Snack((1, col), self.player))
                elif row[0] == 'Teleport Scroll':
                    self.items.append(Teleport_Scroll((1, col), self.player))
                elif row[0] == 'Magic Shield':
                    self.items.append(Magic_Shield((1, col), self.player))
                if row[0] == 'Medium Snack':
                    self.items.append(Medium_Snack((1, col), self.player))
                if row[0] == 'Weaklings':
                    self.items.append(Weaklings((1, col), self.player))
                col += 4

    def run(self, dt):
        """
        Exécute la boucle principale du magasin.

        Args:
            dt (float): Le temps écoulé depuis la dernière mise à jour.
        """
        self.draw()
        self.handle_input()

    def draw(self):
        """
        Dessine l'interface du magasin sur la surface d'affichage.
        """
        self.display_surface.fill(WHITE)
        self.draw_shop()
        self.player.draw_information_player(self.display_surface)

    def handle_input(self):
        """
        Gère les entrées de l'utilisateur dans le magasin.
        """
        self.handle_continue_button()
        for item in self.items:
            item.handle_input()

    def draw_shop(self):
        """
        Dessine le shop
        """
        pygame.draw.rect(self.display_surface, GRAY,
                         (0, 0, UI_SIZE * 15, UI_SIZE * 2))

        round_radius = int(UI_SIZE)
        for i in range(15):
            pygame.draw.rect(self.display_surface, GRAY,
                             (i * UI_SIZE, UI_SIZE * 2, UI_SIZE, UI_SIZE), border_bottom_left_radius=round_radius, border_bottom_right_radius=round_radius)

        draw_text(self.display_surface, "Shop",
                  (UI_SIZE * 7.5, UI_SIZE * 1.5), FONT, BLACK, center=True)

        for item in self.items:
            item.draw()

        self.draw_continue_button()

    def draw_continue_button(self):
        """
        Dessine le bouton pour continuer après les achats.
        """
        font = pygame.font.Font(None, UI_SIZE)
        rect = pygame.Rect(0, 0, UI_SIZE * 4, UI_SIZE * 2)
        rect.center = (UI_SIZE * 7.5, UI_SIZE * 25)
        pygame.draw.rect(
            self.display_surface, GRAY, rect, border_radius=10)

        text = font.render("Continue", True, BLACK)
        text_rect = text.get_rect(center=rect.center)
        self.display_surface.blit(text, text_rect)
        self.continue_rect = rect

    def handle_continue_button(self):
        """
        Gère l'interaction avec le bouton pour continuer après les achats.
        """
        global can_receive_input
        mouse_pos = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed()[0] and can_receive_input:
            if self.continue_rect.collidepoint(mouse_pos):
                self.completed = True

                self.player.hp += self.player.winning_hp - self.player.losing_hp
                self.player.coins += self.player.winning_coins - self.player.losing_coins

                self.player.losing_coins = 0
                self.player.winning_coins = 0
                self.player.losing_hp = 0
                self.player.winning_hp = 0

                print(self.player.inventory)
        elif not pygame.mouse.get_pressed()[0]:
            can_receive_input = True
        return


class Item(pygame.sprite.Sprite):
    """
    Classe de base pour tous les objets achetables dans le magasin.
    """

    def __init__(self, name, description, price, position, player, use_once=False):
        """
        Initialise un objet achetable.

        Args:
            name (str): Nom de l'objet.
            description (str): Description de l'objet.
            price (int): Prix de l'objet en pièces.
            position (tuple): Position (x, y) de l'objet dans l'interface du magasin.
            player (Player): Référence au joueur.
            use_once (bool): Si True, l'objet peut être utilisé une seule fois.
        """
        super().__init__()
        self.name = name
        self.description = description
        self.price = price
        self.is_bought = False
        self.position = position
        self.display_surface = pygame.display.get_surface()
        self.use_once = use_once
        self.player = player

    def buy(self):
        """
        Achète l'objet si le joueur a assez de pièces et si l'objet n'a pas déjà été acheté.
        """
        if self.player.coins >= self.price and not self.is_bought:

            self.player.losing_coins += self.price
            self.is_bought = True

            if not self.use_once:
                self.use(self.player)
                return

            for item_data in self.player.inventory:
                if isinstance(item_data["item"], type(self)):
                    item_data["quantity"] += 1
                    return

    def use(self, player):
        """
        Utilise l'objet sur le joueur. Doit être redéfini dans les sous-classes.

        Args:
            player (Player): Le joueur sur lequel utiliser l'effet de l'objet.

        Returns:
            bool: True si l'objet a été utilisé avec succès, False sinon.

        Raises:
            NotImplementedError: Si la méthode n'est pas redéfinie dans une sous-classe.
        """
        raise NotImplementedError(
            "This method must be redefined in a subclass")

    def draw(self):
        """
        Dessine l'objet dans l'interface du magasin.
        """
        rect = pygame.Rect(
            self.position[0] * UI_SIZE, self.position[1] * UI_SIZE, UI_SIZE, UI_SIZE)
        if self.is_bought:
            pygame.draw.rect(self.display_surface, BLACK, rect)
        else:
            pygame.draw.rect(self.display_surface, BLACK,
                             rect, int(UI_SIZE*0.15))

        draw_text(self.display_surface, self.name,
                  (self.position[0] * UI_SIZE + (UI_SIZE * 2), self.position[1] * UI_SIZE), FONT, BLACK)
        draw_text(self.display_surface, f"{self.price}¢",
                  (self.position[0] * UI_SIZE + UI_SIZE / 2, self.position[1] * UI_SIZE + (UI_SIZE * 1.5)), DESC_FONT, BLACK, center=True)
        draw_text(self.display_surface, self.description,
                  (self.position[0] * UI_SIZE + (UI_SIZE * 2), self.position[1] * UI_SIZE + (UI_SIZE * 1.5)), DESC_FONT, BLACK, center_y=True, line_width=UI_SIZE * 10)

    def handle_input(self):
        """
        Gère les entrées de l'utilisateur pour cet objet.
        """
        rect = pygame.Rect(
            self.position[0] * UI_SIZE, self.position[1] * UI_SIZE, UI_SIZE, UI_SIZE)
        if rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.buy()
        global can_receive_input
        if not pygame.mouse.get_pressed()[0]:
            can_receive_input = True


"""
    Items that have a direct impact on the player
"""


class Gambler(Item):
    def __init__(self, position, player):
        """
        Initialise un objet Gambler qui peut augmenter ou diminuer aléatoirement les HP du joueur.

        Args:
            position (tuple): La position (x, y) de l'objet dans l'interface.
            player (Player): Le joueur qui peut acheter l'objet.
        """
        super().__init__("Gambler",
                         "Roll: If you roll 4+, gain 10¢. Otherwise, gain 0¢.", 5, position, player)

    def use(self, player):
        """
        Utilise l'objet pour augmenter ou diminuer aléatoirement les HP du joueur.

        Args:
            player (Player): Le joueur sur lequel utiliser l'objet.

        Returns:
            bool: True si l'objet a été utilisé avec succès, False sinon.
        """
        roll = randint(1, 6)
        if roll > 4:
            player.winning_coins += 10
            return True
        return False


class Light_Snack(Item):
    def __init__(self, position, player):
        """
        Initialise un objet Light_Snack qui restaure 1 point de vie.

        Args:
            position (tuple): La position (x, y) de l'objet dans l'interface.
            player (Player): Le joueur qui peut acheter l'objet.
        """
        super().__init__("Light Snack",
                         "Gain 3 HP.", 2, position, player)

    def use(self, player):
        """
        Utilise l'objet pour restaurer 1 point de vie au joueur.

        Args:
            player (Player): Le joueur sur lequel utiliser l'objet.

        Returns:
            bool: True si l'objet a été utilisé avec succès, False sinon.
        """
        player.winning_hp += 3
        return True


class Medium_Snack(Item):
    def __init__(self, position, player):
        """
        Initialise un objet Medium_Snack qui restaure 3 points de vie.

        Args:
            position (tuple): La position (x, y) de l'objet dans l'interface.
            player (Player): Le joueur qui peut acheter l'objet.
        """
        super().__init__("Meduim Snack",
                         "Gain 6 HP.", 9, position, player)

    def use(self, player):
        """
        Utilise l'objet pour restaurer 3 points de vie au joueur.

        Args:
            player (Player): Le joueur sur lequel utiliser l'objet.

        Returns:
            bool: True si l'objet a été utilisé avec succès, False sinon.
        """
        player.winning_hp += 6
        return True


class Hearty_Snack(Item):
    def __init__(self, position, player):
        """
        Initialise un objet Hearty_Snack qui restaure 6 points de vie.

        Args:
            position (tuple): La position (x, y) de l'objet dans l'interface.
            player (Player): Le joueur qui peut acheter l'objet.
        """
        super().__init__("Hearty Snack",
                         "Gain 9 HP", 13, position, player)

    def use(self, player):
        """
        Utilise l'objet pour restaurer 6 points de vie au joueur.

        Args:
            player (Player): Le joueur sur lequel utiliser l'objet.

        Returns:
            bool: True si l'objet a été utilisé avec succès, False sinon.
        """
        player.winning_hp += 9
        return True


"""
    Particular items
"""


class Doubling_Potion(Item):
    def __init__(self, position, player):
        """
        Initialise une Doubling_Potion qui double temporairement les pièces gagnées.

        Args:
            position (tuple): La position (x, y) de l'objet dans l'interface.
            player (Player): Le joueur qui peut acheter l'objet.
        """
        super().__init__("Doubling Potion",
                         "Double the number of a dice roll (use once).", 6, position, player, True)

    def use(self, player):
        """
        Utilise l'objet pour doubler temporairement les pièces gagnées par le joueur.

        Args:
            player (Player): Le joueur sur lequel utiliser l'objet.

        Returns:
            bool: True si l'objet a été utilisé avec succès, False sinon.
        """
        if player.movement_remaining == 0:
            player.movement_roll = randint(1, 6)
            player.movement_remaining = player.movement_roll
            player.movement_remaining *= 2
            player.show_adjacent_tiles = True
            return True
        return False


class Scroll_of_Mulligan(Item):
    def __init__(self, position, player):
        """
        Initialise un Scroll_of_Mulligan qui permet de relancer les dés de déplacement.

        Args:
            position (tuple): La position (x, y) de l'objet dans l'interface.
            player (Player): Le joueur qui peut acheter l'objet.
        """
        super().__init__("Scroll of Mulligan",
                         "re-roll your dice (use once).", 10, position, player, True)

    def use(self, player):
        """
        Utilise l'objet pour relancer les dés de déplacement du joueur.

        Args:
            player (Player): Le joueur sur lequel utiliser l'objet.

        Returns:
            bool: True si l'objet a été utilisé avec succès, False sinon.
        """
        if player.movement_remaining == player.movement_roll:
            player.movement_roll = randint(1, 6)
            player.movement_remaining = player.movement_roll
            player.show_adjacent_tiles = True
            return True
        return False


class Coin_Rush(Item):
    def __init__(self, position, player):
        """
        Initialise un objet Coin_Rush qui donne des pièces supplémentaires au joueur.

        Args:
            position (tuple): La position (x, y) de l'objet dans l'interface.
            player (Player): Le joueur qui peut acheter l'objet.
        """
        super().__init__("Coin Rush",
                         "All coins and treasure chests are worth 2x on next floor only.", 11, position, player)

    def use(self, player):
        """
        Utilise l'objet pour donner des pièces supplémentaires au joueur.

        Args:
            player (Player): Le joueur sur lequel utiliser l'objet.

        Returns:
            bool: True si l'objet a été utilisé avec succès, False sinon.
        """
        player.coin_multiplier = 2
        return True


class Break_on_Trought(Item):
    def __init__(self, position, player):
        """
        Initialise un objet Break_on_Trought permettant de traverser les murs.

        Args:
            position (tuple): La position (x, y) de l'objet dans l'interface.
            player (Player): Le joueur qui peut acheter l'objet.
        """
        super().__init__("Break on Through",
                         "Traver through a wall (use once).", 9, position, player, True)

    def use(self, level):
        """
        Utilise l'objet pour permettre au joueur de traverser temporairement les murs.

        Args:
            level (Player): Le joueur qui pourra traverser les murs.

        Returns:
            bool: True si l'objet a été utilisé avec succès, False sinon.
        """
        self.player.can_go_through_walls = True
        return True


class Teleport_Scroll(Item):
    def __init__(self, position, player):
        """
        Initialise un objet Teleport_Scroll permettant de se téléporter.

        Args:
            position (tuple): La position (x, y) de l'objet dans l'interface.
            player (Player): Le joueur qui peut acheter l'objet.
        """
        super().__init__("Teleport Scroll",
                         "Teleport to anywhere on the map (use once).", 11, position, player, True)

    def use(self, objects):
        """
        Utilise l'objet pour téléporter le joueur vers un téléporteur aléatoire.

        Args:
            objects (pygame.sprite.Group): Les objets du niveau parmi lesquels chercher des téléporteurs.

        Returns:
            bool: True si l'objet a été utilisé avec succès, False sinon.
        """
        while True:
            x, y = randint(0, int(WINDOW_WIDTH // TILE_SIZE - 1)) * TILE_SIZE, randint(0,
                                                                                       int(WINDOW_WIDTH // TILE_SIZE - 1)) * TILE_SIZE

            new_rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

            if not any(sprite.rect.colliderect(new_rect) for sprite in self.player.colliders["walls"]) and \
                    not any(sprite.rect.colliderect(new_rect) for sprite in self.player.colliders["objects"]):

                self.player.rect.x = x
                self.player.rect.y = y
                self.player.movement_remaining = 0
                return True
        return False


class Magic_Shield(Item):
    def __init__(self, position, player):
        """
        Initialise un objet Magic_Shield rendant le joueur invincible temporairement.

        Args:
            position (tuple): La position (x, y) de l'objet dans l'interface.
            player (Player): Le joueur qui peut acheter l'objet.
        """
        super().__init__("Magic Shield",
                         "Provides invinicibility on the next floor only. Enjoy!", 18, position, player)

    def use(self, player):
        """
        Utilise l'objet pour rendre le joueur invincible temporairement.

        Args:
            player (Player): Le joueur sur lequel utiliser l'objet.

        Returns:
            bool: True si l'objet a été utilisé avec succès, False sinon.
        """
        player.is_invincible = True
        return True


class Weaklings(Item):
    def __init__(self, position, player):
        """
        Initialise un objet Weaklings qui réduit les dégâts des ennemis à 1.

        Args:
            position (tuple): La position (x, y) de l'objet dans l'interface.
            player (Player): Le joueur qui peut acheter l'objet.
        """
        super().__init__("Weaklings",
                         "Act as if all monsters on the next floor have only 1 HP.", 15, position, player)

    def use(self, player):
        """
        Utilise l'objet pour réduire les dégâts des ennemis à 1.

        Args:
            player (Player): Le joueur sur lequel utiliser l'objet.

        Returns:
            bool: True si l'objet a été utilisé avec succès, False sinon.
        """
        player.weaklings = True
        return True
