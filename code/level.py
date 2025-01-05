import csv

from mysteryEnemy import MysteryEnemy
from settings import *
from wall import Wall
from object import Object
from player import Player
from standardEnemy import StandardEnemy
from spiderWeb import SpiderWeb

BLACK = (0, 0, 0)
GRAY = (200, 200, 200)


class Level:
    def __init__(self, level_data):
        """
        Initialise le niveau avec les données spécifiées.

        Args:
            level_data (str): Le nom du fichier de données du niveau.
        """
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.all_sprites = pygame.sprite.Group()

        self.walls = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        self.visible_sprites = pygame.sprite.LayeredUpdates()

        self.setup(level_data)

    def setup(self, level_data):
        """
        Configure le niveau en chargeant les données depuis un fichier CSV.

        Args:
            level_data (str): Le nom du fichier de données du niveau.
        """
        with open(join('data', 'levels', level_data + '.csv'), newline='') as csvfile:
            level_reader = csv.reader(csvfile, delimiter=',')
            for y, row in enumerate(level_reader):
                for x, tile in enumerate(row):
                    if tile == '1':
                        # Crée un mur aux coordonnées (x, y) et l'ajoute aux groupes appropriés
                        Wall((x * TILE_SIZE, y * TILE_SIZE),
                             (self.all_sprites, self.walls))
                    elif tile == 'P':
                        # Crée un joueur aux coordonnées (x, y) et l'ajoute aux groupes appropriés
                        Player((x * TILE_SIZE, y * TILE_SIZE),
                               [self.all_sprites, self.player], {"walls": self.walls, "enemies": self.enemies})
                    elif tile == 'Se':
                        # Crée un objet aux coordonnées (x, y) et l'ajoute aux groupes appropriés
                        StandardEnemy((x * TILE_SIZE, y * TILE_SIZE), [self.all_sprites, self.enemies])
                    elif tile == 'Me':
                        # Crée un objet aux coordonnées (x, y) et l'ajoute aux groupes appropriés
                        MysteryEnemy((x * TILE_SIZE, y * TILE_SIZE), [self.all_sprites, self.enemies])
                    elif tile == 'W':
                        # Crée un objet aux coordonnées (x, y) et l'ajoute aux groupes appropriés
                        SpiderWeb((x * TILE_SIZE, y * TILE_SIZE), [self.all_sprites])

    def run(self, dt):
        """
        Exécute la boucle principale du niveau.

        Args:
            dt (float): Le temps écoulé depuis la dernière mise à jour.
        """
        self.all_sprites.update(dt)
        self.display_surface.fill('white')
        for sprite in self.all_sprites:
            sprite.draw(self.display_surface)

        self.draw_grid()
        self.draw_information_player()

    def draw_grid(self):
        """
        Dessine une grille sur la surface d'affichage.
        """
        width = int(TILE_SIZE * 0.06)
        for y in range(0, int(16 * TILE_SIZE), int(TILE_SIZE)):
            pygame.draw.line(self.display_surface, '#cccccc',
                             (0, y - (width // 2)), (int(15 * TILE_SIZE), y - (width // 2)), width)
        for x in range(0, int(16 * TILE_SIZE), int(TILE_SIZE)):
            pygame.draw.line(self.display_surface, '#cccccc',
                             (x - (width // 2), 0), (x - (width // 2), int(15 * TILE_SIZE)), width)



    def draw_text(self, surface, text, position, font, color):
        text_surface = font.render(text, True, color)
        surface.blit(text_surface, position)

    def draw_information_player(self):
        font = pygame.font.Font(None, 36)

        rect_width, rect_height = 100, 50
        rect_x = (WINDOW_WIDTH - 2 * rect_width - 10) // 2
        rect_y = ((640 + WINDOW_HEIGHT) - 2 * rect_height - 10) // 2

        for row in range(2):  # 2 lignes
            for col in range(2):  # 2 colonnes
                pygame.draw.rect(self.display_surface, GRAY,
                                 (rect_x + col * (rect_width + 10),
                                  rect_y + row * (rect_height + 10),
                                  rect_width, rect_height))

        self.draw_text(self.display_surface, "Starting", (rect_x - 100, rect_y - 40), font, BLACK)
        self.draw_text(self.display_surface, "+", (rect_x - 80 + (rect_x + 2 * rect_width + 20) // 4, rect_y - 40), font, BLACK)
        self.draw_text(self.display_surface, "-", (rect_x - 80 + 2 * ((rect_x + 2 * rect_width + 20) // 4), rect_y - 40), font, BLACK)
        self.draw_text(self.display_surface, "Ending", (rect_x + 2 * rect_width + 20, rect_y - 40), font, BLACK)

        self.draw_text(self.display_surface, f'{self.player.sprite.hp} HP', (rect_x - 120, rect_y + 10), font, BLACK)
        self.draw_text(self.display_surface, f'{self.player.sprite.coins} ¢', (rect_x - 120, rect_y + rect_height + 20), font, BLACK)


        # TODO : afficher a la fin du niveau, l'hp et les coins du joueur
        self.draw_text(self.display_surface, "HP ____", (rect_x + 2 * rect_width + 20, rect_y + 10), font, BLACK)
        self.draw_text(self.display_surface, "¢  ____", (rect_x + 2 * rect_width + 20, rect_y + rect_height + 20), font, BLACK)

        # pygame.display.flip()
