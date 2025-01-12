from time import sleep

from settings import *
from pygame.math import Vector2
from random import randint
from teleporter import Teleporter
from stair import Stair


class Player(pygame.sprite.Sprite):

    def __init__(self):
        """
        Initialise un joueur
        """

        super().__init__()
        self.image = pygame.image.load(
            join('graphics', 'players.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))

        self.adjacent_positions = []

        self.direction = Vector2(0, 0)

        self.movement_remaining = 0
        self.movement_roll = 0

        self.last_move_time = 0
        self.current_time = 0
        self.can_move = True
        self.show_adjacent_tiles = False

        # characteristic of a player
        self.hp = 10
        self.coins = 0
        self.deaths = 0
        self.keys = 0

        self.losing_hp = 0
        self.winning_hp = 0
        self.losing_coins = 0
        self.winning_coins = 0

    def setup(self, pos, groups, colliders, level):
        self.kill()
        self.add(groups)
        self.rect = self.image.get_rect(topleft=pos)
        self.colliders = colliders
        self.level = level

    def input(self):
        """
        Gère les entrées de l'utilisateur.
        Il faut relacher le clic de souris pour pouvoir cliquer à nouveau.
        """
        global is_input_active
        if pygame.mouse.get_pressed()[0] and is_input_active:
            mouse_pos = pygame.mouse.get_pos()
            self.handle_mouse_click(mouse_pos)
            is_input_active = False
        elif not pygame.mouse.get_pressed()[0]:
            is_input_active = True

    def handle_mouse_click(self, mouse_pos):
        """
        Gère les clics de souris pour déplacer le joueur.

        Args:
            mouse_pos (tuple): La position (x, y) de la souris.
        """
        if self.can_move:
            # Calcule la tuile cliquée en fonction de la position de la souris
            clicked_tile = self.rect.move(
                (mouse_pos[0] // TILE_SIZE -
                 self.rect.x // TILE_SIZE) * TILE_SIZE,
                (mouse_pos[1] // TILE_SIZE -
                 self.rect.y // TILE_SIZE) * TILE_SIZE
            )

            # S'il clique sur une tuile adjacente et qu'il reste des mouvements
            if (clicked_tile.x, clicked_tile.y) in self.adjacent_positions and self.movement_remaining > 0 and self.show_adjacent_tiles:
                self.can_move = False
                self.show_adjacent_tiles = False
                self.direction = Vector2(
                    (clicked_tile.x - self.rect.x) // TILE_SIZE, (clicked_tile.y - self.rect.y) // TILE_SIZE)

            # Si il clique sur le joueur
            elif (clicked_tile.x, clicked_tile.y) == (self.rect.x, self.rect.y):
                self.show_adjacent_tiles = not self.show_adjacent_tiles
                # Redéfinit le nombre de mouvements restants
                if self.movement_remaining == 0:
                    self.movement_roll = randint(1, 6)
                    self.movement_remaining = self.movement_roll

    def move(self):
        """
        Déplace le joueur selon la direction et le temps écoulé.
        """
        if self.current_time - self.last_move_time >= SLEEP_TIME and not self.can_move:
            if self.direction.x != 0 and self.direction.y != 0:
                self.try_move(self.direction.x * TILE_SIZE,
                              self.direction.y * TILE_SIZE)
            else:
                if self.direction.x != 0:
                    self.try_move(self.direction.x * TILE_SIZE, 0)
                if self.direction.y != 0:
                    self.try_move(0, self.direction.y * TILE_SIZE)

    def try_move(self, dx, dy):
        """
        Tente de déplacer le joueur de dx et dy.

        Args:
            dx (int): Déplacement en x.
            dy (int): Déplacement en y.
        """
        new_rect = self.rect.move(dx, dy)

        # Vérifie les collisions avec les autres sprites walls
        if not any(sprite.rect.colliderect(new_rect) for sprite in self.colliders["walls"]) and self.movement_remaining > 0:
            self.rect.x += dx
            self.rect.y += dy
            self.movement_remaining -= 1
            self.last_move_time = self.current_time

            self.on_collision_with_object()
        else:
            self.can_move = True
            self.direction = Vector2(0, 0)

            if (any(sprite.rect.colliderect(new_rect) for sprite in self.colliders["walls"])):
                self.show_adjacent_tiles = True

    def on_collision_with_object(self):
        # Lors d'une collision avec un objet, le joueur execute la methode on_collision de l'objet.

        for object_collided in pygame.sprite.spritecollide(self, self.colliders["objects"], False):
            print(f"collision with {object_collided}")

            if isinstance(object_collided, Teleporter):
                self = object_collided.on_collision(
                    self, self.level.objects)
                return

            if isinstance(object_collided, Stair):
                object_collided.on_collision(self.level)
                return

            self = object_collided.on_collision(self)

    def update_adjacent_tiles(self):
        """
        Met à jour les tuiles adjacentes que le joueur peut atteindre.
        """
        self.adjacent_positions = []

        if self.movement_roll % 2 != 0:
            for dx, dy in [(-TILE_SIZE, TILE_SIZE), (TILE_SIZE, TILE_SIZE), (TILE_SIZE, -TILE_SIZE), (-TILE_SIZE, -TILE_SIZE)]:
                pos = (self.rect.x + dx, self.rect.y + dy)
                rect = pygame.Rect(pos, (TILE_SIZE, TILE_SIZE))

                # Si la tuile est un mur, ne l'ajoute pas aux tuiles adjacentes
                if not any(sprite.rect.colliderect(rect) for sprite in self.colliders["walls"]):
                    self.adjacent_positions.append(pos)
        else:
            for dx, dy in [(-TILE_SIZE, 0), (TILE_SIZE, 0), (0, -TILE_SIZE), (0, TILE_SIZE)]:
                pos = (self.rect.x + dx, self.rect.y + dy)
                rect = pygame.Rect(pos, (TILE_SIZE, TILE_SIZE))

                # Si la tuile est un mur, ne l'ajoute pas aux tuiles adjacentes
                if not any(sprite.rect.colliderect(rect) for sprite in self.colliders["walls"]):
                    self.adjacent_positions.append(pos)

    def draw_adjacent_tiles(self, surface):
        """
        Ecrit le nombre de mouvements restants sur les tuiles adjacentes.

        Args:
            surface (pygame.Surface): La surface sur laquelle dessiner les tuiles adjacentes.
        """
        if self.can_move and self.movement_remaining > 0 and self.show_adjacent_tiles:
            for pos in self.adjacent_positions:
                font = pygame.font.Font(None, int(TILE_SIZE * 0.5))
                text = font.render(str(self.movement_remaining), True, BLACK)
                text_rect = text.get_rect(center=pos + Vector2(TILE_SIZE // 2))
                pygame.draw.circle(
                    surface, GRAY, pos + Vector2(TILE_SIZE // 2), TILE_SIZE // 4)

                surface.blit(text, text_rect)

    def draw(self, surface):
        """
        Dessine le joueur sur la surface spécifiée.

        Args:
            surface (pygame.Surface): La surface sur laquelle dessiner le joueur.
        """
        surface.blit(self.image, self.rect)
        if self.can_move and self.movement_remaining > 0:
            self.draw_adjacent_tiles(surface)

    def update(self, dt):
        """
        Met à jour l'état du joueur.

        Args:
            dt (float): Le temps écoulé depuis la dernière mise à jour.
        """
        self.current_time = pygame.time.get_ticks()
        self.input()
        self.move()
        self.update_adjacent_tiles()

    def check_player_still_alive(self):
        return self.hp > 0
