import csv
from settings import *
from sprites import Wall
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
        self.all_sprites = pygame.sprite.LayeredUpdates()
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

    def run(self, dt):
        """
        Exécute la boucle principale du niveau.

        Args:
            dt (float): Le temps écoulé depuis la dernière mise à jour.
        """
        self.all_sprites.update(dt)
        self.display_surface.fill('black')
        for sprite in self.all_sprites:
            sprite.draw(self.display_surface)
