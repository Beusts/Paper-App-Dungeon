from settings import *
from pygame.math import Vector2
from random import randint


class Player(pygame.sprite.Sprite):

    def __init__(self, pos, groups, colliders):
        """
        Initialise un joueur à la position donnée et l'ajoute aux groupes spécifiés.

        Args:
            pos (tuple): La position (x, y) du joueur.
            groups (list): Les groupes de sprites auxquels le joueur appartient.
            colliders (pygame.sprite.Group): Les sprites avec lesquels le joueur peut entrer en collision.
        """
        super().__init__(*groups)

        self.image = pygame.image.load(
            join('graphics', 'players.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=pos)

        # self.groups = groups

        self.adjacent_positions = []
        self.colliders = colliders

        self.direction = Vector2(0, 0)

        self.movement_remaining = 0
        self.movement_roll = 0

        self.last_move_time = 0
        self.current_time = 0
        self.can_move = True

        # characteristic of a player
        self.hp = 10
        self.coins = 0
        self.deaths = 0

        self.player = groups[1].sprite

    def input(self):
        """
        Gère les entrées de l'utilisateur.
        """
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            self.handle_mouse_click(mouse_pos)

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

            # Vérifie si la tuile cliquée est adjacente
            if (clicked_tile.x, clicked_tile.y) in self.adjacent_positions:
                self.can_move = False
                self.direction = Vector2(
                    (clicked_tile.x - self.rect.x) // TILE_SIZE, (clicked_tile.y - self.rect.y) // TILE_SIZE)
            # Si la tuile cliquée est la même que la position actuelle
            elif (clicked_tile.x, clicked_tile.y) == (self.rect.x, self.rect.y):
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

    def on_collision_with_object(self):
        # Lors d'un collision avec un objet, le joueur execute la methode on_collision de l'objet.

        for object_collided in pygame.sprite.spritecollide(self.player, self.colliders["objects"], False):
            print(f"collision with {object_collided}")
            self.player = object_collided.on_collision(self.player)

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
        if self.can_move and self.movement_remaining > 0:
            for pos in self.adjacent_positions:
                rect = pygame.Rect(pos, (TILE_SIZE, TILE_SIZE))
                font = pygame.font.Font(None, int(TILE_SIZE * 0.5))
                text = font.render(str(self.movement_remaining), True, 'black')
                text_rect = text.get_rect(center=rect.center)
                surface.blit(text, text_rect)

    def draw(self, surface):
        """
        Dessine le joueur sur la surface spécifiée.

        Args:
            surface (pygame.Surface): La surface sur laquelle dessiner le joueur.
        """
        surface.blit(self.image, self.rect)
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
