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

            for y, row in enumerate(level_reader):
                for x, tile in enumerate(row):
                    if tile == '1':
                        # Crée un mur aux coordonnées (x, y) et l'ajoute aux groupes appropriés
                        Wall((x * TILE_SIZE, y * TILE_SIZE),
                             (self.all_sprites, self.walls))
                    elif tile == 'P':
                        # Crée un joueur aux coordonnées (x, y) et l'ajoute aux groupes appropriés
                        self.player.setup((x * TILE_SIZE, y * TILE_SIZE),
                                          self.all_sprites, {"walls": self.walls, "objects": self.objects}, self)
                    # Regarde si la tuile correspond a un pattern comme ceci : SeN où N est un nombre positif
                    elif re.match(r"Se(\d+)", tile):

                        value = 0
                        match = re.match(r"Se(\d+)", tile)
                        if match:
                            value = int(match.group(1))

                        StandardEnemy((x * TILE_SIZE, y * TILE_SIZE),
                                      [self.all_sprites, self.objects], value)
                    elif tile == 'Me':

                        MysteryEnemy((x * TILE_SIZE, y * TILE_SIZE),
                                     [self.all_sprites, self.objects])
                    elif tile == 'W':

                        SpiderWeb((x * TILE_SIZE, y * TILE_SIZE),
                                  [self.all_sprites, self.objects])
                    elif re.match(r"Sh(\d+)", tile):

                        value = 0
                        match = re.match(r"Sh(\d+)", tile)
                        if match:
                            value = int(match.group(1))

                        StandardHeart((x * TILE_SIZE, y * TILE_SIZE),
                                      [self.all_sprites, self.objects], value)
                    elif tile == 'Mh':

                        MysteryHeart((x * TILE_SIZE, y * TILE_SIZE),
                                     [self.all_sprites, self.objects])
                    elif tile == 'K':

                        Key((x * TILE_SIZE, y * TILE_SIZE),
                            [self.all_sprites, self.objects])
                    elif tile == 'L':

                        Lock((x * TILE_SIZE, y * TILE_SIZE),
                             [self.all_sprites, self.objects])
                    elif tile == 'C':

                        Chest((x * TILE_SIZE, y * TILE_SIZE),
                              [self.all_sprites, self.objects])
                    elif tile == 'Co':

                        Coin((x * TILE_SIZE, y * TILE_SIZE),
                             [self.all_sprites, self.objects])
                    elif tile == 'T':

                        Teleporter((x * TILE_SIZE, y * TILE_SIZE),
                                   [self.all_sprites, self.objects])
                    elif tile == 'S':

                        Stair((x * TILE_SIZE, y * TILE_SIZE),
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

        if self.player.winning_hp > 0:
            draw_text(self.display_surface, str(self.player.winning_hp),
                      draw_rect[0].center, font, BLACK, center=True)

        if self.player.losing_hp > 0:
            draw_text(self.display_surface, str(self.player.losing_hp),
                      draw_rect[1].center, font, BLACK, center=True)

        if self.player.winning_coins > 0:
            draw_text(self.display_surface, str(self.player.winning_coins),
                      draw_rect[2].center, font, BLACK, center=True)

        if self.player.losing_coins > 0:
            draw_text(self.display_surface, str(self.player.losing_coins),
                      draw_rect[3].center, font, BLACK, center=True)

        # Dessiner les textes d'en-tête
        draw_text(self.display_surface, "Starting",
                  (TILE_SIZE * 0.5, TILE_SIZE * 16), font, BLACK)
        draw_text(self.display_surface, "+",
                  (draw_rect[0].centerx, TILE_SIZE * 16), font, BLACK, center_x=True)
        draw_text(self.display_surface, "-",
                  (draw_rect[1].centerx, TILE_SIZE * 16), font, BLACK, center_x=True)
        draw_text(self.display_surface, "Ending",
                  (TILE_SIZE * 12, TILE_SIZE * 16), font, BLACK)

        # Dessiner les valeurs copiées
        draw_text(self.display_surface, f'{self.player.hp} HP',
                  (TILE_SIZE * 0.5, draw_rect[1].centery), font, BLACK)
        draw_text(self.display_surface, f'{self.player.coins} ¢',
                  (TILE_SIZE * 0.5, draw_rect[2].centery), font, BLACK)

        # TODO : afficher à la fin du niveau, l'hp et les coins du joueur
        draw_text(self.display_surface, f'{self.hp_start + self.player.winning_hp - self.player.losing_hp} HP',
                  (TILE_SIZE * 12, draw_rect[1].centery), font, BLACK)

        draw_text(self.display_surface, f'{self.coins_start + self.player.winning_coins - self.player.losing_coins} ¢',
                  (TILE_SIZE * 12, draw_rect[2].centery), font, BLACK)

    def draw_end_level_interface(self):
        """
        Affiche l'interface de fin de niveau pour permettre au joueur de choisir de continuer ou de terminer le niveau.
        """

        global is_input_active
        font = pygame.font.Font(None, TILE_SIZE)

        continue_rect = pygame.Rect(0, 0, TILE_SIZE * 6, TILE_SIZE * 2)
        continue_rect.center = (TILE_SIZE * 7.5, TILE_SIZE * 6)

        finish_rect = pygame.Rect(0, 0, TILE_SIZE * 6, TILE_SIZE * 2)
        finish_rect.center = (TILE_SIZE * 7.5, TILE_SIZE * 9)

        pygame.draw.rect(self.display_surface, GRAY,
                         continue_rect, border_radius=10)
        pygame.draw.rect(self.display_surface, GRAY,
                         finish_rect, border_radius=10)

        draw_text(self.display_surface, "Continue",
                  continue_rect.center, font, BLACK, center=True)
        draw_text(self.display_surface, "Finish",
                  finish_rect.center, font, BLACK, center=True)

        global is_input_active
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and is_input_active:
            if continue_rect.collidepoint(mouse_pos):
                self.paused = False
            elif finish_rect.collidepoint(mouse_pos):
                self.finish_level()
        elif not pygame.mouse.get_pressed()[0]:
            is_input_active = True

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

        if self.player.hp <= 0:
            self.coins = 0
            self.player.hp = 10
            self.player.deaths += 1

        self.completed = True
