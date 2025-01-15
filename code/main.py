import copy
import csv
import math

from settings import *
from level import Level
from shop import Shop
from player import Player
from os.path import join
from random import randint


class Game:
    def __init__(self):
        """
        Initialise le jeu, la fenêtre d'affichage et le niveau actuel.
        """
        pygame.init()
        self.display_surface = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Paper App Dungeon')

        self.clock = pygame.time.Clock()

        self.difficulty = 1

        wall_pourcentage = 0.6 * self.difficulty
        self.rule = {
            'size': (15, 15),
            'walls_pourcentage': wall_pourcentage
        }
        self.current_object_on_level = []
        self.write_level()



        self.level_map_files = {0: 'gen_pro', 1: '1', 2: 'test'}
        self.current_level_index = 0
        self.player = Player()

        self.current_stage = Level(self.level_map_files[self.current_level_index], self.player)
        # self.current_stage = Shop('0', self.player)




    def change_level(self):
        self.current_level_index += 1

        if self.current_level_index >= len(self.level_map_files):
            print("game over")
        else:
            new_level_file = self.level_map_files[self.current_level_index]

            if self.current_level_index % 6 == 0:
                self.current_stage = Shop('0', self.player)
            else:
                self.current_stage = Level(new_level_file, self.player)
            print("changing level")

    def run(self):
        """
        Exécute la boucle principale du jeu.
        """
        while True:
            dt = self.clock.tick(FPS) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if isinstance(self.current_stage, Level) and self.current_stage.completed:
                self.change_level()

            self.current_stage.run(dt)
            pygame.display.update()


    def write_level(self):
        with open(join('data', 'levels', 'gen_pro' + '.csv'), 'w', newline='') as csvfile:
            level = self.generate_level()
            writer = csv.writer(csvfile)

            for row in level:
                formatted_row = [str(item).upper() if isinstance(item, str) else f"{item:.2f}" for item in row]
                writer.writerow(formatted_row)

    def generate_point(self, min, max):
        row = randint(min, max)
        col = randint(min, max)
        point = (row, col)

        if point not in self.current_object_on_level:
            self.current_object_on_level.append(point)
            return point

        while point in self.current_object_on_level:
            row = randint(min, max)
            col = randint(min, max)
            point = (row, col)

        self.current_object_on_level.append(point)
        return point

    def generate_level(self):
        level = self.place_walls_around_map()

        # Place a player on the level
        coo_player = self.generate_point(1, 13)
        level[coo_player[0]][coo_player[1]] = 'P'

        # Place a stair on the level
        coo_stair = self.generate_point(1, 13)
        level[coo_stair[0]][coo_stair[1]] = 'S'

        walls = self.generate_aleatoire_pattern_walls()

        for wall in walls:
            level[wall[0]][wall[1]] = '1'

        self.print_level(level)
        return level

    def generate_aleatoire_pattern_walls(self):

        # Generate a zone
        current_walls = []

        points = int(15 * self.rule['walls_pourcentage'])
        zone = randint(1, 6)

        print(f"nb points {points}")
        # Place randomly different points on the level

        for point in range(points):
            # Place a wall on the level
            coo_wall = self.generate_point(zone, 13 - zone)
            current_walls.append(coo_wall)

        # Shuffle the list of our walls
        shuffle_current_walls = copy.copy(current_walls)
        shuffle_current_walls = self.shuffle_list(shuffle_current_walls)

        print(f"list points : {shuffle_current_walls}")

        # Connect all point
        first_point = shuffle_current_walls[0]
        second_point = shuffle_current_walls[1]

        new_pattern = [first_point, second_point]
        new_pattern = new_pattern + self.connect_two_points(first_point, second_point)

        if points == 2 : return new_pattern


        for i in range(points - 2):
            to = shuffle_current_walls[i + 2]
            closest_point = self.find_closest_point(new_pattern, to)
            print(f"closest point : {closest_point}")
            new_pattern = new_pattern + self.connect_two_points(closest_point, to)

        new_pattern = new_pattern + shuffle_current_walls

        return new_pattern

    def find_closest_point(self, points, to):

        temp = math.sqrt((points[0][0] - to[0]) ** 2 + (points[0][1] - to[1]) ** 2)
        temp_point = points[0]
        for point in points:

            distance_point_to = math.sqrt((point[0] - to[0]) ** 2 + (point[1] - to[1]) ** 2)

            if (distance_point_to < temp) :
                temp = distance_point_to
                temp_point = point

        return temp_point

    def connect_two_points(self, _from , to):
        list_point = []

        r = randint(1, 2)

        if r == 1 :

            for i in range( abs(_from[0] - to[0])):

                if _from[0] > to[0]:
                    _from = (_from[0] - 1, _from[1])

                if _from[0] < to[0]:
                    _from = (_from[0] + 1, _from[1])

                list_point.append(_from)
                self.current_object_on_level.append(_from)

            for i in range(abs(_from[1] - to[1])):

                if _from[1] > to[1]:
                    _from = (_from[0] , _from[1] - 1)

                if _from[1] < to[1]:
                    _from = (_from[0] , _from[1] + 1)

                self.current_object_on_level.append(_from)
                list_point.append(_from)
        else :
            for i in range(abs(_from[1] - to[1])):

                if _from[1] > to[1]:
                    _from = (_from[0], _from[1] - 1)

                if _from[1] < to[1]:
                    _from = (_from[0], _from[1] + 1)

                self.current_object_on_level.append(_from)
                list_point.append(_from)

            for i in range( abs(_from[0] - to[0])):

                if _from[0] > to[0]:
                    _from = (_from[0] - 1, _from[1])

                if _from[0] < to[0]:
                    _from = (_from[0] + 1, _from[1])

                list_point.append(_from)
                self.current_object_on_level.append(_from)

        return list_point

    def shuffle_list(self, list):
        for i in range(len(list)):
            temp = list[i]
            random_index = randint(i, len(list) - 1)
            list[i] = list[random_index]
            list[random_index] = temp
        return  list

    def place_walls_around_map(self):
        level = []
        for col in range(self.rule['size'][0]):
            raw = []
            for row in range(self.rule['size'][1]):

                # Generate walls all around the map
                if row == 0 or row == self.rule['size'][0] - 1 or col == 0 or col == self.rule['size'][1] - 1:
                    raw.append('1')
                    self.current_object_on_level.append((row, col))
                else:
                    raw.append('0')
            level.append(raw)
        return level

    def print_level(self, level):
        str = ''

        for i in range(len(level)):
            for j in range(len(level[i])):
                str += level[i][j]
            str += '\n'

        print(str)



if __name__ == '__main__':
    game = Game()
    game.run()
