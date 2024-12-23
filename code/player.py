from settings import *
from pygame.math import Vector2
from random import randint


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, colliders):
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft=pos)

        self.adjacent_positions = []
        self.colliders = colliders

        self.direction = Vector2(0, 0)
        self.movement_remaining = 0
        self.last_move_time = 0
        self.current_time = 0
        self.can_move = True

    def input(self):
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            self.handle_mouse_click(mouse_pos)

    def handle_mouse_click(self, mouse_pos):
        if self.can_move:
            clicked_tile = self.rect.move(
                (mouse_pos[0] // TILE_SIZE -
                 self.rect.x // TILE_SIZE) * TILE_SIZE,
                (mouse_pos[1] // TILE_SIZE -
                 self.rect.y // TILE_SIZE) * TILE_SIZE
            )

            if (clicked_tile.x, clicked_tile.y) in self.adjacent_positions:
                self.can_move = False
                self.direction = Vector2(
                    (clicked_tile.x - self.rect.x) // TILE_SIZE, (clicked_tile.y - self.rect.y) // TILE_SIZE)
            elif (clicked_tile.x, clicked_tile.y) == (self.rect.x, self.rect.y):
                if self.movement_remaining == 0:
                    self.movement_remaining = randint(1, 6)

    def move(self):
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
        new_rect = self.rect.move(dx, dy)
        if not any(sprite.rect.colliderect(new_rect) for sprite in self.colliders) and self.movement_remaining > 0:
            self.rect.x += dx
            self.rect.y += dy
            self.movement_remaining -= 1
            self.last_move_time = self.current_time
        else:
            self.can_move = True
            self.direction = Vector2(0, 0)

    def update_adjacent_tiles(self):
        self.adjacent_positions = []
        for dx in [-TILE_SIZE, 0, TILE_SIZE]:
            for dy in [-TILE_SIZE, 0, TILE_SIZE]:
                if dx != 0 or dy != 0:
                    pos = (self.rect.x + dx, self.rect.y + dy)
                    rect = pygame.Rect(pos, (TILE_SIZE, TILE_SIZE))
                    if not any(sprite.rect.colliderect(rect) for sprite in self.colliders):
                        self.adjacent_positions.append(pos)

    def draw_adjacent_tiles(self, surface):
        if self.can_move:
            for pos in self.adjacent_positions:
                rect = pygame.Rect(pos, (TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(surface, 'blue', rect, 1)
                font = pygame.font.Font(None, 24)
                text = font.render(str(self.movement_remaining), True, 'white')
                text_rect = text.get_rect(center=rect.center)
                surface.blit(text, text_rect)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.draw_adjacent_tiles(surface)

    def update(self, dt):
        self.current_time = pygame.time.get_ticks()
        self.input()
        self.move()
        self.update_adjacent_tiles()
