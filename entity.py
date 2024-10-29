# entity.py
import pygame
from constants import *


class Entity:
    def __init__(self, screen, font, small_font):
        self.screen = screen
        self.font = font
        self.small_font = small_font

    def draw_circle(self, pos, color, main_text, sub_text="", radius=30):
        pygame.draw.circle(self.screen, color, pos, radius)

        text_surface = self.font.render(main_text, True, BLACK)
        text_rect = text_surface.get_rect(center=(pos[0], pos[1] + radius + 10))
        self.screen.blit(text_surface, text_rect)

        if sub_text:
            sub_surface = self.small_font.render(sub_text, True, BLACK)
            sub_rect = sub_surface.get_rect(center=(pos[0], pos[1] + radius + 30))
            self.screen.blit(sub_surface, sub_rect)

    def draw_poolside(self, pos, radius=30):
        pygame.draw.circle(self.screen, ORANGE, pos, radius)

        x, y = pos
        scale = radius / 30
        pygame.draw.line(self.screen, BLACK,
                         (x - 20 * scale, y + 10 * scale),
                         (x + 20 * scale, y + 10 * scale),
                         max(1, int(3 * scale)))
        pygame.draw.line(self.screen, BLACK,
                         (x - 15 * scale, y),
                         (x + 15 * scale, y - 10 * scale),
                         max(1, int(3 * scale)))

        text_surface = self.font.render("Humans", True, BLACK)
        text_rect = text_surface.get_rect(center=(x, y + radius + 10))
        self.screen.blit(text_surface, text_rect)

        sub_surface = self.small_font.render("Poolside", True, BLACK)
        sub_rect = sub_surface.get_rect(center=(x, y + radius + 30))
        self.screen.blit(sub_surface, sub_rect)


# stage_manager.py
class StageManager:
    def __init__(self):
        self.base_rich_radius = BASE_RADIUS
        self.base_human_radius = BASE_RADIUS
        self.rich_radius = BASE_RADIUS
        self.human_radius = BASE_RADIUS
        self.stage = TRADITIONAL
        self.show_rich = True
        self.show_govt = True
        self.show_humans = True
        self.rich_attack_count = 0
        self.machine_attack_count = 0
        self.attacks_needed = 50
        self.warning_alpha = 0
        self.warning_increasing = True

    def update_circle_sizes(self):
        if self.stage == AI_MATURE:
            self.rich_radius = int(self.base_rich_radius * 1.3)
            self.human_radius = int(self.base_human_radius * 1.2)
        elif self.stage == INEQUALITY:
            self.rich_radius = int(self.base_rich_radius * 1.5)
            self.human_radius = int(self.base_human_radius * 0.8)
        else:
            self.rich_radius = self.base_rich_radius
            self.human_radius = self.base_human_radius

    def advance_stage(self):
        if self.stage == TRADITIONAL:
            self.stage = AI_TRANSITION
        elif self.stage == AI_TRANSITION:
            self.stage = AI_MATURE
        elif self.stage == AI_MATURE:
            self.stage = INEQUALITY
        elif self.stage == INEQUALITY:
            self.stage = UNREST
        elif self.stage == UNREST:
            self.stage = POST_UNREST
        elif self.stage == POST_UNREST:
            self.stage = MACHINE_TAKEOVER
        elif self.stage == MACHINE_TAKEOVER:
            self.stage = AI_ALIGNMENT
        elif self.stage == AI_ALIGNMENT:
            self.stage = END_STATE
        else:
            self.reset()

        self.update_circle_sizes()

    def reset(self):
        self.stage = TRADITIONAL
        self.show_rich = True
        self.show_govt = True
        self.show_humans = True
        self.rich_attack_count = 0
        self.machine_attack_count = 0