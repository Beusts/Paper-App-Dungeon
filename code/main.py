from settings import *
from level import Level
from shop import Shop
from player import Player
from os.path import join
from random import randint

from wallGenerator import WallGenerator


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

        wall_pourcentage = 0.12 * self.difficulty
        self.rule = {
            'size': (15, 15),
            'walls_pourcentage': wall_pourcentage
        }
        self.current_object_on_level = []
        self.write_level()


        self.level_map_files = {0: 'gen_pro', 1: '1', 2: 'test'}
        self.current_level_index = 0
        self.player = Player()

        self.current_stage = Level(
            self.level_map_files[self.current_level_index], self.player)
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

            if isinstance(self.current_stage, Shop) and self.current_stage.close:
                self.current_stage = Level(
                    self.level_map_files[self.current_level_index], self.player)

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

    def connect_two_points(self, _from , to):
        list_point = []
        r = randint(1, 2)

        if r == 1:
            for i in range(abs(_from[0] - to[0])):
                if _from[0] > to[0]:
                    _from = (_from[0] - 1, _from[1])

                if _from[0] < to[0]:
                    _from = (_from[0] + 1, _from[1])

                list_point.append(_from)
                self.current_object_on_level.append(_from)

            for i in range(abs(_from[1] - to[1])):
                if _from[1] > to[1]:
                    _from = (_from[0], _from[1] - 1)

                if _from[1] < to[1]:
                    _from = (_from[0], _from[1] + 1)

                self.current_object_on_level.append(_from)
                list_point.append(_from)
        else:

            for i in range(abs(_from[1] - to[1])):
                if _from[1] > to[1]:
                    _from = (_from[0], _from[1] - 1)

                if _from[1] < to[1]:
                    _from = (_from[0], _from[1] + 1)

                self.current_object_on_level.append(_from)
                list_point.append(_from)

            for i in range(abs(_from[0] - to[0])):
                if _from[0] > to[0]:
                    _from = (_from[0] - 1, _from[1])

                if _from[0] < to[0]:
                    _from = (_from[0] + 1, _from[1])

                list_point.append(_from)
                self.current_object_on_level.append(_from)
        return list_point



    def making_structure(self, level):
        list_point = []

        for row in range(1, self.rule['size'][0] - 2):
            for col in range(2, self.rule['size'][1] - 3):
                if level[row][col] == '1': # if the object is a wall

                    # check if there are other wall all around him
                    if level[row][col - 2] == '1':
                        list_point.append(self.connect_two_points((row, col), (row, col - 2)))

                    if level[row][col + 2] == '1':
                        list_point.append(self.connect_two_points((row, col), (row, col + 2)))

        for row in range(2, self.rule['size'][0] - 3):
            for col in range(1, self.rule['size'][1] - 2):
                if level[row][col] == '1':  # if the object is a wall

                    # check if there are other wall all around him
                    if level[row - 2][col] == '1':
                        list_point.append(self.connect_two_points((row, col), (row - 2, col)))

                    if level[row + 2][col] == '1':
                        list_point.append(self.connect_two_points((row, col), (row + 2, col)))


        for row in range(1, self.rule['size'][0] - 2):
            for col in range(1, self.rule['size'][1] - 2):
                if level[row][col] == '1':  # if the object is a wall

                    # check if there are other wall all around him
                    if level[row - 1][col - 1] == '1':
                        list_point.append(self.connect_two_points((row, col), (row - 1, col - 1)))

                    if level[row - 1][col + 1] == '1':
                        list_point.append(self.connect_two_points((row, col), (row  - 1, col + 1)))

                        # check if there are other wall all around him
                        if level[row + 1][col - 1] == '1':
                            list_point.append(self.connect_two_points((row, col), (row + 1, col - 1)))

                        if level[row + 1][col + 1] == '1':
                            list_point.append(self.connect_two_points((row, col), (row + 1, col + 1)))


        for points in list_point:
            for point in points:
                level[point[0]][point[1]] = '1'

        print(f"new wall = {list_point}")
        return level

    def generate_level(self):
        level = []

        for row in range(self.rule['size'][0]):
            rows = []
            for col in range(self.rule['size'][1]):

                # Place walls all around the map
                if row == 0 or row == self.rule['size'][0] - 1 or col == 0 or col == self.rule['size'][1] - 1:
                    rows.append('1')
                    self.current_object_on_level.append((row, col))
                    continue

                # Place randomly a wall
                if random.random() < self.rule['walls_pourcentage']:
                    rows.append('1')
                    self.current_object_on_level.append((row, col))
                    continue
                rows.append('0')
            level.append(rows)

        level = self.making_structure(level)

        #Place a player on the level
        coo_player = self.generate_point(1, self.rule['size'][0] - 2)
        print(f"coo player : {coo_player}")
        level[coo_player[0]][coo_player[1]] = 'P'

        # Place a stair on the level
        coo_stair = self.generate_point(1, self.rule['size'][0] - 2)
        print(f"coo stair : {coo_stair}")
        level[coo_stair[0]][coo_stair[1]] = 'S'

        return level

    # level = []
    #
    # # Setup matrice level
    # for i in range(15):
    #     row = []
    #     for j in range(15):
    #         row.append("0")
    #     level.append(row)
    #
    # object_on_level = []
    #
    # # Place a player on the level
    # coo_player = self.generate_point(1, self.rule['size'][0] - 2)
    # object_on_level.append(coo_player)
    #
    # # Place a stair on the level
    # coo_stair = self.generate_point(1, self.rule['size'][0] - 2)
    # object_on_level.append(coo_stair)
    #
    # wall = WallGenerator(object_on_level, 0.15)
    # object_on_level = wall.generate_wall_level()
    #
    # for x, y in object_on_level:
    #     level[x][y] = "1"
    #
    # level[coo_stair[0]][coo_stair[1]] = "S"
    # level[coo_player[0]][coo_player[1]] = "P"
    #
    # return level

if __name__ == '__main__':

    game = Game()
    game.run()
