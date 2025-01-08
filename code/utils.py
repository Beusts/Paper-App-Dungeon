import pygame


def draw_text(surface, text, position, font, color, center=False, center_y=False, line_width=None):
    text_surface = font.render(text, True, color)
    if center:
        text_rect = text_surface.get_rect(center=position)
    elif center_y:
        text_rect = text_surface.get_rect(x=position[0], centery=position[1])
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
