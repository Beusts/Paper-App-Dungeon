from settings import *
from object import *
from random import randint


class MysteryHeart(Object):

    def __init__(self, pos, groups):
        """
        Initialise un mystery heart à la position donnée et l'ajoute aux groupes spécifiés. hérite de la classe object

        Args:
            pos (tuple): La position (x, y) du coeur.
            groups (list): Les groupes de sprites auxquels le coeur appartient.
        """
        super().__init__(pos, groups)

    def design(self):
        image = pygame.image.load(
            join('graphics', 'heart.png')).convert_alpha()
        image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))

        font = pygame.font.Font(None, int(TILE_SIZE * 0.5))

        text_surface = font.render("?", True, (0, 0, 0))
        text_rect = text_surface.get_rect(
            centerx=TILE_SIZE / 2, centery=TILE_SIZE / 2)

        enemy = image.copy()
        enemy.blit(text_surface, text_rect)

        return enemy

    def on_collision(self, player):
        if self.has_already_been_used():
            return player

        print(f"Collisions with me {self}")
        player.winning_hp += randint(1, 6)
        self.used = True
        self.has_already_been_used()

        return player
