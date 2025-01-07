from settings import *
from object import *

class StandardHeart(Object):

    def __init__(self, pos, groups, value):
        """
        Initialise un coeur à la position donnée et l'ajoute aux groupes spécifiés.

        Args:
            pos (tuple): La position (x, y) de le coeur.
            groups (list): Les groupes de sprites auxquels le coeur appartient.
            value (int): La valeur associée à l'ennemi.
        """
        self.value = value
        super().__init__(pos, groups)

    def design(self):
        """
        Crée l'image du coeur avec un numéro dessus.

        Returns:
            pygame.Surface: L'image du coeur avec le numéro ajouté.
        """
        image = pygame.image.load(
            join('graphics', 'heart.png')).convert_alpha()
        image = pygame.transform.scale(
            image, (TILE_SIZE, TILE_SIZE))

        return self.adding_number_to_standart_heart(image)

    def adding_number_to_standart_heart(self, image):
        """
        Ajoute un numéro sur l'image du coeur.

        Args:
            image (pygame.Surface): L'image de base du coeur.

        Returns:
            pygame.Surface: L'image avec le numéro ajouté.
        """
        font = pygame.font.Font(None, int(TILE_SIZE * 0.5))
        value_to_string = str(self.value)

        text_surface = font.render(value_to_string, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=image.get_rect().center)

        heart_with_number = image.copy()
        heart_with_number.blit(text_surface, text_rect)

        return heart_with_number

    def on_collision(self, player):
        """
        Gestion de la collision avec un joueur.

        Args:
            player (Player): Le joueur en collision avec ce coeur.

        Returns:
            Player: Le joueur après modification de ses points de vie.
        """
        if self.has_already_been_used(): return player

        print(f"Collision with me {self}")
        player.hp += self.value

        self.used = True
        self.has_already_been_used()

        return player
