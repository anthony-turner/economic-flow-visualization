# ui_manager.py
import pygame
from constants import *

class UIManager:
    def __init__(self, screen, font, small_font, big_font):
        self.screen = screen
        self.font = font
        self.small_font = small_font
        self.big_font = big_font

    def draw_warning_overlay(self, stage, warning_alpha):
        """Draw warning overlay during unrest or machine takeover"""
        if stage in [UNREST, MACHINE_TAKEOVER]:
            warning_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            warning_color = (255, 0, 0, warning_alpha)
            pygame.draw.rect(warning_surface, warning_color, (0, 0, WIDTH, HEIGHT))

            warning_text = "CIVIL UNREST" if stage == UNREST else "MACHINE TAKEOVER"
            text_surface = self.font.render(warning_text, True, RED)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 50))

            self.screen.blit(warning_surface, (0, 0))
            self.screen.blit(text_surface, text_rect)

    def draw_end_state_title(self, stage):
        """Draw title for end state"""
        if stage in [AI_ALIGNMENT, END_STATE]:
            title = STAGE_NAMES[stage]
            text_surface = self.big_font.render(title, True, BLACK)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(text_surface, text_rect)

    def draw_info(self, stage):
        """Draw GDP and stage information"""
        # Skip info display for end sequence stages
        if stage in [MACHINE_SURVIVAL, MACHINE_REPLICATION, AI_ALIGNMENT, END_STATE]:
            return

        gdp_values = {
            TRADITIONAL: 100,
            AI_TRANSITION: 150,
            AI_MATURE: 300,
            INEQUALITY: 300,
            UNREST: 250,
            POST_UNREST: 200,
            MACHINE_TAKEOVER: 400,
            MACHINE_SURVIVAL: 500,    # Added new stages
            MACHINE_REPLICATION: 600,  # Added new stages
            AI_ALIGNMENT: 0,          # Won't be used but added for completeness
            END_STATE: 0              # Won't be used but added for completeness
        }

        gdp_color = RED if stage in [UNREST, MACHINE_TAKEOVER] else BLACK
        gdp_text = f"GDP: {gdp_values[stage]}"
        gdp_surface = self.font.render(gdp_text, True, gdp_color)
        self.screen.blit(gdp_surface, (10, HEIGHT - 40))

        # # Don't show stage name during end sequence
        # if stage not in [MACHINE_SURVIVAL, MACHINE_REPLICATION]:
        #     mode_text = f"{STAGE_NAMES[stage]}"
        #     text_surface = self.font.render(mode_text, True, BLACK)
        #     self.screen.blit(text_surface, ((WIDTH // 2) - len({mode_text}), 10))

        # Don't show stage name during end sequence
        if stage not in [MACHINE_SURVIVAL, MACHINE_REPLICATION]:
            mode_text = f"{STAGE_NAMES[stage]}"
            text_surface = self.font.render(mode_text, True, BLACK)
            text_width = text_surface.get_width()
            text_x = (WIDTH // 2) - (text_width // 2)  # Center horizontally
            self.screen.blit(text_surface, (text_x, 10))

            # Only show space bar instruction during normal stages
            instruction_text = "Press SPACE"
            instruction_surface = self.font.render(instruction_text, True, BLACK)
            self.screen.blit(instruction_surface, (WIDTH - 170, HEIGHT - 40))