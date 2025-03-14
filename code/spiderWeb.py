"""
Module définissant la classe SpiderWeb, un objet qui ralentit le joueur et lui fait perdre des pièces.
"""

from settings import *
from object import *
from pygame.math import Vector2
from random import randint


class SpiderWeb(Object):
    """
    Classe représentant une toile d'araignée qui arrête le mouvement du joueur et lui fait perdre des pièces.
    """

    def __init__(self, pos, groups):
        """
        Initialise une toile d'araignée à la position donnée et l'ajoute aux groupes spécifiés.

        Args:
            pos (tuple): La position (x, y) de la toile d'araignée.
            groups (list): Les groupes de sprites auxquels la toile appartient.
        """
        super().__init__(pos, groups)

    def design(self):
        """
        Crée l'image de la toile d'araignée.

        Returns:
            pygame.Surface: L'image de la toile d'araignée.
        """
        design = pygame.image.load(
            join('graphics', 'spiderweb.png')).convert_alpha()
        design = pygame.transform.scale(
            design, (get_tile_size(), get_tile_size()))
        return design

    def on_collision(self, player):
        """
        Gestion de la collision avec le joueur. Arrête son mouvement et lui fait perdre des pièces.

        Args:
            player (Player): Le joueur en collision avec cette toile d'araignée.

        Returns:
            Player: Le joueur après modification de son état et de ses pièces.
        """
        if self.has_already_been_used():
            return player

        # Stop the player
        player.direction = Vector2(0, 0)
        player.movement_remaining = 0
        player.last_move_time = player.current_time = 0
        player.movement_roll = 0
        player.can_move = True

        # roll the die to determine how many coins the player lose
        losing_coins = randint(1, 6)
        player.losing_coins += losing_coins

        print(f"losing coins {losing_coins}")

        self.used = True
        self.has_already_been_used()
        return player
