import csv
import re

from teleporter import Teleporter
from wall import Wall
from standardEnemy import StandardEnemy
from mysteryEnemy import MysteryEnemy
from spiderWeb import SpiderWeb
from mysteryHeart import MysteryHeart
from standardHeart import StandardHeart
from lock import Lock
from chest import Chest
from coin import Coin
from key import Key
from stair import Stair

from settings import *
from utils import draw_text

BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
WHITE = (255, 255, 255)
TRANSPARENT_BLACK = (0, 0, 0, 180)


class Level:
    def __init__(self, level_data, player):
        """
        Initialise le niveau avec les données spécifiées.

        Args:
            level_data (str): Le nom du fichier de données du niveau.
        """
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.all_sprites = pygame.sprite.Group()

        self.walls = pygame.sprite.Group()
        self.objects = pygame.sprite.Group()

        self.player = player

        self.setup(level_data)

        self.paused = False
        self.completed = False
        self.coin_multiplier = 1  # Valeur par défaut

    def setup(self, level_data):
        """
        Le fichier CSV doit contenir une grille où chaque cellule représente un type d'objet dans le jeu.
        Les valeurs possibles pour chaque cellule sont :
            '1'  : Crée un mur.
            'P'  : Crée un joueur.
            'SeN': Crée un ennemi standard avec N comme valeur.
            'Me' : Crée un ennemi mystère.
            'W'  : Crée une toile d'araignée.
            'ShN': Crée un cœur standard avec N comme valeur.
            'Mh' : Crée un cœur mystère.
            'K'  : Crée une clé.
            'L'  : Crée un verrou.
            'C'  : Crée un coffre.
            'Co' : Crée une pièce.
            'T'  : Crée un téléporteur.
            'S'  : Crée un escalier.
        Configure le niveau en chargeant les données depuis un fichier CSV.

        Args:
            level_data (str): Le nom du fichier de données du niveau.
        """
        with open(join('data', 'levels', level_data + '.csv'), newline='') as csvfile:

            level_reader = csv.reader(csvfile, delimiter=',')
            level_reader = list(level_reader)

            self.rows = len(level_reader)
            self.cols = len(level_reader[0])

            set_tile_size(int(WINDOW_WIDTH / max(self.rows, self.cols)))

            self.x_offset = (WINDOW_WIDTH - (self.cols * get_tile_size())) / 2

            for y, row in enumerate(level_reader):
                for x, tile in enumerate(row):
                    if tile == '1':
                        # Crée un mur aux coordonnées (x, y) et l'ajoute aux groupes appropriés
                        Wall((x * get_tile_size() + self.x_offset, y * get_tile_size()),
                             (self.all_sprites, self.walls))
                    elif tile == 'P':
                        # Crée un joueur aux coordonnées (x, y) et l'ajoute aux groupes appropriés
                        self.player.setup((x * get_tile_size() + self.x_offset, y * get_tile_size()),
                                          self.all_sprites, {"walls": self.walls, "objects": self.objects}, self, self.x_offset)
                    # Regarde si la tuile correspond a un pattern comme ceci : SeN où N est un nombre positif
                    elif re.match(r"Se(\d+)", tile):

                        value = 0
                        match = re.match(r"Se(\d+)", tile)
                        if match:
                            value = int(match.group(1))

                        StandardEnemy((x * get_tile_size() + self.x_offset, y * get_tile_size()),
                                      [self.all_sprites, self.objects], value)
                    elif tile == 'Me':

                        MysteryEnemy((x * get_tile_size() + self.x_offset, y * get_tile_size()),
                                     [self.all_sprites, self.objects])
                    elif tile == 'W':

                        SpiderWeb((x * get_tile_size() + self.x_offset, y * get_tile_size()),
                                  [self.all_sprites, self.objects])
                    elif re.match(r"Sh(\d+)", tile):

                        value = 0
                        match = re.match(r"Sh(\d+)", tile)
                        if match:
                            value = int(match.group(1))

                        StandardHeart((x * get_tile_size() + self.x_offset, y * get_tile_size()),
                                      [self.all_sprites, self.objects], value)
                    elif tile == 'Mh':

                        MysteryHeart((x * get_tile_size() + self.x_offset, y * get_tile_size()),
                                     [self.all_sprites, self.objects])
                    elif tile == 'K':

                        Key((x * get_tile_size() + self.x_offset, y * get_tile_size()),
                            [self.all_sprites, self.objects])
                    elif tile == 'L':

                        Lock((x * get_tile_size() + self.x_offset, y * get_tile_size()),
                             [self.all_sprites, self.objects])
                    elif tile == 'C':

                        Chest((x * get_tile_size() + self.x_offset, y * get_tile_size()),
                              [self.all_sprites, self.objects])
                    elif tile == 'Co':

                        Coin((x * get_tile_size() + self.x_offset, y * get_tile_size()),
                             [self.all_sprites, self.objects])
                    elif tile == 'T':

                        Teleporter((x * get_tile_size() + self.x_offset, y * get_tile_size()),
                                   [self.all_sprites, self.objects])
                    elif tile == 'S':

                        Stair((x * get_tile_size() + self.x_offset, y * get_tile_size()),
                              [self.all_sprites, self.objects])

            self.hp_start = self.player.hp
            self.coins_start = self.player.coins

    def run(self, dt):
        """
        Exécute la boucle principale du niveau.

        Args:
            dt (float): Le temps écoulé depuis la dernière mise à jour.
        """
        if self.paused:
            self.draw_end_level_interface()
            return

        self.all_sprites.update(dt)
        self.display_surface.fill('white')
        for sprite in self.walls:
            sprite.draw(self.display_surface)
        for sprite in self.objects:
            sprite.draw(self.display_surface)

        self.player.draw(self.display_surface)

        self.draw_grid()

    def draw_grid(self):
        """
        Dessine une grille sur la surface d'affichage.
        """
        width = int(get_tile_size() * 0.06)
        if width < 1:
            width = 1
        for y in range(0, (self.rows + 1) * get_tile_size(), get_tile_size()):
            pygame.draw.line(self.display_surface, GRAY,
                             (self.x_offset, y), (self.cols * get_tile_size() + self.x_offset, y), width)
        for x in range(0, (self.cols + 1) * get_tile_size(), get_tile_size()):
            pygame.draw.line(self.display_surface, GRAY,
                             (x + self.x_offset, 0), (x + self.x_offset, self.rows * get_tile_size()), width)

    def draw_end_level_interface(self):
        """
        Affiche l'interface de fin de niveau pour permettre au joueur de choisir de continuer ou de terminer le niveau.
        """

        global can_receive_input
        font = pygame.font.Font(None, UI_SIZE)

        continue_rect = pygame.Rect(
            0, 0, UI_SIZE * 6, UI_SIZE * 2)
        continue_rect.center = (UI_SIZE * 7.5, UI_SIZE * 6)

        finish_rect = pygame.Rect(
            0, 0, UI_SIZE * 6, UI_SIZE * 2)
        finish_rect.center = (UI_SIZE * 7.5, UI_SIZE * 9)

        pygame.draw.rect(self.display_surface, GRAY,
                         continue_rect, border_radius=10)
        pygame.draw.rect(self.display_surface, GRAY,
                         finish_rect, border_radius=10)

        draw_text(self.display_surface, "Continue",
                  continue_rect.center, font, BLACK, center=True)
        draw_text(self.display_surface, "Finish",
                  finish_rect.center, font, BLACK, center=True)

        global can_receive_input
        mouse_pos = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed()[0] and can_receive_input:
            if continue_rect.collidepoint(mouse_pos):
                self.paused = False
            elif finish_rect.collidepoint(mouse_pos):
                self.finish_level()
        elif not pygame.mouse.get_pressed()[0]:
            can_receive_input = True

    def finish_level(self):
        """
        Termine le niveau et affiche les résultats finaux.
        """
        # Logique pour terminer le niveau et afficher les résultats finaux
        print("Niveau terminé")

        self.player.hp = self.hp_start + \
            self.player.winning_hp - self.player.losing_hp
        self.player.hp = self.player.hp if self.player.hp <= 25 else 25
        self.player.coins = self.coins_start + \
            self.player.winning_coins - self.player.losing_coins
        self.player.coins = self.player.coins if self.player.coins >= 0 else 0

        self.player.winning_hp = 0
        self.player.losing_hp = 0
        self.player.winning_coins = 0
        self.player.losing_coins = 0

        self.player.movement_remaining = 0

        if self.player.hp <= 0:
            self.coins = 0
            self.player.hp = 10
            self.player.deaths += 1

        self.completed = True
