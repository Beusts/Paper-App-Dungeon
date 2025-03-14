"""
Module contenant la classe Menu qui gère l'interface du menu principal du jeu.
"""

import sys
import pygame
from settings import FPS, UI_SIZE, BLACK, GRAY, WHITE
from utils import draw_text
from pdfGenerator import PdfGenerator


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

        self.start_rect = pygame.Rect(0, 0, UI_SIZE * 10, UI_SIZE * 2)
        self.start_rect.center = (UI_SIZE * 7.5, UI_SIZE * 6)

        self.quit_rect = pygame.Rect(0, 0, UI_SIZE * 10, UI_SIZE * 2)
        self.quit_rect.center = (UI_SIZE * 7.5, UI_SIZE * 12)

        self.pdf_rect = pygame.Rect(0, 0, UI_SIZE * 10, UI_SIZE * 2)
        self.pdf_rect.center = (UI_SIZE * 7.5, UI_SIZE * 9)

        self.level_map_files = level_map_files

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
            self.draw()
            pygame.display.update()

    def handle_events(self):
        """
        Gère les événements d'entrée utilisateur dans le menu.

        Returns:
            str: L'action à effectuer ('start', 'quit', 'generate_pdf') ou None si aucune action
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self.start_rect.collidepoint(mouse_pos):
                    return 'start'
                elif self.quit_rect.collidepoint(mouse_pos):
                    return 'quit'
                elif self.pdf_rect.collidepoint(mouse_pos):
                    return 'generate_pdf'
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
        self.draw_button(self.start_rect, "Start Game")
        self.draw_button(self.quit_rect, "Quit")
        self.draw_button(self.pdf_rect, "Generate PDF")
        draw_text(self.display_surface, "Paper App Dungeon",
                  (UI_SIZE * 7.5, UI_SIZE * 2), self.font, BLACK, center=True)

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
