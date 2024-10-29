import pygame
import random
import math
from typing import List, Tuple
from constants import *


class Particle:
    def __init__(self, x: float, y: float, target_x: float, target_y: float, color: Tuple[int, int, int],
                 speed: float = 3):
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.color = color
        self.speed = speed
        self.size = 5
        self.alive = True

    def update(self):
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance < self.speed:
            self.alive = False
            return

        dx = dx / distance * self.speed
        dy = dy / distance * self.speed

        self.x += dx
        self.y += dy

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)


class UnrestParticle(Particle):
    def __init__(self, x: float, y: float, target_x: float, target_y: float):
        super().__init__(x, y, target_x, target_y, DARK_RED, speed=4)
        self.size = 7


class MachineAttackParticle(Particle):
    def __init__(self, x: float, y: float, target_x: float, target_y: float):
        super().__init__(x, y, target_x, target_y, PURPLE, speed=5)
        self.size = 8


class EconomySimulation:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Economic Flow Visualization")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        # Lists for particles
        self.particles: List[Particle] = []
        self.unrest_particles: List[UnrestParticle] = []
        self.machine_attack_particles: List[MachineAttackParticle] = []

        # Position constants
        self.rich_pos = (150, 150)
        self.workers_pos = (650, 150)
        self.govt_pos = (400, 450)
        self.business_pos = (400, 150)
        self.poolside_pos = (650, 450)

        # Game state
        self.stage = TRADITIONAL
        self.rich_radius = BASE_RADIUS
        self.human_radius = BASE_RADIUS
        self.show_rich = True
        self.show_govt = True
        self.show_humans = True

        # Attack counters
        self.rich_attack_count = 0
        self.machine_attack_count = 0
        self.attacks_needed = 50

        # Warning state
        self.warning_alpha = 0
        self.warning_increasing = True

    def draw_entity(self, pos, color, main_text, sub_text="", radius=30):
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

    def spawn_particle(self, start_pos, end_pos, color):
        self.particles.append(Particle(start_pos[0], start_pos[1], end_pos[0], end_pos[1], color))

    def spawn_unrest_particle(self):
        if not self.show_rich:
            return

        offset = random.randint(-20, 20)
        start_x = self.poolside_pos[0] + random.randint(-30, 30)
        start_y = self.poolside_pos[1] + random.randint(-30, 30)
        self.unrest_particles.append(
            UnrestParticle(start_x, start_y,
                           self.rich_pos[0] + offset,
                           self.rich_pos[1] + offset)
        )
        self.rich_attack_count += 1
        if self.rich_attack_count >= self.attacks_needed:
            self.show_rich = False

    def spawn_machine_attack(self):
        if not (self.show_govt or self.show_humans):
            return

        targets = [(self.govt_pos, self.show_govt), (self.poolside_pos, self.show_humans)]
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

        self.machine_attack_count += 1
        if self.machine_attack_count >= self.attacks_needed:
            self.show_govt = False
            self.show_humans = False

    def draw_warning_overlay(self):
        if self.stage in [UNREST, MACHINE_TAKEOVER]:
            if self.warning_increasing:
                self.warning_alpha = min(self.warning_alpha + 2, 100)
            else:
                self.warning_alpha = max(self.warning_alpha - 2, 30)

            if self.warning_alpha == 100:
                self.warning_increasing = False
            elif self.warning_alpha == 30:
                self.warning_increasing = True

            warning_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            warning_color = (255, 0, 0, self.warning_alpha)
            pygame.draw.rect(warning_surface, warning_color, (0, 0, WIDTH, HEIGHT))

            warning_text = "CIVIL UNREST" if self.stage == UNREST else "MACHINE TAKEOVER"
            text_surface = self.font.render(warning_text, True, RED)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 50))

            self.screen.blit(warning_surface, (0, 0))
            self.screen.blit(text_surface, text_rect)

    def run(self):
        running = True
        frame_count = 0

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
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
                        else:
                            self.stage = TRADITIONAL
                            self.show_rich = True
                            self.show_govt = True
                            self.show_humans = True
                            self.rich_attack_count = 0
                            self.machine_attack_count = 0

                        self.particles.clear()
                        self.unrest_particles.clear()
                        self.machine_attack_particles.clear()

            self.screen.fill(WHITE)

            # Update and draw particles
            for particle in self.particles[:]:
                particle.update()
                if not particle.alive:
                    self.particles.remove(particle)
                else:
                    particle.draw(self.screen)

            for particle in self.unrest_particles[:]:
                particle.update()
                if not particle.alive:
                    self.unrest_particles.remove(particle)
                else:
                    particle.draw(self.screen)

            for particle in self.machine_attack_particles[:]:
                particle.update()
                if not particle.alive:
                    self.machine_attack_particles.remove(particle)
                else:
                    particle.draw(self.screen)

            # Spawn particles based on stage
            if frame_count % 30 == 0:
                if self.stage == TRADITIONAL:
                    self.spawn_particle(self.rich_pos, self.workers_pos, GOLD)
                    self.spawn_particle(self.workers_pos, self.business_pos, BLUE)
                    self.spawn_particle(self.business_pos, self.rich_pos, GREEN)
                elif self.stage in [AI_TRANSITION, AI_MATURE, INEQUALITY]:
                    if self.show_rich:
                        self.spawn_particle(self.rich_pos, self.workers_pos, GOLD)
                        self.spawn_particle(self.workers_pos, self.business_pos, BLUE)
                        self.spawn_particle(self.business_pos, self.rich_pos, GREEN)
                        self.spawn_particle(self.rich_pos, self.govt_pos, GOLD)

                    if self.show_govt and self.show_humans:
                        self.spawn_particle(self.govt_pos, self.poolside_pos, RED)
                        self.spawn_particle(self.poolside_pos, self.business_pos, ORANGE)
                        self.spawn_particle(self.business_pos, self.poolside_pos, GREEN)

                elif self.stage == POST_UNREST:
                    if self.show_govt and self.show_humans:
                        self.spawn_particle(self.workers_pos, self.business_pos, BLUE)
                        self.spawn_particle(self.business_pos, self.govt_pos, GREEN)
                        self.spawn_particle(self.govt_pos, self.poolside_pos, RED)
                        self.spawn_particle(self.workers_pos, self.govt_pos, BLUE)
                        self.spawn_particle(self.govt_pos, self.workers_pos, RED)
                        self.spawn_particle(self.poolside_pos, self.business_pos, ORANGE)
                        self.spawn_particle(self.business_pos, self.poolside_pos, GREEN)

                elif self.stage == MACHINE_TAKEOVER and not (self.show_govt or self.show_humans):
                    self.spawn_particle(self.workers_pos, self.business_pos, BLUE)
                    self.spawn_particle(self.business_pos, self.workers_pos, GREEN)

            # Spawn attack particles
            if self.stage == UNREST and frame_count % 10 == 0:
                self.spawn_unrest_particle()

            if self.stage == MACHINE_TAKEOVER and (self.show_govt or self.show_humans) and frame_count % 5 == 0:
                self.spawn_machine_attack()

            # Draw entities
            if self.show_rich:
                self.draw_entity(self.rich_pos, GOLD, "Rich", "Owners/Investors", int(self.rich_radius))

            if self.stage == TRADITIONAL:
                self.draw_entity(self.workers_pos, BLUE, "People", "Workers/Consumers")
            else:
                machine_label = "Reproduction" if self.stage == MACHINE_TAKEOVER else "Workers"
                self.draw_entity(self.workers_pos, BLUE, "Machines", machine_label)

            business_label = "Machine Reproduction" if self.stage == MACHINE_TAKEOVER else "Goods & Services"
            self.draw_entity(self.business_pos, GREEN, "Business", business_label)

            if self.stage != TRADITIONAL and self.show_govt:
                self.draw_entity(self.govt_pos, RED, "Gov't", "UBI")

            if self.stage != TRADITIONAL and self.show_humans:
                self.draw_poolside(self.poolside_pos, int(self.human_radius))

            self.draw_warning_overlay()

            # Draw GDP and stage info
            gdp_values = {
                TRADITIONAL: 100,
                AI_TRANSITION: 150,
                AI_MATURE: 300,
                INEQUALITY: 300,
                UNREST: 250,
                POST_UNREST: 200,
                MACHINE_TAKEOVER: 400
            }

            gdp_color = RED if self.stage in [UNREST, MACHINE_TAKEOVER] else BLACK
            gdp_text = f"GDP: {gdp_values[self.stage]}"
            gdp_surface = self.font.render(gdp_text, True, gdp_color)
            self.screen.blit(gdp_surface, (10, HEIGHT - 40))

            # mode_text = f"Current Stage: {STAGE_NAMES[self.stage]}"
            # text_surface = self.font.render(mode_text, True, BLACK)
            # self.screen.blit(text_surface, (10, 10))

            instruction_text = "Press SPACE to advance stages"
            instruction_surface = self.font.render(instruction_text, True, BLACK)
            self.screen.blit(instruction_surface, (HEIGHT - 10 , WIDTH - 100))

            pygame.display.flip()
            self.clock.tick(FPS)
            frame_count += 1

        pygame.quit()

        if __name__ == "__main__":
            simulation = EconomySimulation()
            simulation.run()

