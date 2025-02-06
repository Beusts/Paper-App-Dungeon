from settings import *
from object import *


class Lock(Object):

    def __init__(self, pos, groups, lock):
        """
        Initialise un ennemi à la position donnée et l'ajoute aux groupes spécifiés.

        Args:
            pos (tuple): La position (x, y) de l'ennemi.
            groups (list): Les groupes de sprites auxquels l'ennemi appartient.
            value (int): La valeur associée à l'ennemi.
        """
        self.lock = lock
        groups.append(lock)
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
            image, (get_tile_size(), get_tile_size()))

        return image

    def on_collision(self, player):

        if self.used:
            return player

        print(f"Collision with me {self}")

        if player.keys >= 1:
            # change the lock into a simple case
            self.image.fill((0, 0, 0, 0))
            player.keys -= 1
            self.used = True
            self.remove(self.lock)

        return player
