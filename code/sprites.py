from settings import *


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        """
        Initialise un mur à la position donnée et l'ajoute aux groupes spécifiés.

        Args:
            pos (tuple): La position (x, y) du mur.
            groups (list): Les groupes de sprites auxquels le mur appartient.
        """
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill('white')
        self.rect = self.image.get_rect(topleft=pos)

    def draw(self, surface):
        """
        Dessine le mur sur la surface spécifiée.

        Args:
            surface (pygame.Surface): La surface sur laquelle dessiner le mur.
        """
        # Dessine un contour gris autour du mur
        pygame.draw.rect(self.image, 'gray', self.image.get_rect(), 1)
        surface.blit(self.image, self.rect)
