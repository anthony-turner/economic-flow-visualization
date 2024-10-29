# constants.py
# Window Constants
WIDTH = 800
HEIGHT = 800
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
BLUE = (0, 100, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
DARK_RED = (139, 0, 0)
PURPLE = (128, 0, 128)

# Base configuration
BASE_RADIUS = 30
SMALL_RADIUS = 10
TRANSITION_SPEED = 0.1
ATTACK_COMPLETION_DELAY = 1000
FINAL_DISPLAY_TIME = 10000

# Economic stages
TRADITIONAL = "traditional"
AI_TRANSITION = "ai_transition"
AI_MATURE = "ai_mature"
INEQUALITY = "inequality"
UNREST = "unrest"
POST_UNREST = "post_unrest"
MACHINE_TAKEOVER = "machine_takeover"
MACHINE_SURVIVAL = "machine_survival"
MACHINE_REPLICATION = "machine_replication"
AI_ALIGNMENT = "ai_alignment"
END_STATE = "end_state"

# Stage timing (in frames)
SURVIVAL_TEXT_DELAY = 180  # 3 seconds at 60 FPS
ALIGNMENT_TEXT_DELAY = 240  # 4 seconds
FINAL_TEXT_DELAY = 220     # 4 seconds

# Stage names for display
STAGE_NAMES = {
    TRADITIONAL: "Traditional Economy",
    AI_TRANSITION: "AI Transition (Balanced)",
    AI_MATURE: "Mature AI Economy",
    INEQUALITY: "Growing Inequality",
    UNREST: "Civil Unrest",
    POST_UNREST: "Post-Unrest Reorganization",
    MACHINE_TAKEOVER: "Machine Dominance",
    MACHINE_SURVIVAL: "Machine Survival",
    MACHINE_REPLICATION: "Machine Replication",
    AI_ALIGNMENT: "AI Alignment",
    END_STATE: "THE END"
}