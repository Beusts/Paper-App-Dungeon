"""
Module définissant la classe MysteryEnemy, un ennemi qui inflige des dégâts aléatoires au joueur.
"""

from settings import *
from object import *
from random import randint


class MysteryEnemy(Object):
    """
    Classe représentant un ennemi mystère qui inflige des dégâts aléatoires au joueur.
    """

    def __init__(self, pos, groups):
        """
        Initialise un ennemi mystère à la position donnée et l'ajoute aux groupes spécifiés.

        Args:
            pos (tuple): La position (x, y) de l'ennemi.
            groups (list): Les groupes de sprites auxquels l'ennemi appartient.
        """
        super().__init__(pos, groups)

    def design(self):
        """
        Crée l'image de l'ennemi mystère avec un point d'interrogation.

        Returns:
            pygame.Surface: L'image de l'ennemi mystère.
        """
        image = pygame.image.load(
            join('graphics', 'enemy.png')).convert_alpha()
        image = pygame.transform.scale(
            image, (get_tile_size(), get_tile_size()))

        font = pygame.font.Font(None, int(get_tile_size() * 0.5))

        text_surface = font.render("?", True, BLACK)
        text_rect = text_surface.get_rect(
            centerx=get_tile_size() / 2, centery=get_tile_size() / 2)

        enemy = image.copy()
        enemy.blit(text_surface, text_rect)

        return enemy

    def on_collision(self, player):
        """
        Gestion de la collision avec le joueur. Inflige des dégâts aléatoires entre 1 et 6.

        Args:
            player (Player): Le joueur en collision avec cet ennemi.

        Returns:
            Player: Le joueur après modification de ses points de vie.
        """
        if self.has_already_been_used():
            return player

        print(f"Collisions with me {self}")
        if not player.is_invincible:
            if player.weaklings:
                player.losing_hp += 1
            else:
                player.losing_hp += randint(1, 6)
        self.used = True
        self.has_already_been_used()

        return player
