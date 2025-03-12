from settings import *
from level import Level
from shop import Shop
from player import Player
from os.path import join
from levelGenerator import create_maze_csv_file
from shopGenerator import create_shop_csv_file
import random
from menu import Menu
from utils import draw_text


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

    def calculate_final_score(self):
        """
        Calcule et affiche le score final basé sur les HP, les pièces et les morts du joueur.
        """

        # Create a game finish screen
        finish_font = pygame.font.Font(None, UI_SIZE * 2)
        finish_text = finish_font.render(
            'CONGRATULATIONS!', True, BLACK)
        finish_rect = finish_text.get_rect(
            center=(WINDOW_WIDTH // 2, UI_SIZE * 5))

        sub_font = pygame.font.Font(None, UI_SIZE)
        sub_text = sub_font.render(
            'You have completed all levels!', True, BLACK)
        sub_rect = sub_text.get_rect(
            center=(WINDOW_WIDTH // 2, UI_SIZE * 7))

        self.display_surface.fill(WHITE)
        self.display_surface.blit(finish_text, finish_rect)
        self.display_surface.blit(sub_text, sub_rect)

        # Calculate the score based on HP, coins, and deaths
        hp_score = self.player.hp * 5
        coin_score = self.player.coins * 3
        death_penalty = self.player.deaths
        final_score = hp_score + coin_score - death_penalty
        # Define rectangle dimensions and spacing
        rect_width = UI_SIZE * 3
        rect_height = UI_SIZE * 2
        spacing = int(UI_SIZE * 0.6)  # Space between rectangles

        # Calculate total width and starting position (centered)
        total_width = 4 * rect_width + 3 * spacing
        start_x = (WINDOW_WIDTH - total_width) / 2

        # Fonts
        font = pygame.font.Font(None, int(UI_SIZE * 0.8))
        value_font = pygame.font.Font(None, int(UI_SIZE * 1.5))
        symbol_font = pygame.font.Font(None, int(UI_SIZE))

        # Score data
        score_data = [
            {"title": "HP x 5", "value": str(hp_score)},
            {"title": "¢ x 3", "value": str(coin_score)},
            {"title": "# Deaths", "value": str(death_penalty)},
            {"title": "Score", "value": str(final_score)}
        ]

        # Symbols to display between rectangles
        symbols = ["+", "-", "="]

        # Draw the rectangles and text
        for i, data in enumerate(score_data):
            x_pos = start_x + i * (rect_width + spacing)
            rect = pygame.Rect(x_pos, UI_SIZE * 10, rect_width, rect_height)

            pygame.draw.rect(self.display_surface, GRAY,
                             rect, border_radius=10)

            # Draw title above rectangle
            title_pos = (rect.centerx, rect.bottom + UI_SIZE * 0.5)
            draw_text(self.display_surface,
                      data["title"], title_pos, font, BLACK, center=True)

            # Draw value in rectangle
            value_pos = rect.center
            draw_text(self.display_surface,
                      data["value"], value_pos, value_font, BLACK, center=True)

            # Draw symbols between rectangles
            if i < len(symbols):
                symbol_pos = (x_pos + rect_width + spacing/2, rect.centery)
                draw_text(self.display_surface,
                          symbols[i], symbol_pos, symbol_font, BLACK, center=True)

        draw_text(self.display_surface, "Final Score",
                  (WINDOW_WIDTH // 2, UI_SIZE * 9), pygame.font.Font(None, int(UI_SIZE * 2)), BLACK, center=True)

        pygame.display.update()

    def change_level(self):
        """
        Passe au niveau suivant dans la séquence.
        Si le niveau est un magasin, instancie un objet Shop.
        Si le niveau est un labyrinthe, instancie un objet Level.
        Si tous les niveaux ont été complétés, termine le jeu.
        """
        self.current_level_index += 1

        if self.current_level_index >= len(self.level_map_files):
            self.calculate_final_score()
            # Wait for the player to close the game
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
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
