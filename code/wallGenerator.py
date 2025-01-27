
from settings import *
from random import randint


class WallGenerator(pygame.sprite.Sprite):

    def __init__(self, current_object_on_level, wall_pourcentage, level_size, generation = 3):
        super().__init__()
        self.wall_pourcentage = wall_pourcentage
        self.current_object_on_level = current_object_on_level
        self.level_size_rows, self.level_size_cols = level_size
        self.generation = generation


    # def generate_walls(self, block):
    # 
    #     for i in range(self.generation):
    #         block = self.divide_part(block)
    # 
    #     return self.current_object_on_level
    # 
    # def divide_part(self, block):
    #     self.generate_wall_arround_level()
    # 
    #     x, y, width, height = block
    # 
    #     _len = x + width
    #     large = y + height
    # 
    #     orientation = self.chosing_orientation()
    #     wall_x = x
    #     wall_y = y
    # 
    #     walls = []
    # 
    #     if orientation == "vertical":
    #         wall_x = randint(x + width // 4, x + width - width // 4)
    #         for i in range(large):
    #             walls.append((wall_x, wall_y + i))
    #     else:
    #         wall_y = randint(y + height // 4, y + height - height // 4)
    # 
    #         for i in range(large):
    #             walls.append((wall_x + i, wall_y))
    # 
    #     print(walls)
    #     self.add_block(walls)
    #     self.making_gap(walls, orientation)
    # 
    # def chosing_orientation(self):
    #     res = randint(1, 2)
    # 
    #     if res == 1:
    #         return "vertical"
    #     return "horizontal"
    # 
    # def generate_wall_arround_level(self, ):
    #     for row in range(15):
    #         for col in range(15):
    # 
    #             # Place walls all around the map
    #             if row == 0 or row == self.level_size_rows - 1 or col == 0 or col == self.level_size_cols - 1:
    #                 self.current_object_on_level.append((row, col))
    #                 continue
    # 
    # def add_block(self, wall):
    #     for i in range(len(wall)):
    #         if self.is_valid_wall(wall[i]):
    #             self.current_object_on_level.append(wall[i])
    # 
    # def is_valid_wall(self, wall):
    # 
    #     for i in range(self.level_size_rows):
    #         for i in range(self.level_size_cols):
    #             if wall[0] == 0 or wall[1] == 0 \
    #                 or wall[0] == self.level_size_rows - 1 or wall[1] == self.level_size_cols - 1:
    #                 return False
    # 
    #     if wall in self.current_object_on_level:
    #         return False
    # 
    #     return True
    # 
    # def making_gap(self, walls, orientation):
    # 
    #     size_gap = randint(1, 4)
    # 
    #     while True:
    #         deleted_wall_index = randint(0, len(walls) - 1)
    #         deleted_wall = walls[deleted_wall_index]
    # 
    #         if deleted_wall in self.current_object_on_level and not(\
    #                 deleted_wall[0] == 0 or deleted_wall[1] == 0 \
    #                 or deleted_wall[0] == self.level_size_rows - 1 or deleted_wall[1] == self.level_size_cols - 1):
    #             break
    # 
    #     for i in range(size_gap):
    # 
    #         if orientation == "vertical":
    #             next = deleted_wall[0], deleted_wall[1] + i
    # 
    #             if next not in self.current_object_on_level:
    #                 continue
    # 
    #             self.current_object_on_level.remove(next)
    # 
    #         else:
    #             next = deleted_wall[0] + i, deleted_wall[1]
    # 
    #             if next not in self.current_object_on_level:
    #                 continue
    # 
    #             self.current_object_on_level.remove(next)

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

# if __name__ == '__main__':
    # wall = WallGenerator([], 0.15, (15, 15))
    # walls = wall.divide_part((1, 1, 13, 13))
    #
    # _str = ""
    # for i in range(15):
    #     for j in range(15):
    #         if (i, j) in wall.current_object_on_level:
    #             _str += "1"
    #         else:
    #             _str += "0"
    #     _str += "\n"
    #
    # print(_str)