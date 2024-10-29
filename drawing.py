import pygame
from constants import BLACK, ORANGE

def draw_entity(screen, font, small_font, pos, color, main_text, sub_text="", radius=None):
    # Use passed radius or BASE_RADIUS if none provided
    pygame.draw.circle(screen, color, pos, radius)

    text_surface = font.render(main_text, True, BLACK)
    text_rect = text_surface.get_rect(center=(pos[0], pos[1] + radius + 10))
    screen.blit(text_surface, text_rect)

    if sub_text:
        sub_surface = small_font.render(sub_text, True, BLACK)
        sub_rect = sub_surface.get_rect(center=(pos[0], pos[1] + radius + 30))
        screen.blit(sub_surface, sub_rect)

def draw_poolside(screen, font, small_font, pos, radius=None):
    pygame.draw.circle(screen, ORANGE, pos, radius)

    x, y = pos
    scale = radius / 30  # Scale the decorative lines based on radius
    pygame.draw.line(screen, BLACK,
                     (x - 20 * scale, y + 10 * scale),
                     (x + 20 * scale, y + 10 * scale),
                     max(1, int(3 * scale)))
    pygame.draw.line(screen, BLACK,
                     (x - 15 * scale, y),
                     (x + 15 * scale, y - 10 * scale),
                     max(1, int(3 * scale)))

    text_surface = font.render("Humans", True, BLACK)
    text_rect = text_surface.get_rect(center=(x, y + radius + 10))
    screen.blit(text_surface, text_rect)

    sub_surface = small_font.render("Poolside", True, BLACK)
    sub_rect = sub_surface.get_rect(center=(x, y + radius + 30))
    screen.blit(sub_surface, sub_rect)