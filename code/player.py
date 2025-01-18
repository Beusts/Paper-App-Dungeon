from time import sleep

from settings import *
from pygame.math import Vector2
from random import randint
from teleporter import Teleporter
from stair import Stair
from utils import draw_text

from shop import *

class Player(pygame.sprite.Sprite):

    def __init__(self):
        """
        Initialise un joueur
        """

        super().__init__()

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
        self.coins = 100
        self.deaths = 0
        self.keys = 0

        self.losing_hp = 0
        self.winning_hp = 0
        self.losing_coins = 0
        self.winning_coins = 0

        self.inventory = {
            "Doubling Potion": {"quantity": 0 , "item": Doubling_Potion(self.direction, self)},
            "Scroll of Mulligan": {"quantity": 1 , "item": Scroll_of_Mulligan(self.direction, self)},
            "Break on Through": {"quantity": 0 , "item": Break_on_Trought(self.direction, self)},
            "Teleport Scroll": {"quantity": 1 , "item": Teleport_Scroll(self.direction, self)},
        }

        self.inventory_button_rect = pygame.Rect(
            0, 0, UI_SIZE * 4, UI_SIZE * 2)
        self.inventory_button_rect.center = (
            UI_SIZE * 7.5, UI_SIZE * 25)

        self.show_player_info = True
        self.show_inventory = False

    def setup(self, pos, groups, colliders, level, x_offset):
        self.kill()
        self.add(groups)
        self.image = pygame.image.load(
            join('graphics', 'players.png')).convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (get_tile_size(), get_tile_size()))
        self.rect = self.image.get_rect(topleft=pos)
        self.colliders = colliders
        self.level = level
        self.x_offset = x_offset

    def input(self):
        """
        Gère les entrées de l'utilisateur.
        Il faut relacher le clic de souris pour pouvoir cliquer à nouveau.
        """
        global can_receive_input
        if pygame.mouse.get_pressed()[0] and can_receive_input:
            mouse_pos = pygame.mouse.get_pos()
            self.handle_mouse_click(mouse_pos)
            can_receive_input = False
        elif not pygame.mouse.get_pressed()[0]:
            can_receive_input = True

    def handle_mouse_click(self, mouse_pos):
        """
        Gère les clics de souris pour déplacer le joueur ou ouvrir l'inventaire.

        Args:
            mouse_pos (tuple): La position (x, y) de la souris.
        """
        if self.inventory_button_rect.collidepoint(mouse_pos):
            self.show_inventory = not self.show_inventory
            self.show_player_info = not self.show_player_info
            return

        # Calcule la tuile cliquée en fonction de la position de la souris
        clicked_tile = self.rect.move(
            ((mouse_pos[0] - self.x_offset) // get_tile_size() -
                self.rect.x // get_tile_size()) * get_tile_size(),
            (mouse_pos[1] // get_tile_size() -
                self.rect.y // get_tile_size()) * get_tile_size()
        )

        # S'il clique sur une tuile adjacente et qu'il reste des mouvements
        if (clicked_tile.x, clicked_tile.y) in self.adjacent_positions and self.movement_remaining > 0 and self.show_adjacent_tiles and self.can_move:
            self.can_move = False
            self.show_adjacent_tiles = False
            self.direction = Vector2(
                (clicked_tile.x - self.rect.x) // get_tile_size(), (clicked_tile.y - self.rect.y) // get_tile_size())

        # Si il clique sur le joueur
        elif (clicked_tile.x, clicked_tile.y) == (self.rect.x, self.rect.y) and self.can_move:
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
                self.try_move(self.direction.x * get_tile_size(),
                              self.direction.y * get_tile_size())
            else:
                if self.direction.x != 0:
                    self.try_move(self.direction.x * get_tile_size(), 0)
                if self.direction.y != 0:
                    self.try_move(0, self.direction.y * get_tile_size())

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
            for dx, dy in [(-get_tile_size(), get_tile_size()), (get_tile_size(), get_tile_size()), (get_tile_size(), -get_tile_size()), (-get_tile_size(), -get_tile_size())]:
                pos = (self.rect.x + dx, self.rect.y + dy)
                rect = pygame.Rect(pos, (get_tile_size(), get_tile_size()))

                # Si la tuile est un mur, ne l'ajoute pas aux tuiles adjacentes
                if not any(sprite.rect.colliderect(rect) for sprite in self.colliders["walls"]):
                    self.adjacent_positions.append(pos)
        else:
            for dx, dy in [(-get_tile_size(), 0), (get_tile_size(), 0), (0, -get_tile_size()), (0, get_tile_size())]:
                pos = (self.rect.x + dx, self.rect.y + dy)
                rect = pygame.Rect(pos, (get_tile_size(), get_tile_size()))

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
                font = pygame.font.Font(None, int(get_tile_size() * 0.5))
                text = font.render(str(self.movement_remaining), True, BLACK)
                text_rect = text.get_rect(
                    center=pos + Vector2(get_tile_size() // 2))
                pygame.draw.circle(
                    surface, GRAY, pos + Vector2(get_tile_size() // 2), get_tile_size() // 4)

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
        self.draw_inventory_button(surface)
        if self.show_player_info:
            self.draw_information_player(surface)
        if self.show_inventory:
            self.draw_inventory(surface)

    def draw_inventory(self,surface):
        """
        affiche l'inventaire du joueur.
        """
        font = pygame.font.Font(None, UI_SIZE)

        x, y = (UI_SIZE, UI_SIZE * 17)
        color = GRAY

        inventory_rect = []
        for i in range(len(self.inventory)):

            inventory_rect.append(pygame.draw.rect(surface, color, (x, y, WINDOW_WIDTH - 2 * UI_SIZE, UI_SIZE), width=4))
            y = y + UI_SIZE * 1.5
            color = (160, 160, 160) if color == GRAY else GRAY

        i = 0

        for key, value in self.inventory.items():
            draw_text(surface, f"{value["quantity"] }x - {key}", (inventory_rect[i].x + 6, inventory_rect[i].y + 6), font, BLACK)

            self.handle_click_inventory(inventory_rect[i], value, key)
            i += 1


    def handle_click_inventory(self, rect, value, key):
        # Check for mouse click on the item
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        global can_receive_input
        print(f"if : {rect.collidepoint(mouse_pos) and mouse_click}")

        if rect.collidepoint(mouse_pos) and mouse_click:
            if value["quantity"] > 0:
                # TODO : make use() method of each item

                if key == "Teleport Scroll" :
                    value["item"].use(self.level.all_sprites)

                if key == "Scroll of Mulligan" :
                    print(f"object to use : {value["item"]}")

                if key == "Break on Through":
                    print(f"object to use : {value["item"]}")

                if key == "Doubling Potion":
                    print(f"object to use : {value["item"]}")

                value["quantity"] -= 1

            print(f"object clicked : {key}")
        elif not mouse_click:
            can_receive_input = True

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

    def draw_inventory_button(self, surface):
        font = pygame.font.Font(None, UI_SIZE)
        rect = pygame.Rect(0, 0, UI_SIZE * 4, UI_SIZE * 2)
        rect.center = (UI_SIZE * 7.5, UI_SIZE * 25)
        pygame.draw.rect(
            surface, GRAY, self.inventory_button_rect, border_radius=10)
        text = font.render("Inventory", True, BLACK)
        text_rect = text.get_rect(center=rect.center)
        surface.blit(text, text_rect)

    def draw_information_player(self, surface):
        """
        Dessine un espace pouvant afficher la vie, l'argent, au début et à la fin d'un level.

        Args:
            surface (pygame.Surface): La surface sur laquelle dessiner les informations du joueur.
        """
        font = pygame.font.Font(None, UI_SIZE)

        rect_positions = [
            (UI_SIZE * 4, UI_SIZE * 17),
            (UI_SIZE * 7.5, UI_SIZE * 17),
            (UI_SIZE * 4, UI_SIZE * 20),
            (UI_SIZE * 7.5, UI_SIZE * 20)
        ]

        draw_rect = []
        for pos in rect_positions:
            rect = pygame.Rect(
                pos[0], pos[1], UI_SIZE * 3.5, UI_SIZE * 3)
            rect.inflate_ip(-UI_SIZE * 0.15, -UI_SIZE * 0.15)
            draw_rect.append(rect)

        pygame.draw.rect(
            surface, GRAY, draw_rect[0], border_top_left_radius=10)
        pygame.draw.rect(
            surface, GRAY, draw_rect[1], border_top_right_radius=10)
        pygame.draw.rect(
            surface, GRAY, draw_rect[2], border_bottom_left_radius=10)
        pygame.draw.rect(
            surface, GRAY, draw_rect[3], border_bottom_right_radius=10)

        if self.winning_hp > 0:
            draw_text(surface, str(self.winning_hp),
                      draw_rect[0].center, font, BLACK, center=True)

        if self.losing_hp > 0:
            draw_text(surface, str(self.losing_hp),
                      draw_rect[1].center, font, BLACK, center=True)

        if self.winning_coins > 0:
            draw_text(surface, str(self.winning_coins),
                      draw_rect[2].center, font, BLACK, center=True)

        if self.losing_coins > 0:
            draw_text(surface, str(self.losing_coins),
                      draw_rect[3].center, font, BLACK, center=True)

        draw_text(surface, "Starting", (UI_SIZE *
                  0.5, UI_SIZE * 16), font, BLACK)
        draw_text(
            surface, "+", (draw_rect[0].centerx, UI_SIZE * 16), font, BLACK, center_x=True)
        draw_text(
            surface, "-", (draw_rect[1].centerx, UI_SIZE * 16), font, BLACK, center_x=True)
        draw_text(surface, "Ending", (UI_SIZE *
                  12, UI_SIZE * 16), font, BLACK)

        draw_text(surface, f'{self.hp} HP', (UI_SIZE *
                  0.5, draw_rect[1].centery), font, BLACK)
        draw_text(surface, f'{self.coins} ¢', (UI_SIZE *
                  0.5, draw_rect[2].centery), font, BLACK)

        draw_text(surface, f'{self.hp + self.winning_hp - self.losing_hp} HP',
                  (UI_SIZE * 12, draw_rect[1].centery), font, BLACK)
        draw_text(surface, f'{self.coins + self.winning_coins - self.losing_coins} ¢',
                  (UI_SIZE * 12, draw_rect[2].centery), font, BLACK)
