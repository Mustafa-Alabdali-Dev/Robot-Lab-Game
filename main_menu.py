import pygame
import sys
import os
import math
import random
import subprocess

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Get screen info and set to full screen
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Robotics Present")
pygame.display.set_caption("Robots Game")

# Colors
BACKGROUND = (10, 15, 25)  # Dark blue-black
DARK_BLUE = (20, 30, 50)
BLUE = (30, 80, 180)
LIGHT_BLUE = (100, 180, 255)
NEON_BLUE = (0, 150, 255)
NEON_GREEN = (0, 255, 150)
NEON_RED = (255, 50, 50)
NEON_PURPLE = (180, 70, 255)
WHITE = (240, 240, 240)
GRAY = (120, 120, 120)
BLACK = (5, 5, 10)
SILVER = (200, 200, 210)
GOLD = (255, 215, 0)

# Create fonts
title_font = pygame.font.SysFont("Arial", 120, bold=True)
subtitle_font = pygame.font.SysFont("Arial", 60, bold=True)
menu_font = pygame.font.SysFont("Arial", 48, bold=True)
button_font = pygame.font.SysFont("Arial", 32, bold=True)
button_small_font = pygame.font.SysFont("Arial", 24, bold=True)
info_font = pygame.font.SysFont("Arial", 24)

# Laser effects for robot eyes
LASER_EFFECTS = []


def create_laser_effect(start_pos, end_pos, color, duration=30):
    LASER_EFFECTS.append({
        "start_pos": start_pos,
        "end_pos": end_pos,
        "color": color,
        "life": duration,
        "max_life": duration,
        "width": 2
    })


def update_laser_effects():
    for laser in LASER_EFFECTS[:]:
        laser["life"] -= 1
        if laser["life"] <= 0:
            LASER_EFFECTS.remove(laser)


def draw_laser_effects(surface):
    for laser in LASER_EFFECTS:
        alpha = int(255 * (laser["life"] / laser["max_life"]))
        color = list(laser["color"])
        if len(color) == 3:
            color.append(alpha)
        else:
            color[3] = alpha

        # Draw laser line
        pygame.draw.line(surface, color, laser["start_pos"], laser["end_pos"], laser["width"])

        # Draw glow effect
        glow_surf = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
        for i in range(3):
            glow_width = laser["width"] + i * 2
            glow_color = list(color)
            glow_color[3] = alpha // (i + 2)
            pygame.draw.line(glow_surf, glow_color, laser["start_pos"], laser["end_pos"], glow_width)
        surface.blit(glow_surf, (0, 0))


# Button class with improved text rendering and maximum spacing
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, level_text=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.level_text = level_text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.is_hovered = False

    def draw(self, surface):
        # Draw button with rounded corners
        pygame.draw.rect(surface, self.current_color, self.rect, border_radius=15)
        pygame.draw.rect(surface, WHITE, self.rect, 3, border_radius=15)

        # Draw main button text - MOVED UP SIGNIFICANTLY
        text_surf = button_font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        # Adjust vertical position if there's level text - MOVED UP MORE
        if self.level_text:
            text_rect.y = self.rect.centery - 30  # Changed from -18 to -30 (moved way up)
        surface.blit(text_surf, text_rect)

        # Draw level text if provided - MOVED DOWN SIGNIFICANTLY
        if self.level_text:
            level_surf = button_small_font.render(self.level_text, True, SILVER)
            level_rect = level_surf.get_rect(center=(self.rect.centerx, self.rect.centery + 30))  # Changed from +18 to +30 (moved way down)
            surface.blit(level_surf, level_rect)

        # Draw glow effect when hovered
        if self.is_hovered:
            glow_rect = self.rect.inflate(20, 20)
            s = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(s, (*self.hover_color[:3], 80), (0, 0, glow_rect.width, glow_rect.height),
                             border_radius=25)
            surface.blit(s, glow_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        self.current_color = self.hover_color if self.is_hovered else self.color
        return self.is_hovered

    def is_clicked(self, pos, click):
        return self.rect.collidepoint(pos) and click


# Particle system for background effects
PARTICLES = []


def create_particle(x, y, color, speed=2, size=3, life=60):
    angle = math.radians(pygame.time.get_ticks() % 360)
    PARTICLES.append({
        'x': x, 'y': y,
        'vx': math.cos(angle) * speed * (0.5 + (pygame.time.get_ticks() % 100) / 100),
        'vy': math.sin(angle) * speed * (0.5 + (pygame.time.get_ticks() % 100) / 100),
        'color': color,
        'size': size,
        'life': life,
        'max_life': life
    })


def update_particles():
    for particle in PARTICLES[:]:
        particle['x'] += particle['vx']
        particle['y'] += particle['vy']
        particle['life'] -= 1
        if particle['life'] <= 0:
            PARTICLES.remove(particle)


def draw_particles(surface):
    for particle in PARTICLES:
        alpha = int(255 * (particle['life'] / particle['max_life']))
        size = particle['size'] * (particle['life'] / particle['max_life'])
        color = list(particle['color'])
        if len(color) == 3:
            color.append(alpha)

        s = pygame.Surface((int(size * 2), int(size * 2)), pygame.SRCALPHA)
        pygame.draw.circle(s, color, (int(size), int(size)), int(size))
        surface.blit(s, (particle['x'] - size, particle['y'] - size))


# Text spark system for title text
TEXT_SPARKS = []


def create_text_spark(x, y, text_width, text_height, color, speed=1.5, size=2, life=40):
    # Create sparks that move around the perimeter of text
    side = random.randint(0, 3)  # 0: top, 1: right, 2: bottom, 3: left

    if side == 0:  # Top
        spark_x = x + random.randint(0, text_width)
        spark_y = y
        vx = random.uniform(-0.5, 0.5)
        vy = random.uniform(0.2, 1.0)
    elif side == 1:  # Right
        spark_x = x + text_width
        spark_y = y + random.randint(0, text_height)
        vx = random.uniform(-1.0, -0.2)
        vy = random.uniform(-0.5, 0.5)
    elif side == 2:  # Bottom
        spark_x = x + random.randint(0, text_width)
        spark_y = y + text_height
        vx = random.uniform(-0.5, 0.5)
        vy = random.uniform(-1.0, -0.2)
    else:  # Left
        spark_x = x
        spark_y = y + random.randint(0, text_height)
        vx = random.uniform(0.2, 1.0)
        vy = random.uniform(-0.5, 0.5)

    TEXT_SPARKS.append({
        'x': spark_x, 'y': spark_y,
        'vx': vx * speed, 'vy': vy * speed,
        'color': color,
        'size': size,
        'life': life,
        'max_life': life
    })


def update_text_sparks():
    for spark in TEXT_SPARKS[:]:
        spark['x'] += spark['vx']
        spark['y'] += spark['vy']
        spark['life'] -= 1
        if spark['life'] <= 0:
            TEXT_SPARKS.remove(spark)


def draw_text_sparks(surface):
    for spark in TEXT_SPARKS:
        alpha = int(255 * (spark['life'] / spark['max_life']))
        size = spark['size'] * (spark['life'] / spark['max_life'])
        color = list(spark['color'])
        if len(color) == 3:
            color.append(alpha)

        s = pygame.Surface((int(size * 2), int(size * 2)), pygame.SRCALPHA)
        pygame.draw.circle(s, color, (int(size), int(size)), int(size))
        surface.blit(s, (spark['x'] - size, spark['y'] - size))


# Create background stars
STARS = []
for _ in range(200):
    STARS.append({
        'x': pygame.time.get_ticks() % SCREEN_WIDTH + (pygame.time.get_ticks() % 1000),
        'y': pygame.time.get_ticks() % SCREEN_HEIGHT + (pygame.time.get_ticks() % 800),
        'size': (pygame.time.get_ticks() % 3) + 1,
        'brightness': (pygame.time.get_ticks() % 100) / 100,
        'speed': 0.1 + (pygame.time.get_ticks() % 100) / 500
    })


def update_stars():
    for star in STARS:
        star['x'] -= star['speed']
        star['brightness'] = 0.3 + 0.7 * (math.sin(pygame.time.get_ticks() / 1000 + star['x']) + 1) / 2
        if star['x'] < -10:
            star['x'] = SCREEN_WIDTH + 10
            star['y'] = pygame.time.get_ticks() % SCREEN_HEIGHT


def draw_stars(surface):
    for star in STARS:
        brightness = int(255 * star['brightness'])
        color = (brightness, brightness, brightness)
        pygame.draw.circle(surface, color, (int(star['x']), int(star['y'])), star['size'])


# Draw circuit board background pattern
def draw_circuit_background(surface):
    # Draw circuit lines
    line_color = (0, 80, 160, 50)
    for i in range(0, SCREEN_WIDTH, 40):
        pygame.draw.line(surface, line_color, (i, 0), (i, SCREEN_HEIGHT), 1)
    for i in range(0, SCREEN_HEIGHT, 40):
        pygame.draw.line(surface, line_color, (0, i), (SCREEN_WIDTH, i), 1)

    # Draw circuit nodes
    node_color = (0, 120, 255, 80)
    for x in range(50, SCREEN_WIDTH, 80):
        for y in range(50, SCREEN_HEIGHT, 80):
            if (x + y) % 160 == 0:  # Create pattern
                pygame.draw.circle(surface, node_color, (x, y), 3)


# Enhanced 3D robot drawing with realistic effects
def draw_robot_silhouette(surface, time):
    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2 - 100

    # 3D Robot Body with perspective
    body_width = 200
    body_height = 160
    body_depth = 60

    # Calculate perspective points for 3D box
    perspective = 0.3  # Perspective factor

    # Front face (main body)
    body_front = pygame.Rect(center_x - body_width // 2, center_y - body_height // 2, body_width, body_height)

    # Back face (shifted for perspective)
    back_offset = body_depth * perspective
    body_back = pygame.Rect(center_x - body_width // 2 + back_offset, center_y - body_height // 2 + back_offset,
                            body_width, body_height)

    # Draw 3D body with gradient for depth
    for i in range(body_height):
        # Front face gradient (brighter)
        front_shade = 30 + (i / body_height) * 40
        front_color = (front_shade, front_shade + 20, front_shade + 40)
        pygame.draw.line(surface, front_color,
                         (body_front.x, body_front.y + i),
                         (body_front.x + body_front.width, body_front.y + i))

    # Draw side panels for 3D effect
    side_color = (20, 35, 70)
    for i in range(body_depth):
        # Right side
        x_pos = body_front.x + body_front.width + i * perspective
        y_start = body_front.y + i * perspective
        y_end = body_front.y + body_front.height + i * perspective

        # Gradient for side
        shade = 20 + (i / body_depth) * 20
        side_shade_color = (side_color[0] + shade, side_color[1] + shade, side_color[2] + shade)

        pygame.draw.line(surface, side_shade_color,
                         (x_pos, y_start),
                         (x_pos, y_end), 2)

        # Bottom side
        if i < body_depth // 2:  # Only draw partial bottom for visual clarity
            bottom_y = body_front.y + body_front.height + i * perspective
            pygame.draw.line(surface, side_shade_color,
                             (body_front.x + i * perspective, bottom_y),
                             (body_front.x + body_front.width + i * perspective, bottom_y), 2)

    # Add 3D body panels and details
    pygame.draw.rect(surface, (30, 60, 110), body_front, 3, border_radius=15)

    # Shoulder joints with 3D effect
    shoulder_depth = 10
    left_shoulder_front = (center_x - 100, center_y - 10)
    left_shoulder_back = (center_x - 100 + shoulder_depth * perspective, center_y - 10 + shoulder_depth * perspective)

    right_shoulder_front = (center_x + 100, center_y - 10)
    right_shoulder_back = (center_x + 100 + shoulder_depth * perspective, center_y - 10 + shoulder_depth * perspective)

    # Draw 3D shoulder joints
    pygame.draw.circle(surface, (70, 100, 150), left_shoulder_front, 15)
    pygame.draw.circle(surface, (50, 80, 130), left_shoulder_back, 12)

    pygame.draw.circle(surface, (70, 100, 150), right_shoulder_front, 15)
    pygame.draw.circle(surface, (50, 80, 130), right_shoulder_back, 12)

    # Body panel lines with depth
    for i in range(1, 3):
        panel_y = body_front.y + (body_front.height // 3) * i
        # Front panel line
        pygame.draw.line(surface, (30, 60, 110),
                         (body_front.x + 10, panel_y),
                         (body_front.x + body_front.width - 10, panel_y), 2)
        # Back panel line (lighter)
        back_panel_y = panel_y + back_offset
        pygame.draw.line(surface, (40, 70, 120),
                         (body_back.x + 10, back_panel_y),
                         (body_back.x + body_back.width - 10, back_panel_y), 1)

    # 3D Robot Head
    head_width = 120
    head_height = 80
    head_depth = 30

    head_front = pygame.Rect(center_x - head_width // 2, center_y - body_height // 2 - head_height + 20, head_width,
                             head_height)
    head_back = pygame.Rect(center_x - head_width // 2 + head_depth * perspective,
                            center_y - body_height // 2 - head_height + 20 + head_depth * perspective,
                            head_width, head_height)

    # Draw 3D head with gradient
    for i in range(head_height):
        shade = 40 + (i / head_height) * 30
        color = (shade, shade + 30, shade + 50)
        pygame.draw.line(surface, color,
                         (head_front.x, head_front.y + i),
                         (head_front.x + head_front.width, head_front.y + i))

    # Draw head sides for 3D
    for i in range(head_depth):
        x_pos = head_front.x + head_front.width + i * perspective
        y_start = head_front.y + i * perspective
        y_end = head_front.y + head_front.height + i * perspective

        shade = 30 + (i / head_depth) * 20
        side_color = (shade, shade + 20, shade + 30)

        pygame.draw.line(surface, side_color, (x_pos, y_start), (x_pos, y_end), 2)

    pygame.draw.rect(surface, (40, 80, 130), head_front, 3, border_radius=12)

    # Head details with depth
    detail_rect = pygame.Rect(head_front.x + 10, head_front.y + 10, head_front.width - 20, 15)
    pygame.draw.rect(surface, (30, 60, 110), detail_rect, border_radius=5)

    # 3D Animated Eyes with realistic lens effect
    eye_y = center_y - 130
    left_eye_x = center_x - 25
    right_eye_x = center_x + 25

    # Eye pulse effect
    pulse = (math.sin(time / 200) + 1) / 2
    eye_size = 12 + int(6 * pulse)
    eye_depth = 8

    # Draw 3D eye sockets
    for depth in range(eye_depth, 0, -1):
        alpha = 100 - (depth * 10)
        size = eye_size + depth

        # Left eye socket
        eye_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(eye_surf, (20, 30, 60, alpha), (size, size), size)
        surface.blit(eye_surf, (left_eye_x - size, eye_y - size))

        # Right eye socket
        eye_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(eye_surf, (20, 30, 60, alpha), (size, size), size)
        surface.blit(eye_surf, (right_eye_x - size, eye_y - size))

    # Draw 3D eye lenses with gradient and depth
    for i in range(eye_size):
        intensity = 1.0 - (i / eye_size) * 0.5
        eye_color = (int(100 * intensity * pulse),
                     int(150 * intensity * pulse),
                     int(255 * intensity))

        # Main eye sphere
        pygame.draw.circle(surface, eye_color, (left_eye_x, eye_y), eye_size - i)
        pygame.draw.circle(surface, eye_color, (right_eye_x, eye_y), eye_size - i)

        # Add depth with highlight
        if i == eye_size // 2:
            highlight_color = (min(255, eye_color[0] + 50),
                               min(255, eye_color[1] + 50),
                               min(255, eye_color[2] + 50))
            highlight_size = max(2, (eye_size - i) // 3)
            pygame.draw.circle(surface, highlight_color,
                               (left_eye_x - 3, eye_y - 3), highlight_size)
            pygame.draw.circle(surface, highlight_color,
                               (right_eye_x - 3, eye_y - 3), highlight_size)

    # Create eye glow effect with depth
    glow_alpha = int(80 + 40 * pulse)
    glow_size = eye_size + 8

    for glow in range(3):
        current_glow_size = glow_size + glow * 3
        current_alpha = glow_alpha // (glow + 2)

        glow_surf = pygame.Surface((current_glow_size * 2, current_glow_size * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (100, 150, 255, current_alpha),
                           (current_glow_size, current_glow_size), current_glow_size)

        surface.blit(glow_surf, (left_eye_x - current_glow_size, eye_y - current_glow_size))
        surface.blit(glow_surf, (right_eye_x - current_glow_size, eye_y - current_glow_size))

    # Create occasional 3D eye beams
    if random.random() < 0.02:
        beam_length = 100 + random.randint(0, 50)
        beam_angle = random.uniform(-0.3, 0.3)
        beam_height = random.uniform(-0.1, 0.1)

        # Left eye beam with perspective
        beam_start = (left_eye_x, eye_y)
        beam_end = (
            left_eye_x + beam_length * math.cos(beam_angle),
            eye_y + beam_length * math.sin(beam_angle) + beam_length * beam_height
        )
        create_laser_effect(beam_start, beam_end, (100, 150, 255), 30)

        # Right eye beam with perspective
        beam_start = (right_eye_x, eye_y)
        beam_end = (
            right_eye_x + beam_length * math.cos(beam_angle),
            eye_y + beam_length * math.sin(beam_angle) + beam_length * beam_height
        )
        create_laser_effect(beam_start, beam_end, (100, 150, 255), 30)

    # 3D Robot Arms with proper joints and perspective
    arm_angle = math.sin(time / 300) * 0.5
    arm_swing = math.sin(time / 500) * 0.2

    # Left arm with 3D joints
    left_shoulder_3d = (center_x - 100, center_y - 10)
    left_elbow = (
        center_x - 100 - 60 * math.cos(arm_angle),
        center_y - 10 + 60 * math.sin(arm_angle) + arm_swing * 20
    )
    left_wrist = (
        left_elbow[0] - 45 * math.cos(arm_angle + 0.3),
        left_elbow[1] + 45 * math.sin(arm_angle + 0.3) + arm_swing * 10
    )

    # Right arm with 3D joints
    right_shoulder_3d = (center_x + 100, center_y - 10)
    right_elbow = (
        center_x + 100 + 60 * math.cos(arm_angle),
        center_y - 10 + 60 * math.sin(arm_angle) + arm_swing * 20
    )
    right_wrist = (
        right_elbow[0] + 45 * math.cos(arm_angle + 0.3),
        right_elbow[1] + 45 * math.sin(arm_angle + 0.3) + arm_swing * 10
    )

    # Draw 3D arms with cylindrical effect
    def draw_3d_arm(start, end, width, color1, color2):
        # Calculate arm direction
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        length = math.sqrt(dx * dx + dy * dy)

        if length == 0:
            return

        # Normalize
        dx, dy = dx / length, dy / length

        # Calculate perpendicular
        px, py = -dy, dx

        # Draw arm with gradient for 3D effect
        for i in range(width):
            offset = i - width // 2
            start_point = (start[0] + px * offset, start[1] + py * offset)
            end_point = (end[0] + px * offset, end[1] + py * offset)

            # Gradient from center to edges
            if abs(offset) < width // 3:
                color = color1
            else:
                color = color2

            pygame.draw.line(surface, color, start_point, end_point, 2)

    # Draw arms with 3D effect
    draw_3d_arm(left_shoulder_3d, left_elbow, 12, (50, 90, 150), (30, 60, 110))
    draw_3d_arm(left_elbow, left_wrist, 10, (45, 85, 140), (25, 55, 100))
    draw_3d_arm(right_shoulder_3d, right_elbow, 12, (50, 90, 150), (30, 60, 110))
    draw_3d_arm(right_elbow, right_wrist, 10, (45, 85, 140), (25, 55, 100))

    # Draw 3D elbow joints with depth
    elbow_size = 10
    for depth in range(3):
        size = elbow_size - depth * 2
        alpha = 200 - depth * 60

        # Left elbow
        elbow_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(elbow_surf, (70, 110, 170, alpha), (size, size), size)
        surface.blit(elbow_surf, (int(left_elbow[0]) - size, int(left_elbow[1]) - size))

        # Right elbow
        elbow_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(elbow_surf, (70, 110, 170, alpha), (size, size), size)
        surface.blit(elbow_surf, (int(right_elbow[0]) - size, int(right_elbow[1]) - size))

    # Draw 3D hands
    hand_size = 8
    for depth in range(2):
        size = hand_size - depth * 2

        # Left hand
        hand_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(hand_surf, (60, 100, 160, 200 - depth * 80), (size, size), size)
        surface.blit(hand_surf, (int(left_wrist[0]) - size, int(left_wrist[1]) - size))

        # Right hand
        hand_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(hand_surf, (60, 100, 160, 200 - depth * 80), (size, size), size)
        surface.blit(hand_surf, (int(right_wrist[0]) - size, int(right_wrist[1]) - size))

    # Create 3D electric sparks around the robot
    if random.random() < 0.3:
        # 3D spark locations around robot body
        spark_locations_3d = [
            (center_x - 90, center_y - 70, 0),  # Left shoulder front
            (center_x + 90, center_y - 70, 0),  # Right shoulder front
            (center_x - 90 + back_offset, center_y - 70 + back_offset, back_offset),  # Left shoulder back
            (center_x + 90 + back_offset, center_y - 70 + back_offset, back_offset),  # Right shoulder back
            (center_x - 60, center_y + 50, 0),  # Left hip front
            (center_x + 60, center_y + 50, 0),  # Right hip front
            (center_x - 25, center_y - 150, 0),  # Left side of head
            (center_x + 25, center_y - 150, 0),  # Right side of head
        ]

        spark_pos_3d = random.choice(spark_locations_3d)
        spark_x, spark_y, spark_z = spark_pos_3d

        # Adjust spark position based on depth
        spark_x += spark_z * perspective
        spark_y += spark_z * perspective

        # Create electric spark particles with 3D spread
        for _ in range(3):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(5, 25)
            height = random.uniform(-10, 10)

            spark_x_final = spark_x + math.cos(angle) * distance
            spark_y_final = spark_y + math.sin(angle) * distance + height

            # Electric spark color (blue-white)
            spark_color = (random.randint(150, 255),
                           random.randint(180, 255),
                           255)

            create_particle(spark_x_final, spark_y_final, spark_color,
                            speed=random.uniform(1, 4),
                            size=random.uniform(1, 3),
                            life=random.randint(10, 40))

    # Add 3D robotic details - bolts/screws with depth
    bolt_positions = [
        (center_x - 80, center_y - 60, 0),
        (center_x + 80, center_y - 60, 0),
        (center_x - 80 + back_offset, center_y - 60 + back_offset, back_offset),
        (center_x + 80 + back_offset, center_y - 60 + back_offset, back_offset),
        (center_x - 40, center_y - 140, 0),
        (center_x + 40, center_y - 140, 0)
    ]

    for bolt_x, bolt_y, bolt_z in bolt_positions:
        # Adjust position based on depth
        draw_x = bolt_x + bolt_z * perspective
        draw_y = bolt_y + bolt_z * perspective

        # Draw bolt with 3D effect (smaller when farther)
        size = max(2, 3 - bolt_z * 0.1)
        pygame.draw.circle(surface, (90, 120, 160), (int(draw_x), int(draw_y)), int(size))
        pygame.draw.circle(surface, (130, 160, 200), (int(draw_x), int(draw_y)), max(1, int(size * 0.5)))

    # Create 3D energy core glow in chest
    core_pulse = (math.sin(time / 250) + 1) / 2
    core_x = center_x
    core_y = center_y

    # Draw 3D energy core with multiple layers
    core_layers = [
        (20, 100, 150, 255, core_pulse * 0.8),  # Outer glow
        (15, 80, 120, 200, core_pulse * 0.9),  # Middle glow
        (10, 60, 90, 150, core_pulse)  # Inner core
    ]

    for size, (r, g, b, a, intensity) in enumerate(core_layers):
        core_size = 20 - size * 5
        current_alpha = int(a * intensity)

        core_surf = pygame.Surface((core_size * 2, core_size * 2), pygame.SRCALPHA)
        pygame.draw.circle(core_surf, (r, g, b, current_alpha), (core_size, core_size), core_size)
        surface.blit(core_surf, (core_x - core_size, core_y - core_size))

    # Core details with 3D effect
    pygame.draw.circle(surface, (70, 120, 200), (core_x, core_y), 8)
    pygame.draw.circle(surface, (120, 200, 255), (core_x, core_y), 4)

    # Add core reflection to body
    reflection_alpha = int(40 * core_pulse)
    reflection_surf = pygame.Surface((60, 40), pygame.SRCALPHA)
    pygame.draw.ellipse(reflection_surf, (150, 200, 255, reflection_alpha), (0, 0, 60, 40))
    surface.blit(reflection_surf, (core_x - 30, core_y - 50))


# Animated plus sign class
class AnimatedPlus:
    def __init__(self, x, y, size=30, thickness=6, color=GOLD):
        self.x = x
        self.y = y
        self.size = size
        self.thickness = thickness
        self.color = color
        self.animation_time = 0
        self.rotation_angle = 0
        self.scale_factor = 1.0

    def update(self, time):
        self.animation_time = time
        # Rotate slowly
        self.rotation_angle = math.sin(time / 800) * 10  # ±10 degrees
        # Pulse scale
        self.scale_factor = 1.0 + 0.2 * math.sin(time / 500)

    def draw(self, surface):
        # Create a surface for the plus sign
        plus_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)

        # Calculate scaled size
        scaled_size = int(self.size * self.scale_factor)
        scaled_thickness = int(self.thickness * self.scale_factor)

        # Draw horizontal line (centered)
        h_line_rect = pygame.Rect(
            self.size - scaled_size // 2,
            self.size - scaled_thickness // 2,
            scaled_size,
            scaled_thickness
        )
        pygame.draw.rect(plus_surface, self.color, h_line_rect, border_radius=scaled_thickness // 2)

        # Draw vertical line (centered)
        v_line_rect = pygame.Rect(
            self.size - scaled_thickness // 2,
            self.size - scaled_size // 2,
            scaled_thickness,
            scaled_size
        )
        pygame.draw.rect(plus_surface, self.color, v_line_rect, border_radius=scaled_thickness // 2)

        # Rotate the plus sign
        rotated_plus = pygame.transform.rotate(plus_surface, self.rotation_angle)
        rotated_rect = rotated_plus.get_rect(center=(self.x, self.y))

        # Draw glow effect
        glow_alpha = int(100 + 100 * math.sin(self.animation_time / 350))
        glow_surface = pygame.Surface((scaled_size * 2, scaled_size * 2), pygame.SRCALPHA)
        pygame.draw.rect(glow_surface, (*self.color[:3], glow_alpha),
                         (scaled_size - scaled_size // 2 - 5, scaled_size - scaled_thickness // 2 - 5,
                          scaled_size + 10, scaled_thickness + 10), border_radius=scaled_thickness // 2 + 2)
        pygame.draw.rect(glow_surface, (*self.color[:3], glow_alpha),
                         (scaled_size - scaled_thickness // 2 - 5, scaled_size - scaled_size // 2 - 5,
                          scaled_thickness + 10, scaled_size + 10), border_radius=scaled_thickness // 2 + 2)

        rotated_glow = pygame.transform.rotate(glow_surface, self.rotation_angle)
        glow_rect = rotated_glow.get_rect(center=(self.x, self.y))
        surface.blit(rotated_glow, glow_rect)

        # Draw the plus sign
        surface.blit(rotated_plus, rotated_rect)


# Animated text character class
class AnimatedChar:
    def __init__(self, char, x, y, color, font, delay=0):
        self.char = char
        self.x = x
        self.y = y
        self.color = color
        self.font = font
        self.delay = delay
        self.animation_time = 0
        self.scale = 1.0
        self.y_offset = 0

    def update(self, time):
        self.animation_time = time + self.delay
        # Bounce effect
        bounce = math.sin(self.animation_time / 300) * 5
        self.y_offset = bounce
        # Scale effect
        self.scale = 1.0 + 0.1 * math.sin(self.animation_time / 400)

    def draw(self, surface):
        # Render character
        char_surf = self.font.render(self.char, True, self.color)

        # Apply scale
        if self.scale != 1.0:
            new_width = int(char_surf.get_width() * self.scale)
            new_height = int(char_surf.get_height() * self.scale)
            scaled_surf = pygame.transform.scale(char_surf, (new_width, new_height))
            char_rect = scaled_surf.get_rect(center=(self.x, self.y + self.y_offset))
            surface.blit(scaled_surf, char_rect)
        else:
            char_rect = char_surf.get_rect(center=(self.x, self.y + self.y_offset))
            surface.blit(char_surf, char_rect)

        # Add glow effect
        glow_alpha = int(100 + 100 * math.sin(self.animation_time / 250))
        glow_surf = pygame.Surface(char_surf.get_size(), pygame.SRCALPHA)
        glow_text = self.font.render(self.char, True, (*self.color[:3], glow_alpha))
        glow_surf.blit(glow_text, (0, 0))

        if self.scale != 1.0:
            new_width = int(glow_surf.get_width() * self.scale)
            new_height = int(glow_surf.get_height() * self.scale)
            scaled_glow = pygame.transform.scale(glow_surf, (new_width, new_height))
            surface.blit(scaled_glow, char_rect)
        else:
            surface.blit(glow_surf, char_rect)


# Create animated elements
animated_chars = []
animated_pluses = []

# Initialize animated plus signs
plus1 = AnimatedPlus(0, 0)  # Position will be set in draw_title
plus2 = AnimatedPlus(0, 0)  # Position will be set in draw_title
animated_pluses.append(plus1)
animated_pluses.append(plus2)

# Store title text positions for spark effects
title_text_positions = {
    "robotics_present": {"x": 0, "y": 0, "width": 0, "height": 0},
    "robots_game": {"x": 0, "y": 0, "width": 0, "height": 0}
}


# Draw the main title with special effects
def draw_title(surface, time):
    center_x = SCREEN_WIDTH // 2

    # First line: "ROBOTICS PRESENT"
    # Draw "ROBOTICS" with "ROBOT" in blue and "ICS" in green
    robotics_text = "ROBOTICS"
    robot_part = "ROBOT"
    ics_part = "ICS"

    # Calculate positions for ROBOTICS
    robot_width = title_font.size(robot_part)[0]
    ics_width = title_font.size(ics_part)[0]
    total_robotics_width = robot_width + ics_width

    # Draw "PRESENT" text
    present_text = "PRESENT"
    present_width = title_font.size(present_text)[0]

    # Calculate total width for first line
    plus_size = 30
    plus_spacing = 20
    total_first_line_width = total_robotics_width + plus_size + plus_spacing + present_width

    # Starting position for first line
    first_line_x = center_x - total_first_line_width // 2
    first_line_y = 100

    # Store position for spark effects
    title_text_positions["robotics_present"]["x"] = first_line_x
    title_text_positions["robotics_present"]["y"] = first_line_y
    title_text_positions["robotics_present"]["width"] = total_first_line_width
    title_text_positions["robotics_present"]["height"] = title_font.get_height()

    # Draw "ROBOT" in gradient blue with animation
    robot_x = first_line_x
    for i, char in enumerate(robot_part):
        char_x = robot_x + title_font.size(robot_part[:i])[0] + title_font.size(char)[0] // 2
        char_y = first_line_y + title_font.get_height() // 2

        # Create animated character
        anim_char = AnimatedChar(char, char_x, char_y, NEON_BLUE, title_font, i * 100)
        anim_char.update(time)
        anim_char.draw(surface)

    # Draw "ICS" in gradient green with animation
    ics_x = robot_x + robot_width
    for i, char in enumerate(ics_part):
        char_x = ics_x + title_font.size(ics_part[:i])[0] + title_font.size(char)[0] // 2
        char_y = first_line_y + title_font.get_height() // 2

        # Create animated character
        anim_char = AnimatedChar(char, char_x, char_y, NEON_GREEN, title_font, (i + len(robot_part)) * 100)
        anim_char.update(time)
        anim_char.draw(surface)

    # Draw plus sign between ROBOTICS and PRESENT
    plus_x = ics_x + ics_width + plus_spacing // 2
    plus_y = first_line_y + title_font.get_height() // 2

    # Update and draw animated plus
    plus1.x = plus_x
    plus1.y = plus_y
    plus1.update(time)
    plus1.draw(surface)

    # Draw "PRESENT" with animation
    present_x = plus_x + plus_size // 2 + plus_spacing // 2
    for i, char in enumerate(present_text):
        char_x = present_x + title_font.size(present_text[:i])[0] + title_font.size(char)[0] // 2
        char_y = first_line_y + title_font.get_height() // 2

        # Create animated character
        anim_char = AnimatedChar(char, char_x, char_y, NEON_PURPLE, title_font, (i + len(robotics_text)) * 80)
        anim_char.update(time)
        anim_char.draw(surface)

    # Second line: "ROBOTS GAME"
    # Draw "ROBOTS" with "ROBOT" in blue and "S" in green
    robots_text = "ROBOTS"
    robot_part2 = "ROBOT"
    s_part = "S"

    # Calculate positions for ROBOTS
    robot_width2 = title_font.size(robot_part2)[0]
    s_width = title_font.size(s_part)[0]
    total_robots_width = robot_width2 + s_width

    # Draw "GAME" text
    game_text = "GAME"
    game_width = title_font.size(game_text)[0]

    # Calculate total width for second line
    total_second_line_width = total_robots_width + plus_size + plus_spacing + game_width

    # Starting position for second line
    second_line_x = center_x - total_second_line_width // 2
    second_line_y = first_line_y + title_font.get_height() + 40  # Increased spacing

    # Store position for spark effects
    title_text_positions["robots_game"]["x"] = second_line_x
    title_text_positions["robots_game"]["y"] = second_line_y
    title_text_positions["robots_game"]["width"] = total_second_line_width
    title_text_positions["robots_game"]["height"] = title_font.get_height()

    # Draw "ROBOT" in gradient blue with animation
    robot_x2 = second_line_x
    for i, char in enumerate(robot_part2):
        char_x = robot_x2 + title_font.size(robot_part2[:i])[0] + title_font.size(char)[0] // 2
        char_y = second_line_y + title_font.get_height() // 2

        # Create animated character
        anim_char = AnimatedChar(char, char_x, char_y, NEON_BLUE, title_font, i * 120)
        anim_char.update(time)
        anim_char.draw(surface)

    # Draw "S" in gradient green with animation
    s_x = robot_x2 + robot_width2
    char_x = s_x + title_font.size(s_part)[0] // 2
    char_y = second_line_y + title_font.get_height() // 2

    # Create animated character
    anim_char = AnimatedChar(s_part, char_x, char_y, NEON_GREEN, title_font, len(robot_part2) * 120)
    anim_char.update(time)
    anim_char.draw(surface)

    # Draw plus sign between ROBOTS and GAME
    plus_x2 = s_x + s_width + plus_spacing // 2
    plus_y2 = second_line_y + title_font.get_height() // 2

    # Update and draw animated plus
    plus2.x = plus_x2
    plus2.y = plus_y2
    plus2.update(time)
    plus2.draw(surface)

    # Draw "GAME" with animation
    game_x = plus_x2 + plus_size // 2 + plus_spacing // 2
    for i, char in enumerate(game_text):
        char_x = game_x + title_font.size(game_text[:i])[0] + title_font.size(char)[0] // 2
        char_y = second_line_y + title_font.get_height() // 2

        # Create animated character
        anim_char = AnimatedChar(char, char_x, char_y, NEON_PURPLE, title_font, (i + len(robots_text)) * 100)
        anim_char.update(time)
        anim_char.draw(surface)


# Create buttons with improved text layout and maximum spacing
button_width, button_height = 350, 90
button_x = SCREEN_WIDTH // 2 - button_width // 2
button_spacing = 110

# Create buttons with cleaner text and maximum spaced level indicators
snowbot_button = Button(button_x, 480, button_width, button_height, "SNOWER GAME", (40, 120, 200), (80, 160, 255),
                        "Level 1")
drone_button = Button(button_x, 480 + button_spacing, button_width, button_height, "DRONE GAME", (40, 180, 80),
                      (80, 220, 120), "Level 2")
dogbot_button = Button(button_x, 480 + button_spacing * 2, button_width, button_height, "DOGROBOT GAME", (180, 70, 180),
                       (220, 100, 220), "Level 3")
credit_button = Button(button_x, 480 + button_spacing * 3, button_width, button_height, "CREDITS", (150, 70, 150),
                      (200, 100, 200))
quit_button = Button(button_x, 480 + button_spacing * 4, button_width, button_height, "QUIT", (180, 60, 60),
                     (255, 100, 100))


# Sound effects (placeholder - you can add actual sound files)
def play_button_hover_sound():
    print("Button hover sound")
    # pygame.mixer.Sound("hover.wav").play()


def play_button_click_sound():
    print("Button click sound")
    # pygame.mixer.Sound("click.wav").play()


# Background music - UPDATED: Load and play robot-art.mp3
def play_background_music():
    print("Starting background music")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    music_path = os.path.join(script_dir, "robot-art.mp3")

    try:
        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.5)  # Set volume to 50%
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
            print("Music loaded successfully: robot-art.mp3")
        else:
            print(f"Music file not found at: {music_path}")
            # Try alternative paths
            alternative_paths = [
                os.path.join(script_dir, "music", "robot-art.mp3"),
                os.path.join(script_dir, "sounds", "robot-art.mp3"),
                os.path.join(script_dir, "assets", "robot-art.mp3")
            ]
            for alt_path in alternative_paths:
                if os.path.exists(alt_path):
                    pygame.mixer.music.load(alt_path)
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)
                    print(f"Music loaded from alternative path: {alt_path}")
                    break
            else:
                print("Could not find robot-art.mp3 in any expected location")
    except Exception as e:
        print(f"Error loading music: {e}")


# Launch game functions
def launch_snowbot_game():
    # Stop music before launching game
    pygame.mixer.music.stop()
    pygame.quit()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    game_path = os.path.join(script_dir, "snowbot_game.py")

    try:
        if sys.platform == "win32":
            subprocess.Popen([sys.executable, game_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen([sys.executable, game_path])
    except Exception as e:
        print(f"Failed to launch game: {e}")

    sys.exit()


def launch_drone_game():
    # Stop music before launching game
    pygame.mixer.music.stop()
    pygame.quit()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    game_path = os.path.join(script_dir, "drone_game.py")

    try:
        if sys.platform == "win32":
            subprocess.Popen([sys.executable, game_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen([sys.executable, game_path])
    except Exception as e:
        print(f"Failed to launch game: {e}")

    sys.exit()


def launch_dogbot_game():
    # Stop music before launching game
    pygame.mixer.music.stop()
    pygame.quit()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    game_path = os.path.join(script_dir, "dogbot_game.py")

    try:
        if sys.platform == "win32":
            subprocess.Popen([sys.executable, game_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen([sys.executable, game_path])
    except Exception as e:
        print(f"Failed to launch game: {e}")

    sys.exit()


# NEW FUNCTION: Launch credit script
def launch_credit_game():
    # Stop music before launching credit
    pygame.mixer.music.stop()
    pygame.quit()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    credit_path = os.path.join(script_dir, "credit.py")

    try:
        if sys.platform == "win32":
            subprocess.Popen([sys.executable, credit_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen([sys.executable, credit_path])
    except Exception as e:
        print(f"Failed to launch credit: {e}")

    sys.exit()


# Music control button class
class MusicButton:
    def __init__(self, x, y, size=40):
        self.rect = pygame.Rect(x, y, size, size)
        self.is_muted = False
        self.is_hovered = False

    def draw(self, surface):
        # Draw button background
        color = (100, 100, 100, 180) if self.is_hovered else (60, 60, 60, 180)
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=8)

        # Draw speaker icon
        if self.is_muted:
            # Muted speaker (X through speaker)
            pygame.draw.polygon(surface, WHITE, [
                (self.rect.centerx - 8, self.rect.centery - 6),
                (self.rect.centerx - 3, self.rect.centery - 1),
                (self.rect.centerx + 2, self.rect.centery - 6),
                (self.rect.centerx + 7, self.rect.centery - 1),
                (self.rect.centerx + 2, self.rect.centery + 4),
                (self.rect.centerx - 3, self.rect.centery + 9),
                (self.rect.centerx - 8, self.rect.centery + 4)
            ])
            # Draw X over speaker
            pygame.draw.line(surface, NEON_RED,
                             (self.rect.centerx - 10, self.rect.centery - 10),
                             (self.rect.centerx + 10, self.rect.centery + 10), 3)
            pygame.draw.line(surface, NEON_RED,
                             (self.rect.centerx + 10, self.rect.centery - 10),
                             (self.rect.centerx - 10, self.rect.centery + 10), 3)
        else:
            # Normal speaker
            pygame.draw.polygon(surface, WHITE, [
                (self.rect.centerx - 8, self.rect.centery - 6),
                (self.rect.centerx - 3, self.rect.centery - 1),
                (self.rect.centerx - 3, self.rect.centery + 9),
                (self.rect.centerx - 8, self.rect.centery + 4)
            ])
            # Sound waves
            pygame.draw.arc(surface, WHITE,
                            (self.rect.centerx - 2, self.rect.centery - 8, 12, 16),
                            -3.14 / 2, 3.14 / 2, 2)
            pygame.draw.arc(surface, WHITE,
                            (self.rect.centerx - 7, self.rect.centery - 12, 22, 24),
                            -3.14 / 2, 3.14 / 2, 2)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered

    def toggle_music(self):
        self.is_muted = not self.is_muted
        if self.is_muted:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
        return self.is_muted


# Main menu loop
def main_menu():
    clock = pygame.time.Clock()
    running = True

    # Create music button
    music_button = MusicButton(SCREEN_WIDTH - 60, 20)

    # Start background music
    play_background_music()

    # Create initial particles
    for _ in range(50):
        create_particle(
            pygame.time.get_ticks() % SCREEN_WIDTH,
            pygame.time.get_ticks() % SCREEN_HEIGHT,
            (100, 150, 255),
            1, 2, 90
        )

    while running:
        current_time = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_m:  # M key to toggle music
                    music_button.toggle_music()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_click = True
                    # Check if music button was clicked
                    if music_button.rect.collidepoint(mouse_pos):
                        music_button.toggle_music()

        # Update
        update_particles()
        update_stars()
        update_laser_effects()
        update_text_sparks()

        # Occasionally create new particles
        if current_time % 30 == 0:
            create_particle(
                -10,
                pygame.time.get_ticks() % SCREEN_HEIGHT,
                (100, 200, 255),
                2, 3, 120
            )

        # Create text sparks for title text
        if current_time % 5 == 0:  # Create sparks frequently
            # Sparks for "ROBOTICS PRESENT"
            robotics_present = title_text_positions["robotics_present"]
            if robotics_present["width"] > 0:  # Only create if position is set
                create_text_spark(
                    robotics_present["x"],
                    robotics_present["y"],
                    robotics_present["width"],
                    robotics_present["height"],
                    (random.randint(150, 255), random.randint(180, 255), 255)
                )

            # Sparks for "ROBOTS GAME"
            robots_game = title_text_positions["robots_game"]
            if robots_game["width"] > 0:  # Only create if position is set
                create_text_spark(
                    robots_game["x"],
                    robots_game["y"],
                    robots_game["width"],
                    robots_game["height"],
                    (random.randint(150, 255), random.randint(180, 255), 255)
                )

        # Check button hover
        buttons = [snowbot_button, drone_button, dogbot_button, credit_button, quit_button]
        any_hovered = False

        for button in buttons:
            if button.check_hover(mouse_pos):
                any_hovered = True
                if not button.is_hovered:
                    play_button_hover_sound()

        # Check music button hover
        music_button.check_hover(mouse_pos)

        # Check button clicks
        if snowbot_button.is_clicked(mouse_pos, mouse_click):
            play_button_click_sound()
            launch_snowbot_game()

        if drone_button.is_clicked(mouse_pos, mouse_click):
            play_button_click_sound()
            launch_drone_game()

        if dogbot_button.is_clicked(mouse_pos, mouse_click):
            play_button_click_sound()
            launch_dogbot_game()

        # NEW: Handle credit button click
        if credit_button.is_clicked(mouse_pos, mouse_click):
            play_button_click_sound()
            launch_credit_game()

        if quit_button.is_clicked(mouse_pos, mouse_click):
            play_button_click_sound()
            running = False

        # Drawing
        screen.fill(BACKGROUND)

        # Draw background elements
        draw_circuit_background(screen)
        draw_stars(screen)
        draw_particles(screen)
        draw_laser_effects(screen)
        draw_robot_silhouette(screen, current_time)

        # Draw title with animations
        draw_title(screen, current_time)

        # Draw text sparks
        draw_text_sparks(screen)

        # Draw buttons
        for button in buttons:
            button.draw(screen)

        # Draw music button
        music_button.draw(screen)

        # Draw music instruction
        music_text = info_font.render("Press M to toggle music", True, GRAY)
        screen.blit(music_text, (20, SCREEN_HEIGHT - 40))

        # Draw footer text
        footer_text = info_font.render("Robotics Lapland (AMK)", True, GRAY)
        screen.blit(footer_text, (SCREEN_WIDTH // 2 - footer_text.get_width() // 2, SCREEN_HEIGHT - 50))

        # Draw version info
        version_text = info_font.render("v1.0", True, (80, 80, 100))
        screen.blit(version_text, (SCREEN_WIDTH - version_text.get_width() - 20, SCREEN_HEIGHT - 40))

        pygame.display.flip()
        clock.tick(60)

    # Stop music before quitting
    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main_menu()