"""
Module définissant la classe MysteryHeart, un objet qui restaure une quantité aléatoire de points de vie.
"""

from settings import *
from object import *
from random import randint


class MysteryHeart(Object):
    """
    Classe représentant un cœur mystère qui restaure une quantité aléatoire de points de vie au joueur.
    """

    def __init__(self, pos, groups):
        """
        Initialise un cœur mystère à la position donnée et l'ajoute aux groupes spécifiés.

        Args:
            pos (tuple): La position (x, y) du cœur.
            groups (list): Les groupes de sprites auxquels le cœur appartient.
        """
        super().__init__(pos, groups)

    def design(self):
        """
        Crée l'image du cœur mystère avec un point d'interrogation.

        Returns:
            pygame.Surface: L'image du cœur mystère.
        """
        image = pygame.image.load(
            join('graphics', 'heart.png')).convert_alpha()
        image = pygame.transform.scale(
            image, (get_tile_size(), get_tile_size()))

        font = pygame.font.Font(None, int(get_tile_size() * 0.5))

        text_surface = font.render("?", True, (0, 0, 0))
        text_rect = text_surface.get_rect(
            centerx=get_tile_size() / 2, centery=get_tile_size() / 2)

        enemy = image.copy()
        enemy.blit(text_surface, text_rect)

        return enemy

    def on_collision(self, player):
        """
        Gestion de la collision avec le joueur. Restaure une quantité aléatoire de points de vie entre 1 et 6.

        Args:
            player (Player): Le joueur en collision avec ce cœur.

        Returns:
            Player: Le joueur après modification de ses points de vie.
        """
        if self.has_already_been_used():
            return player

        print(f"Collisions with me {self}")
        player.winning_hp += randint(1, 6)
        self.used = True
        self.has_already_been_used()

        return player
