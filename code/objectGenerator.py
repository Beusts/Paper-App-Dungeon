
from settings import *
from random import randint


class ObjectsGenerator(pygame.sprite.Sprite):

    def __init__(self, current_object_on_level, wall, object_pourcentage, level_size):
        super().__init__()
        self.object_pourcentage = object_pourcentage
        self.current_object_on_level = current_object_on_level
        self.current_coo_object = wall
        self.level_size_rows, self.level_size_cols = level_size

    def generate_objects_level(self):

        size_level = self.level_size_rows * self.level_size_cols
        max_objects = size_level * self.object_pourcentage

        # Place a player on the level
        coo_player = self.generate_point(1, self.level_size_rows - 2)

        # Place a stair on the level
        coo_stair = self.generate_point(1, self.level_size_rows - 2)
        self.current_object_on_level.append({"coo": coo_player, "symbol": "P"})
        self.current_object_on_level.append({"coo": coo_stair, "symbol": "S"})

        object_count = 2
        
        while object_count < max_objects:
            object = self.generate_random_object()
            self.current_object_on_level.append(object)
            object_count += 1

        return self.current_object_on_level

    def generate_random_object(self):

        object_id = randint(1, 6)

        if object_id == 1: # Standart Enemy
            value = randint(1, 6)
            symbol = "Se" + str(value)
            return {"coo": self.generate_point(1, self.level_size_rows - 2), "symbol": symbol}

        if object_id == 2: # Mystery Enemy
            return {"coo": self.generate_point(1, self.level_size_rows - 2), "symbol": "Me"}

        if object_id == 3: # Standart Heart
            value = randint(1, 6)
            symbol = "Sh" + str(value)
            return {"coo": self.generate_point(1, self.level_size_rows - 2), "symbol": symbol}

        if object_id == 4: # Mystery Heart
            return {"coo": self.generate_point(1, self.level_size_rows - 2), "symbol": "Me"}

        if object_id == 5: # Coin
            return {"coo": self.generate_point(1, self.level_size_rows - 2), "symbol": "Co"}

        if object_id == 6: # Chest
            return {"coo": self.generate_point(1, self.level_size_rows - 2), "symbol": "C"}


    def generate_point(self, min, max):
        row = randint(min, max)
        col = randint(min, max)
        point = (row, col)

        if point not in self.current_coo_object:
            self.current_coo_object.append(point)
            return point

        while point in self.current_coo_object:
            row = randint(min, max)
            col = randint(min, max)
            point = (row, col)

        self.current_coo_object.append(point)
        return point