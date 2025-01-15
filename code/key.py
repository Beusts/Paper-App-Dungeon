from settings import *
from object import *


class Key(Object):

    def __init__(self, pos, groups):
        super().__init__(pos, groups)

    def design(self):

        image = pygame.image.load(
            join('graphics', 'keys.png')).convert_alpha()
        image = pygame.transform.scale(
            image, (get_tile_size(), get_tile_size()))

        return image

    def on_collision(self, player):

        print(f"Collision with me {self}")

        if self.has_already_been_used():
            return player

        player.keys += 1
        self.used = True
        self.has_already_been_used()
        print(f"number of key {player.keys}")
        return player
