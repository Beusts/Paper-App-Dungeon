"""
Module définissant la classe Coin, un objet collectible qui ajoute une pièce au joueur.
"""

from settings import *
from object import *
from random import randint


class Coin(Object):
    """
    Classe représentant une pièce que le joueur peut collecter pour augmenter son score.
    """

    def __init__(self, pos, groups):
        """
        Initialise une pièce à la position donnée et l'ajoute aux groupes spécifiés.

        Args:
            pos (tuple): La position (x, y) de la pièce.
            groups (list): Les groupes de sprites auxquels la pièce appartient.
        """
        super().__init__(pos, groups)

    def design(self):
        """
        Crée l'image de la pièce.

        Returns:
            pygame.Surface: L'image de la pièce.
        """
        image = pygame.image.load(
            join('graphics', 'coin.png')).convert_alpha()
        image = pygame.transform.scale(
            image, (get_tile_size(), get_tile_size()))

        return image

    def on_collision(self, player):
        """
        Gestion de la collision avec le joueur. Ajoute une pièce au score du joueur, 
        modifié par son multiplicateur de pièces.

        Args:
            player (Player): Le joueur en collision avec cette pièce.

        Returns:
            Player: Le joueur après modification de son score.
        """
        print(f"Collision with me {self}")
        if self.has_already_been_used():
            return player

        player.winning_coins += 1 * player.coin_multiplier

        self.used = True
        self.has_already_been_used()
        return player
