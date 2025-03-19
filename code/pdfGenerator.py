"""
Module pour générer un fichier PDF contenant des captures d'écran de chaque niveau du jeu.
Ce module est utilisé pour permettre de jouer au jeu sur papier.
"""

from shop import *
from level import Level
from player import Player
import os
from fpdf import FPDF
from PIL import Image
import numpy as np


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


class GenerationStepsPdfGenerator(pygame.sprite.Sprite):
    """
    Classe qui génère un fichier PDF contenant des captures d'écran de toutes les étapes 
    de génération d'un niveau sous forme de frise.
    """

    def __init__(self, level_name):
        """
        Initialise le générateur de PDF pour les étapes de génération et crée immédiatement le fichier.

        Args:
            level_name (str): Nom du niveau dont on veut exporter les étapes de génération
        """
        self.clock = pygame.time.Clock()
        dt = self.clock.tick(FPS) / 1000
        self.player = Player()

        save_path = "generation_steps_frames"

        # Create folder if it not exist
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        # Création d'un objet Level pour le niveau spécifié
        level = Level(level_name, self.player)

        # Vérifier que des étapes de génération existent pour ce niveau
        if not level.generation_steps:
            print(
                f"Aucune étape de génération trouvée pour le niveau {level_name}")
            return

        # Activer l'affichage des étapes de génération
        level.showing_generation = True

        # Parcourir toutes les étapes de génération et les capturer
        for i in range(len(level.generation_steps)):
            level.current_step = i
            level.load_generation_step(i)

            # Exécuter le niveau pour afficher l'étape actuelle
            level.run(dt)
            pygame.display.update()

            # Screen shot in memory
            frame_path = os.path.join(
                save_path, f"step_{level_name}_{i:03d}.png")
            pygame.image.save(screen, frame_path)
            pygame.display.update()

            # Crop the bottom of the image
            with Image.open(frame_path) as img:
                width, height = img.size
                # Adjust the height as needed
                cropped_img = img.crop(
                    (0, 0, width, height - int(height * 0.43)))
                cropped_img.save(frame_path)

        # Créer le PDF avec toutes les captures organisées en frise
        self.create_frises_pdf(level_name, save_path)

    def create_frises_pdf(self, level_name, save_path):
        """
        Crée un PDF avec des frises d'images montrant les étapes de génération.

        Args:
            level_name (str): Nom du niveau
            save_path (str): Chemin du dossier contenant les images
        """
        # Récupérer toutes les images de ce niveau
        image_files = sorted([f for f in os.listdir(
            save_path) if f.startswith(f"step_{level_name}")])

        if not image_files:
            print(f"Aucune image trouvée pour le niveau {level_name}")
            return

        # Créer le PDF
        pdf = FPDF()
        pdf.add_page()

        # Ajouter un titre au PDF
        pdf.set_font("Arial", "B", 24)
        pdf.cell(
            0, 20, f"Étapes de génération du niveau {level_name}", 0, 1, "C")

        # Déterminer combien d'images on peut mettre par page
        images_per_row = 4  # Nombre d'images par ligne
        rows_per_page = 4   # Nombre de lignes par page
        images_per_page = images_per_row * rows_per_page
        total_images = len(image_files)

        # Calculer la taille des miniatures
        # 180mm est la largeur utilisable de la page A4
        thumbnail_width = 180 / images_per_row
        thumbnail_height = thumbnail_width  # Pour garder l'aspect carré

        # Créer des frises pour chaque ensemble d'images
        page_count = 1
        for i in range(0, total_images, images_per_page):
            if i > 0:  # Si ce n'est pas la première page
                pdf.add_page()
                page_count += 1

            # Placer les images en grille
            batch_images = image_files[i:i+images_per_page]

            for j, image_file in enumerate(batch_images):
                row = j // images_per_row
                col = j % images_per_row

                # Calculer la position de l'image sur la page
                x = 15 + col * thumbnail_width
                # 40mm de marge en haut, 15mm entre les lignes
                y = 40 + row * (thumbnail_height + 15)

                # Ouvrir et redimensionner l'image avec PIL
                img_path = os.path.join(save_path, image_file)

                # Ajouter l'image à la page
                pdf.image(img_path, x=x, y=y,
                          w=thumbnail_width, h=thumbnail_height)

                # Ajouter le numéro d'étape sous l'image
                step_num = int(image_file.split('_')[-1].split('.')[0]) + 1
                pdf.set_font("Arial", "", 8)
                pdf.set_xy(x, y + thumbnail_height)
                pdf.cell(thumbnail_width, 5, f"Étape {step_num}", 0, 1, "C")

                # Supprimer l'image après l'avoir ajoutée au PDF
                os.remove(img_path)

        # Sauvegarder le PDF
        pdf.output(f"generation_steps_{level_name}.pdf")
        print(
            f"PDF des étapes de génération du niveau {level_name} créé avec succès!")
