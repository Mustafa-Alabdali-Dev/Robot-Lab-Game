import pygame
import sys
import math
import os
import subprocess
import random
import array
import wave
import io

# Initialize pygame
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

# Get screen info and set to full screen
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Snower Assembly Lab - Level 1")

# Colors - Add leaf colors
BACKGROUND = (20, 25, 40)
PANEL_BG = (30, 35, 50)
RED = (220, 60, 60)
GREEN = (60, 220, 60)
DARK_GREEN = (0, 150, 0)  # Added dark green
BLUE = (60, 120, 220)
YELLOW = (220, 220, 60)
PURPLE = (180, 60, 220)
CYAN = (60, 220, 220)
DARK_CYAN = (0, 150, 150)
WHITE = (240, 240, 240)
GRAY = (120, 120, 120)
DARK_GRAY = (60, 60, 70)
METAL_GRAY = (100, 110, 120)
TRACK_GRAY = (80, 85, 90)
SNOW_BLUE = (200, 220, 240)
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

# Additional colors for street scene
STREET_GRAY = (80, 85, 90)
ROAD_MARKING = (255, 255, 200)
SIDEWALK_GRAY = (180, 180, 190)
GRASS_GREEN = (60, 180, 80)
TREE_GREEN = (30, 100, 40)
TREE_BROWN = (100, 70, 30)
BUILDING_BROWN = (120, 100, 80)
BUILDING_GRAY = (150, 140, 130)
LAMP_POST = (100, 100, 100)
LAMP_LIGHT = (255, 255, 200)
LAMP_GLOW = (255, 255, 100)

# Leaf colors
LEAF_GREEN = (40, 180, 60)
LEAF_YELLOW = (220, 200, 40)
LEAF_ORANGE = (255, 140, 30)
LEAF_BROWN = (160, 110, 60)

STONE_COLORS = [
    (140, 130, 120),  # Gray stone
    (120, 110, 100),  # Darker gray
    (160, 150, 140),  # Light gray
    (130, 120, 110),  # Medium gray
    (150, 140, 130),  # Warm gray
]

# Minimap colors
MINIMAP_COLOR = (30, 40, 60)
MINIMAP_BORDER = (60, 80, 100)

# Get base directory
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print(f"Snowbot Game - Base directory: {BASE_DIR}")


# NEW: Load snower image - SIMILAR TO DRONE IMAGE
def load_snower_image():
    """Load the snower.png image from multiple possible locations"""
    possible_paths = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "snower.png"),
        os.path.join(BASE_DIR, "snower.png"),
        os.path.join(os.getcwd(), "snower.png"),
    ]

    snower_image = None
    loaded_path = None

    for path in possible_paths:
        if os.path.exists(path):
            try:
                snower_image = pygame.image.load(path).convert_alpha()
                loaded_path = path
                print(f"✓ Snower image loaded from: {path}")
                break
            except Exception as e:
                print(f"✗ Could not load image from {path}: {e}")

    if snower_image is None:
        print("✗ snower.png not found in any location. Creating placeholder.")
        # Create a placeholder surface
        snower_image = pygame.Surface((350, 250), pygame.SRCALPHA)
        pygame.draw.rect(snower_image, BROWN, (0, 0, 350, 250), border_radius=15)
        text = pygame.font.SysFont("Arial", 24).render("SNOWER IMAGE", True, WHITE)
        snower_image.blit(text, (100, 115))

    # Resize image to fit under score panel
    snower_image = pygame.transform.scale(snower_image, (350, 250))
    return snower_image


# Load snower image
SNOWER_IMAGE = load_snower_image()

# NEW: Snower image display variables
SNOWER_IMAGE_RECT = pygame.Rect(SCREEN_WIDTH - 320, 90, 350, 250)  # Same position as drone game
SHOW_SNOWER_IMAGE = True  # Controls when to show the image


# Create a simple beep sound for collection
def create_beep_sound():
    try:
        # Create a simple beep sound (440Hz for 0.2 seconds)
        sample_rate = 44100
        duration = 0.2
        frequency = 440

        # Generate sine wave
        n_samples = int(sample_rate * duration)
        buf = bytearray()

        for i in range(n_samples):
            # Generate sine wave
            sample = int(32767 * 0.5 * math.sin(2.0 * math.pi * frequency * i / sample_rate))
            # Convert to 16-bit little-endian
            buf.extend(sample.to_bytes(2, 'little', signed=True))
            buf.extend(sample.to_bytes(2, 'little', signed=True))  # Stereo

        sound = pygame.mixer.Sound(buffer=bytes(buf))
        sound.set_volume(0.5)
        return sound
    except Exception as e:
        print(f"Error creating beep sound: {e}")
        # Fallback to empty sound
        return pygame.mixer.Sound(buffer=bytearray([]))


# NEW: Draw snower image under score panel during assembly state
def draw_snower_image_under_score(surface):
    if SHOW_SNOWER_IMAGE:
        # Draw background panel for the image
        image_panel = pygame.Rect(SCREEN_WIDTH - 330, 85, 360, 260)
        pygame.draw.rect(surface, (40, 45, 55), image_panel, border_radius=12)
        pygame.draw.rect(surface, (70, 75, 85), image_panel, 3, border_radius=12)

        # Draw the snower image
        surface.blit(SNOWER_IMAGE, (SCREEN_WIDTH - 320, 90))

        # Draw label
        label = pygame.font.SysFont("Arial", 20, bold=True).render("TARGET SNOWER", True, LIGHT_BLUE)
        surface.blit(label, (SCREEN_WIDTH - 320 + 175 - label.get_width() // 2, 345))


# Load sound effects and music
def load_sounds():
    global bg_music, win_sound, shoot_sound, lose_sound, collect_sound

    print("Snowbot Game: Loading sounds...")

    # Initialize all sounds to None first
    bg_music = None
    win_sound = None
    shoot_sound = None
    lose_sound = None
    collect_sound = None

    try:
        # Check what files exist
        sound_files = ["Level 1.mp3", "Win.mp3", "Lazer.mp3", "Lose.mp3"]
        for sound_file in sound_files:
            sound_path = os.path.join(BASE_DIR, sound_file)
            if os.path.exists(sound_path):
                print(f"✓ Found: {sound_file}")
            else:
                print(f"✗ Missing: {sound_file}")

        # Try to load background music with pygame.mixer.music
        try:
            music_path = os.path.join(BASE_DIR, "Level 1.mp3")
            if os.path.exists(music_path):
                pygame.mixer.music.load(music_path)
                print("✓ Background music loaded")
            else:
                print("✗ Background music not found")
        except Exception as e:
            print(f"Error loading background music: {e}")

        # Try to load sound effects
        try:
            # Try to load each sound
            if os.path.exists(os.path.join(BASE_DIR, "Win.mp3")):
                win_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "Win.mp3"))
                print("✓ Win sound loaded")

            if os.path.exists(os.path.join(BASE_DIR, "Lazer.mp3")):
                shoot_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "Lazer.mp3"))
                print("✓ Shoot sound loaded")

            if os.path.exists(os.path.join(BASE_DIR, "Lose.mp3")):
                lose_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "Lose.mp3"))
                print("✓ Lose sound loaded")

            # Try to load collect sound, create beep if not found
            collect_path = os.path.join(BASE_DIR, "collect.mp3")
            if os.path.exists(collect_path):
                collect_sound = pygame.mixer.Sound(collect_path)
                print("✓ Collect sound loaded from file")
            else:
                print("✗ Collect sound not found, creating beep sound")
                collect_sound = create_beep_sound()
                print("✓ Created beep sound for collection")

        except Exception as e:
            print(f"Error loading sound effects: {e}")
            # Create dummy sounds
            win_sound = pygame.mixer.Sound(buffer=bytearray([]))
            shoot_sound = pygame.mixer.Sound(buffer=bytearray([]))
            lose_sound = pygame.mixer.Sound(buffer=bytearray([]))
            collect_sound = create_beep_sound()

        print("Sounds loading complete!")

    except Exception as e:
        print(f"Error in load_sounds: {e}")
        # Create dummy sounds as fallback
        win_sound = pygame.mixer.Sound(buffer=bytearray([]))
        shoot_sound = pygame.mixer.Sound(buffer=bytearray([]))
        lose_sound = pygame.mixer.Sound(buffer=bytearray([]))
        collect_sound = create_beep_sound()


# Load the sounds
load_sounds()


# Play background music
def play_background_music():
    try:
        # Try multiple formats
        formats = ["Level 1.mp3", "Level 1.ogg", "Level 1.wav"]
        for format in formats:
            music_path = os.path.join(BASE_DIR, format)
            if os.path.exists(music_path):
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.play(-1)
                print(f"✓ Playing background music: {format}")
                return

        print("✗ No background music file found")
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
            win_sound.set_volume(0.7)
    except Exception as e:
        print(f"Error playing win sound: {e}")


# Play shoot sound
def play_shoot_sound():
    try:
        if shoot_sound:
            shoot_sound.play()
            shoot_sound.set_volume(0.6)
    except Exception as e:
        print(f"Error playing shoot sound: {e}")


# Play lose sound
def play_lose_sound():
    try:
        if lose_sound:
            lose_sound.play()
            lose_sound.set_volume(0.7)
    except Exception as e:
        print(f"Error playing lose sound: {e}")


# Play collect sound - FIXED VERSION
def play_collect_sound():
    try:
        if collect_sound:
            # Stop any existing instance to prevent overlap
            collect_sound.stop()
            collect_sound.play()
            collect_sound.set_volume(0.7)
            return True
    except Exception as e:
        print(f"Error playing collect sound: {e}")
    return False


# FIXED: Corrected go_to_main_menu function
def go_to_main_menu():
    print("\nReturning to Main Menu...")
    stop_background_music()

    # Find the main menu script path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_menu_path = os.path.join(script_dir, "main_menu.py")

    # Check if main menu script exists
    if not os.path.exists(main_menu_path):
        print(f"Error: Could not find main menu script at {main_menu_path}")
        # Try alternative paths
        possible_paths = [
            os.path.join(BASE_DIR, "main_menu.py"),
            os.path.join(os.getcwd(), "main_menu.py"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "main_menu.py")
        ]

        for path in possible_paths:
            if os.path.exists(path):
                main_menu_path = path
                print(f"Found main menu at: {path}")
                break
        else:
            print("ERROR: Could not find main_menu.py anywhere!")
            pygame.quit()
            sys.exit(0)
            return

    print(f"Launching main menu: {main_menu_path}")

    try:
        # Stop pygame before launching new process
        pygame.quit()

        # Launch main menu
        if sys.platform == "win32":
            subprocess.Popen([sys.executable, main_menu_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen([sys.executable, main_menu_path])

        print("Main menu launched successfully!")

    except Exception as e:
        print(f"Error launching main menu: {e}")
        # If there's an error, exit cleanly
        pygame.quit()
        sys.exit(1)

    # Exit the current game
    sys.exit(0)


# Launch to level 2: Improved transition_to_drone_level function
def transition_to_drone_level():
    print("\n" + "=" * 50)
    print("VICTORY! Launching Drone Level 2...")
    print("=" * 50)
    stop_background_music()

    possible_filenames = ["drone_game.py", "level 2.py"]
    drone_path = None

    for filename in possible_filenames:
        test_path = os.path.join(BASE_DIR, filename)
        if os.path.exists(test_path):
            drone_path = test_path
            print(f"✓ Found drone game: {drone_path}")
            break

    if not drone_path:
        print("ERROR: Could not find drone game!")
        return

    try:
        print(f"\nLaunching Drone game...")
        subprocess.Popen([sys.executable, drone_path])
        print("✓ Drone level launched successfully!")
    except Exception as e:
        print(f"✗ Failed to launch drone game: {e}")
        return

    pygame.quit()
    sys.exit(0)


# Leaf class for collectible leaves
class Leaf:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collected = False
        self.color = random.choice([LEAF_GREEN, LEAF_YELLOW, LEAF_ORANGE, LEAF_BROWN])
        self.size = random.uniform(0.8, 1.5)
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-0.5, 0.5)
        self.float_offset = random.uniform(0, math.pi * 2)
        self.float_speed = random.uniform(0.02, 0.05)
        self.wiggle = 0
        self.wiggle_speed = random.uniform(0.05, 0.1)
        self.wiggle_amount = random.uniform(0.5, 2.0)

    def update(self):
        # Gentle floating animation
        self.rotation += self.rotation_speed
        self.float_offset += self.float_speed
        self.wiggle += self.wiggle_speed
        if self.rotation > 360:
            self.rotation -= 360
        elif self.rotation < 0:
            self.rotation += 360

    def draw(self, surface):
        if self.collected:
            return

        # Calculate floating offset
        float_y = math.sin(self.float_offset) * 2

        # Calculate wiggle offset
        wiggle_offset = math.sin(self.wiggle) * self.wiggle_amount

        # Draw leaf shadow first
        shadow_surface = pygame.Surface((int(self.size * 30), int(self.size * 15)), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, (0, 0, 0, 80),
                            (0, 0, int(self.size * 30), int(self.size * 15)))
        surface.blit(shadow_surface, (self.x - self.size * 15, self.y - self.size * 7.5 + 5))

        # Create leaf surface
        leaf_surface = pygame.Surface((int(self.size * 30), int(self.size * 30)), pygame.SRCALPHA)

        # Rotate leaf surface
        rotated_leaf = pygame.transform.rotate(leaf_surface, self.rotation + wiggle_offset)

        # Draw leaf shape (simplified leaf shape)
        points = []
        num_points = 10
        for i in range(num_points):
            angle = (i / num_points) * math.pi * 2
            if i < num_points / 2:
                radius = self.size * 15 * (0.5 + 0.5 * math.sin(angle * 2))
            else:
                radius = self.size * 15 * (0.3 + 0.7 * math.sin(angle * 2))

            x = self.size * 15 + math.cos(angle) * radius
            y = self.size * 15 + math.sin(angle) * radius
            points.append((x, y))

        if len(points) > 2:
            pygame.draw.polygon(leaf_surface, self.color, points)
            # Add leaf vein
            pygame.draw.line(leaf_surface, (self.color[0] - 30, self.color[1] - 30, self.color[2] - 30),
                             (self.size * 15, self.size * 15),
                             (self.size * 15 + math.cos(math.radians(self.rotation)) * self.size * 10,
                              self.size * 15 + math.sin(math.radians(self.rotation)) * self.size * 10), 2)

        # Apply rotation
        rotated_leaf = pygame.transform.rotate(leaf_surface, self.rotation + wiggle_offset)
        leaf_rect = rotated_leaf.get_rect(center=(self.x, self.y + float_y))
        surface.blit(rotated_leaf, leaf_rect)

        # Add sparkle effect occasionally
        if random.random() < 0.01:
            sparkle_x = self.x + random.uniform(-10, 10)
            sparkle_y = self.y + random.uniform(-10, 10)
            pygame.draw.circle(surface, (255, 255, 200), (int(sparkle_x), int(sparkle_y)), 2)

    def get_collision_rect(self):
        return pygame.Rect(self.x - self.size * 10, self.y - self.size * 10,
                           self.size * 20, self.size * 20)


# Stone system - MODIFIED: Now comes in groups of 4 horizontally
class Stone:
    def __init__(self, progress, x_offset):
        self.progress = progress  # 0 to 1 (0 = far away, 1 = near player)
        self.x_offset = x_offset  # Horizontal offset from center (-1 to 1)
        self.speed = 0.003  # Increased speed for more challenge
        self.color = random.choice(STONE_COLORS)
        self.size = random.uniform(0.8, 1.5)  # Slightly bigger stones
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-1, 1)
        self.wobble = random.uniform(0, math.pi * 2)
        self.wobble_speed = random.uniform(0.02, 0.05)
        self.wobble_amount = random.uniform(0.5, 2.0)

    def update(self):
        self.progress += self.speed
        self.rotation += self.rotation_speed
        self.wobble += self.wobble_speed
        if self.rotation > 360:
            self.rotation -= 360
        elif self.rotation < 0:
            self.rotation += 360

    def get_position(self, street_top_width, street_bottom_width, street_height):
        # Calculate current street width at this progress
        current_width = street_top_width + (street_bottom_width - street_top_width) * (1 - self.progress)

        # Calculate x position with perspective and wobble
        base_x = SCREEN_WIDTH // 2 + self.x_offset * (current_width * 0.6)  # Wider spread
        wobble_offset = math.sin(self.wobble) * self.wobble_amount

        # Calculate y position with perspective
        y = 50 + self.progress * street_height

        # Scale size based on perspective (smaller when farther away)
        scale = 0.6 + (1 - self.progress) * 0.4

        return base_x + wobble_offset, y, scale * self.size

    def get_collision_rect(self, street_top_width, street_bottom_width, street_height):
        x, y, size = self.get_position(street_top_width, street_bottom_width, street_height)
        radius = size * 22  # Adjusted collision radius
        return pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)


# ENHANCED: Snowbot part types with mechanical parts - ALL AS RECTANGLES
# MODIFIED: One part per slot (36 total parts)
PARTS = {
    # Original electronic parts
    "CPU": {"color": BLUE, "size": (100, 80), "radius": 10},
    "Battery": {"color": (200, 180, 0), "size": (100, 80), "radius": 10},  # Dark yellow
    "Motor": {"color": BLACK, "size": (100, 80), "radius": 10},
    "Camera": {"color": PURPLE, "size": (100, 80), "radius": 10},
    "Sensor": {"color": DARK_CYAN, "size": (100, 80), "radius": 10},
    "Antenna": {"color": DARK_GREEN, "size": (100, 80), "radius": 10},  # Changed to DARK_GREEN

    # New snower parts
    "Hub": {"color": METAL_GRAY, "size": (100, 80), "radius": 10},
    "Track": {"color": TRACK_GRAY, "size": (100, 80), "radius": 10},
    "Cog": {"color": SILVER, "size": (100, 80), "radius": 10},
    "Cabine Plate": {"color": DARK_GRAY, "size": (100, 80), "radius": 10},
    "Drive Pod Plate": {"color": (80, 90, 100), "size": (100, 80), "radius": 10},
    "Drive Pod Frame": {"color": (70, 80, 90), "size": (100, 80), "radius": 10},
    "Center Frame": {"color": (90, 100, 110), "size": (100, 80), "radius": 10},
    "Toothless Cog": {"color": (150, 150, 150), "size": (100, 80), "radius": 10},
    "Plow Link": {"color": (100, 80, 60), "size": (100, 80), "radius": 10},
    "Plow": {"color": (120, 100, 80), "size": (100, 80), "radius": 10},
    "Cabine Plow": {"color": (110, 90, 70), "size": (100, 80), "radius": 10},
    "Plow Lever": {"color": (90, 70, 50), "size": (100, 80), "radius": 10},
    "Servomotor": {"color": (100, 60, 60), "size": (100, 80), "radius": 10},
    "Servo Holder": {"color": (140, 120, 100), "size": (100, 80), "radius": 10}
}

# Calculate positions based on screen size
center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
adjusted_center_x = center_x

# ENHANCED: Snowbot slots with mechanical slots - ENLARGED SNOWER TO INCLUDE ALL SLOTS
SNOWER_WIDTH = 900  # Increased from 800
SNOWER_HEIGHT = 700  # Increased from 600
SNOWER_X = center_x
SNOWER_Y = center_y

SLOTS = [
    # Top row - Electronic components
    {"rect": pygame.Rect(SNOWER_X - 400, SNOWER_Y - 300, 100, 80), "type": "CPU",
     "connected_to": [1, 2, 3, 4, 5, 6, 7, 8]},
    {"rect": pygame.Rect(SNOWER_X - 280, SNOWER_Y - 300, 100, 80), "type": "Battery", "connected_to": [0, 2, 9]},
    {"rect": pygame.Rect(SNOWER_X - 160, SNOWER_Y - 300, 100, 80), "type": "Motor", "connected_to": [0, 1, 10, 11]},
    {"rect": pygame.Rect(SNOWER_X - 40, SNOWER_Y - 300, 100, 80), "type": "Camera", "connected_to": [0, 12]},
    {"rect": pygame.Rect(SNOWER_X + 80, SNOWER_Y - 300, 100, 80), "type": "Sensor", "connected_to": [0, 13]},
    {"rect": pygame.Rect(SNOWER_X + 200, SNOWER_Y - 300, 100, 80), "type": "Antenna", "connected_to": [0, 14]},

    # Second row - Mechanical parts
    {"rect": pygame.Rect(SNOWER_X - 400, SNOWER_Y - 200, 100, 80), "type": "Hub", "connected_to": [0, 7, 15]},
    {"rect": pygame.Rect(SNOWER_X - 280, SNOWER_Y - 200, 100, 80), "type": "Hub", "connected_to": [0, 6, 16]},
    {"rect": pygame.Rect(SNOWER_X - 160, SNOWER_Y - 200, 100, 80), "type": "Track", "connected_to": [2, 17]},
    {"rect": pygame.Rect(SNOWER_X - 40, SNOWER_Y - 200, 100, 80), "type": "Track", "connected_to": [2, 18]},

    # Third row
    {"rect": pygame.Rect(SNOWER_X - 400, SNOWER_Y - 100, 100, 80), "type": "Cog", "connected_to": [2, 19]},
    {"rect": pygame.Rect(SNOWER_X - 280, SNOWER_Y - 100, 100, 80), "type": "Cog", "connected_to": [2, 20]},
    {"rect": pygame.Rect(SNOWER_X - 160, SNOWER_Y - 100, 100, 80), "type": "Cabine Plate", "connected_to": [3, 21]},
    {"rect": pygame.Rect(SNOWER_X - 40, SNOWER_Y - 100, 100, 80), "type": "Cabine Plate", "connected_to": [3, 22]},

    # Fourth row
    {"rect": pygame.Rect(SNOWER_X - 400, SNOWER_Y, 100, 80), "type": "Drive Pod Plate", "connected_to": [4, 23]},
    {"rect": pygame.Rect(SNOWER_X - 280, SNOWER_Y, 100, 80), "type": "Drive Pod Plate", "connected_to": [4, 24]},
    {"rect": pygame.Rect(SNOWER_X - 160, SNOWER_Y, 100, 80), "type": "Drive Pod Frame", "connected_to": [8, 14, 25]},
    {"rect": pygame.Rect(SNOWER_X - 40, SNOWER_Y, 100, 80), "type": "Drive Pod Frame", "connected_to": [9, 5, 26]},

    # Fifth row
    {"rect": pygame.Rect(SNOWER_X - 400, SNOWER_Y + 100, 100, 80), "type": "Center Frame",
     "connected_to": [15, 16, 27]},
    {"rect": pygame.Rect(SNOWER_X - 280, SNOWER_Y + 100, 100, 80), "type": "Toothless Cog", "connected_to": [10, 28]},
    {"rect": pygame.Rect(SNOWER_X - 160, SNOWER_Y + 100, 100, 80), "type": "Toothless Cog", "connected_to": [11, 29]},
    {"rect": pygame.Rect(SNOWER_X - 40, SNOWER_Y + 100, 100, 80), "type": "Plow Link", "connected_to": [12, 30]},

    # Sixth row
    {"rect": pygame.Rect(SNOWER_X - 400, SNOWER_Y + 200, 100, 80), "type": "Plow Link", "connected_to": [13, 31]},
    {"rect": pygame.Rect(SNOWER_X - 280, SNOWER_Y + 200, 100, 80), "type": "Plow", "connected_to": [30, 32]},
    {"rect": pygame.Rect(SNOWER_X - 160, SNOWER_Y + 200, 100, 80), "type": "Plow", "connected_to": [31, 33]},
    {"rect": pygame.Rect(SNOWER_X - 40, SNOWER_Y + 200, 100, 80), "type": "Cabine Plow", "connected_to": [21, 22, 34]},

    # Seventh row
    {"rect": pygame.Rect(SNOWER_X - 280, SNOWER_Y + 300, 100, 80), "type": "Plow Lever", "connected_to": [32, 33, 34]},
    {"rect": pygame.Rect(SNOWER_X - 160, SNOWER_Y + 300, 100, 80), "type": "Servomotor", "connected_to": [25, 26, 35]},
    {"rect": pygame.Rect(SNOWER_X - 40, SNOWER_Y + 300, 100, 80), "type": "Servo Holder", "connected_to": [27]}
]

# Create parts for dragging - ONE PART PER SLOT (36 total)
parts = []
part_id = 0

# MODIFIED: Create a more organized grid for parts panel with 36 parts
parts_panel_width = 400
parts_start_x = 30
# FIXED: Changed from 100 to 180 to move parts down below buttons
parts_start_y = 180
parts_spacing_x = 110
parts_spacing_y = 90

# Count how many of each part type we need based on slots
parts_needed = {}
for slot in SLOTS:
    part_type = slot["type"]
    parts_needed[part_type] = parts_needed.get(part_type, 0) + 1

# Create parts based on what's needed for slots
for part_type, part_info in PARTS.items():
    count_needed = parts_needed.get(part_type, 0)
    for i in range(count_needed):
        column = part_id % 4  # 4 columns
        row = part_id // 4  # multiple rows

        x_pos = parts_start_x + column * parts_spacing_x
        y_pos = parts_start_y + row * parts_spacing_y

        # MODIFIED: Store both full name and abbreviated name
        parts.append({
            "id": part_id,
            "type": part_type,  # Full name for matching
            "abbrev": part_type[:2].upper() if len(part_type) > 2 else part_type.upper(),  # First two letters
            "rect": pygame.Rect(x_pos, y_pos, 100, 80),
            "color": part_info["color"],
            "radius": 10,
            "dragging": False,
            "placed": False,
            "placed_slot": None,
            "original_pos": (x_pos, y_pos)
        })
        part_id += 1

# Verify we have exactly 36 parts
print(f"Created {len(parts)} parts for {len(SLOTS)} slots")

# Create fonts
font = pygame.font.SysFont("Arial", 18)
title_font = pygame.font.SysFont("Arial", 36, bold=True)
small_font = pygame.font.SysFont("Arial", 16)

# Game states
LEVEL_INTRO_STATE = 0
ASSEMBLY_STATE = 1
SUCCESS_STATE = 2
REPAIR_STATE = 3
MOVEMENT_STATE = 4
VICTORY_STATE = 5
GAME_OVER_STATE = 6

# Game features
PARTICLE_SYSTEMS = []
WIRE_ANIMATION = 0
SCORE = 0
COMBO = 0
LAST_PLACEMENT_TIME = 0
BATTERY_LEVEL = 0.5
BATTERY_DIRECTION = 1

# Leaves variables
leaves = []
leaves_collected = 0
total_leaves_needed = 70

# Stones variables
stones = []
stones_avoided = 0
total_stones = 0
stone_spawn_timer = 0
stone_spawn_delay = 1200

# Joystick and button variables
JOYSTICK_BUTTON_ACTIVE = False
JOYSTICK_BUTTON_POS = (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100)
JOYSTICK_BUTTON_RADIUS = 40
JOYSTICK_BUTTON_COLOR = GREEN

# Joystick variables
joystick_base_pos = (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200)
joystick_base_radius = 80
joystick_handle_pos = list(joystick_base_pos)
joystick_handle_radius = 30
joystick_dragging = False
joystick_direction = [0, 0]

# Keyboard control variables
KEYBOARD_CONTROL = False
KEY_LEFT = False
KEY_RIGHT = False
KEY_UP = False
KEY_DOWN = False

# Victory button variables
NEXT_LEVEL_BUTTON = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 60)
NEXT_LEVEL_BUTTON_COLOR = NEON_GREEN
NEXT_LEVEL_BUTTON_HOVER_COLOR = (100, 255, 150)
WIN_SOUND_PLAYED = False

# Pause state
PAUSED = False
PAUSE_BUTTON = pygame.Rect(20, 80, 150, 40)
ESCAPE_BUTTON = pygame.Rect(20, 30, 150, 40)

# Pause menu buttons
RESUME_BUTTON = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 60)
MAIN_MENU_BUTTON = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 60)

# Repair state variables
REPAIR_TIMER = 0
REPAIR_DURATION = 10000
TOOL_ANIMATION = 0
MECHANIC_POSITION = [SNOWER_X - 300, SNOWER_Y + 100]
SPANNER_ANGLE = 0
SPANNER_MOVING = True
CURRENT_TEST_PHASE = 0
TEST_PHASE_TIMER = 0

# Movement state timer
MOVEMENT_STATE_TIMER = 0

# Minimap variables
MINIMAP_RECT = pygame.Rect(SCREEN_WIDTH - 280, 90, 250, 150)
MINIMAP_VIEW_DISTANCE = 0.4


# Simple sound effects
def play_success_sound():
    print("Playing success sound!")


def play_failure_sound():
    print("Playing failure sound!")


def play_movement_sound():
    print("Playing movement sound!")


def play_repair_sound():
    print("Playing repair sound!")


def play_spanner_sound():
    print("Playing spanner sound!")


def play_stone_hit_sound():
    print("Playing stone hit sound!")


def play_stone_avoid_sound():
    print("Playing stone avoid sound!")


def play_leaf_collect_sound():
    if play_collect_sound():
        # Create special celebration effect for leaf collection
        if leaves_collected >= total_leaves_needed - 10:
            for _ in range(20):
                create_particles(snower_x, snower_y, NEON_GREEN, 5)
                create_particles(snower_x, snower_y, LEAF_GREEN, 5)
                create_particles(snower_x, snower_y, GOLD, 3)
        return True
    return False


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


# Update battery animation
def update_battery():
    global BATTERY_LEVEL, BATTERY_DIRECTION
    BATTERY_LEVEL += 0.005 * BATTERY_DIRECTION
    if BATTERY_LEVEL >= 1.0:
        BATTERY_LEVEL = 1.0
        BATTERY_DIRECTION = -1
    elif BATTERY_LEVEL <= 0.1:
        BATTERY_LEVEL = 0.1
        BATTERY_DIRECTION = 1


# Draw joystick button
def draw_joystick_button(surface):
    pygame.draw.circle(surface, JOYSTICK_BUTTON_COLOR, JOYSTICK_BUTTON_POS, JOYSTICK_BUTTON_RADIUS)
    pygame.draw.circle(surface, WHITE, JOYSTICK_BUTTON_POS, JOYSTICK_BUTTON_RADIUS, 3)
    pygame.draw.circle(surface, WHITE, JOYSTICK_BUTTON_POS, JOYSTICK_BUTTON_RADIUS // 2)
    pygame.draw.circle(surface, BLACK, JOYSTICK_BUTTON_POS, JOYSTICK_BUTTON_RADIUS // 2, 2)

    cross_size = JOYSTICK_BUTTON_RADIUS // 3
    pygame.draw.line(surface, BLACK,
                     (JOYSTICK_BUTTON_POS[0] - cross_size, JOYSTICK_BUTTON_POS[1]),
                     (JOYSTICK_BUTTON_POS[0] + cross_size, JOYSTICK_BUTTON_POS[1]), 2)
    pygame.draw.line(surface, BLACK,
                     (JOYSTICK_BUTTON_POS[0], JOYSTICK_BUTTON_POS[1] - cross_size),
                     (JOYSTICK_BUTTON_POS[0], JOYSTICK_BUTTON_POS[1] + cross_size), 2)

    if not JOYSTICK_BUTTON_ACTIVE:
        text = small_font.render("Press ENTER", True, WHITE)
        surface.blit(text, (JOYSTICK_BUTTON_POS[0] - text.get_width() // 2,
                            JOYSTICK_BUTTON_POS[1] + JOYSTICK_BUTTON_RADIUS + 10))


# Draw joystick
def draw_joystick(surface):
    pygame.draw.circle(surface, (50, 50, 60), joystick_base_pos, joystick_base_radius)
    pygame.draw.circle(surface, (70, 70, 80), joystick_base_pos, joystick_base_radius, 4)

    for angle in [0, 90, 180, 270]:
        rad = math.radians(angle)
        x = joystick_base_pos[0] + (joystick_base_radius - 10) * math.cos(rad)
        y = joystick_base_pos[1] + (joystick_base_radius - 10) * math.sin(rad)
        pygame.draw.circle(surface, (100, 100, 120), (int(x), int(y)), 5)

    pygame.draw.circle(surface, (180, 60, 60), (int(joystick_handle_pos[0]), int(joystick_handle_pos[1])),
                       joystick_handle_radius)

    button_colors = [(255, 100, 100), (255, 150, 50)]
    for i, color in enumerate(button_colors):
        angle = i * math.pi
        distance = joystick_handle_radius * 0.6
        x = joystick_handle_pos[0] + distance * math.cos(angle)
        y = joystick_handle_pos[1] + distance * math.sin(angle)
        pygame.draw.circle(surface, color, (int(x), int(y)), 8)

    pygame.draw.circle(surface, (50, 150, 255), (int(joystick_handle_pos[0]), int(joystick_handle_pos[1])), 15)
    pygame.draw.circle(surface, (200, 230, 255), (int(joystick_handle_pos[0]), int(joystick_handle_pos[1])), 10)

    text = small_font.render("Use WASD keys or drag to control", True, WHITE)
    surface.blit(text, (joystick_base_pos[0] - text.get_width() // 2,
                        joystick_base_pos[1] + joystick_base_radius + 10))


# Update joystick position for 2D movement
def update_joystick(mouse_pos):
    global joystick_handle_pos, joystick_direction

    if not joystick_dragging:
        return

    dx = mouse_pos[0] - joystick_base_pos[0]
    dy = mouse_pos[1] - joystick_base_pos[1]

    distance = math.sqrt(dx * dx + dy * dy)
    if distance > joystick_base_radius - joystick_handle_radius:
        scale = (joystick_base_radius - joystick_handle_radius) / distance
        dx *= scale
        dy *= scale

    joystick_handle_pos[0] = joystick_base_pos[0] + dx
    joystick_handle_pos[1] = joystick_base_pos[1] + dy

    joystick_direction[0] = dx / (joystick_base_radius - joystick_handle_radius)
    joystick_direction[1] = dy / (joystick_base_radius - joystick_handle_radius)


# Reset joystick
def reset_joystick():
    global joystick_handle_pos, joystick_direction
    joystick_handle_pos = list(joystick_base_pos)
    joystick_direction = [0, 0]


# Update joystick based on keyboard input (WASD for 2D movement)
def update_joystick_keyboard():
    global joystick_handle_pos, joystick_direction

    joystick_direction = [0, 0]

    if KEY_LEFT:
        joystick_direction[0] = -1
    elif KEY_RIGHT:
        joystick_direction[0] = 1

    if KEY_UP:
        joystick_direction[1] = -1
    elif KEY_DOWN:
        joystick_direction[1] = 1

    if joystick_direction[0] != 0 and joystick_direction[1] != 0:
        length = math.sqrt(joystick_direction[0] ** 2 + joystick_direction[1] ** 2)
        joystick_direction[0] /= length
        joystick_direction[1] /= length

    max_offset = joystick_base_radius - joystick_handle_radius
    joystick_handle_pos[0] = joystick_base_pos[0] + joystick_direction[0] * max_offset
    joystick_handle_pos[1] = joystick_base_pos[1] + joystick_direction[1] * max_offset


# Draw street scene with perspective (street runs from bottom to top)
def draw_street_scene(surface):
    # Sky gradient (darker at top, lighter at bottom)
    for y in range(SCREEN_HEIGHT):
        color_value = 30 + int(70 * (y / SCREEN_HEIGHT))
        pygame.draw.line(surface, (color_value, color_value + 10, color_value + 20),
                         (0, y), (SCREEN_WIDTH, y), 1)

    # Sun/moon at the top (end of street)
    sun_x = SCREEN_WIDTH // 2
    sun_y = 80
    pygame.draw.circle(surface, (255, 255, 200), (sun_x, sun_y), 40)
    pygame.draw.circle(surface, (255, 255, 150), (sun_x, sun_y), 35)

    # Distant clouds at the top
    for i in range(2):
        cloud_x = (i * 400 + pygame.time.get_ticks() // 150) % (SCREEN_WIDTH + 400) - 200
        cloud_y = 40 + i * 30
        cloud_size = 40 + i * 20
        pygame.draw.circle(surface, (220, 230, 240), (cloud_x, cloud_y), cloud_size)
        pygame.draw.circle(surface, (230, 240, 250), (cloud_x - 30, cloud_y - 5), cloud_size - 15)
        pygame.draw.circle(surface, (230, 240, 250), (cloud_x + 30, cloud_y - 5), cloud_size - 15)

    # Street perspective - wider at bottom (near player), narrower at top
    street_top_width = SCREEN_WIDTH // 3
    street_bottom_width = SCREEN_WIDTH * 0.9
    street_height = SCREEN_HEIGHT * 0.8

    # Calculate street polygon points
    top_left = (SCREEN_WIDTH // 2 - street_top_width // 2, 50)
    top_right = (SCREEN_WIDTH // 2 + street_top_width // 2, 50)
    bottom_left = (SCREEN_WIDTH // 2 - street_bottom_width // 2, SCREEN_HEIGHT)
    bottom_right = (SCREEN_WIDTH // 2 + street_bottom_width // 2, SCREEN_HEIGHT)

    # Draw street (road surface)
    street_points = [top_left, top_right, bottom_right, bottom_left]
    pygame.draw.polygon(surface, STREET_GRAY, street_points)

    # Road markings - perspective lines that converge at the top
    marking_length = 40
    marking_gap = 60
    num_markings = int(street_height // (marking_length + marking_gap))

    for i in range(num_markings):
        progress = i / (num_markings - 1) if num_markings > 1 else 0
        y_pos = 50 + progress * street_height

        current_width = street_top_width + (street_bottom_width - street_top_width) * (1 - progress)
        marking_width = 20 * (1 - progress * 0.5)
        marking_x = SCREEN_WIDTH // 2 - marking_width // 2
        marking_y = y_pos - marking_length // 2

        pygame.draw.rect(surface, ROAD_MARKING,
                         (marking_x, marking_y, marking_width, marking_length))

    # Road edge lines (perspective)
    pygame.draw.line(surface, (255, 255, 100), top_left, bottom_left, 4)
    pygame.draw.line(surface, (255, 255, 100), top_right, bottom_right, 4)

    # Grassy areas on sides with perspective
    for side in [-1, 1]:
        if side == -1:
            points = [
                (0, 0),
                (0, SCREEN_HEIGHT),
                (SCREEN_WIDTH // 2 - street_bottom_width // 2, SCREEN_HEIGHT),
                (SCREEN_WIDTH // 2 - street_top_width // 2, 50)
            ]
        else:
            points = [
                (SCREEN_WIDTH, 0),
                (SCREEN_WIDTH, SCREEN_HEIGHT),
                (SCREEN_WIDTH // 2 + street_bottom_width // 2, SCREEN_HEIGHT),
                (SCREEN_WIDTH // 2 + street_top_width // 2, 50)
            ]

        pygame.draw.polygon(surface, GRASS_GREEN, points)

        for j in range(20):
            if side == -1:
                left_boundary = int(SCREEN_WIDTH // 2 - street_bottom_width // 2)
                x_min = 10
                x_max = left_boundary - 10
                if x_min <= x_max:
                    x = random.randint(x_min, x_max)
                else:
                    x = x_min
            else:
                right_boundary = int(SCREEN_WIDTH // 2 + street_bottom_width // 2)
                x_min = right_boundary + 10
                x_max = SCREEN_WIDTH - 10
                if x_min <= x_max:
                    x = random.randint(x_min, x_max)
                else:
                    x = x_min

            y = random.randint(150, SCREEN_HEIGHT - 50)

            blade_length = random.randint(3, 8)
            blade_angle = random.uniform(-30, 30)
            end_x = x + math.cos(math.radians(blade_angle)) * blade_length
            end_y = y + math.sin(math.radians(blade_angle)) * blade_length

            blade_color = (
                min(255, GRASS_GREEN[0] + random.randint(-20, 20)),
                min(255, GRASS_GREEN[1] + random.randint(-20, 20)),
                min(255, GRASS_GREEN[2] + random.randint(-20, 20))
            )
            pygame.draw.line(surface, blade_color, (x, y), (end_x, end_y), 1)

    # Draw trees on both sides with perspective
    tree_spacing = 80
    num_trees_per_side = 6

    for i in range(num_trees_per_side):
        progress = i / (num_trees_per_side - 1) if num_trees_per_side > 1 else 0
        tree_y = SCREEN_HEIGHT - 50 - progress * (street_height - 100)

        tree_x_progress = 1 - progress
        street_width_at_pos = street_top_width + (street_bottom_width - street_top_width) * (1 - progress)
        tree_x = SCREEN_WIDTH // 2 - street_width_at_pos // 2 - 50 * tree_x_progress

        draw_tree_perspective(surface, tree_x, tree_y, tree_x_progress)

    for i in range(num_trees_per_side):
        progress = i / (num_trees_per_side - 1) if num_trees_per_side > 1 else 0
        tree_y = SCREEN_HEIGHT - 50 - progress * (street_height - 100)

        tree_x_progress = 1 - progress
        street_width_at_pos = street_top_width + (street_bottom_width - street_top_width) * (1 - progress)
        tree_x = SCREEN_WIDTH // 2 + street_width_at_pos // 2 + 50 * tree_x_progress

        draw_tree_perspective(surface, tree_x, tree_y, tree_x_progress)

    # Distant buildings at the top
    draw_buildings_perspective(surface)

    # Street lamps with perspective
    for i in range(4):
        progress = i / 3
        lamp_y = SCREEN_HEIGHT - 80 - progress * (street_height - 150)

        street_width_at_pos = street_top_width + (street_bottom_width - street_top_width) * (1 - progress)
        lamp_x_left = SCREEN_WIDTH // 2 - street_width_at_pos // 2 - 30
        draw_street_lamp(surface, lamp_x_left, lamp_y, progress)

        lamp_x_right = SCREEN_WIDTH // 2 + street_width_at_pos // 2 + 30
        draw_street_lamp(surface, lamp_x_right, lamp_y, progress)

    return street_top_width, street_bottom_width, street_height


def draw_tree_perspective(surface, x, y, scale):
    trunk_width = int(15 * scale)
    trunk_height = int(60 * scale)
    pygame.draw.rect(surface, TREE_BROWN, (x - trunk_width // 2, y - trunk_height, trunk_width, trunk_height))

    leaf_layers = max(2, int(3 * scale))
    for layer in range(leaf_layers):
        leaf_size = int(50 * scale * (1 - layer * 0.2))
        leaf_y = y - trunk_height - layer * 15 * scale
        pygame.draw.circle(surface, TREE_GREEN, (x, leaf_y), leaf_size)

        for j in range(2):
            angle = j * 180 + pygame.time.get_ticks() // 2000
            leaf_offset_x = x + math.cos(math.radians(angle)) * (leaf_size * 0.5)
            leaf_offset_y = leaf_y + math.sin(math.radians(angle)) * (leaf_size * 0.3)
            pygame.draw.circle(surface, (TREE_GREEN[0] + 20, TREE_GREEN[1] + 20, TREE_GREEN[2] + 20),
                               (int(leaf_offset_x), int(leaf_offset_y)), leaf_size // 2)

    if random.random() < 0.005 and len(leaves) < total_leaves_needed + 20:
        leaf_x = x + random.uniform(-30, 30) * scale
        leaf_y = y - trunk_height + random.uniform(-20, 20) * scale
        leaves.append(Leaf(leaf_x, leaf_y))


def draw_buildings_perspective(surface):
    building_widths = [150, 180, 200]
    building_heights = [120, 150, 180]

    for i, (width, height) in enumerate(zip(building_widths, building_heights)):
        building_x = SCREEN_WIDTH // 2 - width // 2 + (i - 1) * 100
        building_y = 0

        pygame.draw.rect(surface, BUILDING_BROWN,
                         (building_x, building_y, width, height))

        window_rows = 4
        window_cols = 5
        for row in range(window_rows):
            for col in range(window_cols):
                window_x = building_x + 10 + col * (width - 20) // window_cols
                window_y = building_y + 10 + row * (height - 20) // window_rows
                window_width = 15
                window_height = 20

                if (row + col + pygame.time.get_ticks() // 3000) % 3 == 0:
                    window_color = (255, 255, 200)
                else:
                    window_color = (100, 100, 120)

                pygame.draw.rect(surface, window_color, (window_x, window_y, window_width, window_height))


def draw_street_lamp(surface, x, y, scale):
    post_width = int(8 * scale)
    post_height = int(100 * scale)
    pygame.draw.rect(surface, LAMP_POST, (x - post_width // 2, y - post_height, post_width, post_height))

    arm_length = int(40 * scale)
    pygame.draw.rect(surface, (80, 80, 80), (x - post_width // 2, y - post_height, arm_length, 5))

    bulb_size = int(20 * scale)
    pygame.draw.circle(surface, LAMP_LIGHT, (x + arm_length - bulb_size // 2, y - post_height - bulb_size // 2),
                       bulb_size)

    if pygame.time.get_ticks() // 1000 % 2 == 0:
        glow_radius = int(30 * scale)
        glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (*LAMP_GLOW, 100), (glow_radius, glow_radius), glow_radius)
        surface.blit(glow_surface, (x + arm_length - glow_radius - bulb_size // 2,
                                    y - post_height - glow_radius - bulb_size // 2))


# Draw stones on the street and grass
def draw_stones(surface, stones_list, street_top_width, street_bottom_width, street_height):
    for stone in stones_list[:]:
        x, y, size = stone.get_position(street_top_width, street_bottom_width, street_height)

        shadow_offset = size * 3
        shadow_surface = pygame.Surface((int(size * 40), int(size * 20)), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, (0, 0, 0, 100), (0, 0, int(size * 40), int(size * 20)))
        surface.blit(shadow_surface, (x - size * 20, y - size * 10 + shadow_offset))

        stone_radius = int(size * 22)
        pygame.draw.circle(surface, stone.color, (int(x), int(y)), stone_radius)

        for i in range(int(size * 6)):
            detail_x = x + random.uniform(-stone_radius * 0.7, stone_radius * 0.7)
            detail_y = y + random.uniform(-stone_radius * 0.7, stone_radius * 0.7)
            detail_radius = random.uniform(3, 7) * size
            detail_color = (
                max(0, stone.color[0] - random.randint(20, 40)),
                max(0, stone.color[1] - random.randint(20, 40)),
                max(0, stone.color[2] - random.randint(20, 40))
            )
            pygame.draw.circle(surface, detail_color, (int(detail_x), int(detail_y)), int(detail_radius))

        highlight_radius = int(stone_radius * 0.3)
        highlight_x = x - stone_radius * 0.3
        highlight_y = y - stone_radius * 0.3
        pygame.draw.circle(surface, (stone.color[0] + 40, stone.color[1] + 40, stone.color[2] + 40),
                           (int(highlight_x), int(highlight_y)), highlight_radius)


# Draw leaves on the ground
def draw_leaves(surface, leaves_list):
    for leaf in leaves_list:
        leaf.draw(surface)


# Update leaves animation
def update_leaves(leaves_list):
    for leaf in leaves_list:
        leaf.update()


# Check collision between snower and leaves
def check_leaf_collection(snower_x, snower_y, leaves_list):
    global leaves_collected, SCORE
    snower_rect = pygame.Rect(snower_x - 60, snower_y - 80, 120, 160)

    collected_leaves = []
    for leaf in leaves_list:
        if not leaf.collected:
            leaf_rect = leaf.get_collision_rect()
            if snower_rect.colliderect(leaf_rect):
                leaf.collected = True
                collected_leaves.append(leaf)
                leaves_collected += 1
                SCORE += 5
                play_leaf_collect_sound()

                create_particles(leaf.x, leaf.y, leaf.color, 15)
                create_particles(leaf.x, leaf.y, NEON_GREEN, 10)

    for leaf in collected_leaves:
        if leaf in leaves_list:
            leaves_list.remove(leaf)

    return len(collected_leaves) > 0


# Update stones
def update_stones(stones_list):
    global stones_avoided, SCORE

    for stone in stones_list[:]:
        stone.update()
        if stone.progress > 1.0:
            stones_list.remove(stone)
            stones_avoided += 1
            if stones_avoided <= 100:
                play_stone_avoid_sound()
                SCORE += 2


# Spawn stones in groups of 4 horizontally with space between them
def spawn_stone_group():
    global stone_spawn_timer

    current_time = pygame.time.get_ticks()
    if current_time - stone_spawn_timer < stone_spawn_delay or len(stones) >= 12:
        return

    stone_spawn_timer = current_time

    x_offsets = [-0.8, -0.4, 0.4, 0.8]

    for x_offset in x_offsets:
        progress_offset = random.uniform(-0.02, 0.02)
        stone = Stone(0.0 + progress_offset, x_offset)
        stones.append(stone)


# Spawn leaves randomly on grass and street
def spawn_leaves_randomly(leaves_list, street_top_width, street_bottom_width, street_height, count=3):
    if len(leaves_list) >= total_leaves_needed + 20:
        return

    for _ in range(count):
        on_grass = random.random() < 0.7

        if on_grass:
            side = random.choice([-1, 1])

            if side == -1:
                street_left_edge = int(SCREEN_WIDTH // 2 - street_bottom_width // 2)
                x_min = 50
                x_max = street_left_edge - 50
                if x_min <= x_max:
                    x = random.randint(x_min, x_max)
                else:
                    x = x_min
            else:
                street_right_edge = int(SCREEN_WIDTH // 2 + street_bottom_width // 2)
                x_min = street_right_edge + 50
                x_max = SCREEN_WIDTH - 50
                if x_min <= x_max:
                    x = random.randint(x_min, x_max)
                else:
                    x = x_min
        else:
            street_left_edge = int(SCREEN_WIDTH // 2 - street_bottom_width // 2)
            street_right_edge = int(SCREEN_WIDTH // 2 + street_bottom_width // 2)
            x_min = street_left_edge + 50
            x_max = street_right_edge - 50
            if x_min <= x_max:
                x = random.randint(x_min, x_max)
            else:
                x = x_min

        y = random.randint(SCREEN_HEIGHT - 150, SCREEN_HEIGHT - 50)

        leaf = Leaf(x, y)
        if leaves_collected >= total_leaves_needed - 15:
            leaf.size *= 1.5
            leaf.color = random.choice([LEAF_GREEN, LEAF_YELLOW, GOLD])
        leaves_list.append(leaf)


# Initialize leaves when entering movement state
def initialize_leaves(street_top_width, street_bottom_width, street_height):
    global leaves
    leaves = []

    for _ in range(30):
        spawn_leaves_randomly(leaves, street_top_width, street_bottom_width, street_height, 1)


# Draw minimap camera view
def draw_minimap_camera(surface, snower_x, snower_y, stones_list, leaves_list, street_top_width, street_bottom_width,
                        street_height):
    pygame.draw.rect(surface, MINIMAP_COLOR, MINIMAP_RECT, border_radius=10)
    pygame.draw.rect(surface, MINIMAP_BORDER, MINIMAP_RECT, 3, border_radius=10)

    minimap_text = font.render("FRONT CAMERA", True, NEON_BLUE)
    surface.blit(minimap_text, (MINIMAP_RECT.centerx - minimap_text.get_width() // 2, MINIMAP_RECT.y + 5))

    camera_surface = pygame.Surface((MINIMAP_RECT.width - 20, MINIMAP_RECT.height - 40), pygame.SRCALPHA)
    camera_rect = camera_surface.get_rect(center=(MINIMAP_RECT.centerx, MINIMAP_RECT.centery + 10))

    for y in range(camera_surface.get_height()):
        color_value = 30 + int(70 * (y / camera_surface.get_height()))
        pygame.draw.line(camera_surface, (color_value, color_value + 10, color_value + 20),
                         (0, y), (camera_surface.get_width(), y), 1)

    street_top_cam = street_top_width * 0.3
    street_bottom_cam = street_bottom_width * 0.3

    cam_top_left = (camera_surface.get_width() // 2 - street_top_cam // 2, 20)
    cam_top_right = (camera_surface.get_width() // 2 + street_top_cam // 2, 20)
    cam_bottom_left = (camera_surface.get_width() // 2 - street_bottom_cam // 2, camera_surface.get_height() - 20)
    cam_bottom_right = (camera_surface.get_width() // 2 + street_bottom_cam // 2, camera_surface.get_height() - 20)

    street_points = [cam_top_left, cam_top_right, cam_bottom_right, cam_bottom_left]
    pygame.draw.polygon(camera_surface, STREET_GRAY, street_points)

    marking_spacing = 30
    num_markings = 3

    for i in range(num_markings):
        progress = i / (num_markings - 1) if num_markings > 1 else 0
        y_pos = 20 + progress * (camera_surface.get_height() - 40)

        current_width = street_top_cam + (street_bottom_cam - street_top_cam) * (1 - progress)
        marking_width = max(5, 15 * (1 - progress * 0.5))
        marking_x = camera_surface.get_width() // 2 - marking_width // 2
        marking_y = y_pos - 10

        pygame.draw.rect(camera_surface, ROAD_MARKING,
                         (marking_x, marking_y, marking_width, 5))

    for leaf in leaves_list:
        if not leaf.collected:
            leaf_size = 3
            leaf_x = int((leaf.x / SCREEN_WIDTH) * camera_surface.get_width())
            leaf_y = int((leaf.y / SCREEN_HEIGHT) * camera_surface.get_height())

            if (camera_rect.left < leaf.x < camera_rect.right and
                    camera_rect.top < leaf.y < camera_rect.bottom):
                pygame.draw.circle(camera_surface, LEAF_GREEN, (leaf_x, leaf_y), leaf_size)

    for stone in stones_list:
        if stone.progress < MINIMAP_VIEW_DISTANCE:
            stone_progress_cam = stone.progress / MINIMAP_VIEW_DISTANCE

            current_width = street_top_cam + (street_bottom_cam - street_top_cam) * (1 - stone_progress_cam)

            x = camera_surface.get_width() // 2 + stone.x_offset * (current_width * 0.3)

            y = 20 + stone_progress_cam * (camera_surface.get_height() - 40)

            stone_size = max(3, stone.size * 8 * (1 - stone_progress_cam))
            pygame.draw.circle(camera_surface, stone.color, (int(x), int(y)), int(stone_size))

            pygame.draw.circle(camera_surface, (stone.color[0] + 40, stone.color[1] + 40, stone.color[2] + 40),
                               (int(x - stone_size * 0.3), int(y - stone_size * 0.3)), int(stone_size * 0.3))

    for i in range(4):
        progress = i / 3
        y_pos = 20 + progress * (camera_surface.get_height() - 40)

        marker_x = camera_surface.get_width() // 2
        marker_length = 8 if i % 2 == 0 else 5

        pygame.draw.line(camera_surface, WHITE,
                         (marker_x - marker_length, y_pos),
                         (marker_x + marker_length, y_pos), 2)

        if i % 2 == 0:
            distance = int((1 - progress) * 50)
            distance_text = small_font.render(f"{distance}m", True, WHITE)
            camera_surface.blit(distance_text, (marker_x + 10, y_pos - 6))

    center_x = camera_surface.get_width() // 2
    center_y = camera_surface.get_height() // 2

    cross_size = 8
    pygame.draw.line(camera_surface, NEON_GREEN,
                     (center_x - cross_size, center_y),
                     (center_x + cross_size, center_y), 2)
    pygame.draw.line(camera_surface, NEON_GREEN,
                     (center_x, center_y - cross_size),
                     (center_x, center_y + cross_size), 2)

    pygame.draw.circle(camera_surface, NEON_GREEN, (center_x, center_y), 15, 2)

    status_color = GREEN if len(stones_list) == 0 else YELLOW
    status_text = "CLEAR" if len(stones_list) == 0 else f"STONES: {len(stones_list)}"

    status_surf = small_font.render(status_text, True, status_color)
    camera_surface.blit(status_surf, (5, 5))

    leaf_text = small_font.render(f"LEAVES: {leaves_collected}/{total_leaves_needed}", True, LEAF_GREEN)
    camera_surface.blit(leaf_text, (5, 25))

    if abs(joystick_direction[0]) > 0.1 or abs(joystick_direction[1]) > 0.1:
        motion_text = small_font.render("MOVING", True, NEON_BLUE)
        camera_surface.blit(motion_text, (camera_surface.get_width() - motion_text.get_width() - 5, 5))

        speed = int((abs(joystick_direction[0]) + abs(joystick_direction[1])) * 50)
        speed_text = small_font.render(f"SPEED: {speed}%", True, CYAN)
        camera_surface.blit(speed_text, (camera_surface.get_width() - speed_text.get_width() - 5, 25))

    surface.blit(camera_surface, camera_rect)

    for y in range(camera_rect.top, camera_rect.bottom, 4):
        if random.random() < 0.1:
            pygame.draw.line(surface, (0, 255, 0, 50),
                             (camera_rect.left, y),
                             (camera_rect.right, y), 1)

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


# Check collision between snower and stones
def check_stone_collision(snower_x, snower_y, stones_list, street_top_width, street_bottom_width, street_height):
    snower_rect = pygame.Rect(snower_x - 60, snower_y - 80, 120, 160)

    for stone in stones_list:
        stone_rect = stone.get_collision_rect(street_top_width, street_bottom_width, street_height)
        if snower_rect.colliderect(stone_rect):
            x, y, size = stone.get_position(street_top_width, street_bottom_width, street_height)
            create_particles(x, y, (255, 100, 100), 30)
            create_particles(x, y, (255, 200, 100), 20)
            create_particles(x, y, (255, 255, 255), 10)

            stones_list.remove(stone)
            play_stone_hit_sound()

            return True

    return False


# Draw snower in side view facing upward
def draw_snower_side(surface, x, y, track_movement=0):
    body_rect = pygame.Rect(x - 60, y - 80, 120, 160)
    draw_rounded_rect(surface, body_rect, METAL_GRAY, 10)

    front_rect = pygame.Rect(x - 50, y - 100, 100, 20)
    draw_rounded_rect(surface, front_rect, DARK_GRAY, 5)

    front_light_pulse = (math.sin(pygame.time.get_ticks() / 300) + 1) / 2
    front_light_color = (int(255 * front_light_pulse), 255, int(100 * front_light_pulse))
    pygame.draw.circle(surface, front_light_color, (x - 30, y - 90), 8)
    pygame.draw.circle(surface, front_light_color, (x + 30, y - 90), 8)

    cabin_rect = pygame.Rect(x - 40, y + 60, 80, 30)
    draw_rounded_rect(surface, cabin_rect, (100, 150, 200, 200), 5)

    pygame.draw.circle(surface, PURPLE, (x, y - 70), 12)
    pygame.draw.circle(surface, (200, 150, 255), (x, y - 70), 6)

    pygame.draw.line(surface, GREEN, (x, y - 100), (x, y - 120), 3)
    antenna_pulse = (math.sin(pygame.time.get_ticks() / 200) + 1) / 2
    pygame.draw.circle(surface, (int(100 * antenna_pulse), 255, int(100 * antenna_pulse)), (x, y - 125), 5)

    track_height = 40
    track_width = 30

    left_track_rect = pygame.Rect(x - 90, y - 40, track_width, track_height)
    draw_rounded_rect(surface, left_track_rect, TRACK_GRAY, 5)

    right_track_rect = pygame.Rect(x + 60, y - 40, track_width, track_height)
    draw_rounded_rect(surface, right_track_rect, TRACK_GRAY, 5)

    tread_offset = track_movement % 20
    for i in range(4):
        tread_left = pygame.Rect(x - 85, y - 35 + i * 10 + tread_offset, 20, 4)
        pygame.draw.rect(surface, (60, 60, 70), tread_left)

        tread_right = pygame.Rect(x + 65, y - 35 + i * 10 + tread_offset, 20, 4)
        pygame.draw.rect(surface, (60, 60, 70), tread_right)

    storage_left = pygame.Rect(x - 80, y + 10, 25, 40)
    draw_rounded_rect(surface, storage_left, (70, 75, 80), 3)

    storage_right = pygame.Rect(x + 55, y + 10, 25, 40)
    draw_rounded_rect(surface, storage_right, (70, 75, 80), 3)

    rear_light_pulse = (math.sin(pygame.time.get_ticks() / 500 + 1) + 1) / 2
    pygame.draw.circle(surface, (int(255 * rear_light_pulse), 0, 0), (x - 20, y + 70), 6)
    pygame.draw.circle(surface, (int(255 * rear_light_pulse), 0, 0), (x + 20, y + 70), 6)

    if abs(joystick_direction[0]) > 0.1 or abs(joystick_direction[1]) > 0.1:
        movement_pulse = (math.sin(pygame.time.get_ticks() / 150) + 1) / 2
        pygame.draw.circle(surface, (int(255 * movement_pulse), 255, int(100 * movement_pulse)), (x, y), 8)


# Helper function for rounded rectangles
def draw_rounded_rect(surface, rect, color, radius=10):
    pygame.draw.rect(surface, color, rect, border_radius=radius)


# MODIFIED: Draw parts as rectangles with ABBREVIATED text
def draw_part_as_rectangle(surface, rect, color, part_abbrev, dragging=False):
    # Draw the rectangle
    draw_rounded_rect(surface, rect, color, 10)

    # Draw a highlight effect if not dragging
    if not dragging:
        highlight_rect = pygame.Rect(rect.x + 5, rect.y + 5, rect.width - 10, 20)
        # Ensure color values don't exceed 255
        highlight_color = (
            min(255, color[0] + 40),
            min(255, color[1] + 40),
            min(255, color[2] + 40)
        )
        pygame.draw.rect(surface, highlight_color, highlight_rect, border_radius=5)

    # MODIFIED: Draw the ABBREVIATED part type text
    text = small_font.render(part_abbrev, True, WHITE)
    text_rect = text.get_rect(center=rect.center)
    surface.blit(text, text_rect)

    # Draw a border
    pygame.draw.rect(surface, WHITE, rect, 2, border_radius=10)


# Draw next level button
def draw_next_level_button(surface, mouse_pos):
    is_hovered = NEXT_LEVEL_BUTTON.collidepoint(mouse_pos)
    button_color = NEXT_LEVEL_BUTTON_HOVER_COLOR if is_hovered else NEXT_LEVEL_BUTTON_COLOR

    if is_hovered:
        glow_rect = NEXT_LEVEL_BUTTON.inflate(20, 20)
        glow_surf = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (*button_color, 80), (0, 0, glow_rect.width, glow_rect.height), border_radius=15)
        surface.blit(glow_surf, glow_rect)

    pygame.draw.rect(surface, button_color, NEXT_LEVEL_BUTTON, border_radius=12)
    pygame.draw.rect(surface, WHITE, NEXT_LEVEL_BUTTON, 3, border_radius=12)

    button_text = title_font.render("NEXT LEVEL", True, WHITE)
    text_rect = button_text.get_rect(center=NEXT_LEVEL_BUTTON.center)
    surface.blit(button_text, text_rect)

    instruction_text = small_font.render("Click to launch Drone Level 2", True, WHITE)
    instruction_rect = instruction_text.get_rect(center=(NEXT_LEVEL_BUTTON.centerx, NEXT_LEVEL_BUTTON.bottom + 20))
    surface.blit(instruction_text, instruction_rect)

    return is_hovered


# Draw control buttons
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


# Draw pause screen with clickable buttons
def draw_pause_screen(surface, mouse_pos):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surface.blit(overlay, (0, 0))

    pause_text = title_font.render("GAME PAUSED", True, YELLOW)
    surface.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 2 - 150))

    resume_hover = RESUME_BUTTON.collidepoint(mouse_pos)
    resume_color = (60, 180, 60) if resume_hover else (50, 150, 50)
    pygame.draw.rect(surface, resume_color, RESUME_BUTTON, border_radius=12)
    pygame.draw.rect(surface, WHITE, RESUME_BUTTON, 3, border_radius=12)

    resume_text = font.render("RESUME GAME", True, WHITE)
    resume_text_rect = resume_text.get_rect(center=RESUME_BUTTON.center)
    surface.blit(resume_text, resume_text_rect)

    if resume_hover:
        pygame.draw.rect(surface, (100, 255, 100, 100), RESUME_BUTTON.inflate(10, 10), border_radius=15)

    menu_hover = MAIN_MENU_BUTTON.collidepoint(mouse_pos)
    menu_color = (180, 60, 60) if menu_hover else (150, 50, 50)
    pygame.draw.rect(surface, menu_color, MAIN_MENU_BUTTON, border_radius=12)
    pygame.draw.rect(surface, WHITE, MAIN_MENU_BUTTON, 3, border_radius=12)

    menu_text = font.render("MAIN MENU", True, WHITE)
    menu_text_rect = menu_text.get_rect(center=MAIN_MENU_BUTTON.center)
    surface.blit(menu_text, menu_text_rect)

    if menu_hover:
        pygame.draw.rect(surface, (255, 100, 100, 100), MAIN_MENU_BUTTON.inflate(10, 10), border_radius=15)

    instruction = small_font.render("Press P or click RESUME to continue", True, WHITE)
    surface.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2, SCREEN_HEIGHT // 2 + 160))

    return resume_hover, menu_hover


# Draw detailed mechanic with FULL LEGS
def draw_detailed_mechanic(surface, x, y, spanner_target):
    head_radius = 20
    pygame.draw.circle(surface, SKIN_TONE, (int(x), int(y - 40)), head_radius)

    pygame.draw.ellipse(surface, BROWN, (x - 18, y - 60, 36, 20))

    pygame.draw.ellipse(surface, (200, 230, 255), (x - 18, y - 48, 16, 8))
    pygame.draw.ellipse(surface, (200, 230, 255), (x + 2, y - 48, 16, 8))
    pygame.draw.line(surface, BLACK, (x - 2, y - 44), (x + 2, y - 44), 2)

    body_width = 40
    body_height = 60
    pygame.draw.rect(surface, JEANS_BLUE, (x - body_width // 2, y - 20, body_width, body_height))

    pygame.draw.rect(surface, JEANS_BLUE, (x - body_width // 2 - 5, y - 20, 10, 30))
    pygame.draw.rect(surface, JEANS_BLUE, (x + body_width // 2 - 5, y - 20, 10, 30))

    left_arm_angle = math.sin(TOOL_ANIMATION) * 0.3 - 0.5
    right_arm_angle = math.sin(TOOL_ANIMATION + 1) * 0.5

    draw_arm(surface, x, y, left_arm_angle, 25, SKIN_TONE, True, spanner_target)
    draw_arm(surface, x, y, right_arm_angle, 25, SKIN_TONE, False)

    leg_length = 50
    leg_width = 15

    left_leg_angle = math.sin(TOOL_ANIMATION + 0.5) * 0.2
    left_leg_start_x = x - 10
    left_leg_start_y = y + body_height - 20
    left_leg_end_x = left_leg_start_x + math.sin(left_leg_angle) * leg_length
    left_leg_end_y = left_leg_start_y + math.cos(left_leg_angle) * leg_length

    pygame.draw.line(surface, JEANS_BLUE,
                     (left_leg_start_x, left_leg_start_y),
                     (left_leg_end_x, left_leg_end_y),
                     leg_width)

    pygame.draw.ellipse(surface, BROWN,
                        (left_leg_end_x - 15, left_leg_end_y - 5, 30, 10))

    right_leg_angle = math.sin(TOOL_ANIMATION + 1.5) * 0.2
    right_leg_start_x = x + 10
    right_leg_start_y = y + body_height - 20
    right_leg_end_x = right_leg_start_x + math.sin(right_leg_angle) * leg_length
    right_leg_end_y = right_leg_start_y + math.cos(right_leg_angle) * leg_length

    pygame.draw.line(surface, JEANS_BLUE,
                     (right_leg_start_x, right_leg_start_y),
                     (right_leg_end_x, right_leg_end_y),
                     leg_width)

    pygame.draw.ellipse(surface, BROWN,
                        (right_leg_end_x - 15, right_leg_end_y - 5, 30, 10))


def draw_arm(surface, body_x, body_y, angle, length, color, is_left, spanner_target=None):
    direction = -1 if is_left else 1
    start_x = body_x + direction * 15
    start_y = body_y

    upper_arm_end_x = start_x + math.cos(angle) * length * direction
    upper_arm_end_y = start_y + math.sin(angle) * length

    pygame.draw.line(surface, color, (start_x, start_y), (upper_arm_end_x, upper_arm_end_y), 8)

    lower_arm_angle = angle + 0.5
    lower_arm_end_x = upper_arm_end_x + math.cos(lower_arm_angle) * length * direction
    lower_arm_end_y = upper_arm_end_y + math.sin(lower_arm_angle) * length

    pygame.draw.line(surface, color, (upper_arm_end_x, upper_arm_end_y),
                     (lower_arm_end_x, lower_arm_end_y), 6)

    pygame.draw.circle(surface, color, (int(lower_arm_end_x), int(lower_arm_end_y)), 6)

    if is_left and spanner_target:
        draw_spanner(surface, lower_arm_end_x, lower_arm_end_y, spanner_target)


def draw_spanner(surface, hand_x, hand_y, target):
    global SPANNER_ANGLE

    dx = target[0] - hand_x
    dy = target[1] - hand_y
    distance = math.sqrt(dx * dx + dy * dy)

    if distance > 0:
        dx /= distance
        dy /= distance

        spanner_length = 40
        spanner_x = hand_x + dx * spanner_length
        spanner_y = hand_y + dy * spanner_length

        handle_length = 25
        handle_width = 4
        handle_angle = math.atan2(dy, dx)

        handle_end_x = spanner_x + math.cos(handle_angle) * handle_length
        handle_end_y = spanner_y + math.sin(handle_angle) * handle_length

        pygame.draw.line(surface, (150, 150, 150), (spanner_x, spanner_y),
                         (handle_end_x, handle_end_y), handle_width)

        head_size = 12
        pygame.draw.rect(surface, (180, 180, 180),
                         (spanner_x - head_size // 2, spanner_y - head_size // 2, head_size, head_size))

        jaw_width = 8
        jaw_height = 6
        pygame.draw.rect(surface, (200, 200, 200),
                         (spanner_x - jaw_width // 2, spanner_y - head_size // 2 - jaw_height,
                          jaw_width, jaw_height))

        if SPANNER_MOVING:
            turn_radius = 15
            turn_x = spanner_x + math.cos(SPANNER_ANGLE) * turn_radius
            turn_y = spanner_y + math.sin(SPANNER_ANGLE) * turn_radius
            pygame.draw.circle(surface, (255, 255, 100), (int(turn_x), int(turn_y)), 3)

            if random.random() < 0.1:
                create_particles(target[0], target[1], (255, 255, 100), 3)


# Draw test-specific effects
def draw_test_effects(surface, elapsed_time):
    if CURRENT_TEST_PHASE == 0:
        gauge_x = SNOWER_X - 250
        gauge_y = SNOWER_Y + 60
        draw_tension_gauge(surface, gauge_x, gauge_y)

        if random.random() < 0.1:
            create_particles(SNOWER_X - 250, SNOWER_Y + 80, (200, 200, 200), 5)
    elif CURRENT_TEST_PHASE == 1:
        gauge_x = SNOWER_X + 180
        gauge_y = SNOWER_Y + 20
        draw_rpm_gauge(surface, gauge_x, gauge_y)

        if random.random() < 0.2:
            create_particles(SNOWER_X + 150, SNOWER_Y + 30, (255, 100, 100), 8)
    elif CURRENT_TEST_PHASE == 2:
        gauge_x = SNOWER_X - 40
        gauge_y = SNOWER_Y - 120
        draw_voltage_meter(surface, gauge_x, gauge_y)

        if random.random() < 0.15:
            create_particles(SNOWER_X, SNOWER_Y - 100, (100, 200, 255), 6)
    else:
        draw_checklist(surface, SNOWER_X, SNOWER_Y + 120)

        if random.random() < 0.1:
            create_particles(SNOWER_X + random.randint(-200, 200),
                             SNOWER_Y + random.randint(-150, 150),
                             (100, 255, 100), 4)


def draw_tension_gauge(surface, x, y):
    pygame.draw.rect(surface, (50, 50, 50), (x - 20, y - 30, 40, 60), border_radius=5)
    pygame.draw.rect(surface, (80, 80, 80), (x - 18, y - 28, 36, 56), border_radius=3)

    needle_angle = math.sin(TOOL_ANIMATION * 2) * 0.7 - 0.5
    needle_length = 20
    needle_x = x + math.cos(needle_angle) * needle_length
    needle_y = y + math.sin(needle_angle) * needle_length

    pygame.draw.line(surface, RED, (x, y), (needle_x, needle_y), 3)
    pygame.draw.circle(surface, (100, 100, 100), (x, y), 5)

    label = small_font.render("TENSION", True, WHITE)
    surface.blit(label, (x - label.get_width() // 2, y + 35))


def draw_rpm_gauge(surface, x, y):
    pygame.draw.circle(surface, (50, 50, 50), (x, y), 25)
    pygame.draw.circle(surface, (80, 80, 80), (x, y), 22)

    for i in range(8):
        angle = i * math.pi / 4 - math.pi / 2
        start_x = x + math.cos(angle) * 18
        start_y = y + math.sin(angle) * 18
        end_x = x + math.cos(angle) * 22
        end_y = y + math.sin(angle) * 22
        pygame.draw.line(surface, WHITE, (start_x, start_y), (end_x, end_y), 2)

    rpm_factor = (math.sin(TOOL_ANIMATION * 3) + 1) / 2
    needle_angle = rpm_factor * math.pi - math.pi / 2
    needle_length = 20
    needle_x = x + math.cos(needle_angle) * needle_length
    needle_y = y + math.sin(needle_angle) * needle_length

    pygame.draw.line(surface, YELLOW, (x, y), (needle_x, needle_y), 3)
    pygame.draw.circle(surface, (100, 100, 100), (x, y), 4)

    label = small_font.render("RPM", True, WHITE)
    surface.blit(label, (x - label.get_width() // 2, y + 30))


def draw_voltage_meter(surface, x, y):
    pygame.draw.rect(surface, (30, 30, 40), (x - 25, y - 20, 50, 40), border_radius=5)
    pygame.draw.rect(surface, (60, 60, 70), (x - 23, y - 18, 46, 36), border_radius=3)

    voltage = 12.0 + math.sin(TOOL_ANIMATION * 2) * 0.5
    voltage_text = small_font.render(f"{voltage:.1f}V", True, NEON_GREEN)
    surface.blit(voltage_text, (x - voltage_text.get_width() // 2, y - voltage_text.get_height() // 2))

    label = small_font.render("VOLTS", True, WHITE)
    surface.blit(label, (x - label.get_width() // 2, y + 25))


def draw_checklist(surface, x, y):
    pygame.draw.rect(surface, (40, 40, 50), (x - 60, y - 50, 120, 80), border_radius=8)
    pygame.draw.rect(surface, (60, 60, 70), (x - 58, y - 48, 116, 76), border_radius=6)

    title = small_font.render("SYSTEM CHECK", True, WHITE)
    surface.blit(title, (x - title.get_width() // 2, y - 40))

    items = ["TRACKS ✓", "MOTOR ✓", "ELECTRONICS ✓", "WEAPONS ✓"]

    for i, item in enumerate(items):
        item_text = small_font.render(item, True, GREEN)
        surface.blit(item_text, (x - item_text.get_width() // 2, y - 20 + i * 15))


def get_test_phase_text():
    phases = [
        "Testing track tension...",
        "Calibrating motor power...",
        "Checking electronic systems...",
        "Final systems check..."
    ]
    return phases[CURRENT_TEST_PHASE]


# Draw realistic mechanic with spanner
def draw_realistic_mechanic_with_spanner(surface, elapsed_time):
    global TOOL_ANIMATION, MECHANIC_POSITION, SPANNER_ANGLE, SPANNER_MOVING, CURRENT_TEST_PHASE, TEST_PHASE_TIMER

    TOOL_ANIMATION += 0.05
    TEST_PHASE_TIMER += 1

    if TEST_PHASE_TIMER > 150:
        CURRENT_TEST_PHASE = (CURRENT_TEST_PHASE + 1) % 4
        TEST_PHASE_TIMER = 0
        play_spanner_sound()

    if SPANNER_MOVING:
        SPANNER_ANGLE += 0.2
        if SPANNER_ANGLE > math.pi * 2:
            SPANNER_ANGLE = 0

    if CURRENT_TEST_PHASE == 0:
        target_x = SNOWER_X - 200
        target_y = SNOWER_Y + 100
        spanner_target = (SNOWER_X - 250, SNOWER_Y + 60)
    elif CURRENT_TEST_PHASE == 1:
        target_x = SNOWER_X + 150
        target_y = SNOWER_Y + 50
        spanner_target = (SNOWER_X + 180, SNOWER_Y + 20)
    elif CURRENT_TEST_PHASE == 2:
        target_x = SNOWER_X - 50
        target_y = SNOWER_Y - 100
        spanner_target = (SNOWER_X - 40, SNOWER_Y - 120)
    else:
        target_x = SNOWER_X
        target_y = SNOWER_Y + 150
        spanner_target = (SNOWER_X, SNOWER_Y + 120)

    MECHANIC_POSITION[0] += (target_x - MECHANIC_POSITION[0]) * 0.1
    MECHANIC_POSITION[1] += (target_y - MECHANIC_POSITION[1]) * 0.1

    draw_detailed_mechanic(surface, MECHANIC_POSITION[0], MECHANIC_POSITION[1], spanner_target)
    draw_test_effects(surface, elapsed_time)


# Draw repair state
def draw_repair_state(surface, elapsed_time):
    draw_workshop(surface)
    draw_snow_environment(surface)
    draw_snowflakes(surface)
    draw_parts_panel(surface)

    lab_panel = pygame.Rect(250, 80, SCREEN_WIDTH - 280, SCREEN_HEIGHT - 150)
    s = pygame.Surface((lab_panel.width, lab_panel.height), pygame.SRCALPHA)
    pygame.draw.rect(s, (*PANEL_BG, 200), (0, 0, lab_panel.width, lab_panel.height), border_radius=20)
    surface.blit(s, lab_panel)

    title_text = title_font.render("FINAL TESTING & CALIBRATION", True, LIGHT_BLUE)
    surface.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 40))

    draw_snower(surface, SNOWER_X, SNOWER_Y, track_movement)

    for slot in SLOTS:
        draw_slot(surface, slot, parts)

    draw_wires(surface, SLOTS, parts)

    for part in parts:
        draw_part(surface, part)

    draw_particles(surface)
    draw_score(surface)

    draw_realistic_mechanic_with_spanner(surface, elapsed_time)
    draw_control_buttons(surface, pygame.mouse.get_pos())

    remaining_time = max(0, (REPAIR_DURATION - elapsed_time) // 1000)
    countdown_text = title_font.render(f"Testing: {remaining_time} seconds", True, YELLOW)
    surface.blit(countdown_text, (SCREEN_WIDTH // 2 - countdown_text.get_width() // 2, SCREEN_HEIGHT - 100))

    phase_text = font.render(get_test_phase_text(), True, WHITE)
    surface.blit(phase_text, (SCREEN_WIDTH // 2 - phase_text.get_width() // 2, SCREEN_HEIGHT - 140))


# FIXED: Draw slot with correct color logic - RED when empty, BLUE when filled
def draw_slot(surface, slot, parts):
    slot_filled = False
    # Check if any part is placed in this slot (correctly or not)
    for part in parts:
        if part["placed"] and part["placed_slot"] == slot:
            slot_filled = True
            break

    # RED when empty, BLUE when filled (any part)
    color = BLUE if slot_filled else RED
    draw_rounded_rect(surface, slot["rect"], color, 10)

    text = small_font.render(slot["type"], True, WHITE)
    text_rect = text.get_rect(center=slot["rect"].center)
    surface.blit(text, text_rect)


# Draw wires between connected parts
def draw_wires(surface, slots, parts):
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
                # Check if the index is valid
                if connected_slot_idx < 0 or connected_slot_idx >= len(slots):
                    continue

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


# FIXED: Draw detailed snower body with all mechanical parts - COMPLETELY OPAQUE
def draw_snower(surface, x, y, track_movement=0):
    # Main chassis - COMPLETELY OPAQUE (no transparency)
    chassis_rect = pygame.Rect(x - SNOWER_WIDTH // 2, y - SNOWER_HEIGHT // 2, SNOWER_WIDTH, SNOWER_HEIGHT)
    # Draw solid opaque background first
    pygame.draw.rect(surface, (40, 45, 55), chassis_rect)  # Dark background
    # Then draw the main chassis on top
    pygame.draw.rect(surface, METAL_GRAY, chassis_rect, border_radius=20)
    pygame.draw.rect(surface, DARK_GRAY, chassis_rect, 4, border_radius=20)

    # Draw grid pattern on chassis
    for i in range(-4, 5):
        grid_x = x + i * 80
        pygame.draw.line(surface, DARK_GRAY,
                         (grid_x, y - SNOWER_HEIGHT // 2 + 20),
                         (grid_x, y + SNOWER_HEIGHT // 2 - 20), 1)

    for j in range(-3, 4):
        grid_y = y + j * 80
        pygame.draw.line(surface, DARK_GRAY,
                         (x - SNOWER_WIDTH // 2 + 20, grid_y),
                         (x + SNOWER_WIDTH // 2 - 20, grid_y), 1)

    # Center frame visible
    frame_rect = pygame.Rect(x - 100, y + 150, 200, 80)
    pygame.draw.rect(surface, (90, 100, 110), frame_rect, border_radius=5)

    # Cabin with plates
    cabin_rect = pygame.Rect(x - 250, y - 250, 500, 150)
    pygame.draw.rect(surface, DARK_GRAY, cabin_rect, border_radius=10)

    # Windshield - OPAQUE version (no transparency)
    windshield_rect = pygame.Rect(x - 220, y - 240, 440, 80)
    pygame.draw.rect(surface, (150, 180, 220), windshield_rect, border_radius=8)  # Solid blue-gray
    pygame.draw.rect(surface, (100, 150, 200), windshield_rect, 3, border_radius=8)  # Border

    # Headlights (multiple)
    for i, offset in enumerate([-220, -150, -80, 80, 150, 220]):
        light_x = x + offset
        pulse = (math.sin(pygame.time.get_ticks() / 300 + i) + 1) / 2
        light_color = (int(255 * pulse), 255, int(100 * pulse))
        pygame.draw.circle(surface, light_color, (light_x, y - 220), 15)

    # Tracks with drive pods
    track_width = 120
    track_height = 120
    track_y = y + 100

    # Left track assembly
    left_pod_rect = pygame.Rect(x - 380, track_y - 40, 160, 200)
    pygame.draw.rect(surface, (80, 90, 100), left_pod_rect, border_radius=10)

    left_track_rect = pygame.Rect(x - 340, track_y, track_width, track_height)
    draw_rounded_rect(surface, left_track_rect, TRACK_GRAY, 8)

    # Right track assembly
    right_pod_rect = pygame.Rect(x + 220, track_y - 40, 160, 200)
    pygame.draw.rect(surface, (80, 90, 100), right_pod_rect, border_radius=10)

    right_track_rect = pygame.Rect(x + 220, track_y, track_width, track_height)
    draw_rounded_rect(surface, right_track_rect, TRACK_GRAY, 8)

    # Track treads (moving)
    tread_offset = track_movement % 25
    for i in range(8):
        # Left treads
        tread_left = pygame.Rect(x - 330, track_y + 15 + i * 15 + tread_offset, 100, 10)
        pygame.draw.rect(surface, (60, 60, 70), tread_left, border_radius=3)

        # Right treads
        tread_right = pygame.Rect(x + 230, track_y + 15 + i * 15 + tread_offset, 100, 10)
        pygame.draw.rect(surface, (60, 60, 70), tread_right, border_radius=3)

    # Drive cogs
    cog_radius = 35
    # Left cog
    pygame.draw.circle(surface, SILVER, (x - 280, track_y + 60), cog_radius)
    pygame.draw.circle(surface, DARK_GRAY, (x - 280, track_y + 60), cog_radius - 15)

    # Right cog
    pygame.draw.circle(surface, SILVER, (x + 280, track_y + 60), cog_radius)
    pygame.draw.circle(surface, DARK_GRAY, (x + 280, track_y + 60), cog_radius - 15)

    # Storage compartments
    storage_left = pygame.Rect(x - 300, y - 60, 60, 120)
    draw_rounded_rect(surface, storage_left, (70, 75, 80), 5)

    storage_right = pygame.Rect(x + 240, y - 60, 60, 120)
    draw_rounded_rect(surface, storage_right, (70, 75, 80), 5)

    # Plow assembly at front
    plow_points = [
        (x - 180, y - 300),
        (x - 120, y - 350),
        (x + 120, y - 350),
        (x + 180, y - 300),
        (x + 150, y - 280),
        (x - 150, y - 280)
    ]
    pygame.draw.polygon(surface, (120, 100, 80), plow_points)

    # Plow blade edge
    pygame.draw.line(surface, SILVER, (x - 150, y - 290), (x + 150, y - 290), 10)

    # Servomotor for plow
    servo_rect = pygame.Rect(x - 60, y - 250, 120, 60)
    pygame.draw.rect(surface, (180, 60, 60), servo_rect, border_radius=5)

    # Control linkages
    for side in [-1, 1]:
        link_start = (x + side * 90, y - 250)
        link_end = (x + side * 150, y - 300)
        pygame.draw.line(surface, (100, 80, 60), link_start, link_end, 8)

    # Antenna with blinking light
    antenna_pulse = (math.sin(pygame.time.get_ticks() / 200) + 1) / 2
    pygame.draw.line(surface, GREEN, (x, y - 250), (x, y - 320), 5)
    pygame.draw.circle(surface, (int(100 * antenna_pulse), 255, int(100 * antenna_pulse)),
                       (x, y - 325), 10)

    # Various sensors and cameras
    sensor_positions = [(-200, -200), (200, -200), (-280, -160), (280, -160)]
    for sx, sy in sensor_positions:
        pygame.draw.circle(surface, CYAN, (x + sx, y + sy), 15)
        pygame.draw.circle(surface, (100, 200, 255), (x + sx, y + sy), 8)

    # Rear lights
    rear_pulse = (math.sin(pygame.time.get_ticks() / 500 + 1) + 1) / 2
    for offset in [-120, -60, 60, 120]:
        pygame.draw.circle(surface, (int(255 * rear_pulse), 0, 0),
                           (x + offset, y + 200), 10)

    # Exhaust vents
    for i in range(4):
        vent_x = x - 90 + i * 60
        vent_rect = pygame.Rect(vent_x, y + 50, 25, 60)
        pygame.draw.rect(surface, (50, 55, 60), vent_rect, border_radius=3)

        if random.random() < 0.1:
            create_particles(vent_x + 12, y + 30, (200, 200, 220), 8)


# Draw snow environment
def draw_snow_environment(surface):
    snow_height = 150
    points = []
    for x in range(0, SCREEN_WIDTH + 10, 10):
        y_base = SCREEN_HEIGHT - snow_height
        y_variation = math.sin(x / 50 + pygame.time.get_ticks() / 1000) * 5
        y = y_base + y_variation
        points.append((x, y))

    points.append((SCREEN_WIDTH, SCREEN_HEIGHT))
    points.append((0, SCREEN_HEIGHT))

    if len(points) > 2:
        pygame.draw.polygon(surface, SNOW_BLUE, points)

    for i in range(5):
        x = (i * 200 + 50) % SCREEN_WIDTH
        y = SCREEN_HEIGHT - 100
        radius = 40 + (i * 13) % 30
        pygame.draw.circle(surface, SNOW_BLUE, (x, y), radius)


# Draw snowflakes - BUT DRAW THEM BEFORE THE SNOWER BODY (order is handled in main loop)
def draw_snowflakes(surface):
    for i in range(100):
        x = (pygame.time.get_ticks() // 30 + i * 71) % SCREEN_WIDTH
        y = (pygame.time.get_ticks() // 20 + i * 53) % SCREEN_HEIGHT
        size = 1 + (i % 4)

        if i % 3 == 0:
            pygame.draw.circle(surface, WHITE, (x, y), size)
        elif i % 3 == 1:
            pygame.draw.circle(surface, (240, 240, 255), (x, y), size)
        else:
            s = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (250, 250, 255), (size, size), size)
            surface.blit(s, (x - size, y - size))


# Draw workshop background
def draw_workshop(surface):
    wall_color = (40, 35, 30)
    pygame.draw.rect(surface, wall_color, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    floor_color = (50, 45, 40)
    pygame.draw.rect(surface, floor_color, (0, SCREEN_HEIGHT - 200, SCREEN_WIDTH, 200))

    shelf_color = (60, 55, 50)
    for i in range(3):
        shelf_rect = pygame.Rect(50 + i * 300, 100, 200, 20)
        pygame.draw.rect(surface, shelf_color, shelf_rect)

        for j in range(4):
            tool_rect = pygame.Rect(60 + i * 300 + j * 45, 80, 30, 15)
            pygame.draw.rect(surface, (80, 75, 70), tool_rect)

    bench_rect = pygame.Rect(SCREEN_WIDTH - 300, SCREEN_HEIGHT - 250, 250, 50)
    pygame.draw.rect(surface, (70, 60, 50), bench_rect)

    pygame.draw.rect(surface, (60, 50, 40), (SCREEN_WIDTH - 300, SCREEN_HEIGHT - 200, 20, 200))
    pygame.draw.rect(surface, (60, 50, 40), (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 200, 20, 200))


# ENHANCED: Draw parts panel for more parts - REORGANIZED
def draw_parts_panel(surface):
    # FIXED: Updated panel position to match new parts_start_y
    panel_rect = pygame.Rect(30, 180, 450, SCREEN_HEIGHT - 230)
    pygame.draw.rect(surface, (40, 45, 55), panel_rect)
    pygame.draw.rect(surface, (70, 75, 85), panel_rect, 3)

    title_text = font.render("SNOWER COMPONENTS", True, LIGHT_BLUE)
    title_y = panel_rect.bottom - 30
    surface.blit(title_text, (35, title_y))

    placed = sum(1 for part in parts if part["placed"])
    total = len(parts)
    count_text = small_font.render(f"Parts: {placed}/{total}", True, WHITE)
    surface.blit(count_text, (35, panel_rect.bottom - 50))

    pygame.draw.line(surface, (70, 75, 85), (30, 210), (480, 210), 2)


# Draw level intro
def draw_level_intro(surface, timer):
    surface.fill((0, 0, 0))

    pulse = (math.sin(timer / 200) + 1) / 2
    pulse_scale = 0.5 + pulse * 0.5

    level_text = title_font.render("LEVEL 1", True, WHITE)
    level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))

    scaled_text = pygame.transform.scale(
        level_text,
        (int(level_text.get_width() * pulse_scale),
         int(level_text.get_height() * pulse_scale))
    )
    scaled_rect = scaled_text.get_rect(center=level_rect.center)
    surface.blit(scaled_text, scaled_rect)

    subtitle_text = font.render("SNOWER ASSEMBLY", True, CYAN)
    subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
    surface.blit(subtitle_text, subtitle_rect)

    if timer > 1500:
        alpha = min(255, (timer - 1500) * 2)
        instruction_text = small_font.render("Assemble the snower to make it move", True, (200, 200, 200))
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))

        instruction_surface = pygame.Surface(instruction_text.get_size(), pygame.SRCALPHA)
        instruction_surface.fill((0, 0, 0, 0))
        instruction_surface.blit(instruction_text, (0, 0))
        instruction_surface.set_alpha(alpha)
        surface.blit(instruction_surface, instruction_rect)


# Check if all parts are correctly placed
def check_win_condition(parts, slots):
    correctly_filled = 0
    for slot in slots:
        for part in parts:
            if part["placed"] and part["placed_slot"] == slot and part["type"] == slot["type"]:
                correctly_filled += 1
                break
    return correctly_filled == len(slots)


# Draw score
def draw_score(surface):
    score_panel = pygame.Rect(SCREEN_WIDTH - 250, 20, 230, 60)
    pygame.draw.rect(surface, (40, 45, 55), score_panel, border_radius=10)
    pygame.draw.rect(surface, (70, 75, 85), score_panel, 2, border_radius=10)

    score_text = font.render(f"SCORE: {SCORE}", True, WHITE)
    surface.blit(score_text, (SCREEN_WIDTH - 240, 30))

    if COMBO > 1:
        combo_text = font.render(f"COMBO: x{COMBO}", True, NEON_GREEN)
        surface.blit(combo_text, (SCREEN_WIDTH - 240, 55))


# Draw leaves counter
def draw_leaves_counter(surface):
    leaves_panel = pygame.Rect(SCREEN_WIDTH - 250, 250, 230, 60)
    pygame.draw.rect(surface, (40, 45, 55), leaves_panel, border_radius=10)
    pygame.draw.rect(surface, (70, 75, 85), leaves_panel, 2, border_radius=10)

    leaves_text = font.render(f"LEAVES: {leaves_collected}/{total_leaves_needed}", True, WHITE)
    surface.blit(leaves_text, (SCREEN_WIDTH - 240, 260))

    if total_leaves_needed > 0:
        progress_width = 200
        progress_filled = int(progress_width * (leaves_collected / total_leaves_needed))
        pygame.draw.rect(surface, DARK_GRAY, (SCREEN_WIDTH - 230, 290, progress_width, 10), border_radius=5)
        if progress_filled > 0:
            progress_color = GREEN if leaves_collected >= total_leaves_needed else LEAF_GREEN
            pygame.draw.rect(surface, progress_color, (SCREEN_WIDTH - 230, 290, progress_filled, 10), border_radius=5)


# Draw stones counter
def draw_stones_counter(surface):
    stones_panel = pygame.Rect(SCREEN_WIDTH - 250, 320, 230, 60)
    pygame.draw.rect(surface, (40, 45, 55), stones_panel, border_radius=10)
    pygame.draw.rect(surface, (70, 75, 85), stones_panel, 2, border_radius=10)

    stones_text = font.render(f"STONES AVOIDED: {stones_avoided}", True, WHITE)
    surface.blit(stones_text, (SCREEN_WIDTH - 240, 330))


# ENHANCED: Draw victory screen with more information
def draw_victory(surface, mouse_pos):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 50, 0, 180))
    surface.blit(overlay, (0, 0))

    victory_text = title_font.render("COMPLETE VICTORY!", True, NEON_GREEN)
    surface.blit(victory_text, (SCREEN_WIDTH // 2 - victory_text.get_width() // 2, SCREEN_HEIGHT // 2 - 120))

    assembled_text = font.render(f"Snower Successfully Assembled with {len(SLOTS)} parts!", True, CYAN)
    surface.blit(assembled_text, (SCREEN_WIDTH // 2 - assembled_text.get_width() // 2, SCREEN_HEIGHT // 2 - 70))

    leaves_text = font.render(f"Leaves Collected: {leaves_collected}/{total_leaves_needed}", True, LEAF_GREEN)
    surface.blit(leaves_text, (SCREEN_WIDTH // 2 - leaves_text.get_width() // 2, SCREEN_HEIGHT // 2 - 30))

    score_text = font.render(f"Final Score: {SCORE}", True, GOLD)
    surface.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))

    stones_text = font.render(f"Stones Avoided: {stones_avoided}", True, WHITE)
    surface.blit(stones_text, (SCREEN_WIDTH // 2 - stones_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))

    is_hovered = draw_next_level_button(surface, mouse_pos)

    return is_hovered


# Draw game over screen
def draw_game_over_screen(surface, mouse_pos):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((50, 0, 0, 180))
    surface.blit(overlay, (0, 0))

    game_over_text = title_font.render("GAME OVER", True, RED)
    surface.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 80))

    leaves_text = font.render(f"Leaves Collected: {leaves_collected}/{total_leaves_needed}", True, LEAF_GREEN)
    surface.blit(leaves_text, (SCREEN_WIDTH // 2 - leaves_text.get_width() // 2, SCREEN_HEIGHT // 2 - 30))

    score_text = font.render(f"Final Score: {SCORE}", True, WHITE)
    surface.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))

    stones_text = font.render(f"Stones Avoided: {stones_avoided}", True, WHITE)
    surface.blit(stones_text, (SCREEN_WIDTH // 2 - stones_text.get_width() // 2, SCREEN_HEIGHT // 2 + 30))

    restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 60)
    restart_hover = restart_button.collidepoint(mouse_pos)
    restart_color = (60, 180, 60) if restart_hover else (50, 150, 50)

    if restart_hover:
        glow_rect = restart_button.inflate(20, 20)
        glow_surf = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (*restart_color, 80), (0, 0, glow_rect.width, glow_rect.height), border_radius=15)
        surface.blit(glow_surf, glow_rect)

    pygame.draw.rect(surface, restart_color, restart_button, border_radius=12)
    pygame.draw.rect(surface, WHITE, restart_button, 3, border_radius=12)

    restart_text = font.render("RESTART GAME", True, WHITE)
    restart_rect = restart_text.get_rect(center=restart_button.center)
    surface.blit(restart_text, restart_rect)

    instruction_text = small_font.render("Press R to restart", True, WHITE)
    surface.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, SCREEN_HEIGHT // 2 + 180))

    return restart_button, restart_hover


# ENHANCED: Reset game function for all new parts - CREATES 36 PARTS FOR 36 SLOTS
def reset_game():
    global parts, part_id, game_state, snower_x, snower_y, movement_speed, track_movement
    global COMBO, JOYSTICK_BUTTON_ACTIVE, JOYSTICK_BUTTON_COLOR
    global KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, KEYBOARD_CONTROL, WIN_SOUND_PLAYED, PAUSED
    global REPAIR_TIMER, TOOL_ANIMATION, MECHANIC_POSITION, SPANNER_ANGLE, SPANNER_MOVING, CURRENT_TEST_PHASE, TEST_PHASE_TIMER
    global MOVEMENT_STATE_TIMER, stones, stones_avoided, stone_spawn_timer, leaves, leaves_collected
    global SHOW_SNOWER_IMAGE  # NEW: Added for image display

    parts = []
    part_id = 0

    # MODIFIED: Create exactly one part per slot (36 parts total)
    # Count how many of each part type we need
    parts_needed = {}
    for slot in SLOTS:
        part_type = slot["type"]
        parts_needed[part_type] = parts_needed.get(part_type, 0) + 1

    # Create parts based on what's needed for slots
    for part_type, part_info in PARTS.items():
        count_needed = parts_needed.get(part_type, 0)
        for i in range(count_needed):
            column = part_id % 4
            row = part_id // 4

            x_pos = parts_start_x + column * parts_spacing_x
            y_pos = parts_start_y + row * parts_spacing_y

            parts.append({
                "id": part_id,
                "type": part_type,
                "abbrev": part_type[:2].upper() if len(part_type) > 2 else part_type.upper(),
                "rect": pygame.Rect(x_pos, y_pos, 100, 80),
                "color": part_info["color"],
                "radius": 10,
                "dragging": False,
                "placed": False,
                "placed_slot": None,
                "original_pos": (x_pos, y_pos)
            })
            part_id += 1

    print(f"Reset: Created {len(parts)} parts for {len(SLOTS)} slots")

    game_state = ASSEMBLY_STATE
    snower_x = SCREEN_WIDTH // 2
    snower_y = SCREEN_HEIGHT // 2
    movement_speed = 0
    track_movement = 0
    COMBO = 0
    JOYSTICK_BUTTON_ACTIVE = False
    JOYSTICK_BUTTON_COLOR = GREEN
    KEY_LEFT = False
    KEY_RIGHT = False
    KEY_UP = False
    KEY_DOWN = False
    KEYBOARD_CONTROL = False
    WIN_SOUND_PLAYED = False
    PAUSED = False
    REPAIR_TIMER = 0
    TOOL_ANIMATION = 0
    MECHANIC_POSITION = [SNOWER_X - 300, SNOWER_Y + 100]
    SPANNER_ANGLE = 0
    SPANNER_MOVING = True
    CURRENT_TEST_PHASE = 0
    TEST_PHASE_TIMER = 0
    MOVEMENT_STATE_TIMER = 0
    stones = []
    stones_avoided = 0
    stone_spawn_timer = 0
    leaves = []
    leaves_collected = 0
    SHOW_SNOWER_IMAGE = True  # NEW: Show image on reset
    reset_joystick()

    play_background_music()


# MODIFIED: Main drawing function for parts - UPDATED TO USE RECTANGLES AND ABBREVIATIONS
def draw_part(surface, part, alpha=255):
    if part["dragging"]:
        s = pygame.Surface((part["rect"].width, part["rect"].height), pygame.SRCALPHA)
        temp_rect = pygame.Rect(0, 0, part["rect"].width, part["rect"].height)

        # MODIFIED: Use abbreviated name for dragging part
        draw_part_as_rectangle(s, temp_rect, part["color"], part["abbrev"], True)

        s.set_alpha(180)
        surface.blit(s, part["rect"])

        shadow = pygame.Surface((part["rect"].width + 10, part["rect"].height + 10), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0, 0, 0, 100), (0, 0, part["rect"].width + 10, part["rect"].height + 10),
                         border_radius=part["radius"] + 5)
        surface.blit(shadow, (part["rect"].x - 5, part["rect"].y - 5))
    else:
        # MODIFIED: Use abbreviated name for regular part
        draw_part_as_rectangle(surface, part["rect"], part["color"], part["abbrev"], False)


# Main game loop
clock = pygame.time.Clock()
dragging_part = None
offset_x, offset_y = 0, 0
game_state = LEVEL_INTRO_STATE
intro_timer = 0
success_timer = 0
activation_timer = 0
snower_x = SCREEN_WIDTH // 2
snower_y = SCREEN_HEIGHT // 2
movement_speed = 0
track_movement = 0

# Start background music
play_background_music()

print("\n" + "=" * 50)
print("SNOWER GAME - LEVEL 1")
print("=" * 50)
print(f"Current directory: {os.getcwd()}")
print(f"Base directory: {BASE_DIR}")
print("=" * 50 + "\n")

while True:
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if not PAUSED:
                    # When not paused, ESC goes to main menu
                    print("ESC pressed - Returning to main menu...")
                    go_to_main_menu()
                elif PAUSED:
                    # When paused, ESC also goes to main menu
                    print("ESC pressed in pause - Returning to main menu...")
                    go_to_main_menu()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if PAUSED:
                resume_hover = RESUME_BUTTON.collidepoint(mouse_pos)
                menu_hover = MAIN_MENU_BUTTON.collidepoint(mouse_pos)
                if resume_hover:
                    PAUSED = False
                    print("Resuming game...")
                elif menu_hover:
                    print("Returning to main menu...")
                    # FIXED: Call the correct function
                    go_to_main_menu()
            else:
                if game_state == ASSEMBLY_STATE:
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

                elif game_state == MOVEMENT_STATE:
                    escape_hover, pause_hover = draw_control_buttons(screen, mouse_pos)
                    if escape_hover:
                        go_to_main_menu()
                    elif pause_hover:
                        PAUSED = True
                    else:
                        dx = event.pos[0] - joystick_handle_pos[0]
                        dy = event.pos[1] - joystick_handle_pos[1]
                        distance = math.sqrt(dx * dx + dy * dy)

                        if distance <= joystick_handle_radius:
                            joystick_dragging = True

                elif game_state == VICTORY_STATE and NEXT_LEVEL_BUTTON.collidepoint(mouse_pos):
                    transition_to_drone_level()

                elif game_state == GAME_OVER_STATE:
                    restart_button, restart_hover = draw_game_over_screen(screen, mouse_pos)
                    if restart_hover:
                        reset_game()

        if not PAUSED:
            if game_state == ASSEMBLY_STATE:
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and dragging_part:
                        dragging_part["dragging"] = False

                        part_placed = False
                        for slot in SLOTS:
                            if (slot["rect"].colliderect(dragging_part["rect"]) and
                                    dragging_part["type"] == slot["type"]):
                                slot_already_filled = False
                                for other_part in parts:
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

                        if check_win_condition(parts, SLOTS):
                            game_state = SUCCESS_STATE
                            success_timer = pygame.time.get_ticks()
                            SCORE += 100 * COMBO if COMBO > 0 else 100

                elif event.type == pygame.MOUSEMOTION:
                    if dragging_part:
                        dragging_part["rect"].x = event.pos[0] + offset_x
                        dragging_part["rect"].y = event.pos[1] + offset_y

            elif game_state == MOVEMENT_STATE:
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and joystick_dragging:
                        joystick_dragging = False
                        reset_joystick()

                elif event.type == pygame.MOUSEMOTION:
                    if joystick_dragging:
                        update_joystick(event.pos)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                PAUSED = not PAUSED
            elif event.key == pygame.K_a and game_state == MOVEMENT_STATE and not PAUSED:
                KEY_LEFT = True
                KEYBOARD_CONTROL = True
            elif event.key == pygame.K_d and game_state == MOVEMENT_STATE and not PAUSED:
                KEY_RIGHT = True
                KEYBOARD_CONTROL = True
            elif event.key == pygame.K_w and game_state == MOVEMENT_STATE and not PAUSED:
                KEY_UP = True
                KEYBOARD_CONTROL = True
            elif event.key == pygame.K_s and game_state == MOVEMENT_STATE and not PAUSED:
                KEY_DOWN = True
                KEYBOARD_CONTROL = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                KEY_LEFT = False
            elif event.key == pygame.K_d:
                KEY_RIGHT = False
            elif event.key == pygame.K_w:
                KEY_UP = False
            elif event.key == pygame.K_s:
                KEY_DOWN = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and game_state == SUCCESS_STATE and not PAUSED:
                game_state = REPAIR_STATE
                REPAIR_TIMER = pygame.time.get_ticks()
                play_repair_sound()
                # Hide snower image when moving to repair state
                SHOW_SNOWER_IMAGE = False

            if event.key == pygame.K_r and (
                    game_state == VICTORY_STATE or game_state == GAME_OVER_STATE) and not PAUSED:
                reset_game()

    if not PAUSED:
        if game_state == LEVEL_INTRO_STATE:
            intro_timer += clock.get_time()
            if intro_timer > 4000:
                game_state = ASSEMBLY_STATE

        elif game_state == SUCCESS_STATE:
            pass

        elif game_state == REPAIR_STATE:
            elapsed_time = pygame.time.get_ticks() - REPAIR_TIMER

            TOOL_ANIMATION += 0.05

            if random.random() < 0.2:
                spark_x = SNOWER_X + random.randint(-200, 200)
                spark_y = SNOWER_Y + random.randint(-150, 150)
                create_particles(spark_x, spark_y, (255, 255, 100), 5)

            if elapsed_time >= REPAIR_DURATION:
                game_state = MOVEMENT_STATE
                MOVEMENT_STATE_TIMER = 0
                stones = []
                stones_avoided = 0
                stone_spawn_timer = pygame.time.get_ticks()
                leaves = []
                leaves_collected = 0
                play_movement_sound()

        elif game_state == MOVEMENT_STATE:
            MOVEMENT_STATE_TIMER += clock.get_time()

            if KEYBOARD_CONTROL and not joystick_dragging:
                update_joystick_keyboard()

            movement_speed = 5
            snower_x += movement_speed * joystick_direction[0] * 2
            snower_y += movement_speed * joystick_direction[1] * 2

            snower_x = max(100, min(SCREEN_WIDTH - 100, snower_x))
            snower_y = max(120, min(SCREEN_HEIGHT - 120, snower_y))

            track_movement += movement_speed
            if track_movement > 70:
                track_movement = 0

            if pygame.time.get_ticks() % 10 == 0 and (joystick_direction[0] != 0 or joystick_direction[1] != 0):
                create_particles(snower_x, snower_y, (200, 200, 255), 2)

            spawn_stone_group()
            update_stones(stones)

            screen.fill(BACKGROUND)
            street_top_width, street_bottom_width, street_height = draw_street_scene(screen)

            if len(leaves) == 0 and leaves_collected == 0:
                initialize_leaves(street_top_width, street_bottom_width, street_height)

            if random.random() < 0.01 and len(leaves) < total_leaves_needed:
                spawn_leaves_randomly(leaves, street_top_width, street_bottom_width, street_height, 1)

            update_leaves(leaves)
            check_leaf_collection(snower_x, snower_y, leaves)

            if check_stone_collision(snower_x, snower_y, stones, street_top_width, street_bottom_width, street_height):
                game_state = GAME_OVER_STATE
                play_lose_sound()
                stop_background_music()

            if leaves_collected >= total_leaves_needed and game_state != VICTORY_STATE:
                game_state = VICTORY_STATE
                create_particles(snower_x, snower_y, NEON_GREEN, 100)
                create_particles(snower_x, snower_y, LEAF_GREEN, 80)
                create_particles(snower_x, snower_y, GOLD, 60)

                if not WIN_SOUND_PLAYED:
                    play_win_sound()
                    WIN_SOUND_PLAYED = True
                    stop_background_music()

        update_particles()
        update_battery()

        if game_state == MOVEMENT_STATE and joystick_dragging:
            update_joystick(mouse_pos)

    screen.fill(BACKGROUND)

    if game_state == LEVEL_INTRO_STATE:
        draw_level_intro(screen, intro_timer)

    elif game_state == ASSEMBLY_STATE or game_state == SUCCESS_STATE:
        draw_workshop(screen)
        draw_snow_environment(screen)
        draw_snowflakes(screen)
        draw_parts_panel(screen)

        lab_panel = pygame.Rect(250, 80, SCREEN_WIDTH - 280, SCREEN_HEIGHT - 150)
        s = pygame.Surface((lab_panel.width, lab_panel.height), pygame.SRCALPHA)
        pygame.draw.rect(s, (*PANEL_BG, 200), (0, 0, lab_panel.width, lab_panel.height), border_radius=20)
        screen.blit(s, lab_panel)

        title_text = title_font.render("SNOWER ASSEMBLY STATION", True, LIGHT_BLUE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 40))

        # FIXED: Draw snower body BEFORE slots and parts (completely opaque)
        draw_snower(screen, SNOWER_X, SNOWER_Y, track_movement)

        # Draw slots on top of snower body
        for slot in SLOTS:
            draw_slot(screen, slot, parts)

        # Draw wires on top of slots
        draw_wires(screen, SLOTS, parts)

        # Draw parts on top
        for part in parts:
            draw_part(screen, part)

        draw_particles(screen)
        draw_score(screen)

        # NEW: Draw snower image under score during assembly state
        draw_snower_image_under_score(screen)

        instructions = font.render(f"Assemble all {len(SLOTS)} components to build your Snower", True, WHITE)
        screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, SCREEN_HEIGHT - 50))

        placed_count = sum(1 for part in parts if part["placed"])
        total_count = len(parts)
        count_text = small_font.render(f"Components Placed: {placed_count}/{total_count}", True, WHITE)
        screen.blit(count_text, (SCREEN_WIDTH - count_text.get_width() - 30, SCREEN_HEIGHT - 80))

        hint_text = small_font.render(
            "Match components to their correct slots - Mechanical parts need precise placement!", True, YELLOW)
        screen.blit(hint_text, (SCREEN_WIDTH // 2 - hint_text.get_width() // 2, SCREEN_HEIGHT - 30))

        draw_control_buttons(screen, mouse_pos)

        if game_state == SUCCESS_STATE:
            win_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            win_surface.fill((0, 0, 0, 150))
            screen.blit(win_surface, (0, 0))

            win_text = title_font.render("SNOWER ASSEMBLED SUCCESSFULLY!", True, GREEN)
            screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))

            bonus_text = font.render(f"Bonus: +{100 * COMBO if COMBO > 0 else 100} points!", True, NEON_GREEN)
            screen.blit(bonus_text, (SCREEN_WIDTH // 2 - bonus_text.get_width() // 2, SCREEN_HEIGHT // 2))

            activation_text = font.render("Press ENTER for final testing and calibration", True, WHITE)
            screen.blit(activation_text,
                        (SCREEN_WIDTH // 2 - activation_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))

    elif game_state == REPAIR_STATE:
        elapsed_time = pygame.time.get_ticks() - REPAIR_TIMER
        draw_repair_state(screen, elapsed_time)

    elif game_state == MOVEMENT_STATE or game_state == VICTORY_STATE or game_state == GAME_OVER_STATE:
        street_top_width, street_bottom_width, street_height = draw_street_scene(screen)
        draw_snowflakes(screen)
        draw_particles(screen)
        draw_score(screen)
        draw_leaves_counter(screen)
        draw_stones_counter(screen)
        draw_joystick(screen)
        draw_snower_side(screen, snower_x, snower_y, track_movement)

        draw_leaves(screen, leaves)
        draw_minimap_camera(screen, snower_x, snower_y, stones, leaves, street_top_width, street_bottom_width,
                            street_height)
        draw_stones(screen, stones, street_top_width, street_bottom_width, street_height)

        move_text = title_font.render(f"COLLECT {total_leaves_needed} LEAVES!", True, LEAF_GREEN)
        screen.blit(move_text, (SCREEN_WIDTH // 2 - move_text.get_width() // 2, 80))

        progress_text = font.render(f"Leaves: {leaves_collected}/{total_leaves_needed} - Keep going!", True, WHITE)
        screen.blit(progress_text, (SCREEN_WIDTH // 2 - progress_text.get_width() // 2, 120))

        instructions = font.render("Use WASD or joystick to move - Build momentum to collect leaves faster!", True,
                                   WHITE)
        screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, SCREEN_HEIGHT - 50))

        draw_control_buttons(screen, mouse_pos)

        if game_state == VICTORY_STATE:
            draw_victory(screen, mouse_pos)
        elif game_state == GAME_OVER_STATE:
            draw_game_over_screen(screen, mouse_pos)

    if PAUSED:
        draw_pause_screen(screen, mouse_pos)

    pygame.display.flip()
    clock.tick(60)