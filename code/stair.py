"""
Module définissant la classe Stair, un objet escalier permettant de terminer un niveau.
"""

from settings import *
from object import *


class Stair(Object):
    """
    Classe représentant un escalier qui permet de terminer un niveau.
    """

    def __init__(self, pos, groups):
        """
        Initialise un escalier à la position donnée et l'ajoute aux groupes spécifiés.

        Args:
            pos (tuple): La position (x, y) de l'escalier
            groups (list): Les groupes de sprites auxquels l'escalier appartient
        """
        super().__init__(pos, groups)

    def design(self):
        """
        Crée l'image de l'escalier.

        Returns:
            pygame.Surface: L'image de l'escalier
        """
        image = pygame.image.load(
            join('graphics', 'stairs.png')).convert_alpha()
        image = pygame.transform.scale(
            image, (get_tile_size(), get_tile_size()))

        return image

    def on_collision(self, level):
        """
        Gestion de la collision avec l'escalier. Met le niveau en pause pour afficher l'écran de fin de niveau.

        Args:
            level (Level): Le niveau actuel
        """
        print(f"Collision with me {self}")
        level.paused = True
