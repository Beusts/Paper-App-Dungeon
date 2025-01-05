from settings import *
from object import *

class StandardEnemy(Object):

    def __init__(self, pos, groups):
        """
        Initialise un ennemi à la position donnée et l'ajoute aux groupes spécifiés. hérite de la classe object

        Args:
            pos (tuple): La position (x, y) de l'ennemi.
            groups (list): Les groupes de sprites auxquels l'enemy appartient.
        """
        super().__init__(pos, groups)

    def design(self):
        design = pygame.image.load(
            join('graphics', 'standard_enemy.png')).convert_alpha()
        design = pygame.transform.scale(
            design, (TILE_SIZE, TILE_SIZE))
        return design

    def interaction(self):
        return
