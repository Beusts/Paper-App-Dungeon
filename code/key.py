"""
Module définissant la classe Key, un objet clé permettant d'ouvrir les serrures.
"""

from settings import *
from object import *


class Key(Object):

    def __init__(self, pos, groups):
        """
        Initialise une clé à la position donnée et l'ajoute aux groupes spécifiés.

        Args:
            pos (tuple): La position (x, y) de la clé
            groups (list): Les groupes de sprites auxquels la clé appartient
        """
        super().__init__(pos, groups)

    def design(self):
        """
        Crée l'image de la clé.

        Returns:
            pygame.Surface: L'image de la clé
        """
        image = pygame.image.load(
            join('graphics', 'keys.png')).convert_alpha()
        image = pygame.transform.scale(
            image, (get_tile_size(), get_tile_size()))

        return image

    def on_collision(self, player):
        """
        Gestion de la collision avec un joueur. Ajoute une clé à l'inventaire du joueur.

        Args:
            player (Player): Le joueur en collision avec cette clé

        Returns:
            Player: Le joueur après modification de son inventaire
        """
        print(f"Collision with me {self}")

        if self.has_already_been_used():
            return player

        player.keys += 1
        self.used = True
        self.has_already_been_used()
        print(f"number of key {player.keys}")
        return player
