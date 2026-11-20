import pygame
import sys
import math
import os
import subprocess
import random

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Get screen info and set to full screen
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Drone Assembly Lab - Level 2")

# Victory button rect
VICTORY_BUTTON_RECT = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 60)

# Colors
BACKGROUND = (20, 25, 40)
PANEL_BG = (30, 35, 50)
RED = (220, 60, 60)
GREEN = (60, 220, 60)
BLUE = (60, 120, 220)
YELLOW = (220, 220, 60)
PURPLE = (180, 60, 220)
CYAN = (60, 220, 220)
WHITE = (240, 240, 240)
GRAY = (120, 120, 120)
DARK_GRAY = (60, 60, 70)
METAL_GRAY = (100, 110, 120)
BLACK = (20, 20, 20)
SILVER = (200, 200, 210)
GOLD = (212, 175, 55)
LIGHT_BLUE = (170, 200, 230)
NEON_GREEN = (50, 255, 100)
NEON_BLUE = (50, 150, 255)
ORANGE = (255, 150, 50)
BROWN = (160, 120, 80)
JEANS_BLUE = (70, 100, 150)
SKIN_TONE = (240, 200, 160)
BATTERY_GREEN = (0, 200, 80)
POWER_CAN_COLOR = BATTERY_GREEN
PLANE_COLOR = (200, 200, 220)

# NEW: Minimap colors
MINIMAP_COLOR = (30, 40, 60)
MINIMAP_BORDER = (60, 80, 100)
MINIMAP_SKY = (40, 50, 80)
MINIMAP_GROUND = (60, 80, 40)
MINIMAP_DRONE = (50, 150, 255)
MINIMAP_ENEMY = (220, 60, 60)
MINIMAP_POWER = (0, 200, 80)

# Pilot appearance colors
PILOT_SUIT = (60, 70, 90)
PILOT_HELMET = (40, 50, 70)
PILOT_GLOVES = (200, 180, 150)
PILOT_VISOR = (100, 180, 255)
PILOT_HARNESS = (180, 60, 60)

# Sound variables
bg_music = None
win_sound = None
shoot_sound = None
lose_sound = None
rotor_sound = None
explosion_sound = None
collect_sound = None


# Load sound effects and music with better error handling
def load_sounds():
    global bg_music, win_sound, shoot_sound, lose_sound, rotor_sound, explosion_sound, collect_sound

    print("Loading sounds...")

    # List of required sound files
    sound_files = {
        "bg_music": "Level 2.mp3",
        "win_sound": "Win.mp3",
        "shoot_sound": "Lazer.mp3",
        "lose_sound": "Lose.mp3",
        "rotor_sound": "Rotor.mp3",
        "explosion_sound": "collect.mp3",
        "collect_sound": "collect.mp3"
    }

    # Check if files exist
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Current directory: {current_dir}")

    for sound_name, filename in sound_files.items():
        file_path = os.path.join(current_dir, filename)
        if os.path.exists(file_path):
            print(f"✓ Found: {filename}")
        else:
            print(f"✗ Missing: {filename}")

    try:
        # Try to load background music with pygame.mixer.music for better MP3 support
        if os.path.exists(os.path.join(current_dir, "Level 2.mp3")):
            pygame.mixer.music.load("Level 2.mp3")
            print("✓ Background music loaded successfully")
        else:
            print("✗ Level 2.mp3 not found")

        # Load sound effects
        sound_objects = {}
        for sound_name, filename in sound_files.items():
            if sound_name == "bg_music":
                continue

            try:
                if os.path.exists(os.path.join(current_dir, filename)):
                    sound_objects[sound_name] = pygame.mixer.Sound(filename)
                    print(f"✓ Loaded: {filename}")
                else:
                    print(f"✗ Could not load: {filename}")
                    # Create a silent placeholder
                    sound_objects[sound_name] = pygame.mixer.Sound(buffer=bytearray([]))
            except Exception as e:
                print(f"Error loading {filename}: {e}")
                sound_objects[sound_name] = pygame.mixer.Sound(buffer=bytearray([]))

        # Assign to global variables
        win_sound = sound_objects["win_sound"]
        shoot_sound = sound_objects["shoot_sound"]
        lose_sound = sound_objects["lose_sound"]
        rotor_sound = sound_objects["rotor_sound"]
        explosion_sound = sound_objects["collect_sound"]
        collect_sound = sound_objects["collect_sound"]

        # Set volumes
        pygame.mixer.music.set_volume(0.5)
        if win_sound: win_sound.set_volume(0.7)
        if shoot_sound: shoot_sound.set_volume(0.6)
        if lose_sound: lose_sound.set_volume(0.7)
        if rotor_sound: rotor_sound.set_volume(0.5)
        if explosion_sound: explosion_sound.set_volume(0.8)
        if collect_sound: collect_sound.set_volume(0.6)

        print("All sounds processed!")

    except Exception as e:
        print(f"Error in sound loading: {e}")
        print("Creating silent placeholder sounds...")

        # Create silent placeholder sounds
        def create_silent_sound():
            return pygame.mixer.Sound(buffer=bytearray([]))

        win_sound = create_silent_sound()
        shoot_sound = create_silent_sound()
        lose_sound = create_silent_sound()
        rotor_sound = create_silent_sound()
        explosion_sound = create_silent_sound()
        collect_sound = create_silent_sound()


# Load the sounds
load_sounds()


# Play background music
def play_background_music():
    try:
        pygame.mixer.music.play(-1)
        print("Background music started")
    except Exception as e:
        print(f"Error playing background music: {e}")


# Stop background music
def stop_background_music():
    try:
        pygame.mixer.music.stop()
        print("Background music stopped")
    except Exception as e:
        print(f"Error stopping background music: {e}")


# Play win sound
def play_win_sound():
    try:
        if win_sound:
            win_sound.play()
            print("Win sound played")
    except Exception as e:
        print(f"Error playing win sound: {e}")


# Play shoot sound (removed since no shooting)
def play_shoot_sound():
    pass


# Play lose sound
def play_lose_sound():
    try:
        if lose_sound:
            lose_sound.play()
            print("Lose sound played")
    except Exception as e:
        print(f"Error playing lose sound: {e}")


# Play rotor sound
def play_rotor_sound():
    try:
        if rotor_sound:
            rotor_sound.play()
            print("Rotor sound played")
    except Exception as e:
        print(f"Error playing rotor sound: {e}")


# Play explosion sound
def play_explosion_sound():
    try:
        if explosion_sound:
            explosion_sound.play()
            print("Explosion sound played")
    except Exception as e:
        print(f"Error playing explosion sound: {e}")


# Play collect sound for power cans
def play_collect_sound():
    try:
        if collect_sound:
            collect_sound.play()
            print("Collect sound played")
    except Exception as e:
        print(f"Error playing collect sound: {e}")


# NEW: Play pilot testing sounds
def play_pilot_sound():
    print("Playing pilot check sound!")


def play_controller_sound():
    print("Playing controller sound!")


def play_takeoff_sound():
    print("Playing takeoff sound!")


# NEW: Load drone image - UPDATED WITH LARGER SIZE
def load_drone_image():
    """Load the drone.png image from multiple possible locations"""
    possible_paths = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "drone.png"),
        os.path.join("C:\\", "Users", "musta", "PycharmProjects", "PythonProject1", "drone.png"),
        os.path.join(os.getcwd(), "drone.png"),
    ]

    drone_image = None
    loaded_path = None

    for path in possible_paths:
        if os.path.exists(path):
            try:
                drone_image = pygame.image.load(path).convert_alpha()
                loaded_path = path
                print(f"✓ Drone image loaded from: {path}")
                break
            except Exception as e:
                print(f"✗ Could not load image from {path}: {e}")

    if drone_image is None:
        print("✗ drone.png not found in any location. Creating placeholder.")
        # Create a placeholder surface
        drone_image = pygame.Surface((350, 250), pygame.SRCALPHA)  # LARGER PLACEHOLDER
        pygame.draw.rect(drone_image, BLUE, (0, 0, 350, 250), border_radius=15)
        text = pygame.font.SysFont("Arial", 24).render("DRONE IMAGE", True, WHITE)
        drone_image.blit(text, (100, 115))

    # Resize image to fit under score panel - LARGER SIZE
    drone_image = pygame.transform.scale(drone_image, (350, 250))  # INCREASED FROM 200x150 TO 350x250
    return drone_image


# Load drone image
DRONE_IMAGE = load_drone_image()

# Drone part types - INCREASED SIZES FOR ASSEMBLY STATE
DRONE_PARTS = {
    "Flight Controller": {"color": BLUE, "size": (100, 100), "radius": 5, "count": 1},
    "Battery": {"color": YELLOW, "size": (90, 120), "radius": 8, "count": 1},
    "Motor": {"color": RED, "size": (80, 80), "radius": 30, "count": 4},
    "Camera": {"color": PURPLE, "size": (80, 80), "radius": 10, "count": 1},
    "GPS": {"color": CYAN, "size": (70, 70), "radius": 10, "count": 1},
    "Propeller": {"color": GREEN, "size": (100, 25), "radius": 3, "count": 4}
}

# Calculate positions
center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
drone_center_x = center_x + 150

# Drone slots - INCREASED SIZES AND SPACING
DRONE_SLOTS = [
    {"rect": pygame.Rect(drone_center_x - 50, center_y - 50, 100, 100), "type": "Flight Controller",
     "connected_to": [1, 2, 3, 4, 5]},
    {"rect": pygame.Rect(drone_center_x - 150, center_y + 40, 90, 120), "type": "Battery", "connected_to": [0]},
    {"rect": pygame.Rect(drone_center_x - 130, center_y - 130, 80, 80), "type": "Motor", "connected_to": [0]},
    {"rect": pygame.Rect(drone_center_x + 50, center_y - 130, 80, 80), "type": "Motor", "connected_to": [0]},
    {"rect": pygame.Rect(drone_center_x - 130, center_y + 130, 80, 80), "type": "Motor", "connected_to": [0]},
    {"rect": pygame.Rect(drone_center_x + 50, center_y + 130, 80, 80), "type": "Motor", "connected_to": [0]},
    {"rect": pygame.Rect(drone_center_x + 130, center_y, 80, 80), "type": "Camera", "connected_to": [0]},
    {"rect": pygame.Rect(drone_center_x, center_y - 150, 70, 70), "type": "GPS", "connected_to": [0]},
    {"rect": pygame.Rect(drone_center_x - 130, center_y - 130, 100, 25), "type": "Propeller", "connected_to": [2]},
    {"rect": pygame.Rect(drone_center_x + 30, center_y - 130, 100, 25), "type": "Propeller", "connected_to": [3]},
    {"rect": pygame.Rect(drone_center_x - 130, center_y + 105, 100, 25), "type": "Propeller", "connected_to": [4]},
    {"rect": pygame.Rect(drone_center_x + 30, center_y + 105, 100, 25), "type": "Propeller", "connected_to": [5]},
]

# Create parts for dragging
drone_parts = []
part_id = 0

total_parts = sum(part_info["count"] for part_info in DRONE_PARTS.values())
parts_per_column = (total_parts + 1) // 2

for part_type, part_info in DRONE_PARTS.items():
    for i in range(part_info["count"]):
        column = part_id // parts_per_column
        row = part_id % parts_per_column

        x_pos = 50 + column * 130
        y_pos = 180 + row * 140

        drone_parts.append({
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

# Create fonts
font = pygame.font.SysFont("Arial", 18)
title_font = pygame.font.SysFont("Arial", 36, bold=True)
small_font = pygame.font.SysFont("Arial", 16)

# Game states
LEVEL_INTRO_STATE = 0
ASSEMBLY_STATE = 1
SUCCESS_STATE = 2
PRE_FLIGHT_STATE = 3
FLIGHT_STATE = 4
VICTORY_STATE = 5

# Game features
PARTICLE_SYSTEMS = []
WIRE_ANIMATION = 0
SCORE = 0
COMBO = 0
LAST_PLACEMENT_TIME = 0
BATTERY_LEVEL = 0.5
BATTERY_DIRECTION = 1

# Flight control variables
drone_x = drone_center_x
drone_y = SCREEN_HEIGHT - 300
drone_altitude = 0
max_altitude = 400
drone_speed_x = 0
drone_speed_y = 0
ROTOR_ANIMATION = 0

# NEW: Enemy and power can variables
ENEMIES = []
POWER_CANS = []
POWER_CANS_COLLECTED = 0
TOTAL_POWER_CANS = 40
ENEMY_SPAWN_TIMER = 0
GAME_OVER = False
ENEMY_GROUP_SIZE = 4
ENEMY_GROUP_GAP = 80
ENEMY_GROUP_COUNTER = 0
ENEMY_GROUP_TIMER = 0
POWER_CAN_SPAWN_TIMER = 0
POWER_CAN_SPAWN_INTERVAL = 90

# NEW: Drone body color that changes with energy collection
DRONE_BODY_COLOR = BLUE

# NEW: Minimap variables
MINIMAP_RECT = pygame.Rect(SCREEN_WIDTH - 280, 160, 250, 150)  # Positioned under the scores
MINIMAP_VIEW_RADIUS = 300  # How far the minimap can "see" around the drone

# NEW: Drone image display variables - UPDATED WITH LARGER SIZE
DRONE_IMAGE_RECT = pygame.Rect(SCREEN_WIDTH - 320, 90, 350, 250)  # LARGER: Position under score panel, increased size
SHOW_DRONE_IMAGE = True  # Controls when to show the image

# Control buttons
PAUSED = False
PAUSE_BUTTON = pygame.Rect(20, 80, 150, 40)
ESCAPE_BUTTON = pygame.Rect(20, 30, 150, 40)

# Pause menu buttons
RESUME_BUTTON = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 60)
MAIN_MENU_BUTTON = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 60)

# NEW: Pilot testing state variables
PRE_FLIGHT_TIMER = 0
PRE_FLIGHT_DURATION = 10000
PILOT_ANIMATION = 0
PILOT_POSITION = [drone_center_x - 300, center_y + 100]
CONTROLLER_ANGLE = 0
CONTROLLER_MOVING = True
CURRENT_CHECK_PHASE = 0
CHECK_PHASE_TIMER = 0

# Victory button
NEXT_LEVEL_BUTTON = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 60)
NEXT_LEVEL_BUTTON_COLOR = NEON_GREEN
NEXT_LEVEL_BUTTON_HOVER_COLOR = (100, 255, 150)
WIN_SOUND_PLAYED = False


# NEW: Function to update drone body color based on energy cans collected
def update_drone_color():
    global DRONE_BODY_COLOR

    # Calculate ratio of cans collected (0 to 1)
    ratio = POWER_CANS_COLLECTED / TOTAL_POWER_CANS
    ratio = min(1.0, ratio)

    # Interpolate between BLUE (60, 120, 220) and RED (220, 60, 60)
    red = int(60 + (220 - 60) * ratio)
    green = int(120 + (60 - 120) * ratio)
    blue = int(220 + (60 - 220) * ratio)

    DRONE_BODY_COLOR = (red, green, blue)


# NEW: Draw drone image under score panel during assembly state - UPDATED FOR LARGER SIZE
def draw_drone_image_under_score(surface):
    if SHOW_DRONE_IMAGE:
        # Draw background panel for the image - LARGER SIZE
        image_panel = pygame.Rect(SCREEN_WIDTH - 330, 85, 360, 260)  # Larger panel
        pygame.draw.rect(surface, (40, 45, 55), image_panel, border_radius=12)
        pygame.draw.rect(surface, (70, 75, 85), image_panel, 3, border_radius=12)

        # Draw the drone image
        surface.blit(DRONE_IMAGE, (SCREEN_WIDTH - 320, 90))

        # Draw label with larger font
        label = pygame.font.SysFont("Arial", 20, bold=True).render("TARGET DRONE", True, LIGHT_BLUE)
        surface.blit(label, (SCREEN_WIDTH - 320 + 175 - label.get_width() // 2, 345))


# NEW: Draw minimap camera view (similar to snowbot but adapted for drone game)
def draw_minimap_camera(surface, drone_x, drone_y, enemies_list, power_cans_list):
    pygame.draw.rect(surface, MINIMAP_COLOR, MINIMAP_RECT, border_radius=10)
    pygame.draw.rect(surface, MINIMAP_BORDER, MINIMAP_RECT, 3, border_radius=10)

    minimap_text = font.render("TOP-DOWN VIEW", True, NEON_BLUE)
    surface.blit(minimap_text, (MINIMAP_RECT.centerx - minimap_text.get_width() // 2, MINIMAP_RECT.y + 5))

    camera_surface = pygame.Surface((MINIMAP_RECT.width - 20, MINIMAP_RECT.height - 40), pygame.SRCALPHA)
    camera_rect = camera_surface.get_rect(center=(MINIMAP_RECT.centerx, MINIMAP_RECT.centery + 10))

    # Draw sky background
    pygame.draw.rect(camera_surface, MINIMAP_SKY, (0, 0, camera_surface.get_width(), camera_surface.get_height()))

    # Draw ground area (bottom half)
    ground_height = camera_surface.get_height() // 2
    ground_y = camera_surface.get_height() - ground_height
    pygame.draw.rect(camera_surface, MINIMAP_GROUND, (0, ground_y, camera_surface.get_width(), ground_height))

    # Draw a grid for reference
    grid_spacing = 20
    grid_color = (80, 90, 110, 100)
    for x in range(0, camera_surface.get_width(), grid_spacing):
        pygame.draw.line(camera_surface, grid_color, (x, 0), (x, camera_surface.get_height()), 1)
    for y in range(0, camera_surface.get_height(), grid_spacing):
        pygame.draw.line(camera_surface, grid_color, (0, y), (camera_surface.get_width(), y), 1)

    # Center point (drone position)
    center_x = camera_surface.get_width() // 2
    center_y = camera_surface.get_height() // 2

    # Draw crosshair at center
    cross_size = 8
    pygame.draw.line(camera_surface, NEON_GREEN,
                     (center_x - cross_size, center_y),
                     (center_x + cross_size, center_y), 2)
    pygame.draw.line(camera_surface, NEON_GREEN,
                     (center_x, center_y - cross_size),
                     (center_x, center_y + cross_size), 2)

    # Draw drone at center
    drone_size = 6
    pygame.draw.circle(camera_surface, MINIMAP_DRONE, (center_x, center_y), drone_size)
    pygame.draw.circle(camera_surface, (200, 230, 255), (center_x, center_y), drone_size - 2)

    # Draw directional indicator
    direction_radius = 15
    direction_x = center_x + math.cos(ROTOR_ANIMATION) * direction_radius
    direction_y = center_y + math.sin(ROTOR_ANIMATION) * direction_radius
    pygame.draw.line(camera_surface, (255, 255, 200), (center_x, center_y), (direction_x, direction_y), 2)

    # Draw enemies in minimap
    for enemy in enemies_list:
        # Calculate relative position to drone
        rel_x = enemy["x"] - drone_x
        rel_y = enemy["y"] - drone_y

        # Only show if within view radius
        distance = math.sqrt(rel_x ** 2 + rel_y ** 2)
        if distance < MINIMAP_VIEW_RADIUS:
            # Scale position to minimap
            map_x = center_x + (rel_x / MINIMAP_VIEW_RADIUS) * (camera_surface.get_width() // 2 - 10)
            map_y = center_y + (rel_y / MINIMAP_VIEW_RADIUS) * (camera_surface.get_height() // 2 - 10)

            # Draw enemy based on type
            if enemy["type"] == "plane":
                # Plane - larger dot
                pygame.draw.circle(camera_surface, MINIMAP_ENEMY, (int(map_x), int(map_y)), 4)
                # Add wings
                pygame.draw.line(camera_surface, MINIMAP_ENEMY,
                                 (int(map_x) - 4, int(map_y)),
                                 (int(map_x) + 4, int(map_y)), 2)
            elif enemy["type"] == "small_drone":
                # Small drone - triangle shape
                points = [
                    (map_x, map_y - 3),
                    (map_x - 3, map_y + 3),
                    (map_x + 3, map_y + 3)
                ]
                pygame.draw.polygon(camera_surface, MINIMAP_ENEMY, points)
            else:  # bird
                # Bird - smaller dot
                pygame.draw.circle(camera_surface, (200, 150, 50), (int(map_x), int(map_y)), 3)

    # Draw power cans in minimap
    for can in power_cans_list:
        if not can["collected"]:
            # Calculate relative position to drone
            rel_x = can["x"] - drone_x
            rel_y = can["y"] - drone_y

            # Only show if within view radius
            distance = math.sqrt(rel_x ** 2 + rel_y ** 2)
            if distance < MINIMAP_VIEW_RADIUS:
                # Scale position to minimap
                map_x = center_x + (rel_x / MINIMAP_VIEW_RADIUS) * (camera_surface.get_width() // 2 - 10)
                map_y = center_y + (rel_y / MINIMAP_VIEW_RADIUS) * (camera_surface.get_height() // 2 - 10)

                # Draw power can as green battery symbol
                # Battery body
                pygame.draw.rect(camera_surface, MINIMAP_POWER,
                                 (int(map_x) - 3, int(map_y) - 5, 6, 10))
                # Battery terminal
                pygame.draw.rect(camera_surface, (50, 150, 50),
                                 (int(map_x) - 2, int(map_y) - 6, 4, 2))

    # Draw view radius circle
    pygame.draw.circle(camera_surface, (100, 120, 150, 150), (center_x, center_y),
                       camera_surface.get_width() // 2 - 10, 1)

    # Add status text
    status_color = GREEN if len(enemies_list) == 0 else YELLOW
    status_text = "CLEAR" if len(enemies_list) == 0 else f"THREATS: {len(enemies_list)}"

    status_surf = small_font.render(status_text, True, status_color)
    camera_surface.blit(status_surf, (5, 5))

    # Add power can counter in minimap
    power_text = small_font.render(f"ENERGY: {POWER_CANS_COLLECTED}/{TOTAL_POWER_CANS}", True, MINIMAP_POWER)
    camera_surface.blit(power_text, (5, 25))

    # Add distance indicators
    for i in range(3):
        radius = (i + 1) * (camera_surface.get_width() // 6)
        pygame.draw.circle(camera_surface, (100, 120, 150, 80), (center_x, center_y), radius, 1)

        if i > 0:
            distance = (i + 1) * 100
            distance_text = small_font.render(f"{distance}m", True, (150, 170, 190))
            text_x = center_x + radius - distance_text.get_width() // 2
            text_y = center_y - 10
            camera_surface.blit(distance_text, (text_x, text_y))

    # Blit the camera surface onto the main surface
    surface.blit(camera_surface, camera_rect)

    # Draw decorative border around camera
    corner_size = 15
    pygame.draw.line(surface, CYAN,
                     (camera_rect.left, camera_rect.top),
                     (camera_rect.left + corner_size, camera_rect.top), 2)
    pygame.draw.line(surface, CYAN,
                     (camera_rect.left, camera_rect.top),
                     (camera_rect.left, camera_rect.top + corner_size), 2)

    pygame.draw.line(surface, CYAN,
                     (camera_rect.right - corner_size, camera_rect.top),
                     (camera_rect.right, camera_rect.top), 2)
    pygame.draw.line(surface, CYAN,
                     (camera_rect.right, camera_rect.top),
                     (camera_rect.right, camera_rect.top + corner_size), 2)

    pygame.draw.line(surface, CYAN,
                     (camera_rect.left, camera_rect.bottom - corner_size),
                     (camera_rect.left, camera_rect.bottom), 2)
    pygame.draw.line(surface, CYAN,
                     (camera_rect.left, camera_rect.bottom),
                     (camera_rect.left + corner_size, camera_rect.bottom), 2)

    pygame.draw.line(surface, CYAN,
                     (camera_rect.right - corner_size, camera_rect.bottom),
                     (camera_rect.right, camera_rect.bottom), 2)
    pygame.draw.line(surface, CYAN,
                     (camera_rect.right, camera_rect.bottom - corner_size),
                     (camera_rect.right, camera_rect.bottom), 2)


# NEW: Main menu transition
def go_to_main_menu():
    print("Returning to Main Menu...")
    stop_background_music()

    if getattr(sys, 'frozen', False):
        script_dir = os.path.dirname(sys.executable)
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))

    main_menu_path = os.path.join(script_dir, "main_menu.py")

    if not os.path.exists(main_menu_path):
        print("ERROR: main_menu.py not found!")
        return

    try:
        if sys.platform == "win32":
            subprocess.Popen([sys.executable, main_menu_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen([sys.executable, main_menu_path])
    except Exception as e:
        print(f"Failed to launch main_menu.py: {e}")

    pygame.quit()
    sys.exit(0)


# NEW: Transition to dogbot level
def transition_to_dogbot_level():
    print("VICTORY! Launching Dogbot Level 3...")
    stop_background_music()

    if getattr(sys, 'frozen', False):
        script_dir = os.path.dirname(sys.executable)
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))

    dogbot_path = os.path.join(script_dir, "dogbot_game.py")

    if not os.path.exists(dogbot_path):
        print("ERROR: dogbot_game.py not found!")
        print(f"Looked in: {script_dir}")
        return

    try:
        print(f"Launching: {dogbot_path}")

        if sys.platform == "win32":
            subprocess.Popen([sys.executable, dogbot_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen([sys.executable, dogbot_path])

        print("Dogbot level launched successfully!")

    except Exception as e:
        print(f"Failed to launch dogbot_game.py: {e}")

    pygame.quit()
    sys.exit(0)


# Sound effects
def play_success_sound():
    print("Playing success sound!")


def play_failure_sound():
    print("Playing failure sound!")


# Particle system
def create_particles(x, y, color, count=10):
    for _ in range(count):
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(0.5, 2)
        PARTICLE_SYSTEMS.append({
            "x": x,
            "y": y,
            "vx": math.cos(angle) * speed,
            "vy": math.sin(angle) * speed,
            "color": color,
            "life": random.randint(20, 40),
            "max_life": 30
        })


def update_particles():
    for particle in PARTICLE_SYSTEMS[:]:
        particle["x"] += particle["vx"]
        particle["y"] += particle["vy"]
        particle["life"] -= 1
        if particle["life"] <= 0:
            PARTICLE_SYSTEMS.remove(particle)


def draw_particles(surface):
    for particle in PARTICLE_SYSTEMS:
        life_ratio = particle["life"] / particle["max_life"]
        size = max(1, int(3 * life_ratio))
        pygame.draw.circle(surface, particle["color"], (int(particle["x"]), int(particle["y"])), size)


# Battery animation
def update_battery():
    global BATTERY_LEVEL, BATTERY_DIRECTION
    BATTERY_LEVEL += 0.005 * BATTERY_DIRECTION
    if BATTERY_LEVEL >= 1.0:
        BATTERY_LEVEL = 1.0
        BATTERY_DIRECTION = -1
    elif BATTERY_LEVEL <= 0.1:
        BATTERY_LEVEL = 0.1
        BATTERY_DIRECTION = 1


# NEW: Enemy system functions - UPDATED FOR MORE ENEMIES WITH SPACING
def create_enemy():
    # Create different types of enemies with adjusted frequencies
    enemy_weights = ["plane", "small_drone", "bird", "small_drone"]
    enemy_type = random.choice(enemy_weights)

    # Make enemies spawn across more of the screen width
    spawn_x = random.randint(80, SCREEN_WIDTH - 80)

    if enemy_type == "plane":
        ENEMIES.append({
            "x": spawn_x,
            "y": -200,
            "speed": random.uniform(0.8, 1.5),
            "radius": 60,
            "color": PLANE_COLOR,
            "type": "plane"
        })
    elif enemy_type == "small_drone":
        ENEMIES.append({
            "x": spawn_x,
            "y": -60,
            "speed": random.uniform(1.8, 2.8),
            "radius": 20,
            "color": BLUE,
            "type": "small_drone"
        })
    else:  # bird
        ENEMIES.append({
            "x": spawn_x,
            "y": -80,
            "speed": random.uniform(2.2, 3.2),
            "radius": 20,
            "color": (150, 100, 50),
            "type": "bird"
        })


def update_enemies():
    global GAME_OVER

    for enemy in ENEMIES[:]:
        # Move enemies downward with slight horizontal movement for planes
        if enemy["type"] == "plane":
            enemy["x"] += math.sin(pygame.time.get_ticks() / 1000) * 0.5
        enemy["y"] += enemy["speed"]

        # Remove enemies that go off screen
        if enemy["y"] > SCREEN_HEIGHT + 200:
            ENEMIES.remove(enemy)
            continue

        # Check if enemy collides with drone
        dx = enemy["x"] - drone_x
        dy = enemy["y"] - drone_y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < enemy["radius"] + 40:
            GAME_OVER = True
            create_particles(drone_x, drone_y, RED, 50)
            play_explosion_sound()
            play_lose_sound()


def draw_enemies(surface):
    for enemy in ENEMIES:
        if enemy["type"] == "plane":
            draw_passenger_plane(surface, enemy["x"], enemy["y"], enemy["speed"])
        elif enemy["type"] == "small_drone":
            draw_small_drone(surface, enemy["x"], enemy["y"], enemy["speed"])
        else:  # bird
            draw_enemy_bird(surface, enemy["x"], enemy["y"], enemy["speed"])


def draw_passenger_plane(surface, x, y, speed):
    # Passenger plane body
    plane_length = 120
    plane_height = 40
    plane_color = PLANE_COLOR

    # Main fuselage
    pygame.draw.ellipse(surface, plane_color,
                        (x - plane_length // 2, y - plane_height // 2, plane_length, plane_height))

    # Cockpit
    pygame.draw.circle(surface, (100, 150, 255), (int(x - plane_length // 2 + 15), int(y)), 12)

    # Windows
    for i in range(6):
        window_x = x - plane_length // 2 + 40 + i * 12
        pygame.draw.circle(surface, (100, 150, 255), (int(window_x), int(y)), 4)

    # Wings
    wing_width = 80
    wing_height = 15
    pygame.draw.rect(surface, (180, 180, 200), (x - wing_width // 2, y + 10, wing_width, wing_height))

    # Tail
    pygame.draw.polygon(surface, plane_color, [
        (x + plane_length // 2 - 10, y - 20),
        (x + plane_length // 2 + 20, y),
        (x + plane_length // 2 - 10, y + 20)
    ])

    # Engines
    pygame.draw.circle(surface, (80, 80, 90), (int(x - 30), int(y + 25)), 10)
    pygame.draw.circle(surface, (80, 80, 90), (int(x + 30), int(y + 25)), 10)


def draw_small_drone(surface, x, y, speed):
    # Small drone (similar to player drone but smaller)
    body_radius = 15
    arm_length = 30

    # Draw arms
    for i in range(4):
        angle = i * math.pi / 2
        arm_x = x + math.cos(angle) * arm_length
        arm_y = y + math.sin(angle) * arm_length

        # Draw arm
        pygame.draw.line(surface, METAL_GRAY, (x, y), (arm_x, arm_y), 4)

        # Draw motor at end of arm
        motor_radius = 8
        pygame.draw.circle(surface, RED, (int(arm_x), int(arm_y)), motor_radius)

        # Draw small propeller
        prop_radius = 12
        blade_angle = ROTOR_ANIMATION + i * math.pi / 2

        for j in range(2):
            blade_angle_actual = blade_angle + j * math.pi
            blade_x = arm_x + math.cos(blade_angle_actual) * prop_radius
            blade_y = arm_y + math.sin(blade_angle_actual) * prop_radius

            blade_points = [
                (arm_x + math.cos(blade_angle_actual + 0.2) * 3,
                 arm_y + math.sin(blade_angle_actual + 0.2) * 3),
                (blade_x, blade_y),
                (arm_x + math.cos(blade_angle_actual - 0.2) * 3,
                 arm_y + math.sin(blade_angle_actual - 0.2) * 3)
            ]
            pygame.draw.polygon(surface, GREEN, blade_points)

    # Central body
    pygame.draw.circle(surface, DARK_GRAY, (x, y), body_radius)
    pygame.draw.circle(surface, BLUE, (x, y), body_radius - 3)


def draw_enemy_bird(surface, x, y, speed):
    # Enemy bird
    bird_color = (150, 100, 50)

    # Bird body
    pygame.draw.ellipse(surface, bird_color, (x - 15, y - 10, 30, 20))

    # Bird head
    pygame.draw.circle(surface, bird_color, (int(x + 10), int(y - 10)), 8)

    # Bird beak
    pygame.draw.polygon(surface, (200, 150, 50), [
        (x + 18, y - 10),
        (x + 25, y - 8),
        (x + 18, y - 6)
    ])

    # Bird wings (animated)
    wing_offset = math.sin(pygame.time.get_ticks() / 100) * 5
    pygame.draw.ellipse(surface, (120, 80, 40), (x - 20, y - 5 + wing_offset, 25, 10))


# NEW: Power can system functions - CHANGED TO BATTERY SHAPE
def create_power_can():
    # Create a power can at the top of the screen
    POWER_CANS.append({
        "x": random.randint(100, SCREEN_WIDTH - 100),
        "y": -50,
        "speed": 2.0,
        "radius": 15,
        "color": POWER_CAN_COLOR,
        "animation": 0,
        "collected": False
    })


def update_power_cans():
    global POWER_CANS_COLLECTED, SCORE

    for can in POWER_CANS[:]:
        # Move can downward
        can["y"] += can["speed"]
        can["animation"] += 0.1

        # Remove if goes off bottom of screen
        if can["y"] > SCREEN_HEIGHT + 100:
            POWER_CANS.remove(can)
            continue

        # Check if drone collects the power can
        dx = can["x"] - drone_x
        dy = can["y"] - drone_y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < can["radius"] * 2 + 30:
            # Collect the power can
            POWER_CANS.remove(can)
            POWER_CANS_COLLECTED += 1
            SCORE += 25

            # Create collection particles
            create_particles(can["x"], can["y"], POWER_CAN_COLOR, 15)
            create_particles(can["x"], can["y"], YELLOW, 10)
            play_collect_sound()


def draw_power_cans(surface):
    for can in POWER_CANS:
        # Draw power can as a battery instead of circle
        pulse = (math.sin(can["animation"]) + 1) / 2
        pulse_size = int(pulse * 3)

        # Draw outer glow/aura
        pygame.draw.rect(surface, (0, 255, 100, 100),
                         (int(can["x"]) - can["radius"] - 3 - pulse_size,
                          int(can["y"]) - can["radius"] - 3 - pulse_size,
                          can["radius"] * 2 + 6 + pulse_size * 2,
                          can["radius"] * 3 + 6 + pulse_size * 2),
                         border_radius=5)

        # Battery body (main rectangle)
        battery_width = can["radius"] * 2
        battery_height = can["radius"] * 3
        battery_rect = pygame.Rect(
            int(can["x"]) - can["radius"],
            int(can["y"]) - battery_height // 2,
            battery_width,
            battery_height
        )

        # Main battery body
        pygame.draw.rect(surface, POWER_CAN_COLOR, battery_rect, border_radius=3)
        pygame.draw.rect(surface, (0, 150, 50), battery_rect, 2, border_radius=3)

        # Battery terminal/cap (top part)
        terminal_width = battery_width // 3
        terminal_height = battery_height // 6
        terminal_rect = pygame.Rect(
            int(can["x"]) - terminal_width // 2,
            int(can["y"]) - battery_height // 2 - terminal_height + 2,
            terminal_width,
            terminal_height
        )
        pygame.draw.rect(surface, (50, 50, 60), terminal_rect, border_radius=2)

        # Battery charge level indicator
        charge_level = (math.sin(can["animation"] * 2) + 1) / 2
        charge_height = int((battery_height - 6) * charge_level)
        charge_rect = pygame.Rect(
            battery_rect.x + 3,
            battery_rect.y + battery_height - 3 - charge_height,
            battery_width - 6,
            charge_height
        )
        pygame.draw.rect(surface, (0, 255, 100), charge_rect, border_radius=2)

        # Battery plus sign (optional detail)
        plus_size = battery_width // 4
        # Horizontal line of plus sign
        pygame.draw.rect(surface, (0, 150, 50),
                         (int(can["x"]) - plus_size // 2,
                          int(can["y"]) - 1,
                          plus_size, 2))
        # Vertical line of plus sign
        pygame.draw.rect(surface, (0, 150, 50),
                         (int(can["x"]) - 1,
                          int(can["y"]) - plus_size // 2,
                          2, plus_size))


# NEW: Enhanced pilot with flight controller
def draw_realistic_pilot_with_controller(surface, elapsed_time):
    global PILOT_ANIMATION, PILOT_POSITION, CONTROLLER_ANGLE, CONTROLLER_MOVING, CURRENT_CHECK_PHASE, CHECK_PHASE_TIMER

    # Update animation
    PILOT_ANIMATION += 0.05
    CHECK_PHASE_TIMER += 1

    # Change check phase every 2.5 seconds
    if CHECK_PHASE_TIMER > 150:
        CURRENT_CHECK_PHASE = (CURRENT_CHECK_PHASE + 1) % 4
        CHECK_PHASE_TIMER = 0
        play_controller_sound()

    # Update controller animation
    if CONTROLLER_MOVING:
        CONTROLLER_ANGLE += 0.15
        if CONTROLLER_ANGLE > math.pi * 2:
            CONTROLLER_ANGLE = 0

    # Position pilot based on current check phase
    if CURRENT_CHECK_PHASE == 0:
        target_x = drone_center_x - 200
        target_y = center_y + 100
        controller_target = (drone_center_x - 150, center_y - 50)
    elif CURRENT_CHECK_PHASE == 1:
        target_x = drone_center_x
        target_y = center_y + 80
        controller_target = (drone_center_x, center_y)
    elif CURRENT_CHECK_PHASE == 2:
        target_x = drone_center_x + 150
        target_y = center_y + 100
        controller_target = (drone_center_x + 120, center_y - 80)
    else:
        target_x = drone_center_x
        target_y = center_y + 150
        controller_target = (drone_center_x, center_y + 50)

    # Smooth movement
    PILOT_POSITION[0] += (target_x - PILOT_POSITION[0]) * 0.1
    PILOT_POSITION[1] += (target_y - PILOT_POSITION[1]) * 0.1

    # Draw pilot
    draw_detailed_pilot(surface, PILOT_POSITION[0], PILOT_POSITION[1], controller_target)

    # Draw check effects
    draw_check_effects(surface, elapsed_time)


def draw_detailed_pilot(surface, x, y, controller_target):
    # Pilot body with flight suit
    head_radius = 20
    body_width = 45
    body_height = 65
    leg_length = 45

    # Flight helmet
    pygame.draw.circle(surface, PILOT_HELMET, (int(x), int(y - 40)), head_radius + 2)

    # Helmet visor
    visor_rect = pygame.Rect(x - 15, y - 48, 30, 15)
    pygame.draw.ellipse(surface, PILOT_VISOR, visor_rect)

    # Visor reflection
    pygame.draw.ellipse(surface, (200, 230, 255), (x - 12, y - 46, 10, 5))

    # Head (under helmet)
    pygame.draw.circle(surface, SKIN_TONE, (int(x), int(y - 40)), head_radius - 2)

    # Flight suit body
    pygame.draw.rect(surface, PILOT_SUIT, (x - body_width // 2, y - 20, body_width, body_height))

    # Safety harness
    pygame.draw.line(surface, PILOT_HARNESS, (x - body_width // 2, y - 10), (x, y - 5), 4)
    pygame.draw.line(surface, PILOT_HARNESS, (x + body_width // 2, y - 10), (x, y - 5), 4)
    pygame.draw.line(surface, PILOT_HARNESS, (x - body_width // 2, y + 20), (x, y + 15), 4)
    pygame.draw.line(surface, PILOT_HARNESS, (x + body_width // 2, y + 20), (x, y + 15), 4)

    # Harness buckle
    pygame.draw.rect(surface, (200, 180, 60), (x - 8, y + 12, 16, 8))

    # Arms - animated
    left_arm_angle = math.sin(PILOT_ANIMATION) * 0.4 - 0.6
    right_arm_angle = math.sin(PILOT_ANIMATION + 1) * 0.3

    # Left arm (holding controller)
    draw_pilot_arm(surface, x, y, left_arm_angle, 30, PILOT_GLOVES, True, controller_target)

    # Right arm (operating controller)
    draw_pilot_arm(surface, x, y, right_arm_angle, 28, PILOT_GLOVES, False, controller_target)

    # Legs
    left_leg_angle = math.sin(PILOT_ANIMATION * 0.5) * 0.1
    right_leg_angle = math.sin(PILOT_ANIMATION * 0.5 + 1) * 0.1

    draw_pilot_leg(surface, x - 12, y + 45, left_leg_angle, leg_length, PILOT_SUIT)
    draw_pilot_leg(surface, x + 12, y + 45, right_leg_angle, leg_length, PILOT_SUIT)

    # Flight boots
    pygame.draw.rect(surface, BLACK, (x - 20, y + 90, 16, 12))
    pygame.draw.rect(surface, BLACK, (x + 4, y + 90, 16, 12))


def draw_pilot_arm(surface, body_x, body_y, angle, length, color, is_left, controller_target=None):
    direction = -1 if is_left else 1
    start_x = body_x + direction * 18
    start_y = body_y - 8

    # Upper arm
    upper_arm_end_x = start_x + math.cos(angle) * length * direction
    upper_arm_end_y = start_y + math.sin(angle) * length

    # Draw upper arm
    pygame.draw.line(surface, PILOT_SUIT, (start_x, start_y), (upper_arm_end_x, upper_arm_end_y), 10)

    # Shoulder pad
    pygame.draw.circle(surface, PILOT_SUIT, (start_x, start_y), 12)

    # Lower arm
    lower_arm_angle = angle + 0.7
    lower_arm_end_x = upper_arm_end_x + math.cos(lower_arm_angle) * length * 0.8 * direction
    lower_arm_end_y = upper_arm_end_y + math.sin(lower_arm_angle) * length * 0.8

    # Draw lower arm
    pygame.draw.line(surface, PILOT_SUIT, (upper_arm_end_x, upper_arm_end_y),
                     (lower_arm_end_x, lower_arm_end_y), 8)

    # Draw gloved hand
    hand_radius = 8
    pygame.draw.circle(surface, color, (int(lower_arm_end_x), int(lower_arm_end_y)), hand_radius)

    # Draw fingers
    for i in range(4):
        finger_angle = math.radians(20 + i * 15)
        finger_x = lower_arm_end_x + math.cos(finger_angle) * hand_radius * 1.2 * (1 if is_left else -1)
        finger_y = lower_arm_end_y + math.sin(finger_angle) * hand_radius * 1.2
        pygame.draw.circle(surface, color, (int(finger_x), int(finger_y)), 3)

    # Draw flight controller
    if is_left and controller_target:
        draw_flight_controller(surface, lower_arm_end_x, lower_arm_end_y, controller_target)


def draw_pilot_leg(surface, x, y, angle, length, color):
    # Upper leg
    upper_leg_end_x = x + math.cos(angle) * length * 0.6
    upper_leg_end_y = y + math.sin(angle) * length * 0.6

    pygame.draw.line(surface, color, (x, y), (upper_leg_end_x, upper_leg_end_y), 14)

    # Lower leg
    lower_leg_angle = angle - 0.2
    lower_leg_end_x = upper_leg_end_x + math.cos(lower_leg_angle) * length * 0.6
    lower_leg_end_y = upper_leg_end_y + math.sin(lower_leg_angle) * length * 0.6

    pygame.draw.line(surface, color, (upper_leg_end_x, upper_leg_end_y),
                     (lower_leg_end_x, lower_leg_end_y), 12)


def draw_flight_controller(surface, hand_x, hand_y, target):
    global CONTROLLER_ANGLE

    dx = target[0] - hand_x
    dy = target[1] - hand_y
    distance = math.sqrt(dx * dx + dy * dy)

    if distance > 0:
        dx /= distance
        dy /= distance

        controller_length = min(distance, 60)
        controller_x = hand_x + dx * controller_length
        controller_y = hand_y + dy * controller_length

        # Draw controller body
        controller_width = 80
        controller_height = 40
        controller_rect = pygame.Rect(
            controller_x - controller_width // 2,
            controller_y - controller_height // 2,
            controller_width,
            controller_height
        )
        draw_rounded_rect(surface, controller_rect, (30, 30, 40), 8)

        # Draw controller screen
        screen_rect = pygame.Rect(
            controller_x - controller_width // 2 + 5,
            controller_y - controller_height // 2 + 5,
            controller_width - 10,
            15
        )
        pygame.draw.rect(surface, (0, 20, 40), screen_rect)

        # Draw screen content
        screen_text = get_controller_screen_text()
        text_surface = small_font.render(screen_text, True, NEON_GREEN)
        surface.blit(text_surface, (screen_rect.centerx - text_surface.get_width() // 2,
                                    screen_rect.centery - text_surface.get_height() // 2))

        # Draw control sticks
        stick_radius = 6
        left_stick_x = controller_x - 20
        right_stick_x = controller_x + 20
        stick_y = controller_y + 10

        # Animated stick movement
        left_stick_offset = math.sin(CONTROLLER_ANGLE) * 3
        right_stick_offset = math.cos(CONTROLLER_ANGLE) * 3

        pygame.draw.circle(surface, (60, 60, 70), (left_stick_x, stick_y), stick_radius + 2)
        pygame.draw.circle(surface, (200, 60, 60),
                           (int(left_stick_x + left_stick_offset), int(stick_y + left_stick_offset)),
                           stick_radius)

        pygame.draw.circle(surface, (60, 60, 70), (right_stick_x, stick_y), stick_radius + 2)
        pygame.draw.circle(surface, (60, 200, 60),
                           (int(right_stick_x + right_stick_offset), int(stick_y + right_stick_offset)),
                           stick_radius)

        # Draw buttons
        for i in range(4):
            button_x = controller_x - 30 + i * 15
            button_y = controller_y - 5
            pygame.draw.circle(surface, (50, 50, 60), (button_x, button_y), 4)
            pygame.draw.circle(surface, (100, 100, 120), (button_x, button_y), 2)


def get_controller_screen_text():
    texts = ["ROTOR TEST", "SYS CHECK", "GPS CALIB", "READY ✓"]
    return texts[CURRENT_CHECK_PHASE]


def draw_check_effects(surface, elapsed_time):
    if CURRENT_CHECK_PHASE == 0:
        draw_rotor_rpm_display(surface, drone_center_x - 150, center_y - 80)

        if random.random() < 0.15:
            for i in range(4):
                angle = i * math.pi / 2
                particle_x = drone_center_x + math.cos(angle) * 100
                particle_y = center_y + math.sin(angle) * 100
                create_particles(particle_x, particle_y, (200, 200, 255), 3)

    elif CURRENT_CHECK_PHASE == 1:
        draw_system_status(surface, drone_center_x, center_y - 50)

        if random.random() < 0.1:
            create_particles(drone_center_x, center_y, (100, 200, 255), 5)

    elif CURRENT_CHECK_PHASE == 2:
        draw_gps_display(surface, drone_center_x + 120, center_y - 80)

        if random.random() < 0.2:
            create_particles(drone_center_x + 120, center_y - 60, (50, 255, 100), 4)

    else:
        draw_pre_flight_checklist(surface, drone_center_x, center_y + 120)

        if random.random() < 0.1:
            create_particles(drone_center_x + random.randint(-100, 100),
                             center_y + random.randint(-80, 80),
                             NEON_GREEN, 3)


def draw_rotor_rpm_display(surface, x, y):
    pygame.draw.rect(surface, (20, 25, 35), (x - 40, y - 30, 80, 50), border_radius=5)
    pygame.draw.rect(surface, (40, 45, 55), (x - 38, y - 28, 76, 46), border_radius=3)

    rpm_value = 8500 + int(math.sin(PILOT_ANIMATION * 3) * 500)
    rpm_text = small_font.render(f"{rpm_value} RPM", True, NEON_GREEN)
    surface.blit(rpm_text, (x - rpm_text.get_width() // 2, y - 15))

    label = small_font.render("ROTOR", True, WHITE)
    surface.blit(label, (x - label.get_width() // 2, y + 5))


def draw_system_status(surface, x, y):
    pygame.draw.rect(surface, (20, 25, 35), (x - 50, y - 40, 100, 60), border_radius=6)
    pygame.draw.rect(surface, (40, 45, 55), (x - 48, y - 38, 96, 56), border_radius=4)

    status_items = [
        ("BATT", "OK ✓", NEON_GREEN),
        ("GPS", "LOCK ✓", NEON_GREEN),
        ("IMU", "CAL ✓", NEON_GREEN),
        ("RF", "LINK ✓", NEON_GREEN)
    ]

    for i, (label, status, color) in enumerate(status_items):
        label_text = small_font.render(label, True, WHITE)
        status_text = small_font.render(status, True, color)

        surface.blit(label_text, (x - 40, y - 30 + i * 12))
        surface.blit(status_text, (x + 10, y - 30 + i * 12))


def draw_gps_display(surface, x, y):
    pygame.draw.rect(surface, (20, 25, 35), (x - 35, y - 25, 70, 40), border_radius=5)
    pygame.draw.rect(surface, (40, 45, 55), (x - 33, y - 23, 66, 36), border_radius=3)

    signal_strength = int((math.sin(PILOT_ANIMATION * 2) + 1) * 3) + 1

    for i in range(4):
        bar_height = 8 + i * 4
        bar_color = NEON_GREEN if i < signal_strength else (60, 70, 80)
        pygame.draw.rect(surface, bar_color, (x - 20 + i * 8, y - 5, 5, bar_height))

    label = small_font.render("GPS", True, WHITE)
    surface.blit(label, (x - label.get_width() // 2, y + 10))


def draw_pre_flight_checklist(surface, x, y):
    pygame.draw.rect(surface, (30, 35, 45), (x - 70, y - 50, 140, 80), border_radius=8)
    pygame.draw.rect(surface, (50, 55, 70), (x - 68, y - 48, 136, 76), border_radius=6)

    title = small_font.render("PRE-FLIGHT CHECK", True, WHITE)
    surface.blit(title, (x - title.get_width() // 2, y - 40))

    items = ["ROTORS ✓", "SYSTEMS ✓", "GPS ✓", "READY FOR FLIGHT ✓"]

    for i, item in enumerate(items):
        item_text = small_font.render(item, True, NEON_GREEN)
        surface.blit(item_text, (x - item_text.get_width() // 2, y - 20 + i * 12))


def get_check_phase_text():
    phases = [
        "Testing rotor systems...",
        "Checking flight systems...",
        "Calibrating GPS navigation...",
        "Final pre-flight check..."
    ]
    return phases[CURRENT_CHECK_PHASE]


# Draw functions for drone parts
def draw_rounded_rect(surface, rect, color, radius=10):
    pygame.draw.rect(surface, color, rect, border_radius=radius)


def draw_flight_controller_part(surface, rect, dragging=False):
    draw_rounded_rect(surface, rect, BLUE, 5)

    # Circuit board details
    for i in range(5):
        pin_rect = pygame.Rect(rect.x + 10 + i * 15, rect.y + rect.height - 8, 8, 8)
        pygame.draw.rect(surface, GOLD, pin_rect)

    chip_rect = pygame.Rect(rect.x + rect.width // 2 - 15, rect.y + rect.height // 2 - 15, 30, 30)
    pygame.draw.rect(surface, BLACK, chip_rect)

    if not dragging:
        for i in range(3):
            led_x = rect.x + 10 + i * 25
            led_y = rect.y + 10
            pulse = (math.sin(pygame.time.get_ticks() / 200 + i) + 1) / 2
            led_color = (int(50 + 205 * pulse), int(100 + 155 * pulse), 255)
            pygame.draw.circle(surface, led_color, (led_x, led_y), 3)


def draw_drone_battery(surface, rect, dragging=False):
    draw_rounded_rect(surface, rect, YELLOW, 8)

    terminal_rect = pygame.Rect(rect.x + rect.width // 2 - 15, rect.y - 5, 30, 10)
    pygame.draw.rect(surface, SILVER, terminal_rect)

    level_width = rect.width - 20
    level_height = 8
    level_x = rect.x + 10
    level_y = rect.y + rect.height // 2 - level_height // 2

    current_level = int(level_width * BATTERY_LEVEL)

    if BATTERY_LEVEL > 0.7:
        level_color = GREEN
    elif BATTERY_LEVEL > 0.3:
        level_color = YELLOW
    else:
        level_color = RED

    pygame.draw.rect(surface, DARK_GRAY, (level_x, level_y, level_width, level_height))

    if current_level > 0:
        level_rect = pygame.Rect(level_x, level_y, current_level, level_height)
        pygame.draw.rect(surface, level_color, level_rect)

    label_rect = pygame.Rect(rect.x + 10, rect.y + rect.height - 25, rect.width - 20, 15)
    pygame.draw.rect(surface, BLACK, label_rect)

    percent_text = small_font.render(f"{int(BATTERY_LEVEL * 100)}%", True, WHITE)
    percent_rect = percent_text.get_rect(center=label_rect.center)
    surface.blit(percent_text, percent_rect)


def draw_motor_part(surface, rect, dragging=False):
    pygame.draw.circle(surface, RED, rect.center, rect.width // 2)

    shaft_radius = rect.width // 4
    pygame.draw.circle(surface, SILVER, rect.center, shaft_radius)
    pygame.draw.circle(surface, BLACK, rect.center, shaft_radius - 3)

    if not dragging:
        rotation = pygame.time.get_ticks() / 50
        for i in range(3):
            angle = rotation + i * math.pi * 2 / 3
            line_length = shaft_radius + 8
            end_x = rect.centerx + int(line_length * math.cos(angle))
            end_y = rect.centery + int(line_length * math.sin(angle))
            pygame.draw.line(surface, GOLD, rect.center, (end_x, end_y), 2)


def draw_camera_part(surface, rect, dragging=False):
    draw_rounded_rect(surface, rect, PURPLE, 10)

    lens_radius = rect.width // 3
    pygame.draw.circle(surface, BLACK, rect.center, lens_radius)

    reflection_radius = lens_radius // 3
    reflection_pos = (rect.centerx - lens_radius // 3, rect.centery - lens_radius // 3)
    pygame.draw.circle(surface, (100, 100, 150), reflection_pos, reflection_radius)

    if not dragging:
        pulse = (math.sin(pygame.time.get_ticks() / 300) + 1) / 2
        record_color = (int(255 * pulse), 0, 0)
        pygame.draw.circle(surface, record_color, (rect.x + rect.width - 10, rect.y + 10), 3)


def draw_gps_part(surface, rect, dragging=False):
    draw_rounded_rect(surface, rect, CYAN, 8)

    # GPS satellite dish
    dish_radius = rect.width // 3
    pygame.draw.circle(surface, SILVER, rect.center, dish_radius)
    pygame.draw.circle(surface, (80, 80, 100), rect.center, dish_radius - 3)

    # Signal waves
    if not dragging:
        for i in range(2):
            wave_radius = dish_radius + 5 + i * 8
            alpha = 100 - i * 40
            wave_surface = pygame.Surface((wave_radius * 2, wave_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(wave_surface, (*CYAN, alpha), (wave_radius, wave_radius), wave_radius, 2)
            surface.blit(wave_surface, (rect.centerx - wave_radius, rect.centery - wave_radius))


def draw_propeller_part(surface, rect, dragging=False):
    draw_rounded_rect(surface, rect, GREEN, 3)

    # Propeller blades
    blade_length = rect.width - 10
    blade_width = 6

    # Center hub
    hub_radius = 8
    pygame.draw.circle(surface, SILVER, rect.center, hub_radius)

    if not dragging:
        rotation = pygame.time.get_ticks() / 30
        for i in range(2):
            angle = rotation + i * math.pi
            end_x = rect.centerx + int(blade_length * math.cos(angle))
            end_y = rect.centery + int(blade_length * math.sin(angle))

            # Draw blade
            blade_points = [
                (rect.centerx + int(blade_width * math.cos(angle + math.pi / 2)),
                 rect.centery + int(blade_width * math.sin(angle + math.pi / 2))),
                (end_x + int(blade_width * math.cos(angle + math.pi / 2)),
                 end_y + int(blade_width * math.sin(angle + math.pi / 2))),
                (end_x + int(blade_width * math.cos(angle - math.pi / 2)),
                 end_y + int(blade_width * math.sin(angle - math.pi / 2))),
                (rect.centerx + int(blade_width * math.cos(angle - math.pi / 2)),
                 rect.centery + int(blade_width * math.sin(angle - math.pi / 2)))
            ]
            pygame.draw.polygon(surface, GREEN, blade_points)


def draw_drone_part(surface, part, alpha=255):
    if part["dragging"]:
        s = pygame.Surface((part["rect"].width, part["rect"].height), pygame.SRCALPHA)
        temp_rect = pygame.Rect(0, 0, part["rect"].width, part["rect"].height)

        if part["type"] == "Flight Controller":
            draw_flight_controller_part(s, temp_rect, True)
        elif part["type"] == "Battery":
            draw_drone_battery(s, temp_rect, True)
        elif part["type"] == "Motor":
            draw_motor_part(s, temp_rect, True)
        elif part["type"] == "Camera":
            draw_camera_part(s, temp_rect, True)
        elif part["type"] == "GPS":
            draw_gps_part(s, temp_rect, True)
        elif part["type"] == "Propeller":
            draw_propeller_part(s, temp_rect, True)

        s.set_alpha(180)
        surface.blit(s, part["rect"])

        shadow = pygame.Surface((part["rect"].width + 10, part["rect"].height + 10), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0, 0, 0, 100), (0, 0, part["rect"].width + 10, part["rect"].height + 10),
                         border_radius=part["radius"] + 5)
        surface.blit(shadow, (part["rect"].x - 5, part["rect"].y - 5))
    else:
        if part["type"] == "Flight Controller":
            draw_flight_controller_part(surface, part["rect"])
        elif part["type"] == "Battery":
            draw_drone_battery(surface, part["rect"])
        elif part["type"] == "Motor":
            draw_motor_part(surface, part["rect"])
        elif part["type"] == "Camera":
            draw_camera_part(surface, part["rect"])
        elif part["type"] == "GPS":
            draw_gps_part(surface, part["rect"])
        elif part["type"] == "Propeller":
            draw_propeller_part(surface, part["rect"])


def draw_drone_slot(surface, slot, parts):
    slot_filled = False
    for part in parts:
        if part["placed"] and part["placed_slot"] == slot:
            slot_filled = True
            break

    color = GREEN if slot_filled else RED
    draw_rounded_rect(surface, slot["rect"], color, 10)

    text = font.render(slot["type"], True, WHITE)
    text_rect = text.get_rect(center=slot["rect"].center)
    surface.blit(text, text_rect)


def draw_drone_wires(surface, slots, parts):
    global WIRE_ANIMATION
    WIRE_ANIMATION += 0.02

    for i, slot in enumerate(slots):
        part_in_slot = None
        for part in parts:
            if part["placed"] and part["placed_slot"] == slot:
                part_in_slot = part
                break

        if part_in_slot:
            for connected_slot_idx in slot["connected_to"]:
                connected_slot = slots[connected_slot_idx]
                connected_part = None
                for part in parts:
                    if part["placed"] and part["placed_slot"] == connected_slot:
                        connected_part = part
                        break

                if connected_part:
                    start_pos = part_in_slot["rect"].center
                    end_pos = connected_part["rect"].center

                    control_x = (start_pos[0] + end_pos[0]) // 2
                    control_y = min(start_pos[1], end_pos[1]) - 80

                    points = []
                    for t in range(0, 101, 5):
                        t = t / 100
                        x = (1 - t) ** 2 * start_pos[0] + 2 * (1 - t) * t * control_x + t ** 2 * end_pos[0]
                        y = (1 - t) ** 2 * start_pos[1] + 2 * (1 - t) * t * control_y + t ** 2 * end_pos[1]
                        points.append((x, y))

                    if len(points) > 1:
                        pygame.draw.lines(surface, ORANGE, False, points, 3)
                        pygame.draw.circle(surface, ORANGE, start_pos, 6)
                        pygame.draw.circle(surface, ORANGE, end_pos, 6)


def draw_assembled_drone(surface, x, y, rotor_animation=0):
    # Main drone body (X shape)
    body_radius = 60
    arm_length = 120

    # Draw arms
    for i in range(4):
        angle = i * math.pi / 2
        arm_x = x + math.cos(angle) * arm_length
        arm_y = y + math.sin(angle) * arm_length

        # Draw arm
        pygame.draw.line(surface, METAL_GRAY, (x, y), (arm_x, arm_y), 12)

        # Draw motor at end of arm
        motor_radius = 25
        pygame.draw.circle(surface, RED, (int(arm_x), int(arm_y)), motor_radius)
        pygame.draw.circle(surface, SILVER, (int(arm_x), int(arm_y)), motor_radius - 5)

        # Draw rotating propeller
        if rotor_animation > 0:
            prop_radius = 40
            blade_angle = rotor_animation + i * math.pi / 2

            for j in range(2):
                blade_angle_actual = blade_angle + j * math.pi
                blade_x = arm_x + math.cos(blade_angle_actual) * prop_radius
                blade_y = arm_y + math.sin(blade_angle_actual) * prop_radius

                blade_points = [
                    (arm_x + math.cos(blade_angle_actual + 0.2) * 10,
                     arm_y + math.sin(blade_angle_actual + 0.2) * 10),
                    (blade_x, blade_y),
                    (arm_x + math.cos(blade_angle_actual - 0.2) * 10,
                     arm_y + math.sin(blade_angle_actual - 0.2) * 10)
                ]
                pygame.draw.polygon(surface, GREEN, blade_points)

    # Central body - UPDATED: Use DRONE_BODY_COLOR which changes with energy collection
    pygame.draw.circle(surface, DARK_GRAY, (x, y), body_radius)
    pygame.draw.circle(surface, DRONE_BODY_COLOR, (x, y), body_radius - 10)

    # Camera on front
    camera_x = x + body_radius - 10
    camera_y = y
    pygame.draw.rect(surface, PURPLE, (camera_x, camera_y - 15, 20, 30), border_radius=5)
    pygame.draw.circle(surface, BLACK, (camera_x + 10, camera_y), 8)

    # GPS module on top
    gps_x = x
    gps_y = y - body_radius + 10
    pygame.draw.rect(surface, CYAN, (gps_x - 15, gps_y - 10, 30, 20), border_radius=3)

    # Status LED - also changes color with drone body
    led_pulse = (math.sin(pygame.time.get_ticks() / 200) + 1) / 2
    led_red = min(255, DRONE_BODY_COLOR[0] + 50)
    led_green = min(255, DRONE_BODY_COLOR[1] + 50)
    led_blue = min(255, DRONE_BODY_COLOR[2] + 50)
    led_color = (int(led_red * led_pulse), int(led_green * led_pulse), int(led_blue * led_pulse))
    pygame.draw.circle(surface, led_color, (x, y), 5)


def draw_hangar_background(surface):
    # Hangar walls
    wall_color = (35, 40, 45)
    pygame.draw.rect(surface, wall_color, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    # Hangar floor
    floor_color = (45, 50, 55)
    pygame.draw.rect(surface, floor_color, (0, SCREEN_HEIGHT - 200, SCREEN_WIDTH, 200))

    # Workbenches
    bench_color = (60, 65, 70)
    for i in range(2):
        bench_rect = pygame.Rect(100 + i * 400, SCREEN_HEIGHT - 180, 300, 30)
        pygame.draw.rect(surface, bench_color, bench_rect)

        # Bench legs
        pygame.draw.rect(surface, (50, 55, 60), (100 + i * 400, SCREEN_HEIGHT - 150, 20, 150))
        pygame.draw.rect(surface, (50, 55, 60), (380 + i * 400, SCREEN_HEIGHT - 150, 20, 150))

    # Tool cabinets
    cabinet_color = (70, 75, 80)
    for i in range(3):
        cabinet_rect = pygame.Rect(SCREEN_WIDTH - 200, 100 + i * 120, 150, 100)
        pygame.draw.rect(surface, cabinet_color, cabinet_rect)
        pygame.draw.rect(surface, (90, 95, 100), cabinet_rect, 2)

        # Drawers
        for j in range(3):
            drawer_rect = pygame.Rect(SCREEN_WIDTH - 190, 110 + i * 120 + j * 25, 130, 20)
            pygame.draw.rect(surface, (60, 65, 70), drawer_rect)
            pygame.draw.rect(surface, (100, 105, 110), drawer_rect, 1)


def draw_drone_assembly_station(surface):
    # Assembly platform - INCREASED SIZE
    platform_rect = pygame.Rect(drone_center_x - 180, center_y - 180, 360, 360)
    pygame.draw.rect(surface, (50, 55, 60), platform_rect, border_radius=10)
    pygame.draw.rect(surface, (70, 75, 80), platform_rect, 3, border_radius=10)

    # Grid pattern on platform
    for i in range(6):
        for j in range(6):
            cell_x = drone_center_x - 150 + i * 50
            cell_y = center_y - 150 + j * 50
            cell_rect = pygame.Rect(cell_x, cell_y, 45, 45)
            pygame.draw.rect(surface, (60, 65, 70), cell_rect, 1)


def draw_parts_panel(surface):
    panel_rect = pygame.Rect(30, 120, 250, SCREEN_HEIGHT - 200)
    pygame.draw.rect(surface, (40, 45, 55), panel_rect)
    pygame.draw.rect(surface, (70, 75, 85), panel_rect, 3)

    title_text = font.render("DRONE COMPONENTS", True, LIGHT_BLUE)
    title_y = panel_rect.bottom - 30
    surface.blit(title_text, (35, title_y))

    pygame.draw.line(surface, (70, 75, 85), (30, 150), (280, 150), 2)


def draw_level_intro(surface, timer):
    surface.fill((0, 0, 0))

    pulse = (math.sin(timer / 200) + 1) / 2
    pulse_scale = 0.5 + pulse * 0.5

    level_text = title_font.render("LEVEL 2", True, WHITE)
    level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))

    scaled_text = pygame.transform.scale(
        level_text,
        (int(level_text.get_width() * pulse_scale),
         int(level_text.get_height() * pulse_scale))
    )
    scaled_rect = scaled_text.get_rect(center=level_rect.center)
    surface.blit(scaled_text, scaled_rect)

    subtitle_text = font.render("DRONE ASSEMBLY", True, CYAN)
    subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
    surface.blit(subtitle_text, subtitle_rect)

    if timer > 1500:
        alpha = min(255, (timer - 1500) * 2)
        instruction_text = small_font.render("Assemble the drone to make it fly", True, (200, 200, 200))
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))

        instruction_surface = pygame.Surface(instruction_text.get_size(), pygame.SRCALPHA)
        instruction_surface.fill((0, 0, 0, 0))
        instruction_surface.blit(instruction_text, (0, 0))
        instruction_surface.set_alpha(alpha)
        surface.blit(instruction_surface, instruction_rect)


def check_win_condition(parts, slots):
    correctly_filled = 0
    for slot in slots:
        for part in parts:
            if part["placed"] and part["placed_slot"] == slot and part["type"] == slot["type"]:
                correctly_filled += 1
                break
    return correctly_filled == len(slots)


def draw_score(surface):
    score_panel = pygame.Rect(SCREEN_WIDTH - 250, 20, 230, 60)
    pygame.draw.rect(surface, (40, 45, 55), score_panel, border_radius=10)
    pygame.draw.rect(surface, (70, 75, 85), score_panel, 2, border_radius=10)

    score_text = font.render(f"SCORE: {SCORE}", True, WHITE)
    surface.blit(score_text, (SCREEN_WIDTH - 240, 30))

    if COMBO > 1:
        combo_text = font.render(f"COMBO: x{COMBO}", True, NEON_GREEN)
        surface.blit(combo_text, (SCREEN_WIDTH - 240, 55))


# NEW: Draw power can counter
def draw_power_can_counter(surface):
    power_panel = pygame.Rect(SCREEN_WIDTH - 250, 90, 230, 60)
    pygame.draw.rect(surface, (40, 45, 55), power_panel, border_radius=10)
    pygame.draw.rect(surface, (70, 75, 85), power_panel, 2, border_radius=10)

    power_text = font.render(f"ENERGY: {POWER_CANS_COLLECTED}/{TOTAL_POWER_CANS}", True, WHITE)
    surface.blit(power_text, (SCREEN_WIDTH - 240, 100))

    progress_width = 200
    progress_filled = int(progress_width * (POWER_CANS_COLLECTED / TOTAL_POWER_CANS))
    pygame.draw.rect(surface, DARK_GRAY, (SCREEN_WIDTH - 230, 125, progress_width, 10), border_radius=5)
    if progress_filled > 0:
        pygame.draw.rect(surface, POWER_CAN_COLOR, (SCREEN_WIDTH - 230, 125, progress_filled, 10), border_radius=5)


def draw_control_buttons(surface, mouse_pos):
    escape_hover = ESCAPE_BUTTON.collidepoint(mouse_pos)
    escape_color = (180, 60, 60) if escape_hover else (150, 50, 50)
    pygame.draw.rect(surface, escape_color, ESCAPE_BUTTON, border_radius=8)
    pygame.draw.rect(surface, WHITE, ESCAPE_BUTTON, 2, border_radius=8)

    escape_text = font.render("ESC - Main Menu", True, WHITE)
    escape_text_rect = escape_text.get_rect(center=ESCAPE_BUTTON.center)
    surface.blit(escape_text, escape_text_rect)

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
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surface.blit(overlay, (0, 0))

    # Draw title
    pause_text = title_font.render("GAME PAUSED", True, YELLOW)
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
    instruction = small_font.render("Press P or click RESUME to continue", True, WHITE)
    surface.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2, SCREEN_HEIGHT // 2 + 160))

    return resume_hover, menu_hover


# NEW: Draw game over screen
def draw_game_over(surface):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surface.blit(overlay, (0, 0))

    game_over_text = title_font.render("GAME OVER", True, RED)
    surface.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))

    score_text = font.render(f"Final Score: {SCORE}", True, WHITE)
    surface.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))

    power_text = font.render(f"Energy Collected: {POWER_CANS_COLLECTED}/{TOTAL_POWER_CANS}", True, WHITE)
    surface.blit(power_text, (SCREEN_WIDTH // 2 - power_text.get_width() // 2, SCREEN_HEIGHT // 2 + 30))

    restart_text = font.render("Press R to restart or ESC to quit", True, YELLOW)
    surface.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 80))


# NEW: Draw victory screen with button
def draw_victory_screen(surface, mouse_pos):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 50, 0, 180))
    surface.blit(overlay, (0, 0))

    victory_text = title_font.render("VICTORY!", True, NEON_GREEN)
    surface.blit(victory_text, (SCREEN_WIDTH // 2 - victory_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))

    score_text = font.render(f"Final Score: {SCORE}", True, WHITE)
    surface.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))

    power_text = font.render(f"Collected all {TOTAL_POWER_CANS} energy cans!", True, WHITE)
    surface.blit(power_text, (SCREEN_WIDTH // 2 - power_text.get_width() // 2, SCREEN_HEIGHT // 2 + 30))

    # Draw next level button
    button_color = NEXT_LEVEL_BUTTON_HOVER_COLOR if VICTORY_BUTTON_RECT.collidepoint(
        mouse_pos) else NEXT_LEVEL_BUTTON_COLOR
    pygame.draw.rect(surface, button_color, VICTORY_BUTTON_RECT, border_radius=12)
    pygame.draw.rect(surface, WHITE, VICTORY_BUTTON_RECT, 3, border_radius=12)

    button_text = title_font.render("NEXT LEVEL", True, WHITE)
    text_rect = button_text.get_rect(center=VICTORY_BUTTON_RECT.center)
    surface.blit(button_text, text_rect)

    instruction_text = small_font.render("Click to launch Dogbot Level 3", True, WHITE)
    instruction_rect = instruction_text.get_rect(center=(VICTORY_BUTTON_RECT.centerx, VICTORY_BUTTON_RECT.bottom + 20))
    surface.blit(instruction_text, instruction_rect)


# NEW: Draw pre-flight state with pilot
def draw_pre_flight_state(surface, elapsed_time):
    draw_hangar_background(surface)
    draw_drone_assembly_station(surface)
    draw_assembled_drone(surface, drone_center_x, center_y, 0)

    title_text = title_font.render("PRE-FLIGHT SYSTEMS CHECK", True, LIGHT_BLUE)
    surface.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 40))

    draw_particles(surface)
    draw_score(surface)

    draw_realistic_pilot_with_controller(surface, elapsed_time)
    draw_control_buttons(surface, pygame.mouse.get_pos())

    remaining_time = max(0, (PRE_FLIGHT_DURATION - elapsed_time) // 1000)
    countdown_text = title_font.render(f"Pre-flight: {remaining_time} seconds", True, YELLOW)
    surface.blit(countdown_text, (SCREEN_WIDTH // 2 - countdown_text.get_width() // 2, SCREEN_HEIGHT - 100))

    phase_text = font.render(get_check_phase_text(), True, WHITE)
    surface.blit(phase_text, (SCREEN_WIDTH // 2 - phase_text.get_width() // 2, SCREEN_HEIGHT - 140))


def check_quit():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        go_to_main_menu()


def reset_game():
    global drone_parts, part_id, game_state, drone_x, drone_y, drone_altitude
    global ROTOR_ANIMATION, ENEMIES, POWER_CANS, POWER_CANS_COLLECTED, DRONE_BODY_COLOR
    global ENEMY_SPAWN_TIMER, GAME_OVER, SCORE, COMBO, WIN_SOUND_PLAYED, PAUSED
    global PRE_FLIGHT_TIMER, PILOT_ANIMATION, PILOT_POSITION, CONTROLLER_ANGLE
    global CURRENT_CHECK_PHASE, CHECK_PHASE_TIMER, ENEMY_GROUP_COUNTER, ENEMY_GROUP_TIMER
    global POWER_CAN_SPAWN_TIMER, SHOW_DRONE_IMAGE

    drone_parts = []
    part_id = 0
    for part_type, part_info in DRONE_PARTS.items():
        for i in range(part_info["count"]):
            column = part_id // parts_per_column
            row = part_id % parts_per_column

            x_pos = 50 + column * 130
            y_pos = 180 + row * 140

            drone_parts.append({
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

    game_state = ASSEMBLY_STATE
    drone_x = drone_center_x
    drone_y = SCREEN_HEIGHT - 300
    drone_altitude = 0
    ROTOR_ANIMATION = 0
    ENEMIES = []
    POWER_CANS = []
    POWER_CANS_COLLECTED = 0
    DRONE_BODY_COLOR = BLUE
    ENEMY_SPAWN_TIMER = 0
    GAME_OVER = False
    SCORE = 0
    COMBO = 0
    WIN_SOUND_PLAYED = False
    PAUSED = False
    PRE_FLIGHT_TIMER = 0
    PILOT_ANIMATION = 0
    PILOT_POSITION = [drone_center_x - 300, center_y + 100]
    CONTROLLER_ANGLE = 0
    CURRENT_CHECK_PHASE = 0
    CHECK_PHASE_TIMER = 0
    ENEMY_GROUP_COUNTER = 0
    ENEMY_GROUP_TIMER = 0
    POWER_CAN_SPAWN_TIMER = 0
    SHOW_DRONE_IMAGE = True

    play_background_music()


# Main game loop
clock = pygame.time.Clock()
dragging_part = None
offset_x, offset_y = 0, 0
game_state = LEVEL_INTRO_STATE
intro_timer = 0
success_timer = 0

play_background_music()

while True:
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Handle pause with mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_click = True

            if PAUSED:
                resume_hover, menu_hover = draw_pause_screen(screen, mouse_pos)
                if resume_hover:
                    PAUSED = False
                elif menu_hover:
                    go_to_main_menu()
            else:
                if game_state == ASSEMBLY_STATE:
                    escape_hover, pause_hover = draw_control_buttons(screen, mouse_pos)
                    if escape_hover:
                        go_to_main_menu()
                    elif pause_hover:
                        PAUSED = True
                    else:
                        for part in drone_parts:
                            if part["rect"].collidepoint(event.pos) and not part["placed"]:
                                part["dragging"] = True
                                dragging_part = part
                                offset_x = part["rect"].x - event.pos[0]
                                offset_y = part["rect"].y - event.pos[1]
                                break

                elif game_state in [PRE_FLIGHT_STATE, FLIGHT_STATE]:
                    escape_hover, pause_hover = draw_control_buttons(screen, mouse_pos)
                    if escape_hover:
                        go_to_main_menu()
                    elif pause_hover:
                        PAUSED = True

                # Check for next level button in victory state
                elif game_state == VICTORY_STATE:
                    if VICTORY_BUTTON_RECT.collidepoint(event.pos):
                        transition_to_dogbot_level()
                    else:
                        escape_hover, pause_hover = draw_control_buttons(screen, mouse_pos)
                        if escape_hover:
                            go_to_main_menu()
                        elif pause_hover:
                            PAUSED = True

        if not PAUSED:
            if game_state == ASSEMBLY_STATE:
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and dragging_part:
                        dragging_part["dragging"] = False

                        part_placed = False
                        for slot in DRONE_SLOTS:
                            if (slot["rect"].colliderect(dragging_part["rect"]) and
                                    dragging_part["type"] == slot["type"]):
                                slot_already_filled = False
                                for other_part in drone_parts:
                                    if other_part["placed"] and other_part["placed_slot"] == slot:
                                        slot_already_filled = True
                                        break

                                if not slot_already_filled:
                                    dragging_part["rect"].center = slot["rect"].center
                                    dragging_part["placed"] = True
                                    dragging_part["placed_slot"] = slot
                                    play_success_sound()

                                    current_time = pygame.time.get_ticks()
                                    time_since_last = current_time - LAST_PLACEMENT_TIME
                                    if time_since_last < 2000:
                                        COMBO += 1
                                    else:
                                        COMBO = 1

                                    SCORE += 10 * COMBO
                                    LAST_PLACEMENT_TIME = current_time

                                    create_particles(slot["rect"].centerx, slot["rect"].centery, dragging_part["color"],
                                                     15)
                                    part_placed = True
                                    break

                        if not part_placed:
                            dragging_part["rect"].topleft = dragging_part["original_pos"]
                            play_failure_sound()
                            COMBO = 0

                        dragging_part = None

                        if check_win_condition(drone_parts, DRONE_SLOTS):
                            game_state = SUCCESS_STATE
                            success_timer = pygame.time.get_ticks()
                            SCORE += 100 * COMBO if COMBO > 0 else 100

                elif event.type == pygame.MOUSEMOTION:
                    if dragging_part:
                        dragging_part["rect"].x = event.pos[0] + offset_x
                        dragging_part["rect"].y = event.pos[1] + offset_y

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                PAUSED = not PAUSED

            # Handle ESC key properly
            if event.key == pygame.K_ESCAPE:
                # Don't go to main menu if paused (let pause screen handle it)
                if not PAUSED:
                    go_to_main_menu()
                elif PAUSED:
                    # Allow ESC to exit from pause screen
                    go_to_main_menu()

            if event.key == pygame.K_RETURN and game_state == SUCCESS_STATE and not PAUSED:
                game_state = PRE_FLIGHT_STATE
                PRE_FLIGHT_TIMER = pygame.time.get_ticks()
                play_pilot_sound()
                # Hide drone image when moving to pre-flight state
                SHOW_DRONE_IMAGE = False

            if event.key == pygame.K_r and (GAME_OVER or game_state == VICTORY_STATE) and not PAUSED:
                reset_game()

    check_quit()

    if not PAUSED:
        if game_state == LEVEL_INTRO_STATE:
            intro_timer += clock.get_time()
            if intro_timer > 4000:
                game_state = ASSEMBLY_STATE

        elif game_state == SUCCESS_STATE:
            pass

        # NEW: PRE_FLIGHT_STATE - pilot checking the drone
        elif game_state == PRE_FLIGHT_STATE:
            elapsed_time = pygame.time.get_ticks() - PRE_FLIGHT_TIMER

            PILOT_ANIMATION += 0.05

            if random.random() < 0.2:
                spark_x = drone_center_x + random.randint(-150, 150)
                spark_y = center_y + random.randint(-100, 100)
                create_particles(spark_x, spark_y, (100, 200, 255), 4)

            if elapsed_time >= PRE_FLIGHT_DURATION:
                game_state = FLIGHT_STATE
                play_takeoff_sound()
                play_rotor_sound()
                # Ensure drone image is hidden in flight state
                SHOW_DRONE_IMAGE = False

        elif game_state == FLIGHT_STATE:
            # Basic drone flight controls - FIXED: Allow movement to top of screen
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                drone_altitude = min(drone_altitude + 3, max_altitude)
            if keys[pygame.K_s]:
                drone_altitude = max(drone_altitude - 3, 0)
            if keys[pygame.K_a]:
                drone_x = max(drone_x - 5, 100)
            if keys[pygame.K_d]:
                drone_x = min(drone_x + 5, SCREEN_WIDTH - 100)
            if keys[pygame.K_UP]:
                # FIXED: Allow moving to top of screen by removing the lower bound
                drone_y = max(drone_y - 3, 50)
            if keys[pygame.K_DOWN]:
                drone_y = min(drone_y + 3, SCREEN_HEIGHT - 100)

            # FIXED: Allow drone to move to top of screen by adjusting altitude calculation
            drone_y = SCREEN_HEIGHT - 300 - drone_altitude

            # Ensure drone doesn't go above the top of the screen
            drone_y = max(50, drone_y)

            ROTOR_ANIMATION += 0.3

            # NEW: Update drone color based on energy cans collected
            update_drone_color()

            # NEW: Group enemy spawning - enemies come more frequently with reduced gap
            ENEMY_GROUP_TIMER += 1

            # Calculate dynamic gap based on time or score
            dynamic_gap = max(40, ENEMY_GROUP_GAP - (POWER_CANS_COLLECTED // 5))

            if ENEMY_GROUP_TIMER > dynamic_gap and POWER_CANS_COLLECTED < TOTAL_POWER_CANS:
                # Spawn a group of 4 enemies (increased from 3)
                if ENEMY_GROUP_COUNTER < ENEMY_GROUP_SIZE:
                    create_enemy()
                    ENEMY_GROUP_COUNTER += 1
                    ENEMY_GROUP_TIMER = 0
                else:
                    # Finished spawning group, wait for gap
                    if ENEMY_GROUP_TIMER > dynamic_gap * 1.2:
                        ENEMY_GROUP_COUNTER = 0
                        ENEMY_GROUP_TIMER = 0

            # NEW: Power can spawning
            POWER_CAN_SPAWN_TIMER += 1
            if (POWER_CAN_SPAWN_TIMER > POWER_CAN_SPAWN_INTERVAL and
                    len(POWER_CANS) < 15 and
                    POWER_CANS_COLLECTED < TOTAL_POWER_CANS):
                create_power_can()
                POWER_CAN_SPAWN_TIMER = 0

            # Update enemies and power cans
            update_enemies()
            update_power_cans()

            # Create drone exhaust particles - color matches drone body
            if pygame.time.get_ticks() % 5 == 0:
                create_particles(drone_x, drone_y + 60, DRONE_BODY_COLOR, 1)

            # NEW: Check for victory condition - collect 40 power cans
            if POWER_CANS_COLLECTED >= TOTAL_POWER_CANS and game_state != VICTORY_STATE:
                game_state = VICTORY_STATE
                # Create celebration particles
                create_particles(drone_x, drone_y, NEON_GREEN, 100)
                create_particles(drone_x, drone_y, GOLD, 80)
                create_particles(drone_x, drone_y, CYAN, 60)
                create_particles(drone_x, drone_y, POWER_CAN_COLOR, 120)

                # Play win sound
                if not WIN_SOUND_PLAYED:
                    play_win_sound()
                    WIN_SOUND_PLAYED = True
                    stop_background_music()

        update_particles()
        update_battery()

    screen.fill(BACKGROUND)

    if game_state == LEVEL_INTRO_STATE:
        draw_level_intro(screen, intro_timer)

    elif game_state == ASSEMBLY_STATE or game_state == SUCCESS_STATE:
        draw_hangar_background(screen)
        draw_parts_panel(screen)

        lab_panel = pygame.Rect(250, 80, SCREEN_WIDTH - 280, SCREEN_HEIGHT - 150)
        s = pygame.Surface((lab_panel.width, lab_panel.height), pygame.SRCALPHA)
        pygame.draw.rect(s, (*PANEL_BG, 200), (0, 0, lab_panel.width, lab_panel.height), border_radius=20)
        screen.blit(s, lab_panel)

        title_text = title_font.render("DRONE ASSEMBLY STATION", True, LIGHT_BLUE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 40))

        draw_drone_assembly_station(screen)
        draw_assembled_drone(screen, drone_center_x, center_y, 0)

        for slot in DRONE_SLOTS:
            draw_drone_slot(screen, slot, drone_parts)

        draw_drone_wires(screen, DRONE_SLOTS, drone_parts)

        for part in drone_parts:
            draw_drone_part(screen, part)

        draw_particles(screen)
        draw_score(screen)

        # NEW: Draw drone image under score during assembly state - NOW LARGER
        draw_drone_image_under_score(screen)

        instructions = font.render("Drag components from the left panel to the drone assembly", True, WHITE)
        screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, SCREEN_HEIGHT - 50))

        placed_count = sum(1 for part in drone_parts if part["placed"])
        total_count = len(drone_parts)
        count_text = small_font.render(f"Components Placed: {placed_count}/{total_count}", True, WHITE)
        screen.blit(count_text, (SCREEN_WIDTH - count_text.get_width() - 30, SCREEN_HEIGHT - 80))

        hint_text = small_font.render("Match the component shapes to the slots on the drone", True, YELLOW)
        screen.blit(hint_text, (SCREEN_WIDTH // 2 - hint_text.get_width() // 2, SCREEN_HEIGHT - 30))

        draw_control_buttons(screen, mouse_pos)

        if game_state == SUCCESS_STATE:
            win_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            win_surface.fill((0, 0, 0, 150))
            screen.blit(win_surface, (0, 0))

            win_text = title_font.render("DRONE ASSEMBLED SUCCESSFULLY!", True, GREEN)
            screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))

            bonus_text = font.render(f"Bonus: +{100 * COMBO if COMBO > 0 else 100} points!", True, NEON_GREEN)
            screen.blit(bonus_text, (SCREEN_WIDTH // 2 - bonus_text.get_width() // 2, SCREEN_HEIGHT // 2))

            activation_text = font.render("Press ENTER for pre-flight systems check", True, WHITE)
            screen.blit(activation_text,
                        (SCREEN_WIDTH // 2 - activation_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))

    # NEW: PRE_FLIGHT_STATE - show pilot with flight controller
    elif game_state == PRE_FLIGHT_STATE:
        elapsed_time = pygame.time.get_ticks() - PRE_FLIGHT_TIMER
        draw_pre_flight_state(screen, elapsed_time)

    elif game_state == FLIGHT_STATE or game_state == VICTORY_STATE:
        # Draw sky background
        sky_color = (30, 40, 60)
        pygame.draw.rect(screen, sky_color, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        # Draw some clouds
        for i in range(5):
            cloud_x = (i * 300 + pygame.time.get_ticks() // 50) % (SCREEN_WIDTH + 400) - 200
            cloud_y = 100 + (i * 80) % 200
            pygame.draw.circle(screen, (200, 220, 240), (cloud_x, cloud_y), 40)
            pygame.draw.circle(screen, (200, 220, 240), (cloud_x + 30, cloud_y - 10), 35)
            pygame.draw.circle(screen, (200, 220, 240), (cloud_x + 60, cloud_y), 40)

        draw_particles(screen)
        draw_score(screen)

        # NEW: Draw power can counter
        draw_power_can_counter(screen)

        # NEW: Draw minimap camera
        draw_minimap_camera(screen, drone_x, drone_y, ENEMIES, POWER_CANS)

        # Draw flying drone - UPDATED: Now uses DRONE_BODY_COLOR that changes with energy collection
        draw_assembled_drone(screen, drone_x, drone_y, ROTOR_ANIMATION)

        # NEW: Draw enemies and power cans
        draw_enemies(screen)
        draw_power_cans(screen)

        flight_text = title_font.render("DRONE IS FLYING!", True, GREEN)
        screen.blit(flight_text, (SCREEN_WIDTH // 2 - flight_text.get_width() // 2, 100))

        # UPDATED: Changed instructions to reflect new gameplay
        instructions = font.render("Use W/A/S/D keys to fly, collect 40 energy cans to win", True, WHITE)
        screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, SCREEN_HEIGHT - 50))

        # Add warning about enemies
        warning_text = small_font.render("Avoid passenger planes, small drones, and birds!", True, YELLOW)
        screen.blit(warning_text, (SCREEN_WIDTH // 2 - warning_text.get_width() // 2, SCREEN_HEIGHT - 80))

        altitude_text = font.render(f"Altitude: {drone_altitude}m", True, WHITE)
        screen.blit(altitude_text, (SCREEN_WIDTH - 200, 150))

        # NEW: Show drone power level
        power_level = small_font.render(f"Drone Power: {POWER_CANS_COLLECTED}/{TOTAL_POWER_CANS}", True, WHITE)
        screen.blit(power_level, (SCREEN_WIDTH - 200, 180))

        draw_control_buttons(screen, mouse_pos)

        # NEW: Draw game over screen if game over
        if GAME_OVER:
            draw_game_over(screen)
        # NEW: Draw victory screen if collected all power cans
        elif game_state == VICTORY_STATE:
            draw_victory_screen(screen, mouse_pos)

    if PAUSED:
        draw_pause_screen(screen, mouse_pos)

    pygame.display.flip()
    clock.tick(60)