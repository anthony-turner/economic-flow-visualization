# stage_manager.py
from constants import *


class StageManager:
    def __init__(self):
        # Base circle sizes
        self.base_rich_radius = BASE_RADIUS
        self.base_human_radius = BASE_RADIUS
        self.rich_radius = BASE_RADIUS
        self.human_radius = BASE_RADIUS

        # Current stage and visibility flags
        self.stage = TRADITIONAL
        self.show_rich = True
        self.show_govt = True
        self.show_humans = True

        # Attack tracking
        self.rich_attack_count = 0
        self.machine_attack_count = 0
        self.attacks_needed = 50

        # Warning overlay state
        self.warning_alpha = 0
        self.warning_increasing = True

        # End sequence timer
        self.end_sequence_timer = 0

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


    def reset(self):
        self.stage = TRADITIONAL
        self.show_rich = True
        self.show_govt = True
        self.show_humans = True
        self.rich_attack_count = 0
        self.machine_attack_count = 0
        self.end_sequence_timer = 0

    def update_warning(self):
        if self.warning_increasing:
            self.warning_alpha = min(self.warning_alpha + 2, 100)
        else:
            self.warning_alpha = max(self.warning_alpha - 2, 30)

        if self.warning_alpha == 100:
            self.warning_increasing = False
        elif self.warning_alpha == 30:
            self.warning_increasing = True

    def handle_rich_attack(self):
        self.rich_attack_count += 1
        if self.rich_attack_count >= self.attacks_needed:
            self.show_rich = False

    def handle_machine_attack(self):
        self.machine_attack_count += 1
        if self.machine_attack_count >= self.attacks_needed:
            self.show_govt = False
            self.show_humans = False

    def advance_stage(self):
        """Advances to the next stage in the simulation"""
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
            self.stage = MACHINE_SURVIVAL
        elif self.stage == MACHINE_SURVIVAL:
            self.stage = MACHINE_REPLICATION
        elif self.stage == MACHINE_REPLICATION:
            self.stage = AI_ALIGNMENT
        elif self.stage == AI_ALIGNMENT:
            self.stage = END_STATE
        else:
            self.reset()

        self.end_sequence_timer = 0
        self.update_circle_sizes()