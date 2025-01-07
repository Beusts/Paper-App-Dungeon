import pygame


def draw_text(surface, text, position, font, color):
    """
    Dessine un texte
    """
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)


def draw_center_text(surface, text, position, font, color):
    """
    Dessine un texte au centre de la surface
    """
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(position[0], position[1]))
    surface.blit(text_surface, text_rect)


def draw_centery_text(surface, text, position, font, color):
    """
    Dessine un texte centré verticalement
    """
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(x=position[0], centery=position[1])
    surface.blit(text_surface, text_rect)
