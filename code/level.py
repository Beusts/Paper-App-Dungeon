import csv
import re
import copy


from settings import *
from wall import Wall
from random import randint

from player import Player
from standardEnemy import StandardEnemy
from mysteryEnemy import MysteryEnemy
from spiderWeb import SpiderWeb
from mysteryHeart import MysteryHeart
from standardHeart import StandardHeart

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
                               [self.all_sprites, self.player], {"walls": self.walls, "objects": self.objects})
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
        # self.draw_shop([["Teleport Scroll", "Teleport to anywhere on the map (use once).", 11], ["Doubling Potion", "Double the number of a dice roll (use once).", 9],["Coin Rush", "All coins and treasure chests are worth 2x on next floor only.", 12]])
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

    def draw_center_text(self, surface, text, position, font, color):
        """
        Dessine un texte au centre de la surface
        """
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(
            center=(position[0], position[1]))
        surface.blit(text_surface, text_rect)

    def draw_centery_text(self, surface, text, position, font, color):
        """
        Dessine un texte centré verticalement
        """
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(x=position[0], centery=position[1])
        surface.blit(text_surface, text_rect)

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

        # Dessiner les textes d'en-tête
        self.draw_text(self.display_surface, "Starting",
                       (TILE_SIZE * 0.5, TILE_SIZE * 16), font, BLACK)
        self.draw_text(self.display_surface, "+",
                       (draw_rect[0].centerx, TILE_SIZE * 16), font, BLACK)
        self.draw_text(self.display_surface, "-",
                       (draw_rect[1].centerx, TILE_SIZE * 16), font, BLACK)
        self.draw_text(self.display_surface, "Ending",
                       (TILE_SIZE * 12, TILE_SIZE * 16), font, BLACK)

        # Dessiner les valeurs copiées
        self.draw_text(self.display_surface, f'{self.hp_start} HP',
                       (TILE_SIZE * 0.5, draw_rect[1].centery), font, BLACK)
        self.draw_text(self.display_surface, f'{self.coins_start} ¢',
                       (TILE_SIZE * 0.5, draw_rect[2].centery), font, BLACK)

        # TODO : afficher à la fin du niveau, l'hp et les coins du joueur
        self.draw_text(self.display_surface, "HP ____",
                       (TILE_SIZE * 12, draw_rect[1].centery), font, BLACK)
        self.draw_text(self.display_surface, "¢  ____",
                       (TILE_SIZE * 12, draw_rect[2].centery), font, BLACK)

    def draw_shop(self, items):
        """
        Dessine le shop
        """
        def draw_iteam(name, description, price, position):
            pygame.draw.rect(self.display_surface, BLACK,
                             (position[0] * TILE_SIZE, position[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE), int(TILE_SIZE*0.15))
            self.draw_text(self.display_surface, name,
                           (position[0] * TILE_SIZE + (TILE_SIZE * 2), position[1] * TILE_SIZE), font, BLACK)
            self.draw_center_text(self.display_surface, f"{price}¢",
                                  (position[0] * TILE_SIZE + TILE_SIZE / 2, position[1] * TILE_SIZE + (TILE_SIZE * 1.5)), price_font, BLACK)
            self.draw_centery_text(self.display_surface, description,
                                   (position[0] * TILE_SIZE + (TILE_SIZE * 2), position[1] * TILE_SIZE + (TILE_SIZE * 1.5)), price_font, BLACK)

        font = pygame.font.Font(None, int(TILE_SIZE * 1.5))
        price_font = pygame.font.Font(None, int(TILE_SIZE * 0.5))
        pygame.draw.rect(self.display_surface, GRAY,
                         (0, 0, TILE_SIZE * 15, TILE_SIZE * 3))

        self.draw_center_text(self.display_surface, "Shop",
                              (TILE_SIZE * 7.5, TILE_SIZE), font, BLACK)

        draw_iteam(items[0][0], items[0][1], items[0][2], (1, 4))
        draw_iteam(items[1][0], items[1][1], items[1][2], (1, 8))
        draw_iteam(items[2][0], items[2][1], items[2][2], (1, 12))
