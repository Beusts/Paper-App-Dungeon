"""
Module définissant la classe de base Object pour tous les objets interactifs du jeu.
"""

from contextlib import nullcontext

from settings import *


class Object(pygame.sprite.Sprite):
    """
    Classe de base pour tous les objets interactifs du jeu.
    Cette classe fournit les fonctionnalités communes à tous les objets comme
    l'initialisation, le dessin et la gestion des collisions.
    """

    def __init__(self, pos, groups):
        """
        Initialise un objet à la position donnée et l'ajoute aux groupes spécifiés.

        Args:
            pos (tuple): La position (x, y) de l'objet.
            groups (list): Les groupes de sprites auxquels l'objet appartient.
        """
        super().__init__(groups)
        self.image = self.design()
        self.rect = self.image.get_rect(topleft=pos)
        self.used = False

        self.pos = pos

    def draw(self, surface):
        """
        Dessine l'objet sur la surface spécifiée.

        Args:
            surface (pygame.Surface): La surface sur laquelle dessiner l'objet.
        """
        surface.blit(self.image, self.rect)

    def design(self):
        """
        Détermine l'apparence de l'objet. Cette méthode doit être redéfinie dans les sous-classes.

        Raises:
            NotImplementedError: Si la méthode n'est pas redéfinie dans une sous-classe.

        Returns:
            pygame.Surface: L'image représentant l'objet.
        """
        raise NotImplementedError(
            "This method must be redefined in a subclass")

    def on_collision(self, player):
        """
        Gère l'interaction avec le joueur lors d'une collision. 
        Cette méthode doit être redéfinie dans les sous-classes.

        Args:
            player (Player): Le joueur en collision avec cet objet.

        Raises:
            NotImplementedError: Si la méthode n'est pas redéfinie dans une sous-classe.

        Returns:
            Player: Le joueur après interaction avec l'objet.
        """
        raise NotImplementedError(
            "This method must be redefined in a subclass")

    def has_already_been_used(self):
        """
        Vérifie si l'objet a déjà été utilisé et change son apparence si c'est le cas.

        Returns:
            bool: True si l'objet a déjà été utilisé, False sinon.
        """
        if self.used:
            print(f"I've already been used {self}")
            image = pygame.image.load(
                join('graphics', 'dust.png')).convert_alpha()
            image = pygame.transform.scale(
                image, (get_tile_size(), get_tile_size()))

            self.image = image
            return True
        return False
