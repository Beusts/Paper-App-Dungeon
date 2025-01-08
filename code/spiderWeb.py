from settings import *
from object import *
from pygame.math import Vector2
from random import randint


class SpiderWeb(Object):

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
            join('graphics', 'spiderweb.png')).convert_alpha()
        design = pygame.transform.scale(
            design, (TILE_SIZE, TILE_SIZE))
        return design

    def on_collision(self, player):

        if self.has_already_been_used(): return player

        # Stop the player
        player.direction = Vector2(0, 0)
        player.movement_remaining = 0
        player.last_move_time = player.current_time = 0
        player.movement_roll = 0
        player.can_move = True

        # roll the die to determine how many coins the player lose
        losing_coins = randint(1, 6)
        player.losing_coins += losing_coins

        print(f"losing coins {losing_coins}")

        self.used = True
        self.has_already_been_used()
        return player
