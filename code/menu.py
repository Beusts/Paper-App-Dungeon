"""
Module contenant la classe Menu qui gère l'interface du menu principal du jeu.
"""

import sys
import pygame
from settings import FPS, UI_SIZE, BLACK, GRAY, WHITE
from utils import draw_text
from pdfGenerator import PdfGenerator, GenerationStepsPdfGenerator


class Menu:
    """
    Classe qui gère le menu principal du jeu avec les options de démarrage, quitter et générer un PDF.
    """

    def __init__(self, display_surface, level_map_files):
        """
        Initialise le menu avec la surface d'affichage et les fichiers de niveau.

        Args:
            display_surface (pygame.Surface): La surface d'affichage du jeu
            level_map_files (list): Liste des fichiers de niveaux pour générer le PDF
        """
        self.display_surface = display_surface
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, UI_SIZE * 2)
        self.small_font = pygame.font.Font(None, UI_SIZE)

        # Ajustement des positions des boutons pour mettre Quit en dernier
        self.start_rect = pygame.Rect(0, 0, UI_SIZE * 10, UI_SIZE * 2)
        self.start_rect.center = (UI_SIZE * 7.5, UI_SIZE * 6)

        self.pdf_rect = pygame.Rect(0, 0, UI_SIZE * 10, UI_SIZE * 2)
        self.pdf_rect.center = (UI_SIZE * 7.5, UI_SIZE * 9)
        
        self.gen_steps_pdf_rect = pygame.Rect(0, 0, UI_SIZE * 10, UI_SIZE * 2)
        self.gen_steps_pdf_rect.center = (UI_SIZE * 7.5, UI_SIZE * 12)

        self.quit_rect = pygame.Rect(0, 0, UI_SIZE * 10, UI_SIZE * 2)
        self.quit_rect.center = (UI_SIZE * 7.5, UI_SIZE * 15)

        self.level_map_files = level_map_files
        self.level_only_files = [
            f for f in level_map_files if f.startswith('level')]

        # Pour l'interface de sélection du niveau
        self.selecting_level = False
        self.level_buttons = []
        self.back_button_rect = pygame.Rect(0, 0, UI_SIZE * 6, UI_SIZE * 1.5)
        self.back_button_rect.center = (UI_SIZE * 7.5, UI_SIZE * 18)

        # Créer les boutons pour chaque niveau
        button_width, button_height = UI_SIZE * 6, UI_SIZE * 1.5
        max_buttons_per_row = 2
        rows = (len(self.level_only_files) +
                max_buttons_per_row - 1) // max_buttons_per_row

        for i, level_name in enumerate(self.level_only_files):
            row = i // max_buttons_per_row
            col = i % max_buttons_per_row
            x = UI_SIZE * 3 + col * (button_width + UI_SIZE) + UI_SIZE
            y = UI_SIZE * 6 + row * (button_height + UI_SIZE)

            button_rect = pygame.Rect(0, 0, button_width, button_height)
            button_rect.center = (x, y)
            self.level_buttons.append((button_rect, level_name))

    def run(self):
        """
        Exécute la boucle principale du menu.

        Cette méthode gère l'affichage et les interactions avec le menu jusqu'à ce que
        l'utilisateur démarre le jeu ou quitte l'application.
        """
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000
            action = self.handle_events()
            if action == 'start':
                running = False
            elif action == 'quit':
                pygame.quit()
                sys.exit()
            elif action == 'generate_pdf':
                PdfGenerator(self.level_map_files)
            elif action == 'select_level_for_gen_steps':
                self.selecting_level = True
            elif action == 'back':
                self.selecting_level = False
            elif action and action.startswith('export_steps_'):
                level_name = action[13:]  # Extrait le nom du niveau
                GenerationStepsPdfGenerator(level_name)
                self.selecting_level = False

            self.draw()
            pygame.display.update()

    def handle_events(self):
        """
        Gère les événements d'entrée utilisateur dans le menu.

        Returns:
            str: L'action à effectuer ou None si aucune action
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                if self.selecting_level:
                    # Vérifier les boutons de niveau quand on est dans le mode sélection
                    for button, level_name in self.level_buttons:
                        if button.collidepoint(mouse_pos):
                            return f'export_steps_{level_name}'

                    if self.back_button_rect.collidepoint(mouse_pos):
                        return 'back'
                else:
                    # Interface principale
                    if self.start_rect.collidepoint(mouse_pos):
                        return 'start'
                    elif self.quit_rect.collidepoint(mouse_pos):
                        return 'quit'
                    elif self.pdf_rect.collidepoint(mouse_pos):
                        return 'generate_pdf'
                    elif self.gen_steps_pdf_rect.collidepoint(mouse_pos):
                        return 'select_level_for_gen_steps'
        return None

    def draw(self):
        """
        Dessine le menu complet sur la surface d'affichage.
        """
        self.display_surface.fill(WHITE)
        pygame.draw.rect(self.display_surface, GRAY,
                         (0, 0, UI_SIZE * 15, UI_SIZE * 3))
        round_radius = int(UI_SIZE)
        for i in range(15):
            pygame.draw.rect(self.display_surface, GRAY,
                             (i * UI_SIZE, UI_SIZE * 3, UI_SIZE, UI_SIZE),
                             border_bottom_left_radius=round_radius, border_bottom_right_radius=round_radius)

        draw_text(self.display_surface, "Paper App Dungeon",
                  (UI_SIZE * 7.5, UI_SIZE * 2), self.font, BLACK, center=True)

        if self.selecting_level:
            # Affichage de l'interface de sélection du niveau

            # Afficher tous les boutons de niveau
            for button, level_name in self.level_buttons:
                self.draw_button(button, level_name)

            # Bouton retour
            self.draw_button(self.back_button_rect, "Retour")
        else:
            # Menu principal
            self.draw_button(self.start_rect, "Start Game")
            self.draw_button(self.pdf_rect, "Generate PDF")
            self.draw_button(self.gen_steps_pdf_rect, "Gen. Steps PDF")
            self.draw_button(self.quit_rect, "Quit")

    def draw_button(self, rect, text):
        """
        Dessine un bouton sur la surface d'affichage.

        Args:
            rect (pygame.Rect): Rectangle définissant la position et taille du bouton
            text (str): Texte à afficher sur le bouton
        """
        pygame.draw.rect(self.display_surface, GRAY, rect, border_radius=10)
        draw_text(self.display_surface, text, rect.center,
                  self.font, BLACK, center=True)
