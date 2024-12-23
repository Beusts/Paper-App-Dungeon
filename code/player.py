from settings import *
from pygame.math import Vector2
from pygame.sprite import spritecollide


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft=pos)

        self.direction = Vector2()
        self.speed = 200

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = Vector2(0, 0)
        if keys[pygame.K_RIGHT]:
            input_vector.x += 1
        if keys[pygame.K_LEFT]:
            input_vector.x -= 1
        if keys[pygame.K_UP]:
            input_vector.y -= 1
        if keys[pygame.K_DOWN]:
            input_vector.y += 1
        self.direction = input_vector

    def move(self, dt):
        if self.direction.x != 0:
            self.rect.x += self.direction.x * TILE_SIZE

        if self.direction.y != 0:
            self.rect.y += self.direction.y * TILE_SIZE

    def update(self, dt):
        self.input()
        self.move(dt)
