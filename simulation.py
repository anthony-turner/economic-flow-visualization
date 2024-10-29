# simulation.py
import pygame
from constants import *
from particles import Particle, UnrestParticle, MachineAttackParticle
from entity import Entity
from stage_manager import StageManager
from ui_manager import UIManager
from end_sequence import EndSequenceManager
import random


class EconomySimulation:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Economic Flow Visualization")
        self.clock = pygame.time.Clock()

        # Initialize fonts
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.tiny_font = pygame.font.Font(None, 16)
        self.big_font = pygame.font.Font(None, 48)

        # Initialize managers
        self.entity = Entity(self.screen, self.font, self.small_font)
        self.stage_manager = StageManager()
        self.ui_manager = UIManager(self.screen, self.font, self.small_font, self.big_font)
        self.end_sequence = EndSequenceManager(self.screen, self.font, self.big_font)

        # Lists for particles
        self.particles = []
        self.unrest_particles = []
        self.machine_attack_particles = []

        # Position constants
        self.rich_pos = (150, 150)
        self.workers_pos = (650, 150)
        self.govt_pos = (400, 450)
        self.business_pos = (400, 150)
        self.poolside_pos = (650, 450)

    def is_attack_in_progress(self):
        """Check if an attack sequence is currently in progress or if we're in end sequence"""
        # Check for civil unrest attack on rich
        if self.stage_manager.stage == UNREST and self.stage_manager.show_rich:
            return True

        # Check for machine attack on govt and humans
        if (self.stage_manager.stage == MACHINE_TAKEOVER and
                (self.stage_manager.show_govt or self.stage_manager.show_humans)):
            return True

        # Prevent space bar during end sequences
        if self.stage_manager.stage in [MACHINE_SURVIVAL, MACHINE_REPLICATION,
                                        AI_ALIGNMENT, END_STATE]:
            return True

        return False

    def spawn_particle(self, start_pos, end_pos, color):
        self.particles.append(Particle(start_pos[0], start_pos[1], end_pos[0], end_pos[1], color))

    def _spawn_stage_particles(self):
        sm = self.stage_manager

        if sm.stage == TRADITIONAL:
            self.spawn_particle(self.rich_pos, self.workers_pos, GOLD)
            self.spawn_particle(self.workers_pos, self.business_pos, BLUE)
            self.spawn_particle(self.business_pos, self.rich_pos, GREEN)

        elif sm.stage in [AI_TRANSITION, AI_MATURE, INEQUALITY]:
            if sm.show_rich:
                self.spawn_particle(self.rich_pos, self.workers_pos, GOLD)
                self.spawn_particle(self.workers_pos, self.business_pos, BLUE)
                self.spawn_particle(self.business_pos, self.rich_pos, GREEN)
                self.spawn_particle(self.rich_pos, self.govt_pos, GOLD)

            if sm.show_govt and sm.show_humans:
                self.spawn_particle(self.govt_pos, self.poolside_pos, RED)
                self.spawn_particle(self.poolside_pos, self.business_pos, ORANGE)
                self.spawn_particle(self.business_pos, self.poolside_pos, GREEN)

        elif sm.stage == POST_UNREST:
            if sm.show_govt and sm.show_humans:
                self.spawn_particle(self.workers_pos, self.business_pos, BLUE)
                self.spawn_particle(self.business_pos, self.govt_pos, GREEN)
                self.spawn_particle(self.govt_pos, self.poolside_pos, RED)
                self.spawn_particle(self.workers_pos, self.govt_pos, BLUE)
                self.spawn_particle(self.govt_pos, self.workers_pos, RED)
                self.spawn_particle(self.poolside_pos, self.business_pos, ORANGE)
                self.spawn_particle(self.business_pos, self.poolside_pos, GREEN)

        elif sm.stage == MACHINE_TAKEOVER and not (sm.show_govt or sm.show_humans):
            self.spawn_particle(self.workers_pos, self.business_pos, BLUE)
            self.spawn_particle(self.business_pos, self.workers_pos, GREEN)

    def _spawn_unrest_particles(self):
        if not self.stage_manager.show_rich:
            return

        offset = random.randint(-20, 20)
        start_x = self.poolside_pos[0] + random.randint(-30, 30)
        start_y = self.poolside_pos[1] + random.randint(-30, 30)

        self.unrest_particles.append(
            UnrestParticle(start_x, start_y,
                           self.rich_pos[0] + offset,
                           self.rich_pos[1] + offset)
        )
        self.stage_manager.handle_rich_attack()

    def _spawn_machine_attack(self):
        if not (self.stage_manager.show_govt or self.stage_manager.show_humans):
            return

        targets = [(self.govt_pos, self.stage_manager.show_govt),
                   (self.poolside_pos, self.stage_manager.show_humans)]

        for target_pos, is_visible in targets:
            if is_visible:
                offset_x = random.randint(-30, 30)
                offset_y = random.randint(-30, 30)
                start_x = self.workers_pos[0] + random.randint(-20, 20)
                start_y = self.workers_pos[1] + random.randint(-20, 20)

                self.machine_attack_particles.append(
                    MachineAttackParticle(start_x, start_y,
                                          target_pos[0] + offset_x,
                                          target_pos[1] + offset_y)
                )

        self.stage_manager.handle_machine_attack()

    def draw_credits(self):
        """Draw tiny credits at the bottom of the screen"""
        if self.stage_manager.stage == END_STATE:
            credit_text = "Created with Claude 3.5 Sonnet | WarGames (1983)"
            credit_surface = self.tiny_font.render(credit_text, True, BLACK)
            credit_rect = credit_surface.get_rect(center=(WIDTH // 2, HEIGHT - 10))
            self.screen.blit(credit_surface, credit_rect)

    def _draw_entities(self):
        sm = self.stage_manager
        if sm.show_rich:
            self.entity.draw_circle(self.rich_pos, GOLD, "Rich", "Owners/Investors",
                                    int(sm.rich_radius))

        if sm.stage == TRADITIONAL:
            self.entity.draw_circle(self.workers_pos, BLUE, "People", "Workers/Consumers")
        else:
            machine_label = "Reproduction" if sm.stage == MACHINE_TAKEOVER else "Workers"
            self.entity.draw_circle(self.workers_pos, BLUE, "Machines", machine_label)

        business_label = "Machine Reproduction" if sm.stage == MACHINE_TAKEOVER else "Goods & Services"
        self.entity.draw_circle(self.business_pos, GREEN, "Business", business_label)

        if sm.stage != TRADITIONAL and sm.show_govt:
            self.entity.draw_circle(self.govt_pos, RED, "Gov't", "UBI")

        if sm.stage != TRADITIONAL and sm.show_humans:
            self.entity.draw_poolside(self.poolside_pos, int(sm.human_radius))

    def handle_particles(self):
        for particle_list in [self.particles, self.unrest_particles, self.machine_attack_particles]:
            for particle in particle_list[:]:
                particle.update()
                if not particle.alive:
                    particle_list.remove(particle)
                else:
                    particle.draw(self.screen)

    def spawn_particles(self, frame_count):
        sm = self.stage_manager
        if frame_count % 30 == 0 and sm.stage not in [AI_ALIGNMENT, END_STATE,
                                                      MACHINE_SURVIVAL, MACHINE_REPLICATION]:
            self._spawn_stage_particles()

        if sm.stage == UNREST and frame_count % 10 == 0:
            self._spawn_unrest_particles()

        if sm.stage == MACHINE_TAKEOVER and frame_count % 5 == 0:
            self._spawn_machine_attack()

    def draw(self):
        sm = self.stage_manager

        if sm.stage in [MACHINE_SURVIVAL, MACHINE_REPLICATION]:
            self.end_sequence.draw(sm.stage, self.business_pos, self.workers_pos)
        elif sm.stage in [AI_ALIGNMENT, END_STATE]:
            self.end_sequence.draw(sm.stage, None, None)
        elif sm.stage not in [AI_ALIGNMENT, END_STATE]:
            self._draw_entities()

        self.ui_manager.draw_warning_overlay(sm.stage, sm.warning_alpha)
        self.ui_manager.draw_info(sm.stage)

        # Draw credits if in end state
        if sm.stage == END_STATE:
            self.draw_credits()

    def run(self):
        running = True
        frame_count = 0

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Only allow space bar control before end sequence
                        if not self.is_attack_in_progress() and self.stage_manager.stage not in [
                            MACHINE_SURVIVAL, MACHINE_REPLICATION, AI_ALIGNMENT, END_STATE
                        ]:
                            self.stage_manager.advance_stage()  # Use stage manager's advance_stage method
                            self.end_sequence.reset_timer()
                            self.particles.clear()
                            self.unrest_particles.clear()
                            self.machine_attack_particles.clear()

            self.screen.fill(WHITE)

            # Handle automatic transitions
            if self.stage_manager.stage == MACHINE_SURVIVAL:
                if self.end_sequence.check_phase_complete(self.stage_manager.stage):
                    self.stage_manager.stage = MACHINE_REPLICATION
                    self.end_sequence.reset_timer()
            elif self.stage_manager.stage == MACHINE_REPLICATION:
                if self.end_sequence.check_phase_complete(self.stage_manager.stage):
                    self.stage_manager.stage = AI_ALIGNMENT
                    self.end_sequence.reset_timer()
            elif self.stage_manager.stage == AI_ALIGNMENT:
                if self.end_sequence.check_phase_complete(self.stage_manager.stage):
                    self.stage_manager.stage = END_STATE
                    self.end_sequence.reset_timer()

            self.handle_particles()
            self.spawn_particles(frame_count)
            self.draw()

            pygame.display.flip()
            self.clock.tick(FPS)
            frame_count += 1

        pygame.quit()