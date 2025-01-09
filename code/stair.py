from settings import *
from object import *

class Stair(Object):

    def __init__(self, pos, groups):
        super().__init__(pos, groups)

    def design(self):

        image = pygame.image.load(
            join('graphics', 'stairs.png')).convert_alpha()
        image = pygame.transform.scale(
            image, (TILE_SIZE, TILE_SIZE))

        return image

    def on_collision(self, paused):
        print(f"Collision with me {self}")

        paused = True
        return paused

