from settings import *
from level import Level
from shop import Shop
from player import Player
from os.path import join


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

        self.level_map_files = {0: '0', 1: '1', 2: 'test'}
        self.current_level_index = 0
        # self.current_stage = Level(self.level_map_files[self.current_level_index])

        self.player = Player()

        self.current_stage = Level('test', self.player)

    def change_level(self):
        self.current_level_index += 1

        if self.current_level_index >= len(self.level_map_files):
            print("game over")
        else:
            new_level_file = self.level_map_files[self.current_level_index]

            if self.current_level_index % 6 == 0:
                self.current_stage = Shop('0')
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


if __name__ == '__main__':
    game = Game()
    game.run()
