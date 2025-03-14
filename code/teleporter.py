"""
Module définissant la classe Teleporter, un objet permettant de se téléporter vers un autre téléporteur.
"""

from settings import *
from object import *
from random import randint
from pygame.math import Vector2


class Teleporter(Object):

    def __init__(self, pos, groups):
        """
        Initialise un téléporteur à la position donnée et l'ajoute aux groupes spécifiés.

        Args:
            pos (tuple): La position (x, y) du téléporteur
            groups (list): Les groupes de sprites auxquels le téléporteur appartient
        """
        super().__init__(pos, groups)

    def design(self):
        """
        Crée l'image du téléporteur.

        Returns:
            pygame.Surface: L'image du téléporteur
        """
        image = pygame.image.load(
            join('graphics', 'teleporters.png')).convert_alpha()
        image = pygame.transform.scale(
            image, (get_tile_size(), get_tile_size()))

        return image

    def on_collision(self, player, objects):
        """
        Gestion de la collision avec un téléporteur. Téléporte le joueur vers un autre téléporteur aléatoire.

        Args:
            player (Player): Le joueur en collision avec ce téléporteur
            objects (pygame.sprite.Group): Groupe de sprites contenant tous les objets du niveau

        Returns:
            Player: Le joueur après téléportation
        """
        print(f"Collisions with me {self}")

        other_teleporter = []

        for o in objects:
            if type(o).__name__ == "Teleporter":
                if o != self:
                    other_teleporter.append(o)

        teleporter_id = randint(0, len(other_teleporter) - 1)
        teleporter = other_teleporter[teleporter_id]

        player.rect.x = teleporter.pos[0]
        player.rect.y = teleporter.pos[1]

        return player
