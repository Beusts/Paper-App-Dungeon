import csv
from settings import *
from sprites import *
from player import Player


class Level:
    def __init__(self, level_data):
        """
        Initialise le niveau avec les données spécifiées.

        Args:
            level_data (str): Le nom du fichier de données du niveau.
        """
        self.display_surface = pygame.display.get_surface()

        # groupes de sprites
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()

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
                               self.all_sprites, self.walls)
                    elif tile == 'O':
                        # Crée un objet aux coordonnées (x, y) et l'ajoute aux groupes appropriés
                        Objet((x * TILE_SIZE, y * TILE_SIZE), self.all_sprites)

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
