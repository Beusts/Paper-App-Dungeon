from contextlib import nullcontext

from settings import *

class Object(pygame.sprite.Sprite):
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

    def draw(self, surface):
        """
        Dessine l'objet sur la surface spécifiée.

        Args:
            surface (pygame.Surface): La surface sur laquelle dessiner l'objet.
        """
        surface.blit(self.image, self.rect)

    def design(self):
        """
        Determine ce que l'objet doit ressembler

        """
        raise NotImplementedError("This method must be redefined in a subclass")

    def on_collision(self, player):
        """
        Traite l'interaction avec un objet

        """
        raise NotImplementedError("This method must be redefined in a subclass")

    def has_already_been_used(self):
        if self.used:
            print(f"I've already been used {self}")
            image =pygame.image.load(
                join('graphics', 'dust.png')).convert_alpha()
            image = pygame.transform.scale(
                image, (TILE_SIZE, TILE_SIZE))

            self.image = image
            return True
        return False
