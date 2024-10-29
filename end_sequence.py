# end_sequence.py
import pygame
import random
import math
from constants import *

import pygame
import random
import math
from constants import *


class EndSequenceManager:
    def __init__(self, screen, font, big_font):
        self.screen = screen
        self.font = font
        self.big_font = big_font
        self.timer = 0
        self.phase = 0
        self.machine_positions = []
        self.active_machines = 0
        self.max_machines = 600  # Increased for more coverage
        self.replication_complete = False
        self._generate_machine_positions()
        self.survival_timer = 0
        self.replication_timer = 0

    def draw(self, stage, business_pos, workers_pos):
        """Main draw method to coordinate all end sequence phases"""
        if stage == MACHINE_SURVIVAL:
            self._draw_survival_phase(business_pos, workers_pos)
        elif stage == MACHINE_REPLICATION:
            self._draw_replication_phase(business_pos, workers_pos)
        elif stage == AI_ALIGNMENT:
            self._draw_alignment_phase()
        elif stage == END_STATE:
            self._draw_end_phase()

    def _generate_machine_positions(self):
        """Generate random positions for machine replications"""
        self.machine_positions = []
        margin = 20  # Reduced margin for more coverage
        rows = 30  # Increased grid density
        cols = 30  # Increased grid density
        spacing_x = (WIDTH - 2 * margin) / cols
        spacing_y = (HEIGHT - 2 * margin) / rows

        # Generate grid-based positions with random offsets
        for i in range(rows * cols):
            row = i // cols
            col = i % cols
            x = margin + col * spacing_x + random.randint(-5, 5)
            y = margin + row * spacing_y + random.randint(-5, 5)
            self.machine_positions.append((int(x), int(y)))

        # Add some completely random positions for more organic feel
        for _ in range(100):  # Additional random positions
            x = random.randint(margin, WIDTH - margin)
            y = random.randint(margin, HEIGHT - margin)
            self.machine_positions.append((int(x), int(y)))

        # Shuffle positions for more random appearance
        random.shuffle(self.machine_positions)

    def _draw_survival_phase(self, business_pos, workers_pos):
        # Draw just the two main circles connected by a clean line
        # pygame.draw.line(self.screen, BLUE, business_pos, workers_pos, 2)
        pygame.draw.circle(self.screen, BLUE, business_pos, SMALL_RADIUS)
        pygame.draw.circle(self.screen, BLUE, workers_pos, SMALL_RADIUS)

        # Draw machine survival text
        text_surface = self.font.render("Machine Survival", True, BLACK)
        text_rect = text_surface.get_rect(center=(business_pos[0], business_pos[1] + 40))
        self.screen.blit(text_surface, text_rect)
        #
        # # Draw machine replication text
        # machine_text = "Machine Replication"
        # text_surface = self.font.render(machine_text, True, BLACK)
        # text_rect = text_surface.get_rect(center=(workers_pos[0], workers_pos[1] + 40))
        # self.screen.blit(text_surface, text_rect)

    def _draw_replication_phase(self, business_pos, workers_pos):
        # Draw main machines and connection
        pygame.draw.circle(self.screen, BLUE, business_pos, SMALL_RADIUS)
        pygame.draw.circle(self.screen, BLUE, workers_pos, SMALL_RADIUS)
        # pygame.draw.line(self.screen, BLUE, business_pos, workers_pos, 2)

        # Calculate how many machines should be active based on timer
        self.timer += 1
        if self.timer % 8 == 0:  # Fast replication
            if self.active_machines == 0:
                self.active_machines = 10  # Start with 2 machines
            else:
                new_machines = min(int(self.active_machines * 1.4) + 2, self.max_machines)
                self.active_machines = new_machines

        # Draw active machines with fade-in effect
        for i in range(self.active_machines):
            alpha = min(255, (self.timer - (i * 2)) * 15)  # Fast fade-in
            if alpha > 0:
                pos = self.machine_positions[i]
                circle_surface = pygame.Surface((SMALL_RADIUS * 2 + 2, SMALL_RADIUS * 2 + 2), pygame.SRCALPHA)
                pygame.draw.circle(circle_surface, (*BLUE[:3], alpha),
                                   (SMALL_RADIUS + 1, SMALL_RADIUS + 1), SMALL_RADIUS)
                self.screen.blit(circle_surface,
                                 (pos[0] - SMALL_RADIUS - 1, pos[1] - SMALL_RADIUS - 1))

        # Draw texts
        text_surface = self.font.render("Machine Survival", True, BLACK)
        text_rect = text_surface.get_rect(center=(business_pos[0], business_pos[1] + 40))
        self.screen.blit(text_surface, text_rect)

        machine_text = "Machine Replication"
        text_surface = self.font.render(machine_text, True, BLACK)
        text_rect = text_surface.get_rect(center=(workers_pos[0], workers_pos[1] + 40))
        self.screen.blit(text_surface, text_rect)


    def _draw_alignment_phase(self):
        # Calculate fade out effect for machines
        machine_alpha = 255
        text_alpha = 0

        if self.replication_timer >= 120:  # After 2 seconds of full coverage
            fade_progress = min(60, self.replication_timer - 120)
            machine_alpha = max(0, 255 - (fade_progress * 4.25))
            text_alpha = min(255, fade_progress * 4.25)

        # Draw machines with fade out
        if machine_alpha > 0:
            for pos in self.machine_positions:
                circle_surface = pygame.Surface((SMALL_RADIUS * 2 + 2, SMALL_RADIUS * 2 + 2), pygame.SRCALPHA)
                pygame.draw.circle(circle_surface, (*BLUE[:3], machine_alpha),
                                   (SMALL_RADIUS + 1, SMALL_RADIUS + 1), SMALL_RADIUS)
                self.screen.blit(circle_surface,
                                 (pos[0] - SMALL_RADIUS - 1, pos[1] - SMALL_RADIUS - 1))

        # Only start drawing text after machines start fading
        if text_alpha > 0:
            subtitle_timer = self.replication_timer - 180  # Start subtitle timer after fade

            if subtitle_timer > 0 and subtitle_timer <= 360:  # First 4 seconds
                # First subtitle
                subtitle1 = "The only winning move is not to play"
                sub1_surface = self.big_font.render(subtitle1, True, BLACK)
                sub1_alpha = min(255, subtitle_timer * 8)
                sub1_surface.set_alpha(sub1_alpha)
                sub1_rect = sub1_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
                self.screen.blit(sub1_surface, sub1_rect)

            elif subtitle_timer > 240:  # After 4 seconds
                fade_in = min(255, (subtitle_timer - 240) * 4)

                # Header text
                header = "Shared Responsibility"
                header_surface = self.big_font.render(header, True, BLACK)
                header_surface.set_alpha(fade_in)
                header_rect = header_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
                self.screen.blit(header_surface, header_rect)

                # AI Alignment text
                align_text = "AI Alignment"
                align_surface = self.font.render(align_text, True, BLACK)
                align_surface.set_alpha(fade_in)

                align_rect = align_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80 ))
                self.screen.blit(align_surface, align_rect)

                # No Kill Switch
                planning_text = "No Kill Switch as 95% of labour"
                planning_surface = self.font.render(planning_text, True, BLACK)
                planning_surface.set_alpha(fade_in)
                planning_rect = planning_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
                self.screen.blit(planning_surface, planning_rect)

                # Planning text
                planning_text = "Planning for Social Change"
                planning_surface = self.font.render(planning_text, True, BLACK)
                planning_surface.set_alpha(fade_in)
                planning_rect = planning_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
                self.screen.blit(planning_surface, planning_rect)

        self.replication_timer += 1

    def _draw_end_phase(self):
        # Draw background machines faded
        for pos in self.machine_positions:
            circle_surface = pygame.Surface((SMALL_RADIUS * 2 + 2, SMALL_RADIUS * 2 + 2), pygame.SRCALPHA)
            pygame.draw.circle(circle_surface, (*BLUE[:3], 30),
                               (SMALL_RADIUS + 1, SMALL_RADIUS + 1), SMALL_RADIUS)
            self.screen.blit(circle_surface,
                             (pos[0] - SMALL_RADIUS - 1, pos[1] - SMALL_RADIUS - 1))

        # Main title
        title = "THE END"
        title_surface = self.big_font.render(title, True, BLACK)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(title_surface, title_rect)

    def check_phase_complete(self, stage):
        """Check if current phase should transition to next"""
        if stage == MACHINE_SURVIVAL:
            self.survival_timer += 1
            return self.survival_timer >= SURVIVAL_TEXT_DELAY
        elif stage == MACHINE_REPLICATION:
            self.replication_timer += 1
            if self.active_machines >= self.max_machines - 5:
                return self.replication_timer >= 180  # 3 seconds after full coverage
            return False
        elif stage == AI_ALIGNMENT:
            return self.timer >= ALIGNMENT_TEXT_DELAY + FINAL_TEXT_DELAY + 360  # Extended for full sequence
        return False

    def reset_timer(self):
        """Reset all timers and counters"""
        self.timer = 0
        self.survival_timer = 0
        self.replication_timer = 0
        self.active_machines = 0
        self.replication_complete = False
        self._generate_machine_positions()