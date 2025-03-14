"""
Module définissant la classe Chest, un objet coffre qui donne un nombre aléatoire de pièces.
"""

from settings import *
from object import *
from random import randint


class Chest(Object):
    """
    Classe représentant un coffre au trésor qui donne un nombre aléatoire de pièces lorsqu'il est ouvert.
    """

    def __init__(self, pos, groups):
        """
        Initialise un coffre à la position donnée et l'ajoute aux groupes spécifiés.

        Args:
            pos (tuple): La position (x, y) du coffre.
            groups (list): Les groupes de sprites auxquels le coffre appartient.
        """
        super().__init__(pos, groups)

    def design(self):
        """
        Crée l'image du coffre.

        Returns:
            pygame.Surface: L'image du coffre.
        """
        image = pygame.image.load(
            join('graphics', 'treasure_chest.png')).convert_alpha()
        image = pygame.transform.scale(
            image, (get_tile_size(), get_tile_size()))

        return image

    def on_collision(self, player):
        """
        Gestion de la collision avec le joueur. Donne un nombre aléatoire de pièces entre 1 et 6,
        modifié par le multiplicateur de pièces du joueur.

        Args:
            player (Player): Le joueur en collision avec ce coffre.

        Returns:
            Player: Le joueur après modification de son score.
        """
        print(f"Collision with me {self}")
        if self.has_already_been_used():
            return player

        winning_coins = randint(1, 6)
        player.winning_coins += winning_coins * player.coin_multiplier

        self.used = True
        self.has_already_been_used()
        return player
