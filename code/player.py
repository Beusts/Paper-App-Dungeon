from settings import *
from pygame.math import Vector2


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

            self.movement_remaining = 5
            self.direction = Vector2(
                (clicked_tile.x - self.rect.x) // TILE_SIZE, (clicked_tile.y - self.rect.y) // TILE_SIZE)

    def move(self, dt):
        if self.current_time - self.last_move_time >= SLEEP_TIME:
            if self.movement_remaining > 0:
                self.can_move = False
                self.movement_remaining -= 1
                self.last_move_time = self.current_time
            else:
                self.can_move = True
                self.direction = Vector2(0, 0)

            if self.direction.x != 0:
                self.rect.x += self.direction.x * TILE_SIZE

            if self.direction.y != 0:
                self.rect.y += self.direction.y * TILE_SIZE

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

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.draw_adjacent_tiles(surface)

    def update(self, dt):
        self.current_time = pygame.time.get_ticks()
        self.input()
        self.move(dt)
        self.update_adjacent_tiles()
