from settings import *
from level import Level
from shop import Shop
from player import Player
from os.path import join
from levelGenerator import create_maze_csv_file
from shopGenerator import create_shop_csv_file
import random
from menu import Menu


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

        self.level_map_files = []

        self.current_level_index = 0

        difficulty = 0
        total_levels = NB_LEVEL
        total_shops = int(NB_LEVEL * FREQUENCY_SPAWN_SHOP)
        total_iterations = total_levels + total_shops
        # Détermine à intervalles réguliers où insérer un shop
        shop_interval = total_iterations // (total_shops + 1)

        level_count = 0
        shop_count = 0

        seed = random.random()
        random.seed(seed)
        print("Seed pour la génération des niveaux : ", seed)

        # Génère une séquence alternée de niveaux et de magasins
        for i in range(total_iterations):
            # Si on est à l'intervalle pour un shop et qu'il reste des shops à ajouter
            if shop_count < total_shops and (i + 1) % shop_interval == 0:
                # Création d'un fichier CSV pour le magasin avec 3 articles
                create_shop_csv_file(f'shop{shop_count}', 3)
                self.level_map_files.append(f'shop{shop_count}')
                shop_count += 1
            else:
                level_count += 1
                # Augmente la difficulté tous les 10 niveaux
                if level_count % 10 == 0 and level_count != 0:
                    difficulty += 1
                # Création d'un labyrinthe de 15x15 avec la difficulté actuelle
                create_maze_csv_file(f'level{level_count}', 15, 15, difficulty)
                self.level_map_files.append(f'level{level_count}')

        # Initialisation du joueur
        self.player = Player()

        # Initialisation du premier niveau
        self.current_stage = Level(
            self.level_map_files[self.current_level_index], self.player)

        # Nouvelle graine aléatoire pour les mouvements dans le jeu
        seed = random.SystemRandom().random()
        random.seed(seed)
        print("Seed pour les mouvements : ", seed)

    def change_level(self):
        """
        Passe au niveau suivant dans la séquence.
        Si le niveau est un magasin, instancie un objet Shop.
        Si le niveau est un labyrinthe, instancie un objet Level.
        Si tous les niveaux ont été complétés, termine le jeu.
        """
        self.current_level_index += 1

        if self.current_level_index >= len(self.level_map_files):
            print("game over")
        else:
            if self.level_map_files[self.current_level_index].startswith('shop'):
                self.current_stage = Shop(
                    self.level_map_files[self.current_level_index], self.player)
            else:
                self.current_stage = Level(
                    self.level_map_files[self.current_level_index], self.player)

            print("changing level")

    def run(self):
        """
        Exécute la boucle principale du jeu.
        """
        menu = Menu(self.display_surface, self.level_map_files)
        menu.run()
        # Boucle principale du jeu
        while True:
            dt = self.clock.tick(FPS) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self.current_stage.completed:
                self.change_level()

            self.current_stage.run(dt)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
