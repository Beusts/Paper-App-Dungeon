"""
Module définissant la classe Lock, un objet verrou nécessitant une clé pour être déverrouillé.
"""

from settings import *
from object import *


class Lock(Object):
    """
    Classe représentant un verrou qui bloque le passage à moins que le joueur possède une clé.
    """

    def __init__(self, pos, groups, lock):
        """
        Initialise un verrou à la position donnée et l'ajoute aux groupes spécifiés.

        Args:
            pos (tuple): La position (x, y) du verrou.
            groups (list): Les groupes de sprites auxquels le verrou appartient.
            lock (pygame.sprite.Group): Groupe spécial pour les verrous qui bloquent le passage.
        """
        self.lock = lock
        groups.append(lock)
        super().__init__(pos, groups)

    def design(self):
        """
        Crée l'image du verrou.

        Returns:
            pygame.Surface: L'image du verrou.
        """
        image = pygame.image.load(
            join('graphics', 'locks.png')).convert_alpha()
        image = pygame.transform.scale(
            image, (get_tile_size(), get_tile_size()))

        return image

    def on_collision(self, player):
        """
        Gestion de la collision avec le joueur. Le verrou peut être déverrouillé si le joueur possède une clé.

        Args:
            player (Player): Le joueur en collision avec ce verrou.

        Returns:
            Player: Le joueur après interaction avec le verrou.
        """
        if self.used:
            return player

        print(f"Collision with me {self}")

        if player.keys >= 1:
            # change the lock into a simple case
            self.image.fill((0, 0, 0, 0))
            player.keys -= 1
            self.used = True
            self.remove(self.lock)

        return player
