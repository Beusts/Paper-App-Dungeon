from settings import *
from random import randint

class Wall(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        """
        Initialise un mur à la position donnée et l'ajoute aux groupes spécifiés.

        Args:
            pos (tuple): La position (x, y) du mur.
            groups (list): Les groupes de sprites auxquels le mur appartient.
        """
        super().__init__(groups)
        gray = randint(100, 200)
        self.color = (gray, gray, gray)
        self.rect = pygame.Rect(
            (pos[0] + TILE_SIZE * 0.05, pos[1] + TILE_SIZE * 0.05),
            (TILE_SIZE * 0.9, TILE_SIZE * 0.9)
        )

    def draw(self, surface):
        """
        Dessine le mur sur la surface spécifiée.

        Args:
            surface (pygame.Surface): La surface sur laquelle dessiner le mur.
        """
        image = pygame.Surface(
            (TILE_SIZE * 0.9, TILE_SIZE * 0.9), pygame.SRCALPHA)
        pygame.draw.rect(image, self.color, image.get_rect(), border_radius=4)
        surface.blit(image, self.rect)
