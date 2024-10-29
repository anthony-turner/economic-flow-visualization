# particles.py
import math
import pygame
from constants import DARK_RED, PURPLE  # Import needed color constants

class Particle:
    def __init__(self, x: float, y: float, target_x: float, target_y: float, color, speed: float = 3):
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