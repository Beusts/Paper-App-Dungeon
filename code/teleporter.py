from settings import *
from object import *
from random import randint
from pygame.math import Vector2


class Teleporter(Object):

    def __init__(self, pos, groups):

        super().__init__(pos, groups)



    def design(self):
        image = pygame.image.load(
            join('graphics', 'teleporters.png')).convert_alpha()
        image = pygame.transform.scale(
            image, (TILE_SIZE, TILE_SIZE))

        return image

    def on_collision(self, player, objects):

        print(f"Collisions with me {self}")

        other_teleporter = []

        for o in objects:
            if type(o).__name__ == "Teleporter":
                if o != self:
                    other_teleporter.append(o)

        teleporter_id = randint(0, len(other_teleporter) - 1)
        teleporter = other_teleporter[teleporter_id]

        player.rect.x = teleporter.pos[0]
        player.rect.y = teleporter.pos[1]

        return player
