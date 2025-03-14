"""
Module contenant des fonctions utilitaires pour le jeu Paper App Dungeon.
"""

import pygame


def draw_text(surface, text, position, font, color, center=False, center_y=False, center_x=False, line_width=None):
    """
    Dessine du texte sur une surface avec différentes options d'alignement.

    Args:
        surface (pygame.Surface): La surface sur laquelle dessiner le texte
        text (str): Le texte à afficher
        position (tuple): La position (x, y) du texte
        font (pygame.font.Font): La police à utiliser
        color (tuple): La couleur RGB du texte
        center (bool): Si True, centre le texte horizontalement et verticalement
        center_y (bool): Si True, centre le texte verticalement uniquement
        center_x (bool): Si True, centre le texte horizontalement uniquement
        line_width (int): Si spécifié, limite la largeur du texte et crée des retours à la ligne
    """
    text_surface = font.render(text, True, color)
    if center:
        text_rect = text_surface.get_rect(center=position)
    elif center_y:
        text_rect = text_surface.get_rect(x=position[0], centery=position[1])
    elif center_x:
        text_rect = text_surface.get_rect(centerx=position[0], y=position[1])
    else:
        text_rect = text_surface.get_rect(topleft=position)

    if line_width != None and text_rect.width > line_width:
        lines = []
        line = ""
        for word in text.split():
            if font.size(line + word)[0] < line_width:
                line += word + " "
            else:
                lines.append(line)
                line = word + " "
        lines.append(line)

        for i, line in enumerate(lines):
            text_surface = font.render(line, True, color)
            text_rect = text_surface.get_rect(
                topleft=(position[0], position[1] + i * text_rect.height))
            surface.blit(text_surface, text_rect)
    else:
        surface.blit(text_surface, text_rect)
