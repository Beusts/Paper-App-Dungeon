from settings import *
from object import *


class Stair(Object):

    def __init__(self, pos, groups):
        super().__init__(pos, groups)

    def design(self):

        image = pygame.image.load(
            join('graphics', 'stairs.png')).convert_alpha()
        image = pygame.transform.scale(
            image, (get_tile_size(), get_tile_size()))

        return image

    def on_collision(self, level):
        print(f"Collision with me {self}")
        level.paused = True
