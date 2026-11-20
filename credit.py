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
pygame.display.set_caption("ROBOTS GAME - Credits")

# Colors
BACKGROUND = (10, 15, 25)
NEON_BLUE = (50, 150, 255)
NEON_CYAN = (50, 255, 255)
NEON_GREEN = (50, 255, 100)
NEON_PURPLE = (180, 50, 255)
NEON_RED = (255, 50, 50)
NEON_YELLOW = (255, 255, 50)
WHITE = (240, 240, 240)
GRAY = (120, 120, 120)

# Fonts
title_font = pygame.font.SysFont("Arial", 48, bold=True)
heading_font = pygame.font.SysFont("Arial", 36, bold=True)
regular_font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 18)


# Load and play background music
def load_music():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        music_path = os.path.join(script_dir, "Credit.mp3")

        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)
            print("Background music loaded successfully")
        else:
            print(f"Music file not found at: {music_path}")
            music_path_wav = os.path.join(script_dir, "Credit.wav")
            if os.path.exists(music_path_wav):
                pygame.mixer.music.load(music_path_wav)
                pygame.mixer.music.play(-1)
                print("Background music loaded successfully (WAV format)")
            else:
                print("No background music file found")
    except Exception as e:
        print(f"Error loading music: {e}")


# Credit content
CREDITS = [
    {"category": "Game Idea", "items": [
        "Tommi kokko"
    ]},
    {"category": "DEVELOPMENT", "items": [
        "Mustafa"
    ]},
    {"category": "DESIGN", "items": [
        "photoshop",
        "photopea",
        "Canva"
    ]},
    {"category": "AUDIO", "items": [
        "Sound Effects: M. T,pixabay",
        "Music: E. W. pixabay",
        "Background Music: H. J"
    ]},
    {"category": "Game make by", "items": [
        "Pygame",
        "Python"
    ]},
    {"category": "SPECIAL THANKS", "items": [
        "Tommi kokko",
        "Robotics Engineering Team",
        "Marja Marin",
        "Redu Vocational School"
    ]}
]

# Effects
PARTICLES = []
STARS = []
for i in range(100):
    STARS.append({
        "x": random.randint(0, SCREEN_WIDTH),
        "y": random.randint(0, SCREEN_HEIGHT),
        "size": random.uniform(0.5, 2),
        "brightness": random.randint(100, 255)
    })


# Button class with semi-transparent background
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color  # RGB
        self.hover_color = hover_color  # RGB
        self.is_hovered = False
        self.bg_alpha = 200  # Background transparency (0-255)

    def draw(self, surface):
        # Draw semi-transparent background
        bg_color = self.hover_color if self.is_hovered else self.color

        # Create surface with alpha
        button_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)

        # Draw background with rounded corners
        pygame.draw.rect(button_surface, (*bg_color, self.bg_alpha),
                         (0, 0, self.rect.width, self.rect.height),
                         border_radius=8)

        # Draw border
        pygame.draw.rect(button_surface, WHITE,
                         (0, 0, self.rect.width, self.rect.height),
                         2, border_radius=8)

        # Draw text
        text_surf = small_font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=(self.rect.width // 2, self.rect.height // 2))
        button_surface.blit(text_surf, text_rect)

        # Draw glow effect when hovered
        if self.is_hovered:
            glow_surface = pygame.Surface((self.rect.width + 10, self.rect.height + 10), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (*bg_color, 80),
                             (0, 0, self.rect.width + 10, self.rect.height + 10),
                             border_radius=12)
            surface.blit(glow_surface, (self.rect.x - 5, self.rect.y - 5))

        # Blit button onto main surface
        surface.blit(button_surface, self.rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered

    def is_clicked(self, pos, click):
        return self.rect.collidepoint(pos) and click


# Create particles
def create_particles(x, y, color, count=5):
    for _ in range(count):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 3)
        size = random.uniform(2, 4)
        PARTICLES.append({
            "x": x, "y": y,
            "vx": math.cos(angle) * speed,
            "vy": math.sin(angle) * speed,
            "color": color,
            "life": 30,
            "max_life": 30,
            "size": size
        })


# Update particles
def update_particles():
    for particle in PARTICLES[:]:
        particle["x"] += particle["vx"]
        particle["y"] += particle["vy"]
        particle["life"] -= 1
        if particle["life"] <= 0:
            PARTICLES.remove(particle)


# Draw particles
def draw_particles(surface):
    for particle in PARTICLES:
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


# Draw stars
def draw_stars(surface):
    for star in STARS:
        brightness = int(star["brightness"] + 50 * math.sin(pygame.time.get_ticks() / 1000 + star["x"]))
        brightness = max(0, min(255, brightness))
        size = max(1, int(star["size"]))
        pygame.draw.circle(surface, (brightness, brightness, brightness),
                           (int(star["x"]), int(star["y"])), size)


# Draw cyber grid background
def draw_grid(surface):
    grid_color = (20, 25, 40)
    line_color = (30, 35, 50)

    pygame.draw.rect(surface, BACKGROUND, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    grid_size = 50
    for x in range(0, SCREEN_WIDTH, grid_size):
        pygame.draw.line(surface, line_color, (x, 0), (x, SCREEN_HEIGHT), 1)
    for y in range(0, SCREEN_HEIGHT, grid_size):
        pygame.draw.line(surface, line_color, (0, y), (SCREEN_WIDTH, y), 1)

    for x in range(grid_size // 2, SCREEN_WIDTH, grid_size):
        for y in range(grid_size // 2, SCREEN_HEIGHT, grid_size):
            pulse = (math.sin(pygame.time.get_ticks() / 1000 + x + y) + 1) / 2
            node_color = (int(50 + 50 * pulse), int(100 + 50 * pulse), int(150 + 50 * pulse))
            pygame.draw.circle(surface, node_color, (x, y), 1)


# Draw cyber canine silhouette
def draw_canine_silhouette(surface, x, y, pulse):
    body_rect = pygame.Rect(x - 120, y - 80, 240, 160)
    pygame.draw.rect(surface, (30, 35, 55), body_rect, border_radius=20)

    head_rect = pygame.Rect(x - 60, y - 160, 120, 80)
    pygame.draw.rect(surface, (25, 30, 50), head_rect, border_radius=15)

    core_radius = 30 + 5 * pulse
    core_alpha = 100 + int(50 * pulse)
    core_surf = pygame.Surface((core_radius * 2, core_radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(core_surf, (*NEON_BLUE, core_alpha), (core_radius, core_radius), core_radius)
    surface.blit(core_surf, (x - core_radius, y - core_radius))

    leg_positions = [
        (x - 100, y + 40),
        (x + 60, y + 40),
        (x - 110, y + 80),
        (x + 70, y + 80)
    ]

    for leg_x, leg_y in leg_positions:
        pygame.draw.rect(surface, (35, 40, 60), (leg_x - 10, leg_y, 20, 60), border_radius=5)

    if random.random() < 0.05:
        create_particles(x, y, NEON_BLUE, 3)


# Draw credits
def draw_credits(surface, scroll_offset):
    title_text = title_font.render("ROBOTS LAB GAME", True, NEON_CYAN)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100 - scroll_offset))

    glow_surf = pygame.Surface((title_rect.width + 20, title_rect.height + 20), pygame.SRCALPHA)
    pygame.draw.rect(glow_surf, (*NEON_CYAN, 80), (0, 0, title_rect.width + 20, title_rect.height + 20),
                     border_radius=15)
    surface.blit(glow_surf, (title_rect.x - 10, title_rect.y - 10))
    surface.blit(title_text, title_rect)

    subtitle_text = heading_font.render("CREDITS", True, NEON_PURPLE)
    subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 160 - scroll_offset))
    surface.blit(subtitle_text, subtitle_rect)

    y_offset = 220 - scroll_offset

    for category in CREDITS:
        category_text = heading_font.render(category["category"], True, NEON_GREEN)
        category_rect = category_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
        surface.blit(category_text, category_rect)
        y_offset += 50

        for item in category["items"]:
            item_text = regular_font.render(item, True, WHITE)
            item_rect = item_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            surface.blit(item_text, item_rect)
            y_offset += 40

        y_offset += 30

    final_y = y_offset + 50
    final_text = heading_font.render("THANK YOU FOR PLAYING!", True, NEON_YELLOW)
    final_rect = final_text.get_rect(center=(SCREEN_WIDTH // 2, final_y))

    pulse = (math.sin(pygame.time.get_ticks() / 300) + 1) / 2
    glow_alpha = int(80 + 40 * pulse)
    glow_surf = pygame.Surface((final_rect.width + 30, final_rect.height + 30), pygame.SRCALPHA)
    pygame.draw.rect(glow_surf, (*NEON_YELLOW, glow_alpha), (0, 0, final_rect.width + 30, final_rect.height + 30),
                     border_radius=20)
    surface.blit(glow_surf, (final_rect.x - 15, final_rect.y - 15))
    surface.blit(final_text, final_rect)

    return final_y + 100


# : Function to return to main menu
def return_to_main_menu():
    """Properly return to the main menu by launching main_menu.py"""
    pygame.mixer.music.stop()
    pygame.quit()

    try:
        # Get the current script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        menu_path = os.path.join(script_dir, "main_menu.py")

        print(f"Attempting to launch: {menu_path}")

        # Check if the file exists
        if os.path.exists(menu_path):
            print(f"Found main_menu.py at: {menu_path}")

            if sys.platform == "win32":
                # On Windows, use CREATE_NEW_CONSOLE flag
                subprocess.Popen([sys.executable, menu_path],
                                 creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                # On macOS/Linux
                subprocess.Popen([sys.executable, menu_path])

            print("Successfully launched main_menu.py")
        else:
            print(f"ERROR: main_menu.py not found at: {menu_path}")
            # Try alternative paths
            alt_paths = [
                os.path.join(os.getcwd(), "main_menu.py"),
                "main_menu.py"
            ]

            for alt_path in alt_paths:
                if os.path.exists(alt_path):
                    print(f"Found main_menu.py at alternative path: {alt_path}")
                    if sys.platform == "win32":
                        subprocess.Popen([sys.executable, alt_path],
                                         creationflags=subprocess.CREATE_NEW_CONSOLE)
                    else:
                        subprocess.Popen([sys.executable, alt_path])
                    break

    except Exception as e:
        print(f"ERROR launching main_menu.py: {e}")
        import traceback
        traceback.print_exc()

    sys.exit(0)


# Main function
def main():
    load_music()

    # CHANGED: Position buttons in top-left corner
    button_width, button_height = 180, 40
    button_spacing = 10

    # Position from top-left corner
    menu_button = Button(
        20,  # X position: left margin
        20,  # Y position: top margin
        button_width, button_height,
        "RETURN TO MENU", NEON_BLUE, NEON_CYAN
    )

    quit_button = Button(
        20,  # Same X position
        20 + button_height + button_spacing,  # Y position: below menu button
        button_width, button_height,
        "QUIT GAME", NEON_RED, (255, 100, 100)
    )

    scroll_offset = -SCREEN_HEIGHT
    scroll_speed = 0.5
    max_scroll = 1500
    clock = pygame.time.Clock()

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # ESC key now returns to main menu
                    return_to_main_menu()
                elif event.key == pygame.K_UP:
                    scroll_offset -= 20
                elif event.key == pygame.K_DOWN:
                    scroll_offset += 20
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_click = True
                elif event.button == 4:
                    scroll_offset -= 30
                elif event.button == 5:
                    scroll_offset += 30

        scroll_offset += scroll_speed

        # Restart credits after they've scrolled through
        if scroll_offset > max_scroll + SCREEN_HEIGHT:
            scroll_offset = -SCREEN_HEIGHT

        menu_button.check_hover(mouse_pos)
        quit_button.check_hover(mouse_pos)

        if menu_button.is_clicked(mouse_pos, mouse_click):
            print("RETURN TO MENU button clicked")
            return_to_main_menu()

        if quit_button.is_clicked(mouse_pos, mouse_click):
            running = False

        draw_grid(screen)
        draw_stars(screen)

        pulse = (math.sin(pygame.time.get_ticks() / 500) + 1) / 2
        draw_canine_silhouette(screen, 200, SCREEN_HEIGHT // 2, pulse)
        draw_canine_silhouette(screen, SCREEN_WIDTH - 200, SCREEN_HEIGHT // 2, pulse)

        final_y = draw_credits(screen, scroll_offset)

        # Always draw buttons in top-left corner
        menu_button.draw(screen)
        quit_button.draw(screen)

        # CHANGED: Move instructions to top-right corner
        instructions = small_font.render("Mouse wheel or UP/DOWN to scroll • ESC for menu", True, GRAY)
        screen.blit(instructions, (SCREEN_WIDTH - instructions.get_width() - 20, 20))  # Top-right position

        update_particles()
        draw_particles(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()