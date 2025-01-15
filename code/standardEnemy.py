from settings import *
from object import *
from utils import draw_text


class StandardEnemy(Object):

    def __init__(self, pos, groups, value):
        """
        Initialise un ennemi à la position donnée et l'ajoute aux groupes spécifiés.

        Args:
            pos (tuple): La position (x, y) de l'ennemi.
            groups (list): Les groupes de sprites auxquels l'ennemi appartient.
            value (int): La valeur associée à l'ennemi.
        """
        self.value = value
        super().__init__(pos, groups)

    def design(self):
        """
        Crée l'image de l'ennemi avec un numéro dessus.

        Returns:
            pygame.Surface: L'image de l'ennemi avec le numéro ajouté.
        """
        image = pygame.image.load(
            join('graphics', 'enemy.png')).convert_alpha()
        image = pygame.transform.scale(
            image, (get_tile_size(), get_tile_size()))

        return self.adding_number_to_standart_enemy(image)

    def adding_number_to_standart_enemy(self, image):
        """
        Ajoute un numéro sur l'image de l'ennemi.

        Args:
            image (pygame.Surface): L'image de base de l'ennemi.

        Returns:
            pygame.Surface: L'image avec le numéro ajouté.
        """
        font = pygame.font.Font(None, int(get_tile_size() * 0.5))
        value_to_string = str(self.value)

        text_surface = font.render(value_to_string, True, (255, 255, 255))
        text_rect = text_surface.get_rect(
            centerx=get_tile_size() / 2, centery=get_tile_size() / 2)

        enemy_with_number = image.copy()
        enemy_with_number.blit(text_surface, text_rect)

        return enemy_with_number

    def on_collision(self, player):
        """
        Gestion de la collision avec un joueur.

        Args:
            player (Player): Le joueur en collision avec cet ennemi.

        Returns:
            Player: Le joueur après modification de ses points de vie.
        """
        print(f"Collision with me {self}")

        if self.has_already_been_used():
            return player

        player.losing_hp += self.value
        self.used = True
        self.has_already_been_used()

        return player
