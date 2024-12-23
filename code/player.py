from settings import *
from pygame.math import Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, colliders):
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft=pos)

        self.direction = Vector2()
        self.speed = 200
        self.colliders = colliders

    def input(self):
        # Check for mouse click
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            self.handle_mouse_click(mouse_pos)

    def handle_mouse_click(self, mouse_pos):
        clicked_tile = self.rect.move(
            (mouse_pos[0] // TILE_SIZE - self.rect.x // TILE_SIZE) * TILE_SIZE,
            (mouse_pos[1] // TILE_SIZE - self.rect.y // TILE_SIZE) * TILE_SIZE
        )
        if clicked_tile.topleft in self.adjacent_positions:
            self.rect.topleft = clicked_tile.topleft

    def move(self, dt):
        if self.direction.x != 0:
            self.rect.x += self.direction.x * TILE_SIZE
            self.collision('horizontal')

        if self.direction.y != 0:
            self.rect.y += self.direction.y * TILE_SIZE
            self.collision('vertical')

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.colliders:
                if sprite.rect.colliderect(self.rect):
                    print("Collision detected!")
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right

        if direction == 'vertical':
            for sprite in self.colliders:
                if sprite.rect.colliderect(self.rect):
                    print("Collision detected!")
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom

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
        for pos in self.adjacent_positions:
            rect = pygame.Rect(pos, (TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(surface, 'blue', rect, 1)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.draw_adjacent_tiles(surface)

    def update(self, dt):
        self.input()
        self.move(dt)
        self.update_adjacent_tiles()
