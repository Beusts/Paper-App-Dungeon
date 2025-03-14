"""
Module pour générer un fichier PDF contenant des captures d'écran de chaque niveau du jeu.
Ce module est utilisé pour permettre de jouer au jeu sur papier.
"""

from shop import *
from level import Level
from player import Player
import os
from fpdf import FPDF


class PdfGenerator(pygame.sprite.Sprite):
    """
    Classe qui génère un fichier PDF contenant des captures d'écran de tous les niveaux du jeu.
    """

    def __init__(self, level_files):
        """
        Initialise le générateur de PDF et crée immédiatement le fichier.

        Args:
            level_files (list): Liste des noms de fichiers de niveaux à inclure dans le PDF
        """
        self.clock = pygame.time.Clock()
        dt = self.clock.tick(FPS) / 1000
        self.player = Player()

        save_path = "recorded_frames"

        # Create folder if it not exist
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        nb_files = len(level_files)

        for i in range(nb_files):

            if level_files[i].startswith('shop'):
                current_stage = Shop(
                    level_files[i], self.player)
            else:
                current_stage = Level(
                    level_files[i], self.player)

            current_stage.run(dt)
            pygame.display.update()

            # Screen shot in memory
            frame_path = os.path.join(
                save_path, f"frame_{i:03d}.png")
            pygame.image.save(screen, frame_path)
            pygame.display.update()

        pdf = FPDF()
        image_files = sorted(os.listdir(save_path))

        for image_file in image_files:
            img_path = os.path.join(save_path, image_file)
            pdf.add_page()
            # manage image size in PDF, image centered on A4 page
            pdf.image(img_path, x=15, y=10, w=180)

            if os.path.exists(save_path):
                os.remove(img_path)

        pdf.output("game_frames.pdf")
