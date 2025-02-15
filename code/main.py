from settings import *
from level import Level
from shop import Shop
from player import Player
from os.path import join
from levelGenerator import create_maze_csv_file
from pdfGenerator import PdfGenerator


class Game:
    def __init__(self):
        """
        Initialise le jeu, la fenêtre d'affichage et le niveau actuel.
        """

        NB_PARTY = 6

        pygame.init()
        self.display_surface = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Paper App Dungeon')

        self.clock = pygame.time.Clock()

        self.level_map_files = []
        self.shop_files = [0, 1, 2]

        self.current_level_index = 0

        difficulty = 0
        for i in range(NB_PARTY):

            if i % 10 == 0:
                difficulty += 1

            create_maze_csv_file(f'grid{i}', 15, 15, difficulty)
            self.level_map_files.append(f'grid{i}')

        self.player = Player()

        self.current_stage = Level(
            self.level_map_files[self.current_level_index], self.player)

        PdfGenerator(self.level_map_files, self.shop_files)


    def change_level(self):

        self.current_level_index += 1

        if self.current_level_index >= len(self.level_map_files):
            print("game over")
        else:
            new_level_file = self.level_map_files[self.current_level_index]

            if self.current_level_index % FREQUENCY_SPAWN_SHOP == 1:
                self.current_stage = Shop('2', self.player)
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


if __name__ == '__main__':
    game = Game()
    game.run()
