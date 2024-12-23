import csv
from settings import *
from sprites import Wall
from player import Player


class Level:
    def __init__(self, level_data):
        self.display_surface = pygame.display.get_surface()

        # groups
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.Group()

        self.setup(level_data)

    def setup(self, level_data):
        with open(join('data', 'levels', level_data + '.csv'), newline='') as csvfile:
            level_reader = csv.reader(csvfile, delimiter=',')
            for y, row in enumerate(level_reader):
                for x, tile in enumerate(row):
                    if tile == '1':
                        Wall((x * TILE_SIZE, y * TILE_SIZE),
                             (self.all_sprites, self.walls))
                    elif tile == 'P':
                        Player((x * TILE_SIZE, y * TILE_SIZE),
                               self.all_sprites, self.walls)

    def run(self, dt):
        self.all_sprites.update(dt)
        self.display_surface.fill('black')
        for sprite in self.all_sprites:
            sprite.draw(self.display_surface)
