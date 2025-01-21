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
            (pos[0], pos[1]),
            (get_tile_size() * 0.9, get_tile_size() * 0.9)
        )
        self.rect.center = (pos[0] + get_tile_size() //
                            2, pos[1] + get_tile_size() // 2)

    def draw(self, surface):
        """
        Dessine le mur sur la surface spécifiée.

        Args:
            surface (pygame.Surface): La surface sur laquelle dessiner le mur.
        """
        image = pygame.Surface(
            (get_tile_size() * 0.9, get_tile_size() * 0.9), pygame.SRCALPHA)
        pygame.draw.rect(image, self.color, image.get_rect(), border_radius=4)
        surface.blit(image, self.rect)
