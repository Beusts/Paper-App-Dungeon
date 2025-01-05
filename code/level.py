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
                    elif tile == 'Se':
                        # Crée un objet aux coordonnées (x, y) et l'ajoute aux groupes appropriés
                        StandardEnemy((x * TILE_SIZE, y * TILE_SIZE),
                                      [self.all_sprites, self.objects])
                    elif tile == 'Me':
                        # Crée un objet aux coordonnées (x, y) et l'ajoute aux groupes appropriés
                        MysteryEnemy((x * TILE_SIZE, y * TILE_SIZE),
                                     [self.all_sprites, self.objects])
                    elif tile == 'W':
                        # Crée un objet aux coordonnées (x, y) et l'ajoute aux groupes appropriés
                        SpiderWeb((x * TILE_SIZE, y * TILE_SIZE),
                                  [self.all_sprites, self.objects])

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
            pygame.draw.line(self.display_surface, GRAY,
                             (0, y - (width / 2)), (int(15 * TILE_SIZE), y - (width / 2)), width)
        for x in range(0, int(15 * TILE_SIZE), int(TILE_SIZE)):
            pygame.draw.line(self.display_surface, GRAY,
                             (x - (width / 2), 0), (x - (width / 2), int(15 * TILE_SIZE)), width)

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

        # Dessiner les textes d'en-tête
        self.draw_text(self.display_surface, "Starting",
                       (TILE_SIZE * 0.5, TILE_SIZE * 16), font, BLACK)
        self.draw_text(self.display_surface, "+",
                       (draw_rect[0].centerx, TILE_SIZE * 16), font, BLACK)
        self.draw_text(self.display_surface, "-",
                       (draw_rect[1].centerx, TILE_SIZE * 16), font, BLACK)
        self.draw_text(self.display_surface, "Ending",
                       (TILE_SIZE * 12, TILE_SIZE * 16), font, BLACK)

        # Afficher les informations du joueur au début du niveau
        self.draw_text(self.display_surface, f'{self.player.sprite.hp} HP',
                       (TILE_SIZE * 0.5, draw_rect[1].centery), font, BLACK)
        self.draw_text(self.display_surface, f'{self.player.sprite.coins} ¢',
                       (TILE_SIZE * 0.5, draw_rect[2].centery), font, BLACK)

        # TODO : afficher à la fin du niveau, l'hp et les coins du joueur
        self.draw_text(self.display_surface, "HP ____",
                       (TILE_SIZE * 12, draw_rect[1].centery), font, BLACK)
        self.draw_text(self.display_surface, "¢  ____",
                       (TILE_SIZE * 12, draw_rect[2].centery), font, BLACK)

        # pygame.display.flip()
