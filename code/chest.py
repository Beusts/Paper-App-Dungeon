from settings import *
from object import *
from random import randint

class Chest(Object):

    def __init__(self, pos, groups):
        """
        Initialise un ennemi à la position donnée et l'ajoute aux groupes spécifiés.

        Args:
            pos (tuple): La position (x, y) de l'ennemi.
            groups (list): Les groupes de sprites auxquels l'ennemi appartient.
            value (int): La valeur associée à l'ennemi.
        """
        super().__init__(pos, groups)

    def design(self):
        """
        Crée l'image de l'ennemi avec un numéro dessus.

        Returns:
            pygame.Surface: L'image de l'ennemi avec le numéro ajouté.
        """
        image = pygame.image.load(
            join('graphics', 'locks.png')).convert_alpha()
        image = pygame.transform.scale(
            image, (TILE_SIZE, TILE_SIZE))

        return image

    def on_collision(self, player):

        print(f"Collision with me {self}")
        if self.has_already_been_used() : return player

        winning_coins = randint(1, 6)
        player.winning_coins += winning_coins

        self.used = True
        self.has_already_been_used()
        return player
