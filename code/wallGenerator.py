
from settings import *
from random import randint


class WallGenerator(pygame.sprite.Sprite):

    def __init__(self, current_object_on_level, wall_pourcentage, level_size):
        super().__init__()
        self.wall_pourcentage = wall_pourcentage
        self.current_object_on_level = current_object_on_level
        self.level_size_rows, self.level_size_cols = level_size

    def generate_wall_level(self):
        size_level = self.level_size_rows * self.level_size_cols
        max_walls = size_level * self.wall_pourcentage

        wall_count = 0
        while wall_count < max_walls:
            block = self.generate_wall_block()
            wall_count += block["size"][0] * block["size"][1]

        return self.current_object_on_level

    def generate_wall_block(self):

        self.generate_wall_arround_level()

        while True:
            size_block = (randint(1,3), 1)
            position = (randint(1, self.level_size_rows - 2), randint(1, self.level_size_cols - 2))
            block = {"size": size_block, "position": position, "orientation": randint(1, 2)}

            if block["orientation"] == 2: block["size"] = (size_block[1], size_block[0])

            if self.is_valid_block(block):
                self.add_block(block)
                return block

    def generate_wall_arround_level(self, ):
        for row in range(15):
            for col in range(15):

                # Place walls all around the map
                if row == 0 or row == self.level_size_rows - 1 or col == 0 or col == self.level_size_cols - 1:
                    self.current_object_on_level.append((row, col))
                    continue

    def is_valid_block(self, block):
        for i in range(block["size"][0]):
            for j in range(block["size"][1]):
                for x, y in self.current_object_on_level:
                    if block["position"][0] + i == x and block["position"][1] + j == y: return False

                    if block["position"][0] + i > self.level_size_rows and block["position"][1] + j > self.level_size_cols: return False

        return True

    def add_block(self, block):
        for i in range(block["size"][0]):
            for j in range(block["size"][1]):
                self.current_object_on_level.append( (block["position"][0] + i, block["position"][1] + j) )