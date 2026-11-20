

import pygame
import sys
import math
import os
import random
import subprocess

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Get screen info and set to full screen
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Robotdog Assembly Lab - Level 3")

# ==============================================
# ROBOTDOG IMAGE FUNCTIONS (AUTO-INSERTED FIX)
# ==============================================

# ==============================================
# ROBOTDOG IMAGE FUNCTIONS (AUTO-INSERTED FIX)
# ==============================================

SHOW_ROBOTDOG_IMAGE = True
ROBOTDOG_IMAGE_RECT = pygame.Rect(SCREEN_WIDTH - 320, 290, 350, 250)  # MOVED DOWN from 90 to 290
robotdog_image = None

def load_robotdog_image():
    try:
        img_path = r"C:\Users\musta\PycharmProjects\PythonProject1\robotdog.png"
        if os.path.exists(img_path):
            img = pygame.image.load(img_path).convert_alpha()
            return pygame.transform.scale(img, (350, 250))
        else:
            print("Robotdog image not found:", img_path)
    except Exception as e:
        print("Error loading robotdog image:", e)
    return None

def draw_robotdog_image(surface):
    if SHOW_ROBOTDOG_IMAGE and robotdog_image:
        surface.blit(robotdog_image, ROBOTDOG_IMAGE_RECT)

# Load the robotdog image after defining the function
robotdog_image = load_robotdog_image()

# Colors
BACKGROUND = (15, 20, 35)
PANEL_BG = (25, 30, 45, 200)
NEON_RED = (255, 50, 50)
NEON_GREEN = (50, 255, 100)
NEON_BLUE = (50, 150, 255)
NEON_PURPLE = (180, 50, 255)
NEON_CYAN = (50, 255, 255)
NEON_YELLOW = (255, 255, 50)
NEON_ORANGE = (255, 150, 50)
HOLO_BLUE = (100, 200, 255)
HOLO_PINK = (255, 100, 200)
HOLO_GREEN = (100, 255, 200)
WHITE = (240, 240, 240)
GRAY = (120, 120, 120)
DARK_GRAY = (60, 60, 70)
METAL_GRAY = (100, 110, 120)
BLACK = (20, 20, 20)
SILVER = (200, 200, 210)
GOLD = (212, 175, 55)
CYBER_YELLOW = (255, 220, 50)
CYBER_BLUE = (50, 100, 255)

# NEW: Radar colors (changed for rectangular radar)
RADAR_BG = (20, 25, 40, 220)
RADAR_GRID = (40, 45, 60, 120)
RADAR_SCAN = (0, 200, 255, 180)
RADAR_ENEMY = (255, 50, 50, 200)
RADAR_PART = (50, 255, 100, 200)
RADAR_HOLE = (255, 150, 50, 200)
RADAR_PLAYER = (100, 200, 255, 255)

# NEW: Color gradient for collected parts
PART_COLOR_GRADIENTS = {
    "circuit": [(50, 150, 255), (180, 50, 255), (255, 50, 150)],  # Blue -> Purple -> Pink
    "chip": [(50, 255, 100), (255, 255, 50), (255, 100, 50)],  # Green -> Yellow -> Orange
    "battery": [(255, 255, 50), (255, 150, 50), (255, 50, 50)],  # Yellow -> Orange -> Red
    "sensor": [(100, 200, 255), (50, 100, 255), (255, 50, 150)]  # Light Blue -> Blue -> Pink
}

# NEW: Load sound effects and music
try:
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Load background music
    background_music = pygame.mixer.Sound(os.path.join(script_dir, "Level 3.mp3"))

    # Load sound effects
    win_sound = pygame.mixer.Sound(os.path.join(script_dir, "Win.mp3"))
    lose_sound = pygame.mixer.Sound(os.path.join(script_dir, "Lose.mp3"))

    # Try to load jump and collect sounds, but handle if they don't exist
    try:
        jump_sound = pygame.mixer.Sound(os.path.join(script_dir, "jump.mp3"))
    except:
        print("Jump sound not found, using placeholder")
        jump_sound = lose_sound  # Use lose sound as placeholder

    try:
        collect_sound = pygame.mixer.Sound(os.path.join(script_dir, "collect.mp3"))
    except:
        print("Collect sound not found, using win sound as placeholder")
        collect_sound = win_sound  # Use win sound as placeholder

    # Set volume for sounds
    background_music.set_volume(0.7)
    win_sound.set_volume(0.8)
    lose_sound.set_volume(0.8)
    jump_sound.set_volume(0.6)
    collect_sound.set_volume(0.5)

    # Flag to track if background music is playing
    background_music_playing = False

except Exception as e:
    print(f"Error loading sound files: {e}")
    # Create dummy sound objects to avoid errors
    background_music = None
    win_sound = None
    lose_sound = None
    jump_sound = None
    collect_sound = None
    background_music_playing = False



# Performance optimization constants
MAX_PARTICLES = 150
MAX_LASERS = 20
MAX_GLITCHES = 10
DRAG_SPEED_MULTIPLIER = 1.0

# NEW: Pause state and buttons
PAUSED = False
ESCAPE_BUTTON = pygame.Rect(20, 30, 150, 40)
PAUSE_BUTTON = pygame.Rect(20, 80, 150, 40)

# Pause menu buttons
RESUME_BUTTON = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 60)
MAIN_MENU_BUTTON = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 60)

# Victory display variables
VICTORY_DISPLAY_TIME = 0
victory_scale = 1.0
victory_pulse = 0.0
victory_glow = 0.0
victory_sparks = []

# NEW: Radar variables (changed to rectangular)
RADAR_POS = (SCREEN_WIDTH - 280, 320)  # moved up to stack under parts  # CHANGED: Moved down below parts counter
RADAR_SIZE = (260, 160)  # unchanged size
radar_scan_angle = 0
radar_scan_speed = 0.1
radar_blips = []
radar_pulse = 0
RADAR_RANGE = 800  # Distance in pixels that radar can detect

# NEW: Part collection animation variables
COLLECTING_PARTS = []
PART_COLLECTION_DURATION = 30  # Frames for collection animation

# NEW: Robot dog color transition variables
ROBOT_DOG_BASE_COLOR = (70, 75, 85)  # Original blue-gray
ROBOT_DOG_TARGET_COLOR = (180, 60, 60)  # Target red color
robot_dog_current_color = list(ROBOT_DOG_BASE_COLOR)
color_transition_progress = 0.0
color_transition_speed = 0.02


# HSV to RGB conversion function for rainbow effects
def hsv_to_rgb(h, s, v):
    if s == 0.0:
        return (v, v, v)
    i = int(h * 6.0)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6
    if i == 0:
        return (v, t, p)
    if i == 1:
        return (q, v, p)
    if i == 2:
        return (p, v, t)
    if i == 3:
        return (p, q, v)
    if i == 4:
        return (t, p, v)
    if i == 5:
        return (v, p, q)


# NEW: Interpolate color between two colors
def interpolate_color(color1, color2, t):
    """Interpolate between two colors based on t (0-1)"""
    r = int(color1[0] + (color2[0] - color1[0]) * t)
    g = int(color1[1] + (color2[1] - color1[1]) * t)
    b = int(color1[2] + (color2[2] - color1[2]) * t)
    return (r, g, b)


# NEW: Interpolate through multiple colors
def interpolate_multiple_colors(colors, t):
    """Interpolate through multiple colors based on t (0-1)"""
    t = max(0, min(1, t))

    if len(colors) == 1:
        return colors[0]

    segment = t * (len(colors) - 1)
    segment_idx = int(segment)
    segment_t = segment - segment_idx

    if segment_idx >= len(colors) - 1:
        return colors[-1]

    return interpolate_color(colors[segment_idx], colors[segment_idx + 1], segment_t)


# Robotdog part types
PARTS = {
    "Neural Processor": {"color": NEON_PURPLE, "size": (80, 80), "radius": 5, "count": 1},
    "Quantum Battery": {"color": NEON_YELLOW, "size": (70, 100), "radius": 8, "count": 1},
    "Hydraulic Actuator": {"color": NEON_RED, "size": (60, 40), "radius": 5, "count": 8},
    "Optical Sensor": {"color": NEON_CYAN, "size": (50, 50), "radius": 25, "count": 2},
    "Audio Receiver": {"color": NEON_GREEN, "size": (40, 30), "radius": 10, "count": 2},
    "Tactile Pad": {"color": NEON_BLUE, "size": (35, 35), "radius": 15, "count": 4},
    "Balance Gyro": {"color": HOLO_BLUE, "size": (60, 60), "radius": 30, "count": 1},
    "Communication Array": {"color": HOLO_PINK, "size": (45, 70), "radius": 5, "count": 1},
    "Thermal Regulator": {"color": HOLO_GREEN, "size": (55, 55), "radius": 8, "count": 1},
    "Mobility Core": {"color": CYBER_BLUE, "size": (65, 65), "radius": 10, "count": 1}
}

# Calculate positions
center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
adjusted_center_x = center_x + 200

# Slots
SLOTS = [
    {"rect": pygame.Rect(adjusted_center_x - 20, center_y - 180, 80, 80), "type": "Neural Processor",
     "connected_to": [1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9]},
    {"rect": pygame.Rect(adjusted_center_x - 60, center_y - 250, 50, 50), "type": "Optical Sensor",
     "connected_to": [0]},
    {"rect": pygame.Rect(adjusted_center_x + 20, center_y - 250, 50, 50), "type": "Optical Sensor",
     "connected_to": [0]},
    {"rect": pygame.Rect(adjusted_center_x - 80, center_y - 200, 40, 30), "type": "Audio Receiver",
     "connected_to": [0]},
    {"rect": pygame.Rect(adjusted_center_x + 50, center_y - 200, 40, 30), "type": "Audio Receiver",
     "connected_to": [0]},
    {"rect": pygame.Rect(adjusted_center_x - 40, center_y - 80, 70, 100), "type": "Quantum Battery",
     "connected_to": [0, 6]},
    {"rect": pygame.Rect(adjusted_center_x - 35, center_y + 30, 65, 65), "type": "Mobility Core",
     "connected_to": [0, 5, 7, 8, 9]},
    {"rect": pygame.Rect(adjusted_center_x - 100, center_y - 40, 55, 55), "type": "Thermal Regulator",
     "connected_to": [0, 6]},
    {"rect": pygame.Rect(adjusted_center_x + 50, center_y - 40, 60, 60), "type": "Balance Gyro",
     "connected_to": [0, 6]},
    {"rect": pygame.Rect(adjusted_center_x - 20, center_y + 110, 45, 70), "type": "Communication Array",
     "connected_to": [0, 6]},
    {"rect": pygame.Rect(adjusted_center_x - 120, center_y - 20, 60, 40), "type": "Hydraulic Actuator",
     "connected_to": [6]},
    {"rect": pygame.Rect(adjusted_center_x - 150, center_y + 40, 60, 40), "type": "Hydraulic Actuator",
     "connected_to": [10]},
    {"rect": pygame.Rect(adjusted_center_x + 70, center_y - 20, 60, 40), "type": "Hydraulic Actuator",
     "connected_to": [6]},
    {"rect": pygame.Rect(adjusted_center_x + 100, center_y + 40, 60, 40), "type": "Hydraulic Actuator",
     "connected_to": [12]},
    {"rect": pygame.Rect(adjusted_center_x - 120, center_y + 80, 60, 40), "type": "Hydraulic Actuator",
     "connected_to": [6]},
    {"rect": pygame.Rect(adjusted_center_x - 150, center_y + 140, 60, 40), "type": "Hydraulic Actuator",
     "connected_to": [14]},
    {"rect": pygame.Rect(adjusted_center_x + 70, center_y + 80, 60, 40), "type": "Hydraulic Actuator",
     "connected_to": [6]},
    {"rect": pygame.Rect(adjusted_center_x + 100, center_y + 140, 60, 40), "type": "Hydraulic Actuator",
     "connected_to": [16]},
    {"rect": pygame.Rect(adjusted_center_x - 160, center_y + 80, 35, 35), "type": "Tactile Pad", "connected_to": [11]},
    {"rect": pygame.Rect(adjusted_center_x + 130, center_y + 80, 35, 35), "type": "Tactile Pad", "connected_to": [13]},
    {"rect": pygame.Rect(adjusted_center_x - 160, center_y + 180, 35, 35), "type": "Tactile Pad", "connected_to": [15]},
    {"rect": pygame.Rect(adjusted_center_x + 130, center_y + 180, 35, 35), "type": "Tactile Pad", "connected_to": [17]}
]

# Create parts
parts = []
part_id = 0
total_parts = sum(part_info["count"] for part_info in PARTS.values())
parts_per_column = (total_parts + 2) // 3
max_part_width = max(part_info["size"][0] for part_info in PARTS.values())
column_spacing = max_part_width + 20

for part_type, part_info in PARTS.items():
    for i in range(part_info["count"]):
        column = part_id // parts_per_column
        row = part_id % parts_per_column
        x_pos = 50 + column * column_spacing
        y_pos = 150 + row * 110
        parts.append({
            "id": part_id,
            "type": part_type,
            "rect": pygame.Rect(x_pos, y_pos, part_info["size"][0], part_info["size"][1]),
            "color": part_info["color"],
            "radius": part_info["radius"],
            "dragging": False,
            "placed": False,
            "placed_slot": None,
            "original_pos": (x_pos, y_pos)
        })
        part_id += 1

# Fonts
font = pygame.font.SysFont("Arial", 16)
title_font = pygame.font.SysFont("Arial", 36, bold=True)
small_font = pygame.font.SysFont("Arial", 14)

# Game states
LEVEL_INTRO_STATE = 0
ASSEMBLY_STATE = 1
SUCCESS_STATE = 2
TESTING_STATE = 3  # NEW: Testing state before combat
RUNNING_STATE = 4  # CHANGED: From COMBAT_STATE to RUNNING_STATE
VICTORY_STATE = 5  # NEW: Victory state before credits
CREDIT_STATE = 6  # NEW: Credit screen state

# Effects
PARTICLE_SYSTEMS = []
WIRE_ANIMATION = 0
SCORE = 0
COMBO = 0
LAST_PLACEMENT_TIME = 0
BATTERY_LEVEL = 0.5
BATTERY_DIRECTION = 1
LASER_EFFECTS = []
CYBER_GLITCHES = []

# NEW: Running state variables
ELECTRONIC_PARTS = []  # Electronic parts to collect
ENEMY_ROBOT_DOGS = []  # Small enemy robot dogs to avoid
STREET_HOLES = []  # Holes in the street to jump over
ENEMY_SPAWN_TIMER = 0
PART_SPAWN_TIMER = 0
HOLE_SPAWN_TIMER = 0
GAME_OVER = False
JUMPING = False
JUMP_VELOCITY = 0
GRAVITY = 0.7  # CHANGED: Increased from 0.5 to come down faster after high jump
JUMP_STRENGTH = -18  # CHANGED: Increased from -12 (more negative = higher jump)
GROUND_LEVEL = SCREEN_HEIGHT - 200  # Where the dog runs
TOTAL_PARTS_TO_COLLECT = 50  # Total electronic parts to collect for victory
PARTS_COLLECTED = 0  # Parts collected so far

# NEW: Health system for the robot dog
HEALTH = 3  # Robot dog has 3 health points
INVINCIBLE_TIMER = 0  # Timer for invincibility after being hit

# NEW: Enemy spawn control variables
MIN_ENEMY_SPACING = 600  # Increased spacing between obstacles for better rhythm
LAST_ENEMY_X = SCREEN_WIDTH  # X position of last spawned enemy

# NEW: Joystick variables
joystick_base_pos = (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200)
joystick_base_radius = 80
joystick_handle_pos = list(joystick_base_pos)
joystick_handle_radius = 30
joystick_dragging = False
joystick_direction = [0, 0]  # x, y direction

# NEW: Jump button variables
JUMP_BUTTON_POS = (100, SCREEN_HEIGHT - 100)
JUMP_BUTTON_RADIUS = 40
JUMP_BUTTON_COLOR = NEON_GREEN
JUMP_BUTTON_PULSE = 0

# NEW: Keyboard control variables
KEYBOARD_CONTROL = False
KEY_LEFT = False
KEY_RIGHT = False
KEY_UP = False
KEY_DOWN = False

# Cyber Canine running position
cyber_canine_x = SCREEN_WIDTH // 4
cyber_canine_y = GROUND_LEVEL - 100  # Starting position above ground
leg_animation = 0
run_cycle = 0

# Street animation variables
street_offset = 0
street_speed = 8

# NEW: Victory timer
victory_start_time = 0

# NEW: Testing state variables
testing_start_time = 0
testing_duration = 10000  # 10 seconds in milliseconds
engineer_x = SCREEN_WIDTH + 100
engineer_y = SCREEN_HEIGHT // 2
engineer_animation = 0
testing_progress = 0
testing_messages = [
    "Running diagnostics...",
    "Calibrating sensors...",
    "Optimizing neural networks...",
    "Testing hydraulic systems...",
    "Charging quantum battery...",
    "Syncing communication array...",
    "Final systems check...",
    "Cyber Canine ready for running!"
]
current_test_message = 0
message_timer = 0
engineer_angle = 0  # NEW: For circular movement around the dog
electric_spark_timer = 0  # NEW: Timer for electric spark effects

# NEW: Spawning pattern variables
SPAWN_PATTERN = ["enemy", "hole", "parts", "hole", "enemy", "hole", "parts", "hole"]  # More holes in pattern
current_pattern_index = 0
pattern_timer = 0
PATTERN_INTERVAL = 150  # Reduced from 180 (2.5 seconds at 60fps)


# NEW: Create victory spark
def create_victory_spark():
    angle = random.uniform(0, 2 * math.pi)
    distance = random.uniform(400, 600)  # Longer trails
    x = SCREEN_WIDTH // 2 + math.cos(angle) * distance
    y = SCREEN_HEIGHT // 2 + math.sin(angle) * distance

    target_x = SCREEN_WIDTH // 2 + random.uniform(-300, 300)
    target_y = SCREEN_HEIGHT // 2 - 150 + random.uniform(-100, 100)

    dx = target_x - x
    dy = target_y - y
    distance_to_target = math.sqrt(dx * dx + dy * dy)
    speed = random.uniform(10, 20)  # Faster sparks

    # Rainbow spark colors
    hue = random.uniform(0, 360)
    r, g, b = hsv_to_rgb(hue / 360, 0.9, 1.0)
    spark_color = (int(r * 255), int(g * 255), int(b * 255))

    victory_sparks.append({
        "x": x, "y": y,
        "vx": dx / distance_to_target * speed,
        "vy": dy / distance_to_target * speed,
        "color": spark_color,
        "life": 80,  # Longer life
        "max_life": 80,
        "size": random.uniform(4, 12),  # Bigger sparks
        "trail": []
    })


# NEW: Update victory sparks
def update_victory_sparks():
    for spark in victory_sparks[:]:
        spark["x"] += spark["vx"]
        spark["y"] += spark["vy"]
        spark["life"] -= 1

        # Add to trail (longer trails)
        spark["trail"].append((spark["x"], spark["y"]))
        if len(spark["trail"]) > 15:
            spark["trail"].pop(0)

        if spark["life"] <= 0:
            victory_sparks.remove(spark)


# NEW: Draw victory sparks
def draw_victory_sparks(surface):
    for spark in victory_sparks:
        # Draw trail with gradient
        for i, (trail_x, trail_y) in enumerate(spark["trail"]):
            alpha = int(255 * (i / len(spark["trail"])))
            size = spark["size"] * (i / len(spark["trail"])) * 0.7

            # Fade color through trail
            trail_color = list(spark["color"])
            if len(trail_color) == 3:
                trail_color.append(alpha)
            else:
                trail_color[3] = alpha

            trail_surf = pygame.Surface((int(size * 2), int(size * 2)), pygame.SRCALPHA)
            pygame.draw.circle(trail_surf, trail_color, (int(size), int(size)), int(size))
            surface.blit(trail_surf, (trail_x - size, trail_y - size))

        # Draw main spark with glow
        main_alpha = int(255 * (spark["life"] / spark["max_life"]))
        main_color = list(spark["color"])
        if len(main_color) == 3:
            main_color.append(main_alpha)
        else:
            main_color[3] = main_alpha

        # Spark glow
        glow_size = spark["size"] * 2
        glow_surf = pygame.Surface((int(glow_size * 2), int(glow_size * 2)), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*spark["color"][:3], main_alpha // 3),
                           (int(glow_size), int(glow_size)), int(glow_size))
        surface.blit(glow_surf, (spark["x"] - glow_size, spark["y"] - glow_size))

        # Main spark
        pygame.draw.circle(surface, main_color, (int(spark["x"]), int(spark["y"])), int(spark["size"]))


# Enhanced draw_victory function with MASSIVE neon lights
def draw_victory(surface):
    global victory_scale, victory_pulse, victory_glow

    # Update victory animation values
    victory_pulse += 0.08
    victory_glow = (math.sin(victory_pulse) + 1) / 2  # 0 to 1 pulse
    victory_scale = 1.0 + victory_glow * 0.5  # More dramatic scale pulsing

    # Create dark background with subtle animation
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))  # Semi-transparent black
    surface.blit(overlay, (0, 0))

    # Add animated starfield background
    for i in range(50):
        star_x = (i * 123) % SCREEN_WIDTH
        star_y = (i * 89) % SCREEN_HEIGHT
        star_size = 1 + (i % 3)
        star_brightness = 100 + int(155 * math.sin(pygame.time.get_ticks() / 1000 + i))
        # Ensure star_brightness is an integer between 0-255
        star_brightness = max(0, min(255, int(star_brightness)))
        pygame.draw.circle(surface, (star_brightness, star_brightness, star_brightness),
                           (int(star_x), int(star_y)), int(star_size))

    # Create MASSIVE VICTORY text - much bigger than before!
    victory_font_size = int(180 + 80 * victory_glow)  # HUGE text that pulses
    victory_font = pygame.font.SysFont("Arial", victory_font_size, bold=True)

    # Create massive glow layers - more layers for bigger effect
    for i in range(20, 0, -1):
        glow_alpha = int(40 * (i / 20) * victory_glow)
        glow_size = victory_font_size + i * 20  # Even bigger glow

        # Create glow font with rainbow effect
        glow_font = pygame.font.SysFont("Arial", glow_size, bold=True)

        # Rainbow color cycling for glow
        hue = (pygame.time.get_ticks() // 50 + i * 10) % 360
        r, g, b = hsv_to_rgb(hue / 360, 0.8, 1.0)
        glow_color = (int(r * 255), int(g * 255), int(b * 255))

        glow_text = glow_font.render("VICTORY", True, glow_color)
        glow_text.set_alpha(glow_alpha)

        glow_rect = glow_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        surface.blit(glow_text, glow_rect)

    # Main victory text with rainbow effect
    main_hue = (pygame.time.get_ticks() // 30) % 360
    r, g, b = hsv_to_rgb(main_hue / 360, 0.9, 1.0)
    main_color = (int(r * 255), int(g * 255), int(b * 255))

    victory_text = victory_font.render("VICTORY", True, main_color)
    victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))

    # Thick outline for main text
    outline_thickness = 12
    for x in range(-outline_thickness, outline_thickness + 1, 2):
        for y in range(-outline_thickness, outline_thickness + 1, 2):
            if x != 0 or y != 0:
                outline_rect = victory_rect.move(x, y)
                outline_text = victory_font.render("VICTORY", True, (0, 0, 0))
                surface.blit(outline_text, outline_rect)

    surface.blit(victory_text, victory_rect)

    # Draw victory sparks
    draw_victory_sparks(surface)

    # Draw score with massive glow
    score_font_size = 48
    score_font = pygame.font.SysFont("Arial", score_font_size, bold=True)
    score_text = score_font.render(f"FINAL SCORE: {SCORE}", True, NEON_CYAN)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

    # Score glow effect
    for i in range(10, 0, -1):
        score_glow_alpha = int(30 * (i / 10) * victory_glow)
        score_glow_size = score_font_size + i * 8

        score_glow_font = pygame.font.SysFont("Arial", score_glow_size, bold=True)
        score_glow_text = score_glow_font.render(f"FINAL SCORE: {SCORE}", True, NEON_CYAN)
        score_glow_text.set_alpha(score_glow_alpha)

        score_glow_rect = score_glow_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        surface.blit(score_glow_text, score_glow_rect)

    surface.blit(score_text, score_rect)

    # Draw parts collected
    parts_text = font.render(f"ALL {TOTAL_PARTS_TO_COLLECT} ELECTRONIC PARTS COLLECTED!", True, WHITE)
    parts_rect = parts_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))

    # Parts text glow
    parts_glow = pygame.Surface((parts_rect.width + 20, parts_rect.height + 10), pygame.SRCALPHA)
    pygame.draw.rect(parts_glow, (*NEON_GREEN, int(100 * victory_glow)),
                     (0, 0, parts_rect.width + 20, parts_rect.height + 10), border_radius=8)
    surface.blit(parts_glow, (parts_rect.x - 10, parts_rect.y - 5))
    surface.blit(parts_text, parts_rect)

    # Draw countdown to credits
    current_time = pygame.time.get_ticks()
    time_elapsed = current_time - victory_start_time
    time_left = max(0, 5000 - time_elapsed)
    seconds_left = time_left // 1000 + 1

    countdown_font = pygame.font.SysFont("Arial", 36, bold=True)
    countdown_text = countdown_font.render(f"CREDITS IN: {seconds_left}", True, NEON_YELLOW)
    countdown_rect = countdown_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 180))

    # Pulsing countdown
    pulse_alpha = int(150 + 105 * math.sin(victory_pulse * 3))
    countdown_text.set_alpha(pulse_alpha)

    # Countdown glow
    countdown_glow = pygame.Surface((countdown_rect.width + 20, countdown_rect.height + 10), pygame.SRCALPHA)
    pygame.draw.rect(countdown_glow, (*NEON_YELLOW, int(80 * victory_glow)),
                     (0, 0, countdown_rect.width + 20, countdown_rect.height + 10), border_radius=8)
    surface.blit(countdown_glow, (countdown_rect.x - 10, countdown_rect.y - 5))
    surface.blit(countdown_text, countdown_rect)

    # Add massive particle explosions occasionally
    if random.random() < 0.1:
        for i in range(3):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(200, 400)
            x = SCREEN_WIDTH // 2 + math.cos(angle) * distance
            y = SCREEN_HEIGHT // 2 + math.sin(angle) * distance
            create_particles(x, y, random.choice([NEON_GREEN, NEON_CYAN, NEON_BLUE, NEON_PURPLE, NEON_YELLOW]), 15, 3.0)


# NEW: Update robot dog color based on parts collected
def update_robot_dog_color():
    global robot_dog_current_color, color_transition_progress

    # Calculate color transition progress based on parts collected
    if TOTAL_PARTS_TO_COLLECT > 0:
        target_progress = min(1.0, PARTS_COLLECTED / TOTAL_PARTS_TO_COLLECT)

        # Smooth transition to target progress
        if color_transition_progress < target_progress:
            color_transition_progress = min(color_transition_progress + color_transition_speed, target_progress)
        elif color_transition_progress > target_progress:
            color_transition_progress = max(color_transition_progress - color_transition_speed, target_progress)

    # Calculate current color based on progress
    robot_dog_current_color = interpolate_color(ROBOT_DOG_BASE_COLOR, ROBOT_DOG_TARGET_COLOR, color_transition_progress)

    return robot_dog_current_color


# NEW: Sound management functions
def play_background_music():
    global background_music_playing
    if background_music and not background_music_playing:
        background_music.play(-1)  # -1 means loop indefinitely
        background_music_playing = True


def stop_background_music():
    global background_music_playing
    if background_music and background_music_playing:
        background_music.stop()
        background_music_playing = False


def play_win_sound():
    if win_sound:
        win_sound.play()


def play_lose_sound():
    if lose_sound:
        lose_sound.play()


def play_jump_sound():
    if jump_sound:
        jump_sound.play()


def play_collect_sound():
    if collect_sound:
        collect_sound.play()


def play_hit_sound():
    if lose_sound:  # Use lose sound for hit
        lose_sound.play()


# NEW: Draw control buttons (same as snowbot level)
def draw_control_buttons(surface, mouse_pos):
    # Draw escape button
    escape_hover = ESCAPE_BUTTON.collidepoint(mouse_pos)
    escape_color = (180, 60, 60) if escape_hover else (150, 50, 50)
    pygame.draw.rect(surface, escape_color, ESCAPE_BUTTON, border_radius=8)
    pygame.draw.rect(surface, WHITE, ESCAPE_BUTTON, 2, border_radius=8)

    escape_text = font.render("ESC - Main Menu", True, WHITE)
    escape_text_rect = escape_text.get_rect(center=ESCAPE_BUTTON.center)
    surface.blit(escape_text, escape_text_rect)

    # Draw pause button
    pause_hover = PAUSE_BUTTON.collidepoint(mouse_pos)
    pause_color = (60, 120, 180) if pause_hover else (50, 100, 150)
    pygame.draw.rect(surface, pause_color, PAUSE_BUTTON, border_radius=8)
    pygame.draw.rect(surface, WHITE, PAUSE_BUTTON, 2, border_radius=8)

    pause_text = font.render("PAUSE/RESUME", True, WHITE)
    pause_text_rect = pause_text.get_rect(center=PAUSE_BUTTON.center)
    surface.blit(pause_text, pause_text_rect)

    return escape_hover, pause_hover


# NEW: Enhanced pause screen with clickable buttons
def draw_pause_screen(surface, mouse_pos):
    # Draw semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surface.blit(overlay, (0, 0))

    # Draw title
    pause_text = title_font.render("GAME PAUSED", True, NEON_YELLOW)
    surface.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 2 - 150))

    # Draw resume button
    resume_hover = RESUME_BUTTON.collidepoint(mouse_pos)
    resume_color = (60, 180, 60) if resume_hover else (50, 150, 50)
    pygame.draw.rect(surface, resume_color, RESUME_BUTTON, border_radius=12)
    pygame.draw.rect(surface, WHITE, RESUME_BUTTON, 3, border_radius=12)

    resume_text = font.render("RESUME GAME", True, WHITE)
    resume_text_rect = resume_text.get_rect(center=RESUME_BUTTON.center)
    surface.blit(resume_text, resume_text_rect)

    if resume_hover:
        pygame.draw.rect(surface, (100, 255, 100, 100), RESUME_BUTTON.inflate(10, 10), border_radius=15)

    # Draw main menu button
    menu_hover = MAIN_MENU_BUTTON.collidepoint(mouse_pos)
    menu_color = (180, 60, 60) if menu_hover else (150, 50, 50)
    pygame.draw.rect(surface, menu_color, MAIN_MENU_BUTTON, border_radius=12)
    pygame.draw.rect(surface, WHITE, MAIN_MENU_BUTTON, 3, border_radius=12)

    menu_text = font.render("MAIN MENU", True, WHITE)
    menu_text_rect = menu_text.get_rect(center=MAIN_MENU_BUTTON.center)
    surface.blit(menu_text, menu_text_rect)

    if menu_hover:
        pygame.draw.rect(surface, (255, 100, 100, 100), MAIN_MENU_BUTTON.inflate(10, 10), border_radius=15)

    # Instructions
    instruction = small_font.render("Press P or use left mouse to click RESUME to continue", True, WHITE)
    surface.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2, SCREEN_HEIGHT // 2 + 160))

    return resume_hover, menu_hover


# NEW: Launch credit screen function
def launch_credit_screen():
    pygame.quit()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    credit_path = os.path.join(script_dir, "credit.py")
    try:
        if sys.platform == "win32":
            subprocess.Popen([sys.executable, credit_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen([sys.executable, credit_path])
    except Exception as e:
        print(f"Failed to launch credit.py: {e}")
    sys.exit()


# NEW: Draw engineer character
def draw_engineer(surface, x, y, animation):
    # Engineer body
    body_rect = pygame.Rect(x - 25, y - 40, 50, 80)
    pygame.draw.rect(surface, (60, 70, 90), body_rect, border_radius=10)

    # Engineer head
    head_radius = 20
    pygame.draw.circle(surface, (240, 200, 160), (x, y - 60), head_radius)

    # Engineer helmet
    helmet_rect = pygame.Rect(x - 22, y - 82, 44, 30)
    pygame.draw.rect(surface, (80, 90, 110), helmet_rect, border_radius=8)
    pygame.draw.arc(surface, NEON_BLUE, (x - 18, y - 78, 36, 22), 0, math.pi, 3)

    # Engineer visor
    visor_rect = pygame.Rect(x - 15, y - 75, 30, 12)
    pygame.draw.rect(surface, (100, 200, 255, 150), visor_rect, border_radius=5)

    # Engineer arms (animated)
    arm_angle = math.sin(animation) * 0.5
    left_arm_start = (x - 25, y - 20)
    left_arm_end = (x - 45 - math.sin(animation) * 10, y - 10 + math.cos(animation) * 15)
    pygame.draw.line(surface, (60, 70, 90), left_arm_start, left_arm_end, 8)

    right_arm_start = (x + 25, y - 20)
    right_arm_end = (x + 45 + math.sin(animation) * 10, y - 10 + math.cos(animation) * 15)
    pygame.draw.line(surface, (60, 70, 90), right_arm_start, right_arm_end, 8)

    # Engineer legs
    pygame.draw.rect(surface, (40, 50, 70), (x - 20, y + 40, 15, 30), border_radius=5)
    pygame.draw.rect(surface, (40, 50, 70), (x + 5, y + 40, 15, 30), border_radius=5)

    # Tool in hand
    tool_x = right_arm_end[0] + 5
    tool_y = right_arm_end[1]
    pygame.draw.rect(surface, (200, 200, 200), (tool_x, tool_y - 3, 15, 6), border_radius=2)
    pygame.draw.circle(surface, NEON_BLUE, (tool_x + 7, tool_y), 4)

    return (tool_x + 7, tool_y)  # Return tool position for spark effects


# NEW: Create electric spark effects
def create_electric_spark(x, y, count=8):
    for _ in range(count):
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(10, 30)
        duration = random.randint(10, 20)

        spark_x = x + math.cos(angle) * distance
        spark_y = y + math.sin(angle) * distance

        PARTICLE_SYSTEMS.append({
            "x": x, "y": y,
            "vx": (spark_x - x) / duration * 2,
            "vy": (spark_y - y) / duration * 2,
            "color": NEON_YELLOW,
            "life": duration,
            "max_life": duration,
            "size": random.uniform(1, 3),
            "type": "spark"
        })


# FIXED: Single draw_testing_screen function (removed duplicate)
def draw_testing_screen(surface, progress, message_index, engineer_x, engineer_y, animation):
    # Draw lab background
    draw_cyber_lab(surface)

    # Draw cyber canine in center (bigger size) - WITH TESTING MODE ENABLED
    # FIXED: Call the correct draw_cyber_canine function
    draw_cyber_canine_realistic(surface, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 0, 0,
                                testing_mode=True, is_jumping=False, is_hit=False, facing_right=False,
                                body_color=robot_dog_current_color)

    # Draw engineer and get tool position for sparks
    tool_pos = draw_engineer(surface, engineer_x, engineer_y, animation)

    # Draw testing panel
    panel_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, 100, 400, 120)
    panel_surf = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
    panel_surf.fill((30, 35, 50, 220))
    pygame.draw.rect(panel_surf, NEON_BLUE, panel_surf.get_rect(), 3, border_radius=10)
    surface.blit(panel_surf, (panel_rect.x, panel_rect.y))

    # Draw testing title
    title_text = title_font.render("SYSTEMS DIAGNOSTICS", True, NEON_CYAN)
    surface.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 110))

    # Draw current test message
    if message_index < len(testing_messages):
        message_text = font.render(testing_messages[message_index], True, WHITE)
        surface.blit(message_text, (SCREEN_WIDTH // 2 - message_text.get_width() // 2, 160))

    # Draw progress bar
    progress_bg = pygame.Rect(SCREEN_WIDTH // 2 - 150, 190, 300, 20)
    pygame.draw.rect(surface, DARK_GRAY, progress_bg, border_radius=10)

    progress_filled = pygame.Rect(SCREEN_WIDTH // 2 - 150, 190, 300 * progress, 20)
    pygame.draw.rect(surface, NEON_GREEN, progress_filled, border_radius=10)
    pygame.draw.rect(surface, WHITE, progress_bg, 2, border_radius=10)

    # Draw progress percentage
    percent_text = font.render(f"{int(progress * 100)}%", True, WHITE)
    surface.blit(percent_text, (SCREEN_WIDTH // 2 - percent_text.get_width() // 2, 195))

    # Draw countdown
    time_left = (testing_duration - (pygame.time.get_ticks() - testing_start_time)) / 1000
    if time_left > 0:
        countdown_text = font.render(f"Running test in: {time_left:.1f}s", True, NEON_YELLOW)
        surface.blit(countdown_text, (SCREEN_WIDTH // 2 - countdown_text.get_width() // 2, 220))

    return tool_pos  # Return tool position for spark effects


# FIXED: Single UPDATED enhanced realistic cyber canine drawing function
def draw_cyber_canine_realistic(surface, x, y, leg_animation=0, run_cycle=0, testing_mode=False, is_jumping=False,
                                is_hit=False, facing_right=True, body_color=None):
    # Use provided body color or default
    if body_color is None:
        body_color = robot_dog_current_color

    # If hit, make body flash red
    if is_hit and (pygame.time.get_ticks() // 100) % 2 == 0:
        body_color = (180, 60, 60)

    # Main body - bigger and more realistic dog proportions
    body_w, body_h = 240, 100  # Increased size
    body_rect = pygame.Rect(x - body_w // 2, y - body_h // 2, body_w, body_h)

    # Draw body with organic, muscular shape - more realistic dog torso
    body_points = [
        (x - body_w // 2 + 20, y - body_h // 2 + 10),  # Top left (shoulder)
        (x + body_w // 2 - 20, y - body_h // 2 + 10),  # Top right (shoulder)
        (x + body_w // 2 - 10, y + body_h // 2 - 15),  # Bottom right (hip)
        (x - body_w // 2 + 10, y + body_h // 2 - 15)  # Bottom left (hip)
    ]

    pygame.draw.polygon(surface, body_color, body_points)

    # Add muscle definition - more prominent
    muscle_color = (min(255, body_color[0] + 10), min(255, body_color[1] + 10), min(255, body_color[2] + 10))
    pygame.draw.ellipse(surface, muscle_color, (x - body_w // 2 + 40, y - body_h // 2 + 15, 50, 30))
    pygame.draw.ellipse(surface, muscle_color, (x + body_w // 2 - 90, y - body_h // 2 + 15, 50, 30))

    # Shoulder/hip joints with more detail
    joint_radius = 15  # Bigger joints
    joint_positions = [
        (x - body_w // 2 + 30, y - 5),  # Front left
        (x + body_w // 2 - 30, y - 5),  # Front right
        (x - body_w // 2 + 30, y + 20),  # Back left
        (x + body_w // 2 - 30, y + 20)  # Back right
    ]

    for jx, jy in joint_positions:
        # Joint base
        pygame.draw.circle(surface,
                           (min(255, body_color[0] + 20), min(255, body_color[1] + 20), min(255, body_color[2] + 20)),
                           (jx, jy), joint_radius)
        # Joint inner
        pygame.draw.circle(surface,
                           (min(255, body_color[0] + 40), min(255, body_color[1] + 40), min(255, body_color[2] + 40)),
                           (jx, jy), joint_radius - 5)
        # Joint highlight
        pygame.draw.circle(surface,
                           (min(255, body_color[0] + 60), min(255, body_color[1] + 60), min(255, body_color[2] + 60)),
                           (jx, jy), joint_radius - 8)

    # Head - bigger and more realistic dog head with detailed snout
    head_w, head_h = 90, 65  # Bigger head

    # Position head based on facing direction
    if facing_right:
        head_x = x + body_w // 2 - 20  # Head on the right side when facing right
    else:
        head_x = x - body_w // 2 - 20  # Head on the left side when facing left

    head_y = y - body_h // 2 - 30  # Adjusted position

    # Head main shape - more dog-like (adjusted for direction)
    if facing_right:
        head_points = [
            (head_x, head_y + head_h // 3),  # Left base
            (head_x + head_w // 2, head_y),  # Top middle
            (head_x + head_w, head_y + head_h // 3),  # Right base
            (head_x + head_w * 0.8, head_y + head_h),  # Right jaw
            (head_x + head_w * 0.2, head_y + head_h)  # Left jaw
        ]
    else:
        head_points = [
            (head_x + head_w, head_y + head_h // 3),  # Right base
            (head_x + head_w // 2, head_y),  # Top middle
            (head_x, head_y + head_h // 3),  # Left base
            (head_x + head_w * 0.2, head_y + head_h),  # Left jaw
            (head_x + head_w * 0.8, head_y + head_h)  # Right jaw
        ]

    pygame.draw.polygon(surface, body_color, head_points)

    # Snout - more pronounced and realistic
    snout_w, snout_h = 60, 40
    if facing_right:
        snout_x = head_x + head_w - 25
    else:
        snout_x = head_x + 25 - snout_w

    snout_y = head_y + head_h // 2 - snout_h // 2 + 5

    # Snout shape
    snout_color = (max(0, body_color[0] - 10), max(0, body_color[1] - 10), max(0, body_color[2] - 10))
    snout_points = [
        (snout_x, snout_y + snout_h // 3),
        (snout_x + snout_w, snout_y + snout_h // 3),
        (snout_x + snout_w, snout_y + snout_h * 2 // 3),
        (snout_x, snout_y + snout_h * 2 // 3)
    ]
    pygame.draw.polygon(surface, snout_color, snout_points)

    # Snout bridge
    if facing_right:
        pygame.draw.line(surface, (max(0, body_color[0] - 5), max(0, body_color[1] - 5), max(0, body_color[2] - 5)),
                         (head_x + head_w // 2, head_y + head_h // 3),
                         (snout_x, snout_y + snout_h // 2), 5)
    else:
        pygame.draw.line(surface, (max(0, body_color[0] - 5), max(0, body_color[1] - 5), max(0, body_color[2] - 5)),
                         (head_x + head_w // 2, head_y + head_h // 3),
                         (snout_x + snout_w, snout_y + snout_h // 2), 5)

    # Ears - more natural positioning and shape
    ear_w, ear_h = 18, 28
    if facing_right:
        left_ear_points = [
            (head_x - 5, head_y + 10),
            (head_x - 5, head_y + 10 + ear_h),
            (head_x - 5 + ear_w, head_y + 10 + ear_h // 2)
        ]
        right_ear_points = [
            (head_x + head_w + 5, head_y + 10),
            (head_x + head_w + 5, head_y + 10 + ear_h),
            (head_x + head_w + 5 - ear_w, head_y + 10 + ear_h // 2)
        ]
    else:
        left_ear_points = [
            (head_x + head_w + 5, head_y + 10),
            (head_x + head_w + 5, head_y + 10 + ear_h),
            (head_x + head_w + 5 - ear_w, head_y + 10 + ear_h // 2)
        ]
        right_ear_points = [
            (head_x - 5, head_y + 10),
            (head_x - 5, head_y + 10 + ear_h),
            (head_x - 5 + ear_w, head_y + 10 + ear_h // 2)
        ]

    ear_color = (max(0, body_color[0] - 20), max(0, body_color[1] - 20), max(0, body_color[2] - 20))
    pygame.draw.polygon(surface, ear_color, left_ear_points)
    pygame.draw.polygon(surface, ear_color, right_ear_points)

    # Eyes - more realistic with depth and expression
    eye_radius = 8
    if facing_right:
        left_eye = (head_x + 25, head_y + 25)
        right_eye = (head_x + head_w - 30, head_y + 25)
    else:
        left_eye = (head_x + head_w - 25, head_y + 25)
        right_eye = (head_x + 30, head_y + 25)

    # Eye glow effect with more realistic positioning
    eye_pulse = (math.sin(pygame.time.get_ticks() / 200) + 1) / 2
    # Adjust eye color based on body color (brighter version)
    eye_color = (min(255, body_color[0] + 50), min(255, body_color[1] + 100), min(255, body_color[2] + 100))

    # Eye sockets
    pygame.draw.circle(surface, (max(0, body_color[0] - 30), max(0, body_color[1] - 30), max(0, body_color[2] - 30)),
                       left_eye, eye_radius + 2)
    pygame.draw.circle(surface, (max(0, body_color[0] - 30), max(0, body_color[1] - 30), max(0, body_color[2] - 30)),
                       right_eye, eye_radius + 2)

    # Eyes
    pygame.draw.circle(surface, eye_color, left_eye, eye_radius)
    pygame.draw.circle(surface, eye_color, right_eye, eye_radius)

    # Pupils with more natural movement (looking forward when running)
    if facing_right:
        # When facing right, pupils look slightly right
        pupil_offset_x = 2 + math.sin(pygame.time.get_ticks() / 400) * 2
        pupil_offset_y = math.cos(pygame.time.get_ticks() / 500) * 2
    else:
        # When facing left, pupils look slightly left
        pupil_offset_x = -2 + math.sin(pygame.time.get_ticks() / 400) * 2
        pupil_offset_y = math.cos(pygame.time.get_ticks() / 500) * 2

    pygame.draw.circle(surface, BLACK, (left_eye[0] + pupil_offset_x, left_eye[1] + pupil_offset_y), eye_radius // 2)
    pygame.draw.circle(surface, BLACK, (right_eye[0] + pupil_offset_x, right_eye[1] + pupil_offset_y), eye_radius // 2)

    # Eye highlights - more realistic placement
    if facing_right:
        highlight_offset = -3
    else:
        highlight_offset = 3

    pygame.draw.circle(surface, WHITE, (left_eye[0] + highlight_offset, left_eye[1] - 3), 3)
    pygame.draw.circle(surface, WHITE, (right_eye[0] + highlight_offset, right_eye[1] - 3), 3)

    # Nose - more detailed and realistic
    nose_radius = 8
    if facing_right:
        nose_pos = (snout_x + snout_w - 10, snout_y + snout_h // 2)
    else:
        nose_pos = (snout_x + 10, snout_y + snout_h // 2)

    pygame.draw.circle(surface, (max(0, body_color[0] - 40), max(0, body_color[1] - 40), max(0, body_color[2] - 40)),
                       nose_pos, nose_radius)

    # Nostrils - more defined
    pygame.draw.circle(surface, (max(0, body_color[0] - 50), max(0, body_color[1] - 50), max(0, body_color[2] - 50)),
                       (nose_pos[0] - 3, nose_pos[1] - 2), 3)
    pygame.draw.circle(surface, (max(0, body_color[0] - 50), max(0, body_color[1] - 50), max(0, body_color[2] - 50)),
                       (nose_pos[0] + 3, nose_pos[1] - 2), 3)

    # Nose bridge
    pygame.draw.line(surface, (max(0, body_color[0] - 35), max(0, body_color[1] - 35), max(0, body_color[2] - 35)),
                     (nose_pos[0] - 5, nose_pos[1] - 3),
                     (nose_pos[0] + 5, nose_pos[1] - 3), 2)

    # Mouth - more expressive
    mouth_y = snout_y + snout_h - 5
    if facing_right:
        mouth_start_x = snout_x + 10
        mouth_end_x = snout_x + snout_w - 10
    else:
        mouth_start_x = snout_x + snout_w - 10
        mouth_end_x = snout_x + 10

    # Mouth line
    mouth_curve = [
        (mouth_start_x, mouth_y),
        (mouth_start_x + (mouth_end_x - mouth_start_x) * 0.3, mouth_y + 3),
        (mouth_start_x + (mouth_end_x - mouth_start_x) * 0.7, mouth_y + 3),
        (mouth_end_x, mouth_y)
    ]
    if len(mouth_curve) > 1:
        pygame.draw.lines(surface, (max(0, body_color[0] - 30), max(0, body_color[1] - 30), max(0, body_color[2] - 30)),
                          False, mouth_curve, 2)

    # More realistic legs with proper joints and musculature
    # Adjusted leg angles for running direction
    if facing_right:
        leg_segments = [
            # Front left leg
            [(x - body_w // 2 + 30, y - 5), 45, -0.5 + math.sin(run_cycle) * 0.7,
             (max(0, body_color[0] + 10), max(0, body_color[1] + 10), max(0, body_color[2] + 10))],
            # Front right leg
            [(x + body_w // 2 - 30, y - 5), 45, 0.5 + math.sin(run_cycle + math.pi) * 0.7,
             (max(0, body_color[0] + 10), max(0, body_color[1] + 10), max(0, body_color[2] + 10))],
            # Back left leg
            [(x - body_w // 2 + 30, y + 20), 50, -0.3 + math.sin(run_cycle + 0.6) * 0.8,
             (max(0, body_color[0] + 5), max(0, body_color[1] + 5), max(0, body_color[2] + 5))],
            # Back right leg
            [(x + body_w // 2 - 30, y + 20), 50, 0.3 + math.sin(run_cycle + 1.6) * 0.8,
             (max(0, body_color[0] + 5), max(0, body_color[1] + 5), max(0, body_color[2] + 5))]
        ]
    else:
        # Facing left - adjust leg angles
        leg_segments = [
            # Front left leg (now on the right when facing left)
            [(x + body_w // 2 - 30, y - 5), 45, 0.5 + math.sin(run_cycle) * 0.7,
             (max(0, body_color[0] + 10), max(0, body_color[1] + 10), max(0, body_color[2] + 10))],
            # Front right leg (now on the left when facing left)
            [(x - body_w // 2 + 30, y - 5), 45, -0.5 + math.sin(run_cycle + math.pi) * 0.7,
             (max(0, body_color[0] + 10), max(0, body_color[1] + 10), max(0, body_color[2] + 10))],
            # Back left leg
            [(x + body_w // 2 - 30, y + 20), 50, 0.3 + math.sin(run_cycle + 0.6) * 0.8,
             (max(0, body_color[0] + 5), max(0, body_color[1] + 5), max(0, body_color[2] + 5))],
            # Back right leg
            [(x - body_w // 2 + 30, y + 20), 50, -0.3 + math.sin(run_cycle + 1.6) * 0.8,
             (max(0, body_color[0] + 5), max(0, body_color[1] + 5), max(0, body_color[2] + 5))]
        ]

    # If jumping, adjust leg angles
    if is_jumping:
        if facing_right:
            leg_segments = [
                # Front left leg (tucked in during jump)
                [(x - body_w // 2 + 30, y - 5), 35, -0.8,
                 (max(0, body_color[0] + 10), max(0, body_color[1] + 10), max(0, body_color[2] + 10))],
                # Front right leg
                [(x + body_w // 2 - 30, y - 5), 35, -0.6,
                 (max(0, body_color[0] + 10), max(0, body_color[1] + 10), max(0, body_color[2] + 10))],
                # Back left leg
                [(x - body_w // 2 + 30, y + 20), 40, -0.2,
                 (max(0, body_color[0] + 5), max(0, body_color[1] + 5), max(0, body_color[2] + 5))],
                # Back right leg
                [(x + body_w // 2 - 30, y + 20), 40, 0.2,
                 (max(0, body_color[0] + 5), max(0, body_color[1] + 5), max(0, body_color[2] + 5))]
            ]
        else:
            leg_segments = [
                # Front left leg (tucked in during jump)
                [(x + body_w // 2 - 30, y - 5), 35, 0.8,
                 (max(0, body_color[0] + 10), max(0, body_color[1] + 10), max(0, body_color[2] + 10))],
                # Front right leg
                [(x - body_w // 2 + 30, y - 5), 35, 0.6,
                 (max(0, body_color[0] + 10), max(0, body_color[1] + 10), max(0, body_color[2] + 10))],
                # Back left leg
                [(x + body_w // 2 - 30, y + 20), 40, 0.2,
                 (max(0, body_color[0] + 5), max(0, body_color[1] + 5), max(0, body_color[2] + 5))],
                # Back right leg
                [(x - body_w // 2 + 30, y + 20), 40, -0.2,
                 (max(0, body_color[0] + 5), max(0, body_color[1] + 5), max(0, body_color[2] + 5))]
            ]

    for (start_x, start_y), length, angle, color in leg_segments:
        # Upper leg (thigh) - more muscular
        end_x = start_x + length * math.cos(angle)
        end_y = start_y + length * math.sin(angle)
        pygame.draw.line(surface, color, (start_x, start_y), (end_x, end_y), 12)

        # Knee joint
        pygame.draw.circle(surface, (min(255, color[0] + 20), min(255, color[1] + 20), min(255, color[2] + 20)),
                           (int(end_x), int(end_y)), 10)

        # Lower leg (shin) - more defined
        lower_angle = angle + math.sin(run_cycle * 2) * 0.4
        foot_x = end_x + (length - 15) * math.cos(lower_angle)
        foot_y = end_y + (length - 15) * math.sin(lower_angle)
        pygame.draw.line(surface, (max(0, color[0] - 10), max(0, color[1] - 10), max(0, color[2] - 10)), (end_x, end_y),
                         (foot_x, foot_y), 10)

        # Ankle joint
        pygame.draw.circle(surface, (min(255, color[0] + 10), min(255, color[1] + 10), min(255, color[2] + 10)),
                           (int(foot_x), int(foot_y)), 8)

        # Paw with toes - more realistic
        paw_width = 20
        paw_height = 12
        paw_rect = pygame.Rect(foot_x - paw_width // 2, foot_y - paw_height // 2, paw_width, paw_height)
        pygame.draw.ellipse(surface, (max(0, color[0] - 20), max(0, color[1] - 20), max(0, color[2] - 20)), paw_rect)

        # Toes - more defined
        for i in range(4):
            toe_x = foot_x - paw_width // 2 + 5 + i * 5
            pygame.draw.circle(surface, (max(0, color[0] - 30), max(0, color[1] - 30), max(0, color[2] - 30)),
                               (int(toe_x), int(foot_y + 4)), 4)

    # Tail - more natural dog tail with fur texture and movement
    if facing_right:
        tail_base = (x + body_w // 2 - 15, y)
    else:
        tail_base = (x - body_w // 2 + 15, y)

    tail_angle = math.sin(pygame.time.get_ticks() / 300) * 0.3
    if not facing_right:
        tail_angle = -tail_angle  # Flip tail direction when facing left

    tail_points = []
    segments = 6
    for i in range(segments + 1):
        segment_angle = tail_angle + i * 0.2
        segment_length = 15
        point_x = tail_base[0] + math.cos(segment_angle) * segment_length * i
        point_y = tail_base[1] + math.sin(segment_angle) * segment_length * i
        tail_points.append((point_x, point_y))

    if len(tail_points) > 1:
        pygame.draw.lines(surface, (max(0, body_color[0] - 5), max(0, body_color[1] - 5), max(0, body_color[2] - 5)),
                          False, tail_points, 10)
        # Add tail fluff
        for point in tail_points[1:]:
            for i in range(4):
                offset_x = random.randint(-4, 4)
                offset_y = random.randint(-4, 4)
                pygame.draw.circle(surface, (
                min(255, body_color[0] + 10), min(255, body_color[1] + 10), min(255, body_color[2] + 10)),
                                   (point[0] + offset_x, point[1] + offset_y), 4)

    # Cybernetic details and armor plating - more prominent
    # Spine armor
    spine_y = y - body_h // 2 + 15
    pygame.draw.line(surface, NEON_BLUE, (x - body_w // 2 + 25, spine_y),
                     (x + body_w // 2 - 25, spine_y), 5)

    # Shoulder armor - more defined
    pygame.draw.ellipse(surface,
                        (min(255, body_color[0] + 20), min(255, body_color[1] + 25), min(255, body_color[2] + 25)),
                        (x - body_w // 2 + 15, y - body_h // 2, 35, 20))
    pygame.draw.ellipse(surface,
                        (min(255, body_color[0] + 20), min(255, body_color[1] + 25), min(255, body_color[2] + 25)),
                        (x + body_w // 2 - 50, y - body_h // 2, 35, 20))

    # Hip armor - more defined
    pygame.draw.ellipse(surface,
                        (min(255, body_color[0] + 15), min(255, body_color[1] + 20), min(255, body_color[2] + 20)),
                        (x - body_w // 2 + 15, y + body_h // 2 - 25, 35, 20))
    pygame.draw.ellipse(surface,
                        (min(255, body_color[0] + 15), min(255, body_color[1] + 20), min(255, body_color[2] + 20)),
                        (x + body_w // 2 - 50, y + body_h // 2 - 25, 35, 20))

    # Rib plating
    for i in range(3):
        rib_y = y - body_h // 2 + 30 + i * 15
        pygame.draw.arc(surface, NEON_BLUE, (x - body_w // 2 + 20, rib_y - 5, body_w - 40, 20),
                        math.pi, 2 * math.pi, 3)

    # Power core glow - more realistic energy effect
    core_pulse = (math.sin(pygame.time.get_ticks() / 180) + 1) / 2
    core_radius = 30  # Bigger core
    core_surf = pygame.Surface((core_radius * 2, core_radius * 2), pygame.SRCALPHA)

    # Core layers for depth
    for i in range(4):
        layer_radius = core_radius - i * 6
        layer_alpha = int(150 - i * 30)
        pygame.draw.circle(core_surf, (*NEON_BLUE, layer_alpha),
                           (core_radius, core_radius), layer_radius)

    # Core energy pulses
    pulse_radius = int(core_radius * (0.7 + 0.3 * core_pulse))
    pygame.draw.circle(core_surf, (*NEON_CYAN, int(200 * core_pulse)),
                       (core_radius, core_radius), pulse_radius)

    # Core inner energy
    inner_pulse = (math.sin(pygame.time.get_ticks() / 100) + 1) / 2
    inner_radius = int(core_radius * 0.4)
    pygame.draw.circle(core_surf, (*WHITE, int(150 * inner_pulse)),
                       (core_radius, core_radius), inner_radius)

    surface.blit(core_surf, (x - core_radius, y - core_radius))

    # Motion trail effect during running - behind the dog based on direction
    if not testing_mode:
        for i in range(1, 4):
            trail_alpha = int(60 / i)
            trail_surf = pygame.Surface((body_w + 60, body_h + 80), pygame.SRCALPHA)

            if facing_right:
                # Trail behind when facing right
                trail_points = [
                    (25 - i * 10, 25 - i * 10),
                    (body_w - 25 + i * 10, 25 - i * 10),
                    (body_w + i * 12, 35),
                    (body_w - 20 + i * 12, body_h + 25 - i * 10),
                    (20 - i * 12, body_h + 25 - i * 10),
                    (-i * 12, 35)
                ]
            else:
                # Trail behind when facing left (flipped)
                trail_points = [
                    (body_w - 25 + i * 10, 25 - i * 10),
                    (25 - i * 10, 25 - i * 10),
                    (-i * 12, 35),
                    (20 - i * 12, body_h + 25 - i * 10),
                    (body_w - 20 + i * 12, body_h + 25 - i * 10),
                    (body_w + i * 12, 35)
                ]

            pygame.draw.polygon(trail_surf, (*NEON_BLUE, trail_alpha), trail_points)
            surface.blit(trail_surf, (x - body_w // 2 - 25, y - body_h // 2 - 25))

    # During testing mode, show diagnostic effects
    if testing_mode:
        # Pulsing diagnostic rings
        ring_pulse = (math.sin(pygame.time.get_ticks() / 250) + 1) / 2
        ring_radius = 150 + int(25 * ring_pulse)  # Bigger rings
        ring_surf = pygame.Surface((ring_radius * 2, ring_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(ring_surf, (*NEON_GREEN, int(100 * ring_pulse)),
                           (ring_radius, ring_radius), ring_radius, 4)
        surface.blit(ring_surf, (x - ring_radius, y - ring_radius))

        # Scanning laser effects
        scan_angle = pygame.time.get_ticks() / 50
        scan_length = 180  # Longer scan
        scan_end_x = x + scan_length * math.cos(scan_angle)
        scan_end_y = y + scan_length * math.sin(scan_angle)
        create_laser_effect((x, y), (scan_end_x, scan_end_y), NEON_CYAN, 10)


# FIXED: Enhanced realistic cyber canine drawing for assembly/testing (facing left)
def draw_cyber_canine(surface, x, y, leg_animation=0, is_hit=False, testing_mode=False):
    # In assembly/testing state, the dog faces LEFT (original direction)
    draw_cyber_canine_realistic(surface, x, y, leg_animation, 0, testing_mode=testing_mode,
                                is_jumping=False, is_hit=is_hit, facing_right=False,
                                body_color=ROBOT_DOG_BASE_COLOR)


# FIXED: Enhanced realistic cyber canine drawing for running state - FACING RIGHT
def draw_cyber_canine_move(surface, x, y, leg_animation=0, run_cycle=0, is_jumping=False, is_hit=False):
    # Update robot dog color based on parts collected
    body_color = update_robot_dog_color()

    # In running state, the dog should face RIGHT (towards enemies)
    draw_cyber_canine_realistic(surface, x, y, leg_animation, run_cycle, testing_mode=False,
                                is_jumping=is_jumping, is_hit=is_hit, facing_right=True,
                                body_color=body_color)


# Effects functions
def create_laser_effect(start_pos, end_pos, color, duration=60):
    if len(LASER_EFFECTS) < MAX_LASERS:
        LASER_EFFECTS.append(
            {"start_pos": start_pos, "end_pos": end_pos, "color": color, "life": duration, "max_life": duration,
             "width": 3})


def create_cyber_glitch(x, y, size):
    if len(CYBER_GLITCHES) < MAX_GLITCHES:
        CYBER_GLITCHES.append({"x": x, "y": y, "size": size, "life": 30, "max_life": 30})


def update_laser_effects():
    for laser in LASER_EFFECTS[:]:
        laser["life"] -= 1
        if laser["life"] <= 0:
            LASER_EFFECTS.remove(laser)


def update_cyber_glitches():
    for glitch in CYBER_GLITCHES[:]:
        glitch["life"] -= 1
        if glitch["life"] <= 0:
            CYBER_GLITCHES.remove(glitch)


def draw_laser_effects(surface):
    for laser in LASER_EFFECTS:
        alpha = int(255 * (laser["life"] / laser["max_life"]))
        color = list(laser["color"])
        if len(color) == 3:
            color.append(alpha)
        else:
            color[3] = alpha
        pygame.draw.line(surface, color, laser["start_pos"], laser["end_pos"], laser["width"])
        glow_surf = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
        for i in range(3):
            glow_width = laser["width"] + i * 2
            glow_color = list(color)
            glow_color[3] = alpha // (i + 2)
            pygame.draw.line(glow_surf, glow_color, laser["start_pos"], laser["end_pos"], glow_width)
        surface.blit(glow_surf, (0, 0))


def draw_cyber_glitches(surface):
    for glitch in CYBER_GLITCHES:
        alpha = int(255 * (glitch["life"] / glitch["max_life"]))
        size = glitch["size"] * (glitch["life"] / glitch["max_life"])
        for i in range(5):
            start_x = glitch["x"] + random.randint(-int(size), int(size))
            start_y = glitch["y"] + random.randint(-int(size), int(size))
            end_x = start_x + random.randint(-20, 20)
            end_y = start_y + random.randint(-20, 20)
            glitch_surf = pygame.Surface((abs(end_x - start_x) + 10, abs(end_y - start_y) + 10), pygame.SRCALPHA)
            pygame.draw.line(glitch_surf, (255, 255, 255, alpha), (5, 5),
                             (abs(end_x - start_x) + 5, abs(end_y - start_y) + 5), 2)
            surface.blit(glitch_surf, (min(start_x, end_x) - 5, min(start_y, end_y) - 5))


def create_particles(x, y, color, count=10, speed_factor=1):
    # Don't create new particles if we're at the limit
    if len(PARTICLE_SYSTEMS) > MAX_PARTICLES:
        return

    for _ in range(min(count, 5)):  # Limit particles per creation
        angle = random.uniform(0, 2 * math.pi)
        speed = 1 + random.random() * 3 * speed_factor
        PARTICLE_SYSTEMS.append({
            "x": x, "y": y, "vx": math.cos(angle) * speed, "vy": math.sin(angle) * speed,
            "color": color, "life": 30, "max_life": 30, "size": random.uniform(2, 5)
        })


def update_particles():
    global PARTICLE_SYSTEMS
    # Limit total particles to prevent slowdown
    if len(PARTICLE_SYSTEMS) > MAX_PARTICLES:
        PARTICLE_SYSTEMS = PARTICLE_SYSTEMS[-100:]  # Keep only recent particles

    for particle in PARTICLE_SYSTEMS[:]:
        particle["x"] += particle["vx"]
        particle["y"] += particle["vy"]
        particle["life"] -= 1
        if particle["life"] <= 0:
            PARTICLE_SYSTEMS.remove(particle)


def draw_particles(surface):
    for particle in PARTICLE_SYSTEMS:
        alpha = int(255 * (particle["life"] / particle["max_life"]))
        size = particle["size"] * (particle["life"] / particle["max_life"])
        color = list(particle["color"])
        if len(color) == 3:
            color.append(alpha)
        else:
            color[3] = alpha
        s = pygame.Surface((int(size * 2), int(size * 2)), pygame.SRCALPHA)
        pygame.draw.circle(s, color, (int(size), int(size)), int(size))
        surface.blit(s, (particle["x"] - size, particle["y"] - size))


def update_battery():
    global BATTERY_LEVEL, BATTERY_DIRECTION
    BATTERY_LEVEL += 0.005 * BATTERY_DIRECTION
    if BATTERY_LEVEL >= 1.0:
        BATTERY_LEVEL = 1.0
        BATTERY_DIRECTION = -1
    elif BATTERY_LEVEL <= 0.1:
        BATTERY_LEVEL = 0.1
        BATTERY_DIRECTION = 1


def draw_rounded_rect(surface, rect, color, radius=10):
    pygame.draw.rect(surface, color, rect, border_radius=radius)


# NEW: Draw joystick
def draw_joystick(surface):
    # Draw joystick base
    pygame.draw.circle(surface, (50, 50, 60), joystick_base_pos, joystick_base_radius)
    pygame.draw.circle(surface, (70, 70, 80), joystick_base_pos, joystick_base_radius, 4)

    # Draw directional indicators
    for angle in [0, 90, 180, 270]:
        rad = math.radians(angle)
        x = joystick_base_pos[0] + (joystick_base_radius - 10) * math.cos(rad)
        y = joystick_base_pos[1] + (joystick_base_radius - 10) * math.sin(rad)
        pygame.draw.circle(surface, (100, 100, 120), (int(x), int(y)), 5)

    # Draw joystick handle
    pygame.draw.circle(surface, (180, 60, 60), joystick_handle_pos, joystick_handle_radius)

    # Draw colorful button on the joystick handle
    button_colors = [(255, 100, 100), (255, 150, 50), (255, 200, 0), (200, 255, 0)]
    for i, color in enumerate(button_colors):
        angle = i * math.pi / 2
        distance = joystick_handle_radius * 0.6
        x = joystick_handle_pos[0] + distance * math.cos(angle)
        y = joystick_handle_pos[1] + distance * math.sin(angle)
        pygame.draw.circle(surface, color, (int(x), int(y)), 8)

    # Draw center button
    pygame.draw.circle(surface, (50, 150, 255), joystick_handle_pos, 15)
    pygame.draw.circle(surface, (200, 230, 255), joystick_handle_pos, 10)

    # Draw instruction text
    text = small_font.render("Use WASD or drag to control", True, WHITE)
    surface.blit(text, (joystick_base_pos[0] - text.get_width() // 2,
                        joystick_base_pos[1] + joystick_base_radius + 10))


# NEW: Update joystick position based on mouse
def update_joystick(mouse_pos):
    global joystick_handle_pos, joystick_direction

    if not joystick_dragging:
        return

    # Calculate distance from base center
    dx = mouse_pos[0] - joystick_base_pos[0]
    dy = mouse_pos[1] - joystick_base_pos[1]
    distance = math.sqrt(dx * dx + dy * dy)

    # Limit to base radius
    if distance > joystick_base_radius - joystick_handle_radius:
        scale = (joystick_base_radius - joystick_handle_radius) / distance
        dx *= scale
        dy *= scale

    # Update handle position
    joystick_handle_pos[0] = joystick_base_pos[0] + dx
    joystick_handle_pos[1] = joystick_base_pos[1] + dy

    # Calculate normalized direction
    joystick_direction[0] = dx / (joystick_base_radius - joystick_handle_radius)
    joystick_direction[1] = dy / (joystick_base_radius - joystick_handle_radius)


# NEW: Reset joystick to center
def reset_joystick():
    global joystick_handle_pos, joystick_direction
    joystick_handle_pos = list(joystick_base_pos)
    joystick_direction = [0, 0]


# NEW: Update joystick based on keyboard input
def update_joystick_keyboard():
    global joystick_handle_pos, joystick_direction

    # Reset direction
    joystick_direction = [0, 0]

    # Update based on keyboard input
    if KEY_LEFT:
        joystick_direction[0] = -1
    elif KEY_RIGHT:
        joystick_direction[0] = 1

    if KEY_UP:
        joystick_direction[1] = -1
    elif KEY_DOWN:
        joystick_direction[1] = 1

    # Update handle position based on keyboard direction
    max_offset = joystick_base_radius - joystick_handle_radius
    joystick_handle_pos[0] = joystick_base_pos[0] + joystick_direction[0] * max_offset
    joystick_handle_pos[1] = joystick_base_pos[1] + joystick_direction[1] * max_offset


# NEW: Draw jump button
def draw_jump_button(surface):
    global JUMP_BUTTON_PULSE

    # Update pulse effect
    JUMP_BUTTON_PULSE += 0.05

    # Draw button
    pygame.draw.circle(surface, JUMP_BUTTON_COLOR, JUMP_BUTTON_POS, JUMP_BUTTON_RADIUS)
    pygame.draw.circle(surface, (255, 255, 255), JUMP_BUTTON_POS, JUMP_BUTTON_RADIUS, 3)

    # Draw jump arrow symbol
    pygame.draw.polygon(surface, WHITE, [
        (JUMP_BUTTON_POS[0], JUMP_BUTTON_POS[1] - 15),
        (JUMP_BUTTON_POS[0] - 10, JUMP_BUTTON_POS[1] + 5),
        (JUMP_BUTTON_POS[0] + 10, JUMP_BUTTON_POS[1] + 5)
    ])

    # Draw instruction text
    text = small_font.render("Press SPACE or UP to jump", True, WHITE)
    surface.blit(text, (JUMP_BUTTON_POS[0] - text.get_width() // 2,
                        JUMP_BUTTON_POS[1] + JUMP_BUTTON_RADIUS + 10))


# NEW: Create electronic parts to collect
def create_electronic_part():
    part_colors = [NEON_RED, NEON_GREEN, NEON_BLUE, NEON_PURPLE, NEON_CYAN, NEON_YELLOW, NEON_ORANGE]
    part_size = random.randint(15, 25)

    ELECTRONIC_PARTS.append({
        "x": SCREEN_WIDTH + 50,
        "y": random.randint(GROUND_LEVEL - 150, GROUND_LEVEL - 50),
        "speed": random.uniform(4.0, 6.0),
        "radius": part_size,
        "color": random.choice(part_colors),
        "type": random.choice(["circuit", "chip", "battery", "sensor"]),
        "rotation": 0,
        "rotation_speed": random.uniform(-0.05, 0.05),
        "color_progress": 0,  # NEW: Color transition progress
        "collection_time": 0  # NEW: Time when collected (0 if not collected)
    })


# NEW: Create small enemy robot dog with controlled spacing
def create_small_enemy_dog():
    global LAST_ENEMY_X

    # Check if there's enough space from the last enemy
    if len(ENEMY_ROBOT_DOGS) > 0:
        # Get the x position of the last enemy
        last_enemy_x = min([enemy["x"] for enemy in ENEMY_ROBOT_DOGS])

        # If the last enemy is too close, don't spawn a new one
        if LAST_ENEMY_X - last_enemy_x < MIN_ENEMY_SPACING:
            return

    # Create new enemy with random speed
    enemy_speed = random.uniform(4.0, 5.0)  # Slower speed

    ENEMY_ROBOT_DOGS.append({
        "x": SCREEN_WIDTH + 50,
        "y": GROUND_LEVEL - 70,  # CHANGED: Lower than player (was -100)
        "speed": enemy_speed,
        "radius": 25,  # Slightly larger for easier collision detection
        "color": NEON_RED,
        "leg_animation": 0,
        "run_cycle": 0,
        "height": 30,  # CHANGED: Smaller enemy (was 40)
        "id": len(ENEMY_ROBOT_DOGS)
    })

    # Update last enemy x position
    LAST_ENEMY_X = SCREEN_WIDTH + 50


# NEW: Create street hole with controlled spacing and different appearances
def create_street_hole():
    global LAST_ENEMY_X

    # Check if there's enough space from the last enemy
    if len(ENEMY_ROBOT_DOGS) > 0:
        # Get the x position of the last enemy
        last_enemy_x = min([enemy["x"] for enemy in ENEMY_ROBOT_DOGS])

        # If the last enemy is too close, don't spawn a hole
        if LAST_ENEMY_X - last_enemy_x < MIN_ENEMY_SPACING * 0.5:
            return

    # Choose hole type with different properties
    hole_types = [
        {"name": "rock", "width": random.randint(80, 120), "height": random.randint(40, 70), "color": (100, 80, 60)},
        {"name": "crack", "width": random.randint(120, 180), "height": random.randint(30, 50), "color": (60, 60, 70)},
        {"name": "pit", "width": random.randint(100, 160), "height": random.randint(50, 80), "color": (20, 25, 40)},
        {"name": "debris", "width": random.randint(90, 140), "height": random.randint(35, 65), "color": (80, 70, 65)},
        {"name": "barrier", "width": random.randint(70, 110), "height": random.randint(45, 75), "color": (120, 100, 80)}
    ]

    hole_type = random.choice(hole_types)

    STREET_HOLES.append({
        "x": SCREEN_WIDTH + 50,
        "y": GROUND_LEVEL - hole_type["height"] + 20,  # Higher than before
        "width": hole_type["width"],
        "height": hole_type["height"],
        "speed": random.uniform(4.0, 5.0),
        "type": hole_type["name"],
        "color": hole_type["color"]
    })


# NEW: Update electronic parts with color transition when collected
def update_electronic_parts():
    global PARTS_COLLECTED, SCORE

    for part in ELECTRONIC_PARTS[:]:
        # If part is being collected, update color progress
        if part["collection_time"] > 0:
            elapsed = pygame.time.get_ticks() - part["collection_time"]
            progress = min(1.0, elapsed / (PART_COLLECTION_DURATION * 16.67))  # Convert frames to ms

            # Update color progress
            part["color_progress"] = progress

            # If collection animation is complete, remove the part
            if progress >= 1.0:
                ELECTRONIC_PARTS.remove(part)
                PARTS_COLLECTED += 1
                SCORE += 25
                play_collect_sound()
                continue

        # Move part if not being collected
        if part["collection_time"] == 0:
            part["x"] -= part["speed"]
            part["rotation"] += part["rotation_speed"]

            # Remove parts that go off screen
            if part["x"] < -50:
                ELECTRONIC_PARTS.remove(part)
                continue

            # Check for collection by cyber canine
            dx = part["x"] - cyber_canine_x
            dy = part["y"] - cyber_canine_y
            distance = math.sqrt(dx * dx + dy * dy)

            if distance < 80 + part["radius"]:  # Collision with cyber canine
                # Start collection animation instead of removing immediately
                part["collection_time"] = pygame.time.get_ticks()

                # Create initial collection particles
                create_particles(part["x"], part["y"], NEON_BLUE, 15, 1.5)
                create_particles(part["x"], part["y"], NEON_YELLOW, 10, 1.0)


# NEW: Update enemy robot dogs with proper collision detection
def update_enemy_robot_dogs():
    global GAME_OVER, HEALTH, INVINCIBLE_TIMER

    for enemy in ENEMY_ROBOT_DOGS[:]:
        enemy["x"] -= enemy["speed"]
        enemy["leg_animation"] += 0.2
        enemy["run_cycle"] += 0.3

        # Remove enemies that go off screen
        if enemy["x"] < -50:
            ENEMY_ROBOT_DOGS.remove(enemy)
            continue

        # Check for collision with cyber canine
        # Use simple distance-based collision detection
        dx = enemy["x"] - cyber_canine_x
        dy = enemy["y"] - cyber_canine_y
        distance = math.sqrt(dx * dx + dy * dy)

        # Collision radius for player is smaller when jumping
        player_radius = 70 if JUMPING else 80  # CHANGED: Increased from 60 to 70 when jumping

        # If player is not invincible and collides with enemy
        if (distance < player_radius + enemy["radius"] and
                INVINCIBLE_TIMER <= 0 and
                not GAME_OVER):

            # Reduce health
            HEALTH -= 1
            play_hit_sound()

            # Create hit particles
            create_particles(cyber_canine_x, cyber_canine_y, NEON_RED, 30, 2.0)
            create_particles(enemy["x"], enemy["y"], NEON_RED, 20, 1.5)

            # Set invincibility timer (1 second)
            INVINCIBLE_TIMER = 60

            # Remove the enemy that caused damage
            ENEMY_ROBOT_DOGS.remove(enemy)

            # Check if game over
            if HEALTH <= 0:
                GAME_OVER = True
                create_particles(cyber_canine_x, cyber_canine_y, NEON_RED, 100, 3.0)
                play_lose_sound()
                break


# NEW: Update street holes with proper collision detection
def update_street_holes():
    global GAME_OVER, HEALTH, INVINCIBLE_TIMER

    for hole in STREET_HOLES[:]:
        hole["x"] -= hole["speed"]

        # Remove holes that go off screen
        if hole["x"] < -hole["width"] - 50:
            STREET_HOLES.remove(hole)
            continue

        # Check if cyber canine falls into hole
        # Cyber canine falls into hole if its x position is within hole and it's on the ground
        if (cyber_canine_x + 40 > hole["x"] and
                cyber_canine_x - 40 < hole["x"] + hole["width"] and
                cyber_canine_y >= GROUND_LEVEL - 50 and  # If dog is at ground level
                INVINCIBLE_TIMER <= 0 and
                not GAME_OVER):

            # Reduce health (hole is more dangerous)
            HEALTH -= 2
            play_lose_sound()

            # Create falling particles
            create_particles(cyber_canine_x, cyber_canine_y, NEON_RED, 50, 2.5)

            # Set invincibility timer (1.5 seconds)
            INVINCIBLE_TIMER = 90

            # Check if game over
            if HEALTH <= 0:
                GAME_OVER = True
                create_particles(cyber_canine_x, cyber_canine_y, NEON_RED, 150, 4.0)
                break


# NEW: Draw health bar (moved to right side)
def draw_health_bar(surface):
    # Draw health bar panel
    health_panel = pygame.Rect(SCREEN_WIDTH - 280, 110, 260, 60)  # stacked under score  # CHANGED: Position to right side
    panel_surf = pygame.Surface((health_panel.width, health_panel.height), pygame.SRCALPHA)
    panel_surf.fill((40, 45, 55, 200))
    pygame.draw.rect(panel_surf, (70, 75, 85), panel_surf.get_rect(), 2, border_radius=10)
    surface.blit(panel_surf, (health_panel.x, health_panel.y))

    # Draw health text
    health_text = font.render("ROBOT DOG HEALTH", True, WHITE)
    surface.blit(health_text, (SCREEN_WIDTH - 270, 120))  # moved under score

    # Draw health hearts
    heart_size = 20
    heart_spacing = 25
    start_x = SCREEN_WIDTH - 270  # CHANGED: Position to right side
    start_y = 250  # CHANGED: Position to right side

    for i in range(3):
        heart_x = start_x + i * heart_spacing

        if i < HEALTH:
            # Draw full heart
            pygame.draw.circle(surface, NEON_RED, (heart_x, start_y), heart_size // 2)
            pygame.draw.circle(surface, NEON_RED, (heart_x + heart_size // 2, start_y), heart_size // 2)
            pygame.draw.polygon(surface, NEON_RED, [
                (heart_x - heart_size // 2, start_y),
                (heart_x + heart_size, start_y),
                (heart_x + heart_size // 2, start_y + heart_size // 2)
            ])

            # Heart glow effect
            glow_pulse = (math.sin(pygame.time.get_ticks() / 300) + 1) / 2
            glow_size = heart_size * (1 + glow_pulse * 0.2)
            glow_surf = pygame.Surface((int(glow_size * 2), int(glow_size)), pygame.SRCALPHA)
            pygame.draw.ellipse(glow_surf, (*NEON_RED, int(50 * glow_pulse)),
                                (0, 0, glow_size * 2, glow_size))
            surface.blit(glow_surf, (heart_x - glow_size, start_y - glow_size // 2))
        else:
            # Draw empty heart (outline)
            pygame.draw.circle(surface, DARK_GRAY, (heart_x, start_y), heart_size // 2, 2)
            pygame.draw.circle(surface, DARK_GRAY, (heart_x + heart_size // 2, start_y), heart_size // 2, 2)
            pygame.draw.polygon(surface, DARK_GRAY, [
                (heart_x - heart_size // 2, start_y),
                (heart_x + heart_size, start_y),
                (heart_x + heart_size // 2, start_y + heart_size // 2)
            ], 2)


def draw_electronic_parts(surface):
    for part in ELECTRONIC_PARTS:
        # Calculate color based on collection progress
        if part["collection_time"] > 0:
            # Get the gradient for this part type
            gradient = PART_COLOR_GRADIENTS.get(part["type"],
                                                [(50, 150, 255), (255, 50, 150)])  # Default blue to pink

            # Get the interpolated color based on progress
            current_color = interpolate_multiple_colors(gradient, part["color_progress"])

            # Calculate size based on progress (shrink when collected)
            size_factor = 1.0 - part["color_progress"] * 0.7  # Shrink to 30% of original size
            draw_radius = int(part["radius"] * size_factor)

            # Create pulsing effect during collection
            pulse = (math.sin(pygame.time.get_ticks() / 50) + 1) / 2 if part["collection_time"] > 0 else 1.0
            alpha = int(255 * (1 - part["color_progress"] * 0.5))  # Fade out
        else:
            current_color = part["color"]
            draw_radius = part["radius"]
            pulse = (math.sin(pygame.time.get_ticks() / 200) + 1) / 2
            alpha = 255

        # Draw rotating electronic part
        part_surf = pygame.Surface((draw_radius * 2, draw_radius * 2), pygame.SRCALPHA)

        # Draw different types of electronic parts
        if part["type"] == "circuit":
            # Draw circuit board
            pygame.draw.rect(part_surf, current_color,
                             (draw_radius * 0.2, draw_radius * 0.2,
                              draw_radius * 1.6, draw_radius * 1.6),
                             border_radius=int(draw_radius * 0.3))
            # Draw circuit lines
            for i in range(4):
                line_color = interpolate_color(NEON_YELLOW, NEON_RED, part["color_progress"])
                pygame.draw.line(part_surf, line_color,
                                 (draw_radius * 0.3, draw_radius * (0.3 + i * 0.4)),
                                 (draw_radius * 1.7, draw_radius * (0.3 + i * 0.4)), 2)
            # Draw connection points
            for i in range(2):
                for j in range(2):
                    point_color = interpolate_color(NEON_CYAN, NEON_RED, part["color_progress"])
                    pygame.draw.circle(part_surf, point_color,
                                       (int(draw_radius * (0.3 + i * 1.4)),
                                        int(draw_radius * (0.3 + j * 1.4))),
                                       int(draw_radius * 0.2))

        elif part["type"] == "chip":
            # Draw microchip
            pygame.draw.rect(part_surf, current_color,
                             (draw_radius * 0.3, draw_radius * 0.3,
                              draw_radius * 1.4, draw_radius * 1.4))
            # Draw chip pins
            for i in range(8):
                pin_y = draw_radius * 0.2 + i * (draw_radius * 1.6 / 7)
                pin_color = interpolate_color(SILVER, (255, 200, 100), part["color_progress"])
                pygame.draw.rect(part_surf, pin_color,
                                 (0, pin_y - 2, draw_radius * 0.3, 4))
                pygame.draw.rect(part_surf, pin_color,
                                 (draw_radius * 1.7, pin_y - 2, draw_radius * 0.3, 4))

        elif part["type"] == "battery":
            # Draw battery
            pygame.draw.rect(part_surf, current_color,
                             (draw_radius * 0.2, draw_radius * 0.2,
                              draw_radius * 1.6, draw_radius * 1.2))

            # Battery terminal with color transition
            terminal_color = interpolate_color(NEON_YELLOW, NEON_RED, part["color_progress"])
            pygame.draw.rect(part_surf, terminal_color,
                             (draw_radius * 0.7, draw_radius * 0.1,
                              draw_radius * 0.6, draw_radius * 0.3))

            # Draw charge level with color transition
            charge_level = (math.sin(pygame.time.get_ticks() / 500) + 1) / 2
            charge_height = draw_radius * 1.0 * charge_level
            charge_color = interpolate_color(NEON_GREEN, NEON_RED, part["color_progress"])
            pygame.draw.rect(part_surf, charge_color,
                             (draw_radius * 0.3, draw_radius * 1.2 - charge_height,
                              draw_radius * 1.2, charge_height))

        elif part["type"] == "sensor":
            # Draw sensor
            pygame.draw.circle(part_surf, current_color,
                               (draw_radius, draw_radius), draw_radius * 0.8)
            center_color = interpolate_color(NEON_CYAN, NEON_RED, part["color_progress"])
            pygame.draw.circle(part_surf, center_color,
                               (draw_radius, draw_radius), draw_radius * 0.5)
            pygame.draw.circle(part_surf, BLACK,
                               (draw_radius, draw_radius), draw_radius * 0.2)

        # Set alpha transparency
        part_surf.set_alpha(alpha)

        # Rotate and draw the part
        rotated_surf = pygame.transform.rotate(part_surf, math.degrees(part["rotation"]))
        surface.blit(rotated_surf,
                     (part["x"] - rotated_surf.get_width() // 2,
                      part["y"] - rotated_surf.get_height() // 2))

        # Draw glow effect
        if part["collection_time"] == 0:  # Only glow if not being collected
            glow_size = draw_radius * 2.5
            glow_surf = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
            glow_alpha = int(100 * pulse)
            pygame.draw.circle(glow_surf, (*current_color, glow_alpha),
                               (glow_size // 2, glow_size // 2), glow_size // 2)
            surface.blit(glow_surf, (part["x"] - glow_size // 2, part["y"] - glow_size // 2))

        # Draw collection effect particles if being collected
        if part["collection_time"] > 0 and random.random() < 0.3:
            angle = random.uniform(0, 2 * math.pi)
            distance = draw_radius * (1 + part["color_progress"] * 2)
            particle_x = part["x"] + math.cos(angle) * distance
            particle_y = part["y"] + math.sin(angle) * distance
            particle_color = interpolate_multiple_colors(gradient, min(1.0, part["color_progress"] + 0.2))
            create_particles(particle_x, particle_y, particle_color, 2, 1.0 + part["color_progress"] * 2)


# NEW: Draw small enemy robot dogs - FACING LEFT (towards player)
def draw_small_enemy_dogs(surface):
    for enemy in ENEMY_ROBOT_DOGS:
        # Draw small enemy robot dog body
        body_w, body_h = 50, 25  # CHANGED: Much smaller (was 60, 30)
        body_rect = pygame.Rect(enemy["x"] - body_w // 2, enemy["y"] - body_h // 2, body_w, body_h)
        draw_rounded_rect(surface, body_rect, enemy["color"], radius=5)

        # Draw small head - FACING LEFT (towards player)
        head_r = 8  # CHANGED: Smaller head (was 10)
        # Head on the left side when facing left
        head_center = (enemy["x"] + body_w // 2 - 15, enemy["y"] - body_h // 2 - 8)
        pygame.draw.circle(surface, enemy["color"], head_center, head_r)

        # Draw angry eyes (on the left side of head when facing left)
        pygame.draw.circle(surface, (255, 50, 50), (head_center[0] - 4, head_center[1] - 3), 4)
        pygame.draw.circle(surface, (255, 50, 50), (head_center[0] + 2, head_center[1] - 3), 4)
        pygame.draw.circle(surface, BLACK, (head_center[0] - 4, head_center[1] - 3), 2)
        pygame.draw.circle(surface, BLACK, (head_center[0] + 2, head_center[1] - 3), 2)

        # Draw small legs (adjusted for facing left)
        seg_len = 18  # CHANGED: Shorter legs (was 20)
        # Leg positions adjusted for facing left
        attach = [
            (body_w // 2 - 15, -body_h // 2 + 10),  # Front leg (on right when facing left)
            (-body_w // 2 + 15, -body_h // 2 + 10),  # Front leg (on left when facing left)
            (body_w // 2 - 15, body_h // 2 - 5),  # Back leg
            (-body_w // 2 + 15, body_h // 2 - 5)  # Back leg
        ]
        phases = [enemy["run_cycle"], enemy["run_cycle"] + math.pi,
                  enemy["run_cycle"] + 0.6, enemy["run_cycle"] + 1.6]

        for i, (ax, ay) in enumerate(attach):
            phase = phases[i]
            a1 = math.sin(phase) * 0.9
            ex = enemy["x"] + ax + seg_len * math.cos(a1)
            ey = enemy["y"] + ay + seg_len * math.sin(a1)
            pygame.draw.line(surface, (150, 50, 50), (enemy["x"] + ax, enemy["y"] + ay), (ex, ey), 3)

            a2 = a1 + math.sin(phase * 1.4) * 0.7
            px = ex + seg_len * 0.8 * math.cos(a2)
            py = ey + seg_len * 0.8 * math.sin(a2)
            pygame.draw.line(surface, (120, 40, 40), (ex, ey), (px, py), 2)

            pygame.draw.circle(surface, (100, 30, 30), (int(px), int(py)), 3)


# NEW: Draw street holes with different appearances
def draw_street_holes(surface):
    for hole in STREET_HOLES:
        # Draw different types of holes
        if hole["type"] == "rock":
            # Draw rocky obstacle
            pygame.draw.rect(surface, hole["color"],
                             (hole["x"], hole["y"], hole["width"], hole["height"]))

            # Draw rock texture
            for i in range(0, hole["width"], 15):
                for j in range(0, hole["height"], 15):
                    if random.random() < 0.3:
                        rock_x = hole["x"] + i + random.randint(-3, 3)
                        rock_y = hole["y"] + j + random.randint(-3, 3)
                        rock_size = random.randint(2, 6)
                        rock_shade = (hole["color"][0] + random.randint(-20, 20),
                                      hole["color"][1] + random.randint(-20, 20),
                                      hole["color"][2] + random.randint(-20, 20))
                        pygame.draw.circle(surface, rock_shade, (rock_x, rock_y), rock_size)

            # Draw warning glow
            glow_size = hole["width"] + 20
            glow_surf = pygame.Surface((glow_size, 15), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (*NEON_ORANGE, 60),
                             (0, 0, glow_size, 15), border_radius=5)
            surface.blit(glow_surf, (hole["x"] - 10, hole["y"] - 20))

        elif hole["type"] == "crack":
            # Draw cracked pavement
            pygame.draw.rect(surface, hole["color"],
                             (hole["x"], hole["y"], hole["width"], hole["height"]))

            # Draw crack lines
            for i in range(3):
                crack_y = hole["y"] + (i + 1) * (hole["height"] // 4)
                crack_start = hole["x"] + random.randint(0, 10)
                crack_end = hole["x"] + hole["width"] - random.randint(0, 10)
                pygame.draw.line(surface, (40, 40, 50),
                                 (crack_start, crack_y), (crack_end, crack_y),
                                 random.randint(1, 2))

            # Draw warning stripes
            stripe_width = 8
            for i in range(0, hole["width"], stripe_width * 2):
                pygame.draw.rect(surface, NEON_YELLOW,
                                 (hole["x"] + i, hole["y"] - 5, stripe_width, 8))

        elif hole["type"] == "pit":
            # Draw deep pit
            pygame.draw.rect(surface, hole["color"],
                             (hole["x"], hole["y"], hole["width"], hole["height"]))

            # Draw pit interior with gradient
            for i in range(3):
                depth_color = (max(10, hole["color"][0] - i * 20),
                               max(15, hole["color"][1] - i * 20),
                               max(20, hole["color"][2] - i * 20))
                depth_rect = pygame.Rect(
                    hole["x"] + i * 5,
                    hole["y"] + i * 3,
                    hole["width"] - i * 10,
                    hole["height"] - i * 6
                )
                pygame.draw.rect(surface, depth_color, depth_rect)

            # Draw danger glow
            glow_pulse = (math.sin(pygame.time.get_ticks() / 200) + 1) / 2
            glow_alpha = int(80 + 40 * glow_pulse)
            glow_surf = pygame.Surface((hole["width"] + 30, 20), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (*NEON_RED, glow_alpha),
                             (0, 0, hole["width"] + 30, 20), border_radius=8)
            surface.blit(glow_surf, (hole["x"] - 15, hole["y"] - 25))

        elif hole["type"] == "debris":
            # Draw debris pile
            pygame.draw.rect(surface, hole["color"],
                             (hole["x"], hole["y"], hole["width"], hole["height"]))

            # Draw debris pieces
            for i in range(8):
                debris_x = hole["x"] + random.randint(5, hole["width"] - 15)
                debris_y = hole["y"] + random.randint(5, hole["height"] - 15)
                debris_w = random.randint(10, 25)
                debris_h = random.randint(8, 20)
                debris_shade = (hole["color"][0] + random.randint(-30, 10),
                                hole["color"][1] + random.randint(-30, 10),
                                hole["color"][2] + random.randint(-30, 10))
                pygame.draw.rect(surface, debris_shade,
                                 (debris_x, debris_y, debris_w, debris_h),
                                 border_radius=3)

        elif hole["type"] == "barrier":
            # Draw solid barrier
            pygame.draw.rect(surface, hole["color"],
                             (hole["x"], hole["y"], hole["width"], hole["height"]))

            # Draw barrier pattern
            pattern_color = (hole["color"][0] + 20, hole["color"][1] + 20, hole["color"][2] + 20)
            for i in range(0, hole["width"], 20):
                pygame.draw.rect(surface, pattern_color,
                                 (hole["x"] + i, hole["y"], 10, hole["height"]))

            # Draw warning chevrons
            for i in range(0, hole["width"], 30):
                chevron_x = hole["x"] + i + 15
                pygame.draw.polygon(surface, NEON_RED, [
                    (chevron_x, hole["y"] - 10),
                    (chevron_x + 10, hole["y"] - 20),
                    (chevron_x - 10, hole["y"] - 20)
                ])


# NEW: Draw parts counter (moved to right side)
def draw_parts_counter(surface):
    # Draw parts counter panel
    parts_panel = pygame.Rect(SCREEN_WIDTH - 280, 190, 260, 60)  # stacked under health  # CHANGED: Position to right side (moved down from 280 to 290)
    panel_surf = pygame.Surface((parts_panel.width, parts_panel.height), pygame.SRCALPHA)
    panel_surf.fill((40, 45, 55, 200))
    pygame.draw.rect(panel_surf, (70, 75, 85), panel_surf.get_rect(), 2, border_radius=10)
    surface.blit(panel_surf, (parts_panel.x, parts_panel.y))

    # Draw parts count
    parts_text = font.render(f"ELECTRONIC PARTS: {PARTS_COLLECTED}/{TOTAL_PARTS_TO_COLLECT}", True, WHITE)
    surface.blit(parts_text, (SCREEN_WIDTH - 270, 200))  # moved under health

    # Draw progress bar
    progress_width = 200
    progress_filled = int(progress_width * (PARTS_COLLECTED / TOTAL_PARTS_TO_COLLECT))
    pygame.draw.rect(surface, DARK_GRAY, (SCREEN_WIDTH - 270, 225, progress_width, 10), border_radius=5)  # moved under health
    if progress_filled > 0:
        pygame.draw.rect(surface, NEON_GREEN, (SCREEN_WIDTH - 270, 225, progress_filled, 10), border_radius=5)  # moved under health


# NEW: Draw game over screen
def draw_game_over(surface):
    # Draw dark overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surface.blit(overlay, (0, 0))

    # Draw game over text
    game_over_text = title_font.render("GAME OVER", True, NEON_RED)
    surface.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))

    # Draw score
    score_text = font.render(f"Final Score: {SCORE}", True, WHITE)
    surface.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))

    # Draw parts collected
    parts_text = font.render(f"Electronic Parts Collected: {PARTS_COLLECTED}/{TOTAL_PARTS_TO_COLLECT}", True, WHITE)
    surface.blit(parts_text, (SCREEN_WIDTH // 2 - parts_text.get_width() // 2, SCREEN_HEIGHT // 2 + 30))

    # Draw restart instruction
    restart_text = font.render("Press R to restart or ESC to quit", True, NEON_YELLOW)
    surface.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 80))


# NEW: Draw rectangular radar display (already on right side)
# NEW: Draw rectangular radar display (already on right side)
def draw_radar(surface):
    global radar_scan_angle, radar_pulse, radar_blips, RADAR_RANGE

    # Update radar animation
    radar_scan_angle += radar_scan_speed
    radar_pulse += 0.05

    # Clear old blips and create new ones based on current game objects
    radar_blips = []

    # Add player position (center of radar)
    radar_blips.append({
        "x": 0,
        "y": 0,
        "type": "player",
        "color": RADAR_PLAYER,
        "size": 6,
        "distance": 0
    })

    # Track closest enemy for warning
    closest_enemy_distance = RADAR_RANGE * 2

    # Add enemies (red points)
    for enemy in ENEMY_ROBOT_DOGS:
        # Convert enemy world position to radar relative position
        rel_x = enemy["x"] - cyber_canine_x
        rel_y = enemy["y"] - cyber_canine_y

        # Only show if within radar range
        distance = math.sqrt(rel_x * rel_x + rel_y * rel_y)
        if distance <= RADAR_RANGE:
            radar_blips.append({
                "x": rel_x,
                "y": rel_y,
                "type": "enemy",
                "color": RADAR_ENEMY,
                "size": 5,
                "distance": distance,
                "direction": enemy.get("direction", 0)
            })
            if distance < closest_enemy_distance:
                closest_enemy_distance = distance

    # Add street holes (orange/yellow points)
    for hole in STREET_HOLES:
        # Use center of hole
        hole_center_x = hole["x"] + hole["width"] / 2
        hole_center_y = hole["y"] + hole["height"] / 2

        rel_x = hole_center_x - cyber_canine_x
        rel_y = hole_center_y - cyber_canine_y

        distance = math.sqrt(rel_x * rel_x + rel_y * rel_y)
        if distance <= RADAR_RANGE:
            # Different colors for different hole types
            hole_color = RADAR_HOLE
            if hole["type"] == "pit":
                hole_color = (255, 100, 50, 200)
            elif hole["type"] == "barrier":
                hole_color = (255, 200, 50, 200)

            radar_blips.append({
                "x": rel_x,
                "y": rel_y,
                "type": "hole",
                "color": hole_color,
                "size": 4,
                "distance": distance
            })

    # Add electronic parts (green points)
    for part in ELECTRONIC_PARTS:
        # Only show parts that haven't been collected yet
        if part["collection_time"] == 0:
            rel_x = part["x"] - cyber_canine_x
            rel_y = part["y"] - cyber_canine_y

            distance = math.sqrt(rel_x * rel_x + rel_y * rel_y)
            if distance <= RADAR_RANGE:
                radar_blips.append({
                    "x": rel_x,
                    "y": rel_y,
                    "type": "part",
                    "color": RADAR_PART,
                    "size": 3,
                    "distance": distance,
                    "pulse": random.random() * math.pi * 2
                })

    # Create radar background panel
    radar_surf = pygame.Surface((RADAR_SIZE[0], RADAR_SIZE[1]), pygame.SRCALPHA)

    # Gradient background for more depth
    for y in range(RADAR_SIZE[1]):
        alpha = 150 + int(50 * (y / RADAR_SIZE[1]))
        pygame.draw.line(radar_surf, (*RADAR_BG[:3], alpha), (0, y), (RADAR_SIZE[0], y))

    pygame.draw.rect(radar_surf, (60, 65, 80, 200), (4, 4, RADAR_SIZE[0] - 8, RADAR_SIZE[1] - 8), border_radius=6)

    # Create camera area
    cam_w = RADAR_SIZE[0] - 20
    cam_h = RADAR_SIZE[1] - 30
    camera_surface = pygame.Surface((cam_w, cam_h), pygame.SRCALPHA)

    # Gradient sky and ground
    for y in range(cam_h):
        if y < cam_h // 2:
            color = (30 + int(10 * y / (cam_h // 2)),
                     40 + int(10 * y / (cam_h // 2)),
                     60 + int(20 * y / (cam_h // 2)))
        else:
            color = (35 + int(10 * (y - cam_h // 2) / (cam_h // 2)),
                     45 + int(10 * (y - cam_h // 2) / (cam_h // 2)),
                     65 + int(10 * (y - cam_h // 2) / (cam_h // 2)))
        pygame.draw.line(camera_surface, color, (0, y), (cam_w, y))

    # Grid lines
    grid_spacing = 20
    grid_color = (80, 90, 110, 60)

    for gx in range(0, cam_w, grid_spacing):
        pygame.draw.line(camera_surface, grid_color, (gx, 0), (gx, cam_h), 1)
    for gy in range(0, cam_h, grid_spacing):
        pygame.draw.line(camera_surface, grid_color, (0, gy), (cam_w, gy), 1)

    # Center crosshair with pulsing effect
    cx = cam_w // 2
    cy = cam_h // 2
    cross_size = 8 + int(2 * math.sin(radar_pulse))
    cross_alpha = 150 + int(50 * math.sin(radar_pulse * 1.5))

    pygame.draw.line(camera_surface, (*NEON_CYAN[:3], cross_alpha),
                     (cx - cross_size, cy), (cx + cross_size, cy), 2)
    pygame.draw.line(camera_surface, (*NEON_CYAN[:3], cross_alpha),
                     (cx, cy - cross_size), (cx, cy + cross_size), 2)

    # Draw small center circle with pulsing
    pulse_radius = 3 + math.sin(radar_pulse * 2) * 0.5
    pygame.draw.circle(camera_surface, NEON_CYAN, (cx, cy), int(pulse_radius))

    # Sort blips by distance for proper layering
    radar_blips.sort(key=lambda b: b.get("distance", 0), reverse=True)

    # Draw radar blips
    for blip in radar_blips:
        # Scale to camera coords
        map_x = cx + int((blip["x"] / RADAR_RANGE) * (cam_w // 2 - 6))
        map_y = cy + int((blip["y"] / RADAR_RANGE) * (cam_h // 2 - 6))

        btype = blip["type"]
        bcolor = blip["color"]
        bsize = blip["size"]

        # Draw different shapes for different types
        if btype == "enemy":
            # Enemy with direction indicator
            pygame.draw.circle(camera_surface, bcolor, (map_x, map_y), bsize)

            # Direction line (if available)
            direction = blip.get("direction", 0)
            dir_x = map_x + int(bsize * 1.5 * math.cos(direction))
            dir_y = map_y + int(bsize * 1.5 * math.sin(direction))
            pygame.draw.line(camera_surface, (255, 100, 100),
                             (map_x, map_y), (dir_x, dir_y), 2)

            # Pulsing effect for close enemies
            if blip["distance"] < RADAR_RANGE * 0.3:
                pulse_alpha = 100 + int(100 * math.sin(radar_pulse * 4))
                pygame.draw.circle(camera_surface, (*bcolor[:3], pulse_alpha),
                                   (map_x, map_y), bsize + 2, 1)

        elif btype == "part":
            # Electronic part with pulsing glow
            pulse = blip.get("pulse", 0)
            pulse_size = 3 + math.sin(radar_pulse * 3 + pulse) * 0.5

            pygame.draw.rect(camera_surface, bcolor,
                             (map_x - pulse_size, map_y - pulse_size,
                              pulse_size * 2, pulse_size * 2))

            # Rotating effect
            angle = radar_pulse * 2 + pulse
            for i in range(4):
                px = map_x + int(5 * math.cos(angle + i * math.pi / 2))
                py = map_y + int(5 * math.sin(angle + i * math.pi / 2))
                pygame.draw.circle(camera_surface, (*bcolor[:3], 150),
                                   (px, py), 1)

        elif btype == "hole":
            # Hole with danger indicator
            points = [(map_x, map_y - bsize),
                      (map_x - bsize, map_y + bsize),
                      (map_x + bsize, map_y + bsize)]
            pygame.draw.polygon(camera_surface, bcolor, points)

            # Inner danger symbol
            pygame.draw.circle(camera_surface, (255, 50, 50, 150),
                               (map_x, map_y), bsize // 2)

        elif btype == "player":
            # Fixed player arrow (pointing upward by default)
            # Use a simple upward-pointing triangle
            points = [
                (map_x, map_y - bsize),  # Tip
                (map_x - bsize, map_y + bsize // 2),  # Bottom left
                (map_x + bsize, map_y + bsize // 2)  # Bottom right
            ]
            pygame.draw.polygon(camera_surface, bcolor, points)

    # Draw distance rings with labels
    for i in range(1, 4):
        rr = int((cam_w // 2 - 6) * (i / 3))
        ring_alpha = 60 + i * 20
        pygame.draw.circle(camera_surface, (100, 120, 150, ring_alpha),
                           (cx, cy), rr, 1)

        # Add distance labels
        distance_label = int((i / 3) * RADAR_RANGE)
        label_font = pygame.font.SysFont("Arial", 10, bold=True)
        label_text = label_font.render(f"{distance_label}m", True, (150, 170, 190, 150))

        # Place labels at 4 positions
        positions = [
            (cx + rr - 10, cy - 10),
            (cx - rr + 10, cy - 10),
            (cx + rr - 10, cy + 10),
            (cx - rr + 10, cy + 10)
        ]
        for pos in positions:
            camera_surface.blit(label_text, pos)

    # Enhanced scanning line effect
    scan_length = cam_w // 2 - 10
    scan_x = cx + int(math.cos(radar_scan_angle) * scan_length)
    scan_y = cy + int(math.sin(radar_scan_angle) * scan_length)

    # Draw scanning line with gradient trail
    for i in range(20, 0, -1):
        alpha = 255 - i * 12
        length = scan_length * (1 - i / 25)
        trail_x = cx + int(math.cos(radar_scan_angle) * length)
        trail_y = cy + int(math.sin(radar_scan_angle) * length)
        pygame.draw.line(camera_surface, (*RADAR_SCAN[:3], alpha // 2),
                         (cx, cy), (trail_x, trail_y), 1)

    # Draw scanning arc
    arc_surface = pygame.Surface((cam_w, cam_h), pygame.SRCALPHA)
    arc_rect = pygame.Rect(0, 0, cam_w, cam_h)
    pygame.draw.arc(arc_surface, (*RADAR_SCAN[:3], 50), arc_rect,
                    radar_scan_angle - 0.2, radar_scan_angle + 0.2, 2)
    camera_surface.blit(arc_surface, (0, 0))

    # Blit camera into radar surface
    camera_rect = camera_surface.get_rect(center=(RADAR_SIZE[0] // 2, RADAR_SIZE[1] // 2 - 5))
    radar_surf.blit(camera_surface, camera_rect)

    # Enhanced border with animated glow
    border_glow = pygame.Surface((RADAR_SIZE[0] + 10, RADAR_SIZE[1] + 10), pygame.SRCALPHA)
    pulse_alpha = int(100 + 50 * math.sin(radar_pulse * 2))

    # Outer glow
    for i in range(3, 0, -1):
        glow_alpha = pulse_alpha // (i + 1)
        glow_size = 4 + i
        pygame.draw.rect(border_glow, (*NEON_CYAN[:3], glow_alpha),
                         (5 - i, 5 - i,
                          RADAR_SIZE[0] + 2 * i, RADAR_SIZE[1] + 2 * i),
                         glow_size, border_radius=10 + i)

    surface.blit(border_glow, (RADAR_POS[0] - 5, RADAR_POS[1] - 5))

    # Main border
    pygame.draw.rect(surface, NEON_CYAN,
                     (RADAR_POS[0], RADAR_POS[1],
                      RADAR_SIZE[0], RADAR_SIZE[1]), 2, border_radius=8)
    surface.blit(radar_surf, RADAR_POS)

    # Enhanced radar legend
    legend_y = RADAR_POS[1] + RADAR_SIZE[1] + 32
    legend_font = pygame.font.SysFont("Arial", 11)

    # Enemy count
    enemy_count = len([b for b in radar_blips if b["type"] == "enemy"])
    pygame.draw.circle(surface, RADAR_ENEMY, (RADAR_POS[0] + 10, legend_y), 4)
    enemy_text = legend_font.render(f"Enemies: {enemy_count}", True, WHITE)
    surface.blit(enemy_text, (RADAR_POS[0] + 20, legend_y - 8))

    # Closest enemy warning
    if closest_enemy_distance < RADAR_RANGE * 0.3:
        warning_text = legend_font.render(f"CLOSE: {int(closest_enemy_distance)}m",
                                          True, (255, 100, 100))
        surface.blit(warning_text, (RADAR_POS[0] + 120, legend_y - 8))

    # Hole legend
    hole_points = [(RADAR_POS[0] + 10, legend_y + 15),
                   (RADAR_POS[0] + 10 - 4, legend_y + 23),
                   (RADAR_POS[0] + 10 + 4, legend_y + 23)]
    pygame.draw.polygon(surface, RADAR_HOLE, hole_points)
    hole_text = legend_font.render("Hazards", True, WHITE)
    surface.blit(hole_text, (RADAR_POS[0] + 20, legend_y + 12))

    # Part count and legend
    part_count = len([b for b in radar_blips if b["type"] == "part"])
    pygame.draw.rect(surface, RADAR_PART,
                     (RADAR_POS[0] + 90, legend_y + 13, 6, 6))
    part_text = legend_font.render(f"Parts: {part_count}", True, WHITE)
    surface.blit(part_text, (RADAR_POS[0] + 102, legend_y + 12))

    # Range control hint
    range_hint = small_font.render("[Z/X] Change Range", True, (200, 200, 200, 150))
    surface.blit(range_hint, (RADAR_POS[0] + RADAR_SIZE[0] - range_hint.get_width() - 5,
                              legend_y + 15))

    # Range display
    range_text = small_font.render(f"Range: {RADAR_RANGE}m", True, WHITE)
    surface.blit(range_text, (RADAR_POS[0] + RADAR_SIZE[0] - range_text.get_width() - 5,
                              RADAR_POS[1] + RADAR_SIZE[1] + 5))

    # Range slider (visual representation)
    slider_width = 60
    slider_x = RADAR_POS[0] + RADAR_SIZE[0] - slider_width - 5
    slider_y = RADAR_POS[1] + RADAR_SIZE[1] + 20
    pygame.draw.rect(surface, (50, 50, 50),
                     (slider_x, slider_y, slider_width, 4))

    # Current range indicator on slider
    max_range = 1000  # Adjust this to your maximum radar range
    range_percent = RADAR_RANGE / max_range
    indicator_x = slider_x + int(slider_width * range_percent)
    pygame.draw.circle(surface, NEON_CYAN, (indicator_x, slider_y + 2), 4)

def draw_quantum_battery(surface, rect, dragging=False):

    pulse = (math.sin(pygame.time.get_ticks() / 400) + 1) / 2
    energy_color = (int(255 * pulse), 255, int(100 * pulse))
    draw_rounded_rect(surface, rect, NEON_YELLOW, 8)
    terminal_rect = pygame.Rect(rect.x + rect.width // 2 - 10, rect.y - 5, 20, 10)
    pygame.draw.rect(surface, SILVER, terminal_rect)
    core_radius = min(rect.width, rect.height) // 4
    core_pulse = (math.sin(pygame.time.get_ticks() / 200) + 1) / 2
    core_color = (int(255 * core_pulse), int(255 * core_pulse), 100)
    for i in range(3):
        radius = core_radius * (0.5 + 0.5 * (i / 3))
        alpha = 100 - i * 30
        s = pygame.Surface((int(radius * 2), int(radius * 2)), pygame.SRCALPHA)
        pygame.draw.circle(s, (*core_color, alpha), (int(radius), int(radius)), int(radius))
        surface.blit(s, (rect.centerx - radius, rect.centery - radius))
    level_width = rect.width - 20
    level_x = rect.x + 10
    level_y = rect.y + rect.height - 20
    fluctuation = math.sin(pygame.time.get_ticks() / 100) * 0.05
    current_level = int(level_width * max(0, min(1, BATTERY_LEVEL + fluctuation)))
    pygame.draw.rect(surface, DARK_GRAY, (level_x, level_y, level_width, 8))
    if current_level > 0:
        for i in range(int(current_level / 5)):
            segment_x = level_x + i * 5
            segment_pulse = (math.sin(pygame.time.get_ticks() / 100 + i) + 1) / 2
            segment_color = (int(255 * segment_pulse), 255, int(100 * segment_pulse))
            pygame.draw.rect(surface, segment_color, (segment_x, level_y, 4, 8))
    label_rect = pygame.Rect(rect.x + 10, rect.y + 10, rect.width - 20, 15)
    pygame.draw.rect(surface, BLACK, label_rect)
    temp_value = 20 + int(15 * pulse)
    temp_text = small_font.render(f"QUANTUM: {int(BATTERY_LEVEL * 100)}%", True, WHITE)
    temp_rect = temp_text.get_rect(center=label_rect.center)
    surface.blit(temp_text, temp_rect)
    if not dragging:
        field_radius = rect.width // 2 + 5
        field_alpha = int(50 + 30 * math.sin(pygame.time.get_ticks() / 200))
        field_surf = pygame.Surface((field_radius * 2, field_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(field_surf, (*energy_color, field_alpha), (field_radius, field_radius), field_radius)
        surface.blit(field_surf, (rect.centerx - field_radius, rect.centery - field_radius))


def draw_hydraulic_actuator(surface, rect, dragging=False):
    draw_rounded_rect(surface, rect, NEON_RED, 5)
    piston_offset = (math.sin(pygame.time.get_ticks() / 150) + 1) / 2 * (rect.width - 30)
    pygame.draw.rect(surface, SILVER, (rect.x + 10, rect.y + rect.height // 2 - 10, int(piston_offset), 20))
    fluid_width = int(rect.width * (0.3 + 0.7 * (math.sin(pygame.time.get_ticks() / 180) + 1) / 2))
    pygame.draw.rect(surface, (200, 50, 50),
                     (rect.x + (rect.width - fluid_width) // 2, rect.y + rect.height - 15, fluid_width, 6))
    for i in range(2):
        pygame.draw.circle(surface, GOLD, (rect.x + 5 + i * (rect.width - 15), rect.y + rect.height // 2), 3)
    if not dragging and random.random() < 0.02:
        create_particles(rect.centerx, rect.top, NEON_RED, 5, 0.5)


def draw_optical_sensor(surface, rect, dragging=False):
    pygame.draw.circle(surface, NEON_CYAN, rect.center, rect.width // 2)
    iris_radius = rect.width // 3
    iris_pulse = (math.sin(pygame.time.get_ticks() / 250) + 1) / 2
    iris_color = (int(50 * iris_pulse), int(150 + 105 * iris_pulse), int(200 + 55 * iris_pulse))
    pygame.draw.circle(surface, iris_color, rect.center, iris_radius)
    scan_angle = pygame.time.get_ticks() / 100
    pupil_offset_x = math.cos(scan_angle) * (iris_radius - iris_radius // 2) * 0.5
    pupil_offset_y = math.sin(scan_angle) * (iris_radius - iris_radius // 2) * 0.5
    pupil_pos = (rect.centerx + pupil_offset_x, rect.centery + pupil_offset_y)
    pygame.draw.circle(surface, BLACK, pupil_pos, iris_radius // 2)
    for i in range(2):
        refl_x = pupil_pos[0] - iris_radius // 3 + i * iris_radius // 2
        refl_y = pupil_pos[1] - iris_radius // 3
        pygame.draw.circle(surface, (150, 200, 255), (refl_x, refl_y), iris_radius // 9)
    if not dragging:
        scan_end_x = rect.centerx + 30 * math.cos(scan_angle)
        scan_end_y = rect.centery + 30 * math.sin(scan_angle)
        create_laser_effect(rect.center, (scan_end_x, scan_end_y), NEON_CYAN, 20)


def draw_audio_receiver(surface, rect, dragging=False):
    draw_rounded_rect(surface, rect, NEON_GREEN, 10)
    for i in range(3):
        wave_height = 5 + i * 2
        wave_width = rect.width - 10
        wave_x = rect.x + 5
        wave_y = rect.y + 5 + i * 8
        wave_points = []
        for j in range(10):
            point_x = wave_x + j * (wave_width / 9)
            point_y = wave_y + math.sin(j + pygame.time.get_ticks() / 80 + i) * wave_height
            wave_points.append((point_x, point_y))
        if len(wave_points) > 1:
            pygame.draw.lines(surface, (100, 255, 100), False, wave_points, 2)
    for i in range(4):
        for j in range(2):
            hole_x = rect.x + 10 + i * 8
            hole_y = rect.y + rect.height - 10 + j * 5
            pygame.draw.circle(surface, (50, 100, 50), (hole_x, hole_y), 2)
    if not dragging and random.random() < 0.03:
        create_particles(rect.centerx, rect.centery, NEON_GREEN, 3, 0.3)


def draw_tactile_pad(surface, rect, dragging=False):
    pygame.draw.circle(surface, NEON_BLUE, rect.center, rect.width // 2)
    for i in range(4):
        angle = i * math.pi / 2
        sensor_x = rect.centerx + (rect.width // 3) * math.cos(angle)
        sensor_y = rect.centery + (rect.height // 3) * math.sin(angle)
        sensor_pulse = (math.sin(pygame.time.get_ticks() / 200 + i) + 1) / 2
        sensor_color = (int(50 + 205 * sensor_pulse), int(100 + 155 * sensor_pulse), 255)
        pygame.draw.circle(surface, sensor_color, (sensor_x, sensor_y), 4)
    cluster_radius = rect.width // 6
    cluster_pulse = (math.sin(pygame.time.get_ticks() / 150) + 1) / 2
    pygame.draw.circle(surface, (100, 150, 255), rect.center, cluster_radius)
    pygame.draw.circle(surface, (50, 100, 200), rect.center, cluster_radius - 2)
    if not dragging and random.random() < 0.02:
        create_particles(rect.centerx, rect.centery, NEON_BLUE, 2, 0.2)


def draw_balance_gyro(surface, rect, dragging=False):
    pygame.draw.circle(surface, HOLO_BLUE, rect.center, rect.width // 2)
    ring_time = pygame.time.get_ticks() / 1000
    outer_radius = rect.width // 2 - 5
    outer_angle = ring_time * 2
    for i in range(8):
        angle = outer_angle + i * math.pi / 4
        marker_x = rect.centerx + outer_radius * math.cos(angle)
        marker_y = rect.centery + outer_radius * math.sin(angle)
        pygame.draw.circle(surface, NEON_BLUE, (marker_x, marker_y), 3)
    middle_radius = rect.width // 3
    middle_angle = -ring_time * 1.5
    for i in range(6):
        angle = middle_angle + i * math.pi / 3
        marker_x = rect.centerx + middle_radius * math.cos(angle)
        marker_y = rect.centery + middle_radius * math.sin(angle)
        pygame.draw.circle(surface, NEON_CYAN, (marker_x, marker_y), 2)
    inner_radius = rect.width // 6
    inner_angle = ring_time
    for i in range(4):
        angle = inner_angle + i * math.pi / 2
        marker_x = rect.centerx + inner_radius * math.cos(angle)
        marker_y = rect.centery + inner_radius * math.sin(angle)
        pygame.draw.circle(surface, WHITE, (marker_x, marker_y), 2)
    pygame.draw.circle(surface, BLACK, rect.center, 5)
    pygame.draw.circle(surface, NEON_BLUE, rect.center, 3)
    if not dragging:
        field_alpha = int(30 + 20 * math.sin(pygame.time.get_ticks() / 150))
        field_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.circle(field_surf, (*HOLO_BLUE, field_alpha), (rect.width // 2, rect.height // 2), rect.width // 2)
        surface.blit(field_surf, rect)


def draw_communication_array(surface, rect, dragging=False):
    draw_rounded_rect(surface, rect, HOLO_PINK, 5)
    for i in range(3):
        antenna_x = rect.x + 10 + i * 15
        antenna_top = rect.y - 5
        signal_pulse = (math.sin(pygame.time.get_ticks() / 200 + i) + 1) / 2
        signal_color = (int(255 * signal_pulse), int(100 + 155 * signal_pulse), int(200 + 55 * signal_pulse))
        pygame.draw.line(surface, SILVER, (antenna_x, rect.y + 15), (antenna_x, antenna_top), 2)
        pygame.draw.circle(surface, signal_color, (antenna_x, antenna_top), 3)
    processor_rect = pygame.Rect(rect.x + 5, rect.y + 20, rect.width - 10, rect.height - 40)
    pygame.draw.rect(surface, BLACK, processor_rect)
    for i in range(4):
        indicator_x = processor_rect.x + 5 + i * 10
        indicator_height = 5 + (i % 3) * 3
        indicator_pulse = (math.sin(pygame.time.get_ticks() / 150 + i) + 1) / 2
        indicator_color = (int(255 * indicator_pulse), int(100 + 155 * indicator_pulse), 255)
        pygame.draw.rect(surface, indicator_color, (
            indicator_x, processor_rect.y + processor_rect.height - indicator_height - 5, 5, indicator_height))
    if not dragging and random.random() < 0.01:
        create_laser_effect((rect.centerx, rect.top), (rect.centerx, rect.top - 50), HOLO_PINK, 30)


def draw_thermal_regulator(surface, rect, dragging=False):
    draw_rounded_rect(surface, rect, HOLO_GREEN, 8)
    fin_count = 5
    fin_width = rect.width // (fin_count + 1)
    for i in range(fin_count):
        fin_x = rect.x + (i + 1) * fin_width
        temp_factor = i / (fin_count - 1) if fin_count > 1 else 0.5
        fin_color = (int(50 + 205 * temp_factor), int(150 + 105 * (1 - temp_factor)), int(50 + 50 * temp_factor))
        pygame.draw.rect(surface, fin_color, (fin_x - 2, rect.y + 10, 4, rect.height - 20))
    display_rect = pygame.Rect(rect.x + 10, rect.y + rect.height - 25, rect.width - 20, 15)
    pygame.draw.rect(surface, BLACK, display_rect)
    temp_pulse = (math.sin(pygame.time.get_ticks() / 300) + 1) / 2
    temp_value = 20 + int(15 * temp_pulse)
    temp_text = small_font.render(f"{temp_value}°C", True, HOLO_GREEN)
    temp_rect = temp_text.get_rect(center=display_rect.center)
    surface.blit(temp_text, temp_rect)
    if not dragging:
        heat_alpha = int(30 + 20 * math.sin(pygame.time.get_ticks() / 250))
        heat_surf = pygame.Surface((rect.width + 10, rect.height + 10), pygame.SRCALPHA)
        pygame.draw.rect(heat_surf, (*HOLO_GREEN, heat_alpha), (0, 0, rect.width + 10, rect.height + 10),
                         border_radius=12)
        surface.blit(heat_surf, (rect.x - 5, rect.y - 5))


def draw_mobility_core(surface, rect, dragging=False):
    pulse = (math.sin(pygame.time.get_ticks() / 400) + 1) / 2
    core_color = (int(CYBER_BLUE[0] * (0.7 + 0.3 * pulse)), int(CYBER_BLUE[1] * (0.7 + 0.3 * pulse)),
                  int(CYBER_BLUE[2] * (0.7 + 0.3 * pulse)))
    draw_rounded_rect(surface, rect, core_color, 10)
    cpu_radius = rect.width // 4
    cpu_pulse = (math.sin(pygame.time.get_ticks() / 150) + 1) / 2
    cpu_color = (int(50 + 205 * cpu_pulse), int(100 + 155 * cpu_pulse), 255)
    pygame.draw.circle(surface, cpu_color, rect.center, cpu_radius)
    for i in range(4):
        angle = i * math.pi / 2
        vector_length = rect.width // 3
        end_x = rect.centerx + vector_length * math.cos(angle)
        end_y = rect.centery + vector_length * math.sin(angle)
        vector_pulse = (math.sin(pygame.time.get_ticks() / 200 + i) + 1) / 2
        vector_color = (int(255 * vector_pulse), int(150 + 105 * vector_pulse), 50)
        pygame.draw.line(surface, vector_color, rect.center, (end_x, end_y), 3)
        pygame.draw.circle(surface, vector_color, (end_x, end_y), 4)
    stream_rect = pygame.Rect(rect.x + 5, rect.y + 5, rect.width - 10, 8)
    pygame.draw.rect(surface, BLACK, stream_rect)
    stream_offset = pygame.time.get_ticks() // 50 % 20
    for i in range(3):
        dot_x = stream_rect.x + (i * 7 + stream_offset) % stream_rect.width
        pygame.draw.circle(surface, NEON_BLUE, (dot_x, stream_rect.centery), 2)
    if not dragging:
        field_alpha = int(40 + 30 * math.sin(pygame.time.get_ticks() / 180))
        field_surf = pygame.Surface((rect.width + 20, rect.height + 20), pygame.SRCALPHA)
        pygame.draw.rect(field_surf, (*CYBER_BLUE, field_alpha), (0, 0, rect.width + 20, rect.height + 20),
                         border_radius=15)
        surface.blit(field_surf, (rect.x - 10, rect.y - 10))


# OPTIMIZED: Simplified drawing for dragging parts
def draw_part(surface, part, alpha=255):
    if part["dragging"]:
        # Simplified drawing for dragging parts - remove complex effects
        s = pygame.Surface((part["rect"].width, part["rect"].height), pygame.SRCALPHA)
        temp_rect = pygame.Rect(0, 0, part["rect"].width, part["rect"].height)

        # Draw simplified version without animations
        if part["type"] == "Neural Processor":
            draw_rounded_rect(s, temp_rect, NEON_PURPLE, 5)
        elif part["type"] == "Quantum Battery":
            draw_rounded_rect(s, temp_rect, NEON_YELLOW, 8)
        elif part["type"] == "Hydraulic Actuator":
            draw_rounded_rect(s, temp_rect, NEON_RED, 5)
        elif part["type"] == "Optical Sensor":
            pygame.draw.circle(s, NEON_CYAN, temp_rect.center, temp_rect.width // 2)
        elif part["type"] == "Audio Receiver":
            draw_rounded_rect(s, temp_rect, NEON_GREEN, 10)
        elif part["type"] == "Tactile Pad":
            pygame.draw.circle(s, NEON_BLUE, temp_rect.center, temp_rect.width // 2)
        elif part["type"] == "Balance Gyro":
            pygame.draw.circle(s, HOLO_BLUE, temp_rect.center, temp_rect.width // 2)
        elif part["type"] == "Communication Array":
            draw_rounded_rect(s, temp_rect, HOLO_PINK, 5)
        elif part["type"] == "Thermal Regulator":
            draw_rounded_rect(s, temp_rect, HOLO_GREEN, 8)
        elif part["type"] == "Mobility Core":
            draw_rounded_rect(s, temp_rect, CYBER_BLUE, 10)

        s.set_alpha(200)  # Slightly more opaque when dragging
        surface.blit(s, part["rect"])

        # Simplified shadow
        shadow = pygame.Surface((part["rect"].width + 6, part["rect"].height + 6), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0, 0, 0, 80), (0, 0, part["rect"].width + 6, part["rect"].height + 6),
                         border_radius=part["radius"] + 3)
        surface.blit(shadow, (part["rect"].x - 3, part["rect"].y - 3))
    else:
        def draw_neural_processor(surface, rect, dragging=False):
            # Draw neural processor with animated neural connections
            draw_rounded_rect(surface, rect, NEON_PURPLE, 5)

            # Draw circuit lines inside
            circuit_color = (180, 50, 255)
            for i in range(4):
                y_pos = rect.y + 10 + i * (rect.height - 20) / 3
                pygame.draw.line(surface, circuit_color,
                                 (rect.x + 10, y_pos),
                                 (rect.x + rect.width - 10, y_pos), 2)

            # Draw neural nodes
            node_pulse = (math.sin(pygame.time.get_ticks() / 300) + 1) / 2
            node_radius = 6
            for i in range(3):
                for j in range(2):
                    node_x = rect.x + 15 + i * (rect.width - 30) / 2
                    node_y = rect.y + 15 + j * (rect.height - 30)
                    node_color = (int(255 * node_pulse), int(50 + 100 * node_pulse), 255)
                    pygame.draw.circle(surface, node_color, (int(node_x), int(node_y)), node_radius)

                    # Draw connecting lines between nodes
                    if i < 2:
                        next_x = rect.x + 15 + (i + 1) * (rect.width - 30) / 2
                        pygame.draw.line(surface, NEON_PURPLE,
                                         (node_x, node_y),
                                         (next_x, node_y), 1)

            # Draw processor core in center
            core_radius = 12
            core_pulse = (math.sin(pygame.time.get_ticks() / 200) + 1) / 2
            core_color = (int(255 * core_pulse), 100, int(255 * core_pulse))
            pygame.draw.circle(surface, core_color, rect.center, core_radius)

            # Draw data stream animation
            stream_offset = pygame.time.get_ticks() // 50 % 20
            stream_rect = pygame.Rect(rect.x + 5, rect.y + rect.height - 15, rect.width - 10, 5)
            pygame.draw.rect(surface, DARK_GRAY, stream_rect)

            for i in range(3):
                stream_x = stream_rect.x + (i * 10 + stream_offset) % stream_rect.width
                pygame.draw.rect(surface, NEON_CYAN,
                                 (stream_x, stream_rect.y, 4, stream_rect.height))

            # Draw neural field effect when not dragging
            if not dragging:
                field_alpha = int(30 + 20 * math.sin(pygame.time.get_ticks() / 250))
                field_surf = pygame.Surface((rect.width + 20, rect.height + 20), pygame.SRCALPHA)
                pygame.draw.rect(field_surf, (*NEON_PURPLE, field_alpha),
                                 (0, 0, rect.width + 20, rect.height + 20),
                                 border_radius=15)
                surface.blit(field_surf, (rect.x - 10, rect.y - 10))
        # Full drawing with effects for stationary parts
        if part["type"] == "Neural Processor":
            draw_neural_processor(surface, part["rect"])
        elif part["type"] == "Quantum Battery":
            draw_quantum_battery(surface, part["rect"])
        elif part["type"] == "Hydraulic Actuator":
            draw_hydraulic_actuator(surface, part["rect"])
        elif part["type"] == "Optical Sensor":
            draw_optical_sensor(surface, part["rect"])
        elif part["type"] == "Audio Receiver":
            draw_audio_receiver(surface, part["rect"])
        elif part["type"] == "Tactile Pad":
            draw_tactile_pad(surface, part["rect"])
        elif part["type"] == "Balance Gyro":
            draw_balance_gyro(surface, part["rect"])
        elif part["type"] == "Communication Array":
            draw_communication_array(surface, part["rect"])
        elif part["type"] == "Thermal Regulator":
            draw_thermal_regulator(surface, part["rect"])
        elif part["type"] == "Mobility Core":
            draw_mobility_core(surface, part["rect"])


def draw_cyber_lab(surface):
    wall_color = (25, 30, 45)
    pygame.draw.rect(surface, wall_color, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    grid_color = (35, 40, 55)
    grid_size = 80
    for x in range(0, SCREEN_WIDTH, grid_size):
        pygame.draw.line(surface, grid_color, (x, 0), (x, SCREEN_HEIGHT), 1)
    for y in range(0, SCREEN_HEIGHT, grid_size):
        pygame.draw.line(surface, grid_color, (0, y), (SCREEN_WIDTH, y), 1)
    for x in range(grid_size // 2, SCREEN_WIDTH, grid_size):
        for y in range(grid_size // 2, SCREEN_HEIGHT, grid_size):
            node_pulse = (math.sin(pygame.time.get_ticks() / 1000 + x + y) + 1) / 2
            node_color = (int(50 + 50 * node_pulse), int(100 + 50 * node_pulse), int(150 + 50 * node_pulse))
            pygame.draw.circle(surface, node_color, (x, y), 2)
    for i in range(3):
        station_x = 100 + i * 300
        station_y = SCREEN_HEIGHT - 200
        base_rect = pygame.Rect(station_x - 80, station_y, 160, 30)
        draw_rounded_rect(surface, base_rect, (40, 45, 60), 5)
        for j in range(2):
            display_x = station_x - 60 + j * 80
            display_rect = pygame.Rect(display_x - 25, station_y - 120, 50, 80)
            hologram_alpha = int(100 + 50 * math.sin(pygame.time.get_ticks() / 500 + i + j))
            hologram_surf = pygame.Surface((50, 80), pygame.SRCALPHA)
            pygame.draw.rect(hologram_surf, (*NEON_BLUE, hologram_alpha), (0, 0, 50, 80), border_radius=5)
            surface.blit(hologram_surf, (display_x - 25, station_y - 120))
            content_lines = random.randint(3, 6)
            for k in range(content_lines):
                line_y = station_y - 110 + k * 12
                line_width = random.randint(20, 40)
                pygame.draw.rect(surface, NEON_CYAN, (display_x - line_width // 2, line_y, line_width, 3))
    for i in range(5):
        conduit_x = 150 + i * 200
        conduit_rect = pygame.Rect(conduit_x - 60, 50, 120, 10)
        pygame.draw.rect(surface, (50, 55, 70), conduit_rect)
        energy_pos = (pygame.time.get_ticks() // 30 + i * 40) % 120
        energy_rect = pygame.Rect(conduit_x - 60 + energy_pos, 50, 20, 10)
        pygame.draw.rect(surface, NEON_BLUE, energy_rect)


def draw_cyber_street(surface, offset):
    # Draw night sky
    sky_color = (10, 15, 30)
    pygame.draw.rect(surface, sky_color, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    # Draw stars
    for i in range(100):
        star_x = (i * 71) % SCREEN_WIDTH
        star_y = (i * 53) % (SCREEN_HEIGHT // 2)
        star_size = 1 + (i % 3)
        star_brightness = 100 + (i % 155)
        pygame.draw.circle(surface, (star_brightness, star_brightness, star_brightness), (star_x, star_y), star_size)

    # Draw moving stars (shooting stars)
    for i in range(3):
        star_time = pygame.time.get_ticks() // 50 + i * 1000
        star_x = star_time % (SCREEN_WIDTH + 100) - 50
        star_y = 50 + (i * 40) % 100
        star_length = 20 + (i * 5)
        pygame.draw.line(surface, WHITE, (star_x, star_y), (star_x - star_length, star_y - star_length // 2), 2)

    # Draw street
    street_color = (30, 30, 35)
    street_rect = pygame.Rect(0, SCREEN_HEIGHT - 200, SCREEN_WIDTH, 200)
    pygame.draw.rect(surface, street_color, street_rect)

    # Draw street markings (moving with offset)
    marking_color = (200, 200, 220)
    marking_width = 20
    marking_height = 10
    marking_spacing = 60

    for i in range(-1, SCREEN_WIDTH // marking_spacing + 2):
        x_pos = (i * marking_spacing + offset) % (SCREEN_WIDTH + marking_spacing) - marking_spacing
        marking_rect = pygame.Rect(x_pos, SCREEN_HEIGHT - 100, marking_width, marking_height)
        pygame.draw.rect(surface, marking_color, marking_rect)

    # Draw sidewalk
    sidewalk_color = (40, 40, 45)
    sidewalk_rect = pygame.Rect(0, SCREEN_HEIGHT - 200, SCREEN_WIDTH, 20)
    pygame.draw.rect(surface, sidewalk_color, sidewalk_rect)

    # Draw buildings (simplified)
    for i in range(10):
        building_x = (i * 200 - offset * 0.5) % (SCREEN_WIDTH + 400) - 200
        building_width = 150
        building_height = 300 + random.randint(0, 200)
        building_y = SCREEN_HEIGHT - 200 - building_height

        building_color = (30 + i * 2, 35 + i * 2, 50 + i * 2)
        pygame.draw.rect(surface, building_color, (building_x, building_y, building_width, building_height))

        # Draw building windows
        window_rows = building_height // 40
        window_cols = building_width // 30
        for row in range(window_rows):
            for col in range(window_cols):
                window_x = building_x + 10 + col * 30
                window_y = building_y + 10 + row * 40

                # Random window lights
                if random.random() > 0.3:
                    window_color = random.choice([NEON_BLUE, NEON_CYAN, NEON_PURPLE, NEON_YELLOW])
                    pygame.draw.rect(surface, window_color, (window_x, window_y, 15, 25))


# FIXED: Move components title to bottom of panel
def draw_parts_panel(surface):
    max_part_width = max(part["rect"].width for part in parts) if parts else 80
    panel_width = max(350, 50 + 3 * (max_part_width + 20))
    panel_rect = pygame.Rect(30, 120, panel_width, SCREEN_HEIGHT - 200)
    for i in range(panel_rect.height):
        gradient_factor = i / panel_rect.height
        line_color = (int(30 + 10 * gradient_factor), int(35 + 10 * gradient_factor), int(50 + 10 * gradient_factor))
        pygame.draw.line(surface, line_color, (panel_rect.x, panel_rect.y + i),
                         (panel_rect.x + panel_rect.width, panel_rect.y + i))
    border_glow = pygame.Surface((panel_rect.width + 10, panel_rect.height + 10), pygame.SRCALPHA)
    pygame.draw.rect(border_glow, (*NEON_BLUE, 80), (0, 0, panel_rect.width + 10, panel_rect.height + 10),
                     border_radius=12)
    surface.blit(border_glow, (panel_rect.x - 5, panel_rect.y - 5))
    pygame.draw.rect(surface, (40, 45, 60), panel_rect, border_radius=10)
    pygame.draw.rect(surface, NEON_BLUE, panel_rect, 3, border_radius=10)

    # MOVED: Title to bottom of panel
    title_text = font.render("CYBERNETIC COMPONENTS", True, NEON_CYAN)
    title_y = panel_rect.bottom - 30
    surface.blit(title_text, (panel_rect.centerx - title_text.get_width() // 2, title_y))

    # Draw divider line at the top
    pygame.draw.line(surface, (70, 75, 85), (panel_rect.x, panel_rect.y + 30),
                     (panel_rect.x + panel_rect.width, panel_rect.y + 30), 2)


def draw_slot(surface, slot, parts):
    slot_filled = any(part["placed"] and part["placed_slot"] == slot for part in parts)
    if slot_filled:
        color = NEON_GREEN
        glow_rect = slot["rect"].inflate(20, 20)
        s = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
        for i in range(3):
            layer_size = glow_rect.inflate(-i * 5, -i * 5)
            layer_alpha = 80 - i * 20
            pygame.draw.rect(s, (*NEON_GREEN, layer_alpha), (i * 2, i * 2, layer_size.width, layer_size.height),
                             border_radius=15 - i * 3)
        surface.blit(s, glow_rect)
        if random.random() < 0.02:
            create_particles(slot["rect"].centerx, slot["rect"].centery, NEON_GREEN, 2, 0.5)
    else:
        pulse = (math.sin(pygame.time.get_ticks() / 300) + 1) / 2
        color = (int(255 * pulse), int(50 + 50 * pulse), int(50 + 50 * pulse))
        pulse_rect = slot["rect"].inflate(10, 10)
        s = pygame.Surface((pulse_rect.width, pulse_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(s, (*color, 60), (0, 0, pulse_rect.width, pulse_rect.height), border_radius=12)
        surface.blit(s, pulse_rect)
    draw_rounded_rect(surface, slot["rect"], color, 8)
    text = font.render(slot["type"], True, WHITE)
    text_rect = text.get_rect(center=slot["rect"].center)
    text_glow = pygame.Surface((text_rect.width + 4, text_rect.height + 4), pygame.SRCALPHA)
    pygame.draw.rect(text_glow, (*color, 100), (0, 0, text_rect.width + 4, text_rect.height + 4), border_radius=3)
    surface.blit(text_glow, (text_rect.x - 2, text_rect.y - 2))
    surface.blit(text, text_rect)


def draw_wires(surface, slots, parts):
    global WIRE_ANIMATION
    WIRE_ANIMATION += 0.03
    for i, slot in enumerate(slots):
        part_in_slot = next((p for p in parts if p["placed"] and p["placed_slot"] == slot), None)
        if part_in_slot:
            for conn_idx in slot["connected_to"]:
                conn_slot = slots[conn_idx]
                conn_part = next((p for p in parts if p["placed"] and p["placed_slot"] == conn_slot), None)
                if conn_part:
                    start = part_in_slot["rect"].center
                    end = conn_part["rect"].center
                    control_x = (start[0] + end[0]) // 2
                    control_y = min(start[1], end[1]) - 80
                    points = []
                    for t in range(0, 101, 5):
                        t /= 100
                        x = (1 - t) ** 2 * start[0] + 2 * (1 - t) * t * control_x + t ** 2 * end[0]
                        y = (1 - t) ** 2 * start[1] + 2 * (1 - t) * t * control_y + t ** 2 * end[1]
                        points.append((x, y))
                    if len(points) > 1:
                        trail_points = []
                        for j in range(len(points) - 1):
                            trail_t = (WIRE_ANIMATION + j * 0.1) % 1
                            if 0 <= trail_t < 1:
                                idx = int(trail_t * (len(points) - 1))
                                if idx < len(points) - 1:
                                    t2 = trail_t * (len(points) - 1) - idx
                                    tx = points[idx][0] + t2 * (points[idx + 1][0] - points[idx][0])
                                    ty = points[idx][1] + t2 * (points[idx + 1][1] - points[idx][1])
                                    trail_points.append((tx, ty))
                        if len(trail_points) > 1:
                            pygame.draw.lines(surface, (*NEON_BLUE, 150), False, trail_points, 4)
                        pygame.draw.lines(surface, NEON_ORANGE, False, points, 3)
                        for pos in [start, end]:
                            pygame.draw.circle(surface, NEON_ORANGE, pos, 6)
                            glow_surf = pygame.Surface((20, 20), pygame.SRCALPHA)
                            pygame.draw.circle(glow_surf, (*NEON_ORANGE, 100), (10, 10), 10)
                            surface.blit(glow_surf, (pos[0] - 10, pos[1] - 10))


def check_win_condition(parts, slots):
    return all(any(p["placed"] and p["placed_slot"] == s and p["type"] == s["type"] for p in parts) for s in slots)


# CHANGED: Score moved to right side and made more top
def draw_score(surface):
    score_panel = pygame.Rect(SCREEN_WIDTH - 280, 20, 260, 80)  # CHANGED: Position to right side, moved up
    for i in range(score_panel.height):
        gradient_factor = i / score_panel.height
        line_color = (int(30 + 10 * gradient_factor), int(35 + 10 * gradient_factor), int(50 + 10 * gradient_factor))
        pygame.draw.line(surface, line_color, (score_panel.x, score_panel.y + i),
                         (score_panel.x + score_panel.width, score_panel.y + i))
    border_glow = pygame.Surface((score_panel.width + 10, score_panel.height + 10), pygame.SRCALPHA)
    pygame.draw.rect(border_glow, (*NEON_BLUE, 80), (0, 0, score_panel.width + 10, score_panel.height + 10),
                     border_radius=12)
    surface.blit(border_glow, (score_panel.x - 5, score_panel.y - 5))
    pygame.draw.rect(surface, (40, 45, 60), score_panel, border_radius=10)
    pygame.draw.rect(surface, NEON_BLUE, score_panel, 3, border_radius=10)
    score_text = font.render(f"SCORE: {SCORE}", True, NEON_CYAN)
    surface.blit(score_text, (SCREEN_WIDTH - 270, 30))  # CHANGED: Position to right side
    if COMBO > 1:
        combo_text = font.render(f"COMBO: x{COMBO}", True, NEON_GREEN)
        surface.blit(combo_text, (SCREEN_WIDTH - 270, 55))  # moved under score text
        combo_pulse = (math.sin(pygame.time.get_ticks() / 150) + 1) / 2
        combo_glow = pygame.Surface((combo_text.get_width() + 15, combo_text.get_height() + 10), pygame.SRCALPHA)
        pygame.draw.rect(combo_glow, (*NEON_GREEN, int(50 + 30 * combo_pulse)),
                         (0, 0, combo_text.get_width() + 15, combo_text.get_height() + 10), border_radius=8)
        surface.blit(combo_glow, (SCREEN_WIDTH - 275, 170))  # CHANGED: Position to right side
    level_text = small_font.render("LEVEL 3 - CYBER CANINE", True, NEON_PURPLE)
    surface.blit(level_text, (SCREEN_WIDTH - 270, 195))  # CHANGED: Position to right side


# NEW: Reset game function
def reset_game():
    global parts, part_id, game_state, cyber_canine_x, cyber_canine_y, leg_animation, run_cycle
    global COMBO, ELECTRONIC_PARTS, ENEMY_ROBOT_DOGS, STREET_HOLES, ENEMY_SPAWN_TIMER, PART_SPAWN_TIMER, HOLE_SPAWN_TIMER
    global PARTS_COLLECTED, GAME_OVER, SCORE, JUMPING, JUMP_VELOCITY, HEALTH, INVINCIBLE_TIMER
    global KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, KEYBOARD_CONTROL, victory_start_time, PAUSED
    global testing_start_time, engineer_x, engineer_y, engineer_animation, testing_progress, current_test_message, message_timer
    global engineer_angle, electric_spark_timer, background_music_playing, LAST_ENEMY_X
    global victory_scale, victory_pulse, victory_glow, victory_sparks, radar_scan_angle, radar_pulse, radar_blips
    global current_pattern_index, pattern_timer, robot_dog_current_color, color_transition_progress  # NEW: Reset color variables

    # Reset parts
    parts = []
    part_id = 0
    for part_type, part_info in PARTS.items():
        for i in range(part_info["count"]):
            column = part_id // parts_per_column
            row = part_id % parts_per_column
            x_pos = 50 + column * column_spacing
            y_pos = 150 + row * 110
            parts.append({
                "id": part_id,
                "type": part_type,
                "rect": pygame.Rect(x_pos, y_pos, part_info["size"][0], part_info["size"][1]),
                "color": part_info["color"],
                "radius": part_info["radius"],
                "dragging": False,
                "placed": False,
                "placed_slot": None,
                "original_pos": (x_pos, y_pos)
            })
            part_id += 1

    # Reset game state
    game_state = ASSEMBLY_STATE
    SHOW_ROBOTDOG_IMAGE = True
    cyber_canine_x = SCREEN_WIDTH // 4
    cyber_canine_y = GROUND_LEVEL - 100
    leg_animation = 0
    run_cycle = 0
    COMBO = 0
    ELECTRONIC_PARTS = []
    ENEMY_ROBOT_DOGS = []
    STREET_HOLES = []
    ENEMY_SPAWN_TIMER = 0
    PART_SPAWN_TIMER = 0
    HOLE_SPAWN_TIMER = 0
    PARTS_COLLECTED = 0
    GAME_OVER = False
    SCORE = 0
    JUMPING = False
    JUMP_VELOCITY = 0
    HEALTH = 3
    INVINCIBLE_TIMER = 0
    LAST_ENEMY_X = SCREEN_WIDTH

    KEY_LEFT = False
    KEY_RIGHT = False
    KEY_UP = False
    KEY_DOWN = False
    KEYBOARD_CONTROL = False
    victory_start_time = 0
    PAUSED = False

    # Reset robot dog color
    robot_dog_current_color = list(ROBOT_DOG_BASE_COLOR)
    color_transition_progress = 0.0

    # Reset victory display
    victory_scale = 1.0
    victory_pulse = 0.0
    victory_glow = 0.0
    victory_sparks = []

    # Reset radar
    radar_scan_angle = 0
    radar_pulse = 0
    radar_blips = []

    # Reset testing state
    testing_start_time = 0
    engineer_x = SCREEN_WIDTH + 100
    engineer_y = SCREEN_HEIGHT // 2
    engineer_animation = 0
    testing_progress = 0
    current_test_message = 0
    message_timer = 0

    # Reset engineer movement
    engineer_angle = 0
    electric_spark_timer = 0

    # Reset music
    stop_background_music()
    background_music_playing = False

    # Reset pattern variables
    current_pattern_index = 0
    pattern_timer = 0

    reset_joystick()


# NEW: Go to main menu function
def go_to_main_menu():
    stop_background_music()  # NEW: Stop music when going to main menu
    pygame.quit()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    menu_path = os.path.join(script_dir, "main_menu.py")
    try:
        if sys.platform == "win32":
            subprocess.Popen([sys.executable, menu_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen([sys.executable, menu_path])
    except Exception as e:
        print(f"Failed to launch main_menu.py: {e}")
    sys.exit()


# NEW: Spawn multiple electronic parts in a row
def spawn_electronic_parts_group(count=3):
    for i in range(count):
        part = {
            "x": SCREEN_WIDTH + 50 + i * 80,  # Space them out
            "y": random.randint(GROUND_LEVEL - 150, GROUND_LEVEL - 50),
            "speed": random.uniform(4.0, 6.0),
            "radius": random.randint(15, 25),
            "color": random.choice([NEON_RED, NEON_GREEN, NEON_BLUE, NEON_PURPLE, NEON_CYAN, NEON_YELLOW]),
            "type": random.choice(["circuit", "chip", "battery", "sensor"]),
            "rotation": 0,
            "rotation_speed": random.uniform(-0.05, 0.05),
            "color_progress": 0,
            "collection_time": 0
        }
        ELECTRONIC_PARTS.append(part)


# Main game loop
clock = pygame.time.Clock()
dragging_part = None
offset_x, offset_y = 0, 0
game_state = LEVEL_INTRO_STATE
intro_timer = 0
success_timer = 0


# Add escape key functionality to quit and return to menu
def check_quit():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        go_to_main_menu()


while True:
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not PAUSED:  # NEW: Only handle game events if not paused
            if game_state == ASSEMBLY_STATE:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # NEW: Check if control buttons were clicked
                    escape_hover, pause_hover = draw_control_buttons(screen, mouse_pos)
                    if escape_hover:
                        go_to_main_menu()
                    elif pause_hover:
                        PAUSED = True
                    else:
                        for part in parts:
                            if part["rect"].collidepoint(event.pos) and not part["placed"]:
                                part["dragging"] = True
                                dragging_part = part
                                offset_x = part["rect"].x - event.pos[0]
                                offset_y = part["rect"].y - event.pos[1]
                                break
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and dragging_part:
                    dragging_part["dragging"] = False
                    part_placed = False
                    for slot in SLOTS:
                        if (slot["rect"].colliderect(dragging_part["rect"]) and dragging_part["type"] == slot["type"]):
                            if not any(p["placed"] and p["placed_slot"] == slot for p in parts):
                                dragging_part["rect"].center = slot["rect"].center
                                dragging_part["placed"] = True
                                dragging_part["placed_slot"] = slot
                                current_time = pygame.time.get_ticks()
                                if current_time - LAST_PLACEMENT_TIME < 2000:
                                    COMBO += 1
                                else:
                                    COMBO = 1
                                SCORE += 15 * COMBO
                                LAST_PLACEMENT_TIME = current_time
                                create_particles(slot["rect"].centerx, slot["rect"].centery, dragging_part["color"], 20,
                                                 1.2)
                                create_laser_effect((slot["rect"].centerx, slot["rect"].top - 10),
                                                    (slot["rect"].centerx, slot["rect"].top - 50),
                                                    dragging_part["color"],
                                                    60)
                                part_placed = True
                                break
                    if not part_placed:
                        dragging_part["rect"].topleft = dragging_part["original_pos"]
                        COMBO = 0
                        create_cyber_glitch(dragging_part["rect"].centerx, dragging_part["rect"].centery, 15)
                    dragging_part = None
                    if check_win_condition(parts, SLOTS):
                        game_state = SUCCESS_STATE
                        success_timer = pygame.time.get_ticks()
                        SCORE += 200 * COMBO if COMBO > 0 else 200
                elif event.type == pygame.MOUSEMOTION and dragging_part:
                    # OPTIMIZED: Direct position updates for responsive dragging
                    dragging_part["rect"].x = event.pos[0] + offset_x
                    dragging_part["rect"].y = event.pos[1] + offset_y

            # NEW: Handle joystick dragging in running state
            elif game_state == RUNNING_STATE:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        # NEW: Check if control buttons were clicked
                        escape_hover, pause_hover = draw_control_buttons(screen, mouse_pos)
                        if escape_hover:
                            go_to_main_menu()
                        elif pause_hover:
                            PAUSED = True
                        else:
                            # Check if mouse is over joystick handle
                            dx = event.pos[0] - joystick_handle_pos[0]
                            dy = event.pos[1] - joystick_handle_pos[1]
                            distance = math.sqrt(dx * dx + dy * dy)

                            if distance <= joystick_handle_radius:
                                joystick_dragging = True

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and joystick_dragging:
                        joystick_dragging = False
                        reset_joystick()

                elif event.type == pygame.MOUSEMOTION:
                    if joystick_dragging:
                        update_joystick(event.pos)

        # NEW: Handle keyboard controls for movement and jumping
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # NEW: P key to toggle pause
                PAUSED = not PAUSED
            elif event.key == pygame.K_a and game_state == RUNNING_STATE and not PAUSED:
                KEY_LEFT = True
                KEYBOARD_CONTROL = True
            elif event.key == pygame.K_d and game_state == RUNNING_STATE and not PAUSED:
                KEY_RIGHT = True
                KEYBOARD_CONTROL = True
            elif event.key == pygame.K_w and game_state == RUNNING_STATE and not PAUSED:
                KEY_UP = True
                KEYBOARD_CONTROL = True
            elif event.key == pygame.K_s and game_state == RUNNING_STATE and not PAUSED:
                KEY_DOWN = True
                KEYBOARD_CONTROL = True
            elif event.key == pygame.K_SPACE and game_state == RUNNING_STATE:
                # Jump if not already jumping
                if not JUMPING and cyber_canine_y >= GROUND_LEVEL - 100 and not PAUSED:
                    JUMPING = True
                    JUMP_VELOCITY = JUMP_STRENGTH
                    play_jump_sound()
            # NEW: Handle restart
            elif event.key == pygame.K_r and (GAME_OVER or PARTS_COLLECTED >= TOTAL_PARTS_TO_COLLECT) and not PAUSED:
                reset_game()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                KEY_LEFT = False
            elif event.key == pygame.K_d:
                KEY_RIGHT = False
            elif event.key == pygame.K_w:
                KEY_UP = False
            elif event.key == pygame.K_s:
                KEY_DOWN = False

    check_quit()

    if not PAUSED:  # NEW: Only update game state if not paused
        # Update invincibility timer
        if INVINCIBLE_TIMER > 0:
            INVINCIBLE_TIMER -= 1

        # Update robot dog color
        update_robot_dog_color()

        if game_state == LEVEL_INTRO_STATE:
            intro_timer += clock.get_time()
            if intro_timer > 5000:
                game_state = ASSEMBLY_STATE
        elif game_state == SUCCESS_STATE:
            if pygame.time.get_ticks() - success_timer > 3000:
                game_state = TESTING_STATE
                testing_start_time = pygame.time.get_ticks()
                SHOW_ROBOTDOG_IMAGE = True
        elif game_state == TESTING_STATE:
            # NEW: Start background music when entering testing state if not already playing
            if not background_music_playing:
                play_background_music()

            # Update engineer position and animation
            engineer_animation += 0.1
            engineer_angle += 0.03  # Move in circular path around the dog

            # Calculate circular movement around the cyber canine
            radius = 180  # Distance from the dog
            engineer_x = SCREEN_WIDTH // 2 + math.cos(engineer_angle) * radius
            engineer_y = SCREEN_HEIGHT // 2 + math.sin(engineer_angle) * radius

            # Update testing progress
            elapsed_time = pygame.time.get_ticks() - testing_start_time
            testing_progress = min(1.0, elapsed_time / testing_duration)

            # Update test messages
            message_timer += clock.get_time()
            if message_timer > 1200:  # Change message every 1.2 seconds
                message_timer = 0
                current_test_message = min(current_test_message + 1, len(testing_messages) - 1)

            # Create electric spark effects periodically
            electric_spark_timer += 1
            if electric_spark_timer > 20:  # Create sparks every 20 frames
                electric_spark_timer = 0
                # Calculate tool position for sparks (approximate based on engineer position)
                tool_x = engineer_x + 45 + math.sin(engineer_animation) * 10
                tool_y = engineer_y - 10 + math.cos(engineer_animation) * 15
                create_electric_spark(tool_x, tool_y, random.randint(5, 10))

            # Create diagnostic effects
            if random.random() < 0.05:
                create_particles(SCREEN_WIDTH // 2 + random.randint(-50, 50),
                                 SCREEN_HEIGHT // 2 + random.randint(-30, 30),
                                 NEON_BLUE, 3, 0.5)

            # Transition to running after testing duration
            if elapsed_time >= testing_duration:
                game_state = RUNNING_STATE
                SHOW_ROBOTDOG_IMAGE = False
        elif game_state == RUNNING_STATE:
            # NEW: Start background music when entering running state if not already playing
            if not background_music_playing:
                play_background_music()

            # NEW: Update joystick based on keyboard input if not dragging with mouse
            if KEYBOARD_CONTROL and not joystick_dragging:
                update_joystick_keyboard()

            # Handle jumping physics
            if JUMPING:
                cyber_canine_y += JUMP_VELOCITY
                JUMP_VELOCITY += GRAVITY

                # Check if landed
                if cyber_canine_y >= GROUND_LEVEL - 100:
                    cyber_canine_y = GROUND_LEVEL - 100
                    JUMPING = False
                    JUMP_VELOCITY = 0
                    # Create landing particles
                    create_particles(cyber_canine_x - 40, cyber_canine_y + 50, robot_dog_current_color, 10, 1.0)
                    create_particles(cyber_canine_x + 40, cyber_canine_y + 50, robot_dog_current_color, 10, 1.0)

            # Make the cyber canine move left/right with joystick control
            movement_speed = 5
            cyber_canine_x += movement_speed * joystick_direction[0] * 2

            # Keep cyber canine within screen bounds
            cyber_canine_x = max(100, min(SCREEN_WIDTH - 100, cyber_canine_x))

            # Animate legs (only if on ground)
            if not JUMPING:
                leg_animation += 0.2
                run_cycle += 0.3

            # Update street offset for scrolling effect
            street_offset = (street_offset + street_speed) % 60

            # NEW: Update electronic parts
            update_electronic_parts()

            # NEW: Update enemy robot dogs
            update_enemy_robot_dogs()

            # NEW: Update street holes
            update_street_holes()

            # NEW: Spawn based on pattern sequence
            pattern_timer += 1
            if pattern_timer >= PATTERN_INTERVAL and PARTS_COLLECTED < TOTAL_PARTS_TO_COLLECT:
                pattern_element = SPAWN_PATTERN[current_pattern_index]

                if pattern_element == "enemy":
                    create_small_enemy_dog()
                elif pattern_element == "hole":
                    create_street_hole()
                elif pattern_element == "parts":
                    # Spawn a group of 3-4 electronic parts
                    spawn_electronic_parts_group(random.randint(3, 4))

                # Move to next pattern element
                current_pattern_index = (current_pattern_index + 1) % len(SPAWN_PATTERN)
                pattern_timer = 0

            # NEW: Check for victory condition
            if PARTS_COLLECTED >= TOTAL_PARTS_TO_COLLECT and victory_start_time == 0:
                victory_start_time = pygame.time.get_ticks()
                game_state = VICTORY_STATE  # NEW: Go to victory state first
                play_win_sound()  # NEW: Play win sound when victory is achieved
                stop_background_music()  # NEW: Stop background music when victory is achieved

                # Create explosion particles for celebration
                for i in range(50):
                    angle = random.uniform(0, 2 * math.pi)
                    distance = random.uniform(100, 400)
                    x = SCREEN_WIDTH // 2 + math.cos(angle) * distance
                    y = SCREEN_HEIGHT // 2 + math.sin(angle) * distance
                    create_particles(x, y, NEON_GREEN, 5, 2.0)
                    create_particles(x, y, NEON_YELLOW, 3, 1.5)
                    create_particles(x, y, NEON_CYAN, 2, 1.0)

            # Create occasional particles during movement
            if pygame.time.get_ticks() % 5 == 0 and not JUMPING:
                for i in range(2):
                    px = cyber_canine_x - 80 + random.randint(-20, 20)
                    py = cyber_canine_y + 120 + random.randint(-10, 10)
                    create_particles(px, py, robot_dog_current_color, 2, 1.0)
                    px = cyber_canine_x + 80 + random.randint(-20, 20)
                    create_particles(px, py, robot_dog_current_color, 2, 1.0)

            # Create occasional laser effects from eyes
            if pygame.time.get_ticks() % 60 == 0 and random.random() < 0.3:
                left_eye = (cyber_canine_x - 40, cyber_canine_y - 120)
                right_eye = (cyber_canine_x + 40, cyber_canine_y - 120)
                dist = 100 + random.randint(0, 50)
                angle = random.uniform(-0.5, 0.5)
                create_laser_effect(left_eye,
                                    (left_eye[0] + dist * math.cos(angle), left_eye[1] + dist * math.sin(angle)),
                                    NEON_CYAN, 45)
                create_laser_effect(right_eye,
                                    (right_eye[0] + dist * math.cos(angle), right_eye[1] + dist * math.sin(angle)),
                                    NEON_CYAN, 45)

        # NEW: Handle victory state - show victory screen for 10 seconds then go to credits
        if game_state == VICTORY_STATE:
            # Update victory sparks
            update_victory_sparks()

            # Create continuous stream of victory sparks
            if random.random() < 0.3:
                create_victory_spark()

            # Check if 10 seconds have passed - do this EVERY FRAME
            current_time = pygame.time.get_ticks()
            time_elapsed = current_time - victory_start_time
            seconds_left = max(0, 10000 - time_elapsed) // 1000 + 1  # ← 5000 → 10000

            # Debug print every second
            if pygame.time.get_ticks() % 1000 == 0:  # Print every second
                print(f"Victory screen: {seconds_left} seconds left until credits")

            # After 10 seconds, transition to credit state
            if time_elapsed >= 10000:  # ← 5000 → 10000
                print("Transitioning to CREDIT_STATE")
                game_state = CREDIT_STATE
                # Optional: Reset victory_start_time if needed for future use
                # victory_start_time = None

        # NEW: Handle credit state - launch credits immediately
        elif game_state == CREDIT_STATE:
            launch_credit_screen()


        # NEW: Handle credit state - launch credits immediately
        elif game_state == CREDIT_STATE:
            launch_credit_screen()


    # Update particles, lasers, and glitches
    update_particles()
    update_laser_effects()
    update_cyber_glitches()
    update_battery()

    # NEW: Update joystick position
    if game_state == RUNNING_STATE and joystick_dragging and not PAUSED:
        mouse_pos = pygame.mouse.get_pos()
        update_joystick(mouse_pos)

    screen.fill(BACKGROUND)

    if game_state == LEVEL_INTRO_STATE:
        screen.fill((5, 10, 20))
        grid_size = 50
        for x in range(0, SCREEN_WIDTH, grid_size):
            alpha = 30 + int(20 * math.sin(intro_timer / 100 + x / 100))
            pygame.draw.line(screen, (20, 30, 50, alpha), (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, grid_size):
            alpha = 30 + int(20 * math.sin(intro_timer / 100 + y / 100))
            pygame.draw.line(screen, (20, 30, 50, alpha), (0, y), (SCREEN_WIDTH, y), 1)

        pulse = (math.sin(intro_timer / 200) + 1) / 2
        pulse_scale = 0.7 + pulse * 0.3
        level_text = title_font.render("LEVEL 3", True, NEON_PURPLE)
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
        scaled_text = pygame.transform.scale(level_text, (
            int(level_text.get_width() * pulse_scale), int(level_text.get_height() * pulse_scale)))
        scaled_rect = scaled_text.get_rect(center=level_rect.center)
        glow_surf = pygame.Surface((scaled_rect.width + 20, scaled_rect.height + 20), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (*NEON_PURPLE, int(100 * pulse)),
                         (0, 0, scaled_rect.width + 20, scaled_rect.height + 20), border_radius=15)
        screen.blit(glow_surf, (scaled_rect.x - 10, scaled_rect.y - 10))
        screen.blit(scaled_text, scaled_rect)

        subtitle_text = font.render("ROBOTDOG ASSEMBLY", True, NEON_CYAN)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 10))
        sub_glow = pygame.Surface((subtitle_rect.width + 10, subtitle_rect.height + 10), pygame.SRCALPHA)
        pygame.draw.rect(sub_glow, (*NEON_CYAN, 80), (0, 0, subtitle_rect.width + 10, subtitle_rect.height + 10),
                         border_radius=8)
        screen.blit(sub_glow, (subtitle_rect.x - 5, subtitle_rect.y - 5))
        screen.blit(subtitle_text, subtitle_rect)

        if intro_timer > 1500:
            alpha = min(255, (intro_timer - 1500) * 2)
            instruction_text = small_font.render("Assemble the cyber canine with advanced components", True,
                                                 (200, 220, 255, alpha))
            instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            instruction_surface = pygame.Surface(instruction_text.get_size(), pygame.SRCALPHA)
            instruction_surface.fill((0, 0, 0, 0))
            instruction_surface.blit(instruction_text, (0, 0))
            instruction_surface.set_alpha(alpha)
            screen.blit(instruction_surface, instruction_rect)

            if intro_timer > 2500:
                difficulty_alpha = min(255, (intro_timer - 2500) * 2)
                difficulty_text = small_font.render("EXPERT MODE: Complex assembly required", True,
                                                    (255, 100, 100, difficulty_alpha))
                difficulty_rect = difficulty_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
                difficulty_surface = pygame.Surface(difficulty_text.get_size(), pygame.SRCALPHA)
                difficulty_surface.fill((0, 0, 0, 0))
                difficulty_surface.blit(difficulty_text, (0, 0))
                difficulty_surface.set_alpha(difficulty_alpha)
                screen.blit(difficulty_surface, difficulty_rect)

    elif game_state in (ASSEMBLY_STATE, SUCCESS_STATE):
        # NEW: Start background music when in assembly state if not already playing
        if not background_music_playing:
            play_background_music()

        draw_cyber_lab(screen)
        draw_parts_panel(screen)
        max_part_width = max(part["rect"].width for part in parts) if parts else 80
        parts_panel_width = max(350, 50 + 3 * (max_part_width + 20))
        assembly_panel_x = 30 + parts_panel_width + 20
        assembly_panel = pygame.Rect(assembly_panel_x, 80, SCREEN_WIDTH - assembly_panel_x - 30, SCREEN_HEIGHT - 150)
        s = pygame.Surface((assembly_panel.width, assembly_panel.height), pygame.SRCALPHA)
        pygame.draw.rect(s, (*PANEL_BG[:3], 180), (0, 0, assembly_panel.width, assembly_panel.height), border_radius=20)
        screen.blit(s, assembly_panel)
        title_text = title_font.render("ROBOTDOG ASSEMBLY STATION", True, NEON_CYAN)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 40))
        draw_cyber_canine(screen, adjusted_center_x, center_y, leg_animation)
        for slot in SLOTS:
            draw_slot(screen, slot, parts)
        draw_wires(screen, SLOTS, parts)
        for part in parts:
            draw_part(screen, part)
        draw_particles(screen)
        draw_laser_effects(screen)
        draw_cyber_glitches(screen)
        draw_score(screen)
        draw_robotdog_image(screen)

        # NEW: Draw control buttons
        draw_control_buttons(screen, mouse_pos)

    elif game_state == TESTING_STATE:
        # Draw testing screen
        tool_pos = draw_testing_screen(screen, testing_progress, current_test_message, engineer_x, engineer_y,
                                       engineer_animation)

        # Draw particles and effects
        draw_particles(screen)
        draw_laser_effects(screen)
        draw_robotdog_image(screen)

        # NEW: Draw control buttons
        draw_control_buttons(screen, mouse_pos)

    elif game_state == RUNNING_STATE:
        # Draw running background
        draw_cyber_street(screen, street_offset)

        # Draw street holes
        draw_street_holes(screen)

        # Draw electronic parts to collect (with color transition)
        draw_electronic_parts(screen)

        # Draw small enemy robot dogs
        draw_small_enemy_dogs(screen)

        # Draw cyber canine with hit effect if invincible
        is_hit = INVINCIBLE_TIMER > 0 and (pygame.time.get_ticks() // 100) % 2 == 0
        draw_cyber_canine_move(screen, cyber_canine_x, cyber_canine_y, leg_animation, run_cycle, JUMPING, is_hit)

        # Draw particles and effects
        draw_particles(screen)
        draw_laser_effects(screen)

        # Draw score (right side, more top)
        draw_score(screen)

        # Draw health bar (under score on right side)
        draw_health_bar(screen)

        # Draw parts counter (under health bar on right side)
        draw_parts_counter(screen)

        # Draw radar (under parts counter on right side)
        draw_radar(screen)

        # Draw controls
        draw_joystick(screen)
        draw_jump_button(screen)

        # NEW: Draw control buttons
        draw_control_buttons(screen, mouse_pos)

        # Draw game over screen if game over
        if GAME_OVER:
            draw_game_over(screen)
            play_lose_sound()  # NEW: Play lose sound when game over

    elif game_state == VICTORY_STATE:
        # Draw the victory screen
        draw_victory(screen)



    # NEW: Draw pause screen if game is paused
    if PAUSED:
        resume_hover, menu_hover = draw_pause_screen(screen, mouse_pos)

        # Check for mouse clicks on pause screen buttons
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if resume_hover:
                    PAUSED = False
                elif menu_hover:
                    go_to_main_menu()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    PAUSED = False
                elif event.key == pygame.K_ESCAPE:
                    go_to_main_menu()

    pygame.display.flip()
    clock.tick(60)