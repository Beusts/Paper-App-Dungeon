import csv
import re

from teleporter import Teleporter
from settings import *
from wall import Wall
from random import randint

from player import Player
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

from utils import draw_text

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
        self.objects = pygame.sprite.Group()
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

            pattern = r"Se(\d+)"

            for y, row in enumerate(level_reader):
                for x, tile in enumerate(row):
                    if tile == '1':
                        # Crée un mur aux coordonnées (x, y) et l'ajoute aux groupes appropriés
                        Wall((x * TILE_SIZE, y * TILE_SIZE),
                             (self.all_sprites, self.walls))
                    elif tile == 'P':
                        # Crée un joueur aux coordonnées (x, y) et l'ajoute aux groupes appropriés
                        Player((x * TILE_SIZE, y * TILE_SIZE),
                               [self.all_sprites, self.player], {"walls": self.walls, "objects": self.objects}, self)
                    # Regarde si la tuile correspond a un pattern comme ceci : SeN où N est un nombre positif
                    elif re.match(r"Se(\d+)", tile):

                        value = 0
                        match = re.match(r"Se(\d+)", tile)
                        if match:
                            value = int(match.group(1))

                        # Crée un objet aux coordonnées (x, y) et l'ajoute aux groupes appropriés
                        StandardEnemy((x * TILE_SIZE, y * TILE_SIZE),
                                      [self.all_sprites, self.objects], value)
                    elif tile == 'Me':
                        # Crée un objet aux coordonnées (x, y) et l'ajoute aux groupes appropriés
                        MysteryEnemy((x * TILE_SIZE, y * TILE_SIZE),
                                     [self.all_sprites, self.objects])
                    elif tile == 'W':
                        # Crée un objet aux coordonnées (x, y) et l'ajoute aux groupes appropriés
                        SpiderWeb((x * TILE_SIZE, y * TILE_SIZE),
                                  [self.all_sprites, self.objects])
                    elif re.match(r"Sh(\d+)", tile):

                        value = 0
                        match = re.match(r"Sh(\d+)", tile)
                        if match:
                            value = int(match.group(1))

                        # Crée un objet aux coordonnées (x, y) et l'ajoute aux groupes appropriés
                        StandardHeart((x * TILE_SIZE, y * TILE_SIZE),
                                      [self.all_sprites, self.objects], value)
                    elif tile == 'Mh':
                        # Crée un objet aux coordonnées (x, y) et l'ajoute aux groupes appropriés
                        MysteryHeart((x * TILE_SIZE, y * TILE_SIZE),
                                     [self.all_sprites, self.objects])
                    elif tile == 'K':
                        # Crée un objet aux coordonnées (x, y) et l'ajoute aux groupes appropriés
                        Key((x * TILE_SIZE, y * TILE_SIZE),
                                     [self.all_sprites, self.objects])
                    elif tile == 'L':
                        # Crée un objet aux coordonnées (x, y) et l'ajoute aux groupes appropriés
                        Lock((x * TILE_SIZE, y * TILE_SIZE),
                                     [self.all_sprites, self.objects])
                    elif tile == 'C':
                        # Crée un objet aux coordonnées (x, y) et l'ajoute aux groupes appropriés
                        Chest((x * TILE_SIZE, y * TILE_SIZE),
                                     [self.all_sprites, self.objects])
                    elif tile == 'Co':
                        # Crée un objet aux coordonnées (x, y) et l'ajoute aux groupes appropriés
                        Coin((x * TILE_SIZE, y * TILE_SIZE),
                                     [self.all_sprites, self.objects])
                    elif tile == 'T':
                        # Crée un objet aux coordonnées (x, y) et l'ajoute aux groupes appropriés
                        Teleporter((x * TILE_SIZE, y * TILE_SIZE),
                                     [self.all_sprites, self.objects])
                    elif tile == 'S':
                        # Crée un objet aux coordonnées (x, y) et l'ajoute aux groupes appropriés
                        Stair((x * TILE_SIZE, y * TILE_SIZE),
                                     [self.all_sprites, self.objects])

            self.hp_start = self.player.sprite.hp
            self.coins_start = self.player.sprite.coins

    def run(self, dt):
        """
        Exécute la boucle principale du niveau.

        Args:
            dt (float): Le temps écoulé depuis la dernière mise à jour.
        """
        self.all_sprites.update(dt)
        self.display_surface.fill('white')
        for sprite in self.walls:
            sprite.draw(self.display_surface)
        for sprite in self.objects:
            sprite.draw(self.display_surface)
        for sprite in self.player:
            sprite.draw(self.display_surface)

        self.draw_grid()
        self.draw_information_player()

    def draw_grid(self):
        """
        Dessine une grille sur la surface d'affichage.
        """
        width = int(TILE_SIZE * 0.06)
        for y in range(0, 16 * TILE_SIZE, TILE_SIZE):
            pygame.draw.line(self.display_surface, GRAY,
                             (0, y - (width / 2)), (15 * TILE_SIZE, y - (width / 2)), width)
        for x in range(0, 15 * TILE_SIZE, TILE_SIZE):
            pygame.draw.line(self.display_surface, GRAY,
                             (x - (width / 2), 0), (x - (width / 2), 15 * TILE_SIZE), width)

    def draw_text(self, surface, text, position, font, color):
        """
        Dessine un texte
        """
        text_surface = font.render(text, True, color)
        surface.blit(text_surface, position)

    def draw_information_player(self):
        """
        Dessine un espace pouvant afficher la vie, l'argent, au début et à la fin d'un level
        """
        # Définir la police et la taille de la police
        font = pygame.font.Font(None, TILE_SIZE)

        # Positions des rectangles d'information
        rect_positions = [
            (TILE_SIZE * 4, TILE_SIZE * 17),
            (TILE_SIZE * 7.5, TILE_SIZE * 17),
            (TILE_SIZE * 4, TILE_SIZE * 20),
            (TILE_SIZE * 7.5, TILE_SIZE * 20)
        ]

        # Créer et ajuster les rectangles
        draw_rect = []
        for pos in rect_positions:
            rect = pygame.Rect(pos[0], pos[1], TILE_SIZE * 3.5, TILE_SIZE * 3)
            rect.inflate_ip(-TILE_SIZE * 0.15, -TILE_SIZE * 0.15)
            draw_rect.append(rect)

        # Dessiner les rectangles avec des coins arrondis
        pygame.draw.rect(self.display_surface, GRAY,
                         draw_rect[0], border_top_left_radius=10)
        pygame.draw.rect(self.display_surface, GRAY,
                         draw_rect[1], border_top_right_radius=10)
        pygame.draw.rect(self.display_surface, GRAY,
                         draw_rect[2], border_bottom_left_radius=10)
        pygame.draw.rect(self.display_surface, GRAY,
                         draw_rect[3], border_bottom_right_radius=10)

        # Afficher les hp et coins pendant la partie du joueur

        if self.player.sprite.winning_hp > 0:
            draw_text(self.display_surface, str(self.player.sprite.winning_hp),
                      (draw_rect[0].centerx * 0.95 , draw_rect[0].centery * 0.98), font, BLACK)

        if self.player.sprite.losing_hp > 0:
            draw_text(self.display_surface, str(self.player.sprite.losing_hp),
                      (draw_rect[1].centerx * 0.95 , draw_rect[1].centery * 0.98), font, BLACK)

        if self.player.sprite.winning_coins > 0:
            draw_text(self.display_surface, str(self.player.sprite.winning_coins),
                      (draw_rect[2].centerx * 0.95 , draw_rect[2].centery * 0.98), font, BLACK)

        if self.player.sprite.losing_coins > 0:
            draw_text(self.display_surface, str(self.player.sprite.losing_coins),
                      (draw_rect[3].centerx * 0.95 , draw_rect[3].centery * 0.98), font, BLACK)

        # Dessiner les textes d'en-tête
        draw_text(self.display_surface, "Starting",
                       (TILE_SIZE * 0.5, TILE_SIZE * 16), font, BLACK)
        draw_text(self.display_surface, "+",
                       (draw_rect[0].centerx, TILE_SIZE * 16), font, BLACK)
        draw_text(self.display_surface, "-",
                       (draw_rect[1].centerx, TILE_SIZE * 16), font, BLACK)
        draw_text(self.display_surface, "Ending",
                       (TILE_SIZE * 12, TILE_SIZE * 16), font, BLACK)

        # Dessiner les valeurs copiées
        draw_text(self.display_surface, f'{self.hp_start} HP',
                       (TILE_SIZE * 0.5, draw_rect[1].centery), font, BLACK)
        draw_text(self.display_surface, f'{self.coins_start} ¢',
                       (TILE_SIZE * 0.5, draw_rect[2].centery), font, BLACK)

        # TODO : afficher à la fin du niveau, l'hp et les coins du joueur
        draw_text(self.display_surface, "HP ____",
                       (TILE_SIZE * 12, draw_rect[1].centery), font, BLACK)
        draw_text(self.display_surface, "¢  ____",
                       (TILE_SIZE * 12, draw_rect[2].centery), font, BLACK)
