from settings import *
from level import Level
from shop import Shop
from player import Player
from os.path import join
from random import randint

from wallGenerator import WallGenerator
from objectGenerator import ObjectsGenerator
import random
import csv


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
                formatted_row = [str(item) if isinstance(item, str) else f"{item:.2f}" for item in row]
                writer.writerow(formatted_row)

    def generate_level(self):
        level_rows = self.rule['size'][0]
        level_cols = self.rule['size'][1]

        level = []

        # Setup matrice level
        for i in range(level_rows):
            row = []
            for j in range(level_cols):
                row.append("0")
            level.append(row)

        walls_on_level = []
        walls = WallGenerator(walls_on_level, 0.15, (level_rows, level_cols))
        walls_on_level = walls.generate_wall_level()

        object_on_level = []
        objects = ObjectsGenerator(object_on_level, walls_on_level, 0.05, (level_rows, level_cols))
        object_on_level = objects.generate_objects_level()

        for x, y in walls_on_level:
            level[x][y] = "1"

        print(object_on_level)

        for object in object_on_level:
            x = object["coo"][0]
            y = object["coo"][1]
            level[x][y] = object["symbol"]

        return level


if __name__ == '__main__':

    game = Game()
    game.run()
