from settings import *
from object import *
from random import randint


class MysteryEnemy(Object):

    def __init__(self, pos, groups):
        """
        Initialise un ennemi à la position donnée et l'ajoute aux groupes spécifiés. hérite de la classe object

        Args:
            pos (tuple): La position (x, y) de l'ennemi.
            groups (list): Les groupes de sprites auxquels l'enemy appartient.
        """
        super().__init__(pos, groups)

    def design(self):
        image = pygame.image.load(
            join('graphics', 'enemy.png')).convert_alpha()
        image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))

        font = pygame.font.Font(None, int(TILE_SIZE * 0.5))

        text_surface = font.render("?", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=image.get_rect().center)

        enemy = image.copy()
        enemy.blit(text_surface, text_rect)

        return enemy

    def on_collision(self, player):
        if self.has_already_been_used(): return player

        print(f"Collisions with me {self}")
        player.hp = player.hp - randint(1, 6)
        self.used = True
        self.has_already_been_used()

        return player
