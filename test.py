import pygame
import random
import time
import json
import math

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Undertale")

# Player variables
player_speed = 5
player_size = (65, 100)
player_x, player_y = SCREEN_WIDTH // 2 - 32.5, SCREEN_HEIGHT // 2 - 50

# Lives counter
lives = 3

# Load assets
player_images = {
    'up': pygame.transform.scale(pygame.image.load("images/player_up.png").convert_alpha(), player_size),
    'down': pygame.transform.scale(pygame.image.load("images/player_down.png").convert_alpha(), player_size),
    'left': pygame.transform.scale(pygame.image.load("images/player_left.png").convert_alpha(), player_size),
    'right': pygame.transform.scale(pygame.image.load("images/player_right.png").convert_alpha(), player_size)
}
current_player_image = player_images['down']

heart_image = pygame.transform.scale(pygame.image.load("images/heart.png").convert_alpha(), (30, 30))
battle_heart = pygame.transform.scale(heart_image, (18, 18))
pygame.display.set_icon(heart_image)

# maps
maps = {
    "start": "locs/start_location.png",
    "flowey": "locs/flowey_location.png",
    "ruins1": "locs/ruins1.jpg"
}

# Player position after teleporting
player_tp_x, player_tp_y = 0, 0

# Enemies
enemies = {
    "flowey_world": "images/flowey_world.png",
    "kind_flowey": "images/flowey_battle.png",
    "evil_flowey": "images/evil_flowey.png"
}
flowey_pos = (3020, -640)

# Interaction range
interaction_range = 50

# Forbidden areas
forbidden_zones = [
    pygame.Rect(1326, 499, 1616, 1),
    pygame.Rect(1300, 99, 1, 370),
    pygame.Rect(1155, 99, 145, 1),
    pygame.Rect(1124, -1, 1, 70),
    pygame.Rect(174, -1, 950, 1),
    pygame.Rect(174, -1, 1, 70),
    pygame.Rect(0, 99, 145, 1),
    pygame.Rect(0, 99, 1, 500),
    pygame.Rect(0, 600, 70, 1),
    pygame.Rect(99, 628, 1, 72),
    pygame.Rect(99, 700, 50, 1),
    pygame.Rect(174, 728, 1, 72),
    pygame.Rect(174, 800, 100, 1),
    pygame.Rect(299, 828, 1, 72),
    pygame.Rect(299, 900, 700, 1),
    pygame.Rect(1000, 828, 1, 72),
    pygame.Rect(1025, 800, 100, 1),
    pygame.Rect(1125, 728, 1, 72),
    pygame.Rect(1150, 700, 2150, 1),
    pygame.Rect(3300, 499, 1, 201),
    pygame.Rect(3200, 499, 100, 1),
    pygame.Rect(3180, 195, 1, 280),
    pygame.Rect(2960, 194, 220, 1),
    pygame.Rect(2960, 195, 1, 280),

    pygame.Rect(2500, -1000, 1, 800),
    pygame.Rect(2500, -1212, 1120, 1),
    pygame.Rect(3620, -1000, 1, 800),
    pygame.Rect(2500, -200, 1120, 1),

    pygame.Rect(3003, -1528, 133, 1),
    pygame.Rect(3003, -1658, 1, 130),
    pygame.Rect(3135, -1658, 1, 130),
    pygame.Rect(2973, -1688, 1, 1),
    pygame.Rect(3165, -1688, 1, 1),
    pygame.Rect(2958, -1703, 1, 1),
    pygame.Rect(3180, -1703, 1, 1),
    pygame.Rect(2938, -1790, 1, 68),
    pygame.Rect(3200, -1790, 1, 68),
    pygame.Rect(2888, -1840, 1, 1),
    pygame.Rect(2918, -1810, 1, 1),
    pygame.Rect(3250, -1840, 1, 1),
    pygame.Rect(3220, -1810, 1, 1),
    pygame.Rect(2740, -1857, 135, 1),
    pygame.Rect(3270, -1857, 135, 1),
    pygame.Rect(2740, -2407, 1, 550),
    pygame.Rect(3397, -2407, 1, 550),
    pygame.Rect(2770, -2407, 1, 1),
    pygame.Rect(2740, -2450, 1, 1),
    pygame.Rect(2710, -2480, 1, 1),
    pygame.Rect(2670, -2660, 1, 150),
    pygame.Rect(3367, -2407, 1, 1),
    pygame.Rect(3397, -2437, 1, 1),
    pygame.Rect(3427, -2467, 1, 1),
    pygame.Rect(3457, -2497, 1, 1),
    pygame.Rect(3467, -2660, 1, 150),
    pygame.Rect(2695, -2720, 1, 1),
    pygame.Rect(2695, -2780, 315, 1),
    pygame.Rect(3430, -2720, 1, 1),
    pygame.Rect(3125, -2780, 315, 1),
    pygame.Rect(3020, -2850, 100, 1),
    pygame.Rect(2970, -2500, 200, 1),
    pygame.Rect(2875, -2643, 390, 1),
    pygame.Rect(3190, -2520, 1, 1),
    pygame.Rect(3240, -2570, 1, 1),
    pygame.Rect(3290, -2620, 1, 1),
    pygame.Rect(2950, -2520, 1, 1),
    pygame.Rect(2900, -2570, 1, 1),
    pygame.Rect(2850, -2620, 1, 1),
]

# Teleportation areas
teleports = {
    "flowey": pygame.Rect(2960, 194, 220, 140),
    "ruins": pygame.Rect(3000, -1212, 140, 100),
    "ruins2": pygame.Rect(3020, -2850, 100, 20)
}

# Save areas
save1_pos = (3035, -2500)

# Loading music
tracks = {
    "flowey": "music/flowey_theme.mp3",
    "fallen_down": "music/fallen_down.mp3",
    "ruins": "music/ruins_theme.mp3",
    "sans": "music/sans_theme.mp3"
}
current_track = None

# Game states
running = True
standard = True
game_over = False
choosing_action = False
battle_with_flowey = False
is_teleporting = False
save = False

# Teleportation stats
teleport_start_time = None
teleport_delay = 1.5
fade = 255

# Battle variables
heart_pos = [SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT // 2 + 70]
heart_speed = 3
obstacles = []
battle_counter = 0
battle_score = 0
obstacle_spawn_timer = 0
flowey_bullet = pygame.transform.scale(pygame.image.load("images/flowey_bullet.png").convert_alpha(), (27 // 3, 53 // 3))
flowey_bullet_rotate = pygame.transform.rotate(flowey_bullet, 90)
battle_phase = 1
wave_active = True
wave_start_time = 0
all_collide = False
max_life = 20
current_life = 20
flowey_end = None

# Screen update
clock = pygame.time.Clock()

# Dictionary for cashing loaded images
loaded_maps = {}

# Dictionary for cashing loaded enemies
loaded_enemies = {}


# Loading maps function
def load_map(map_name):
    if map_name in loaded_maps:
        return loaded_maps[map_name]
    else:
        image = pygame.image.load(maps[map_name]).convert_alpha()
        loaded_maps[map_name] = image
        return image


# Loading enemies function
def load_enemies(enemy_name):
    if enemy_name in loaded_enemies:
        return loaded_enemies[enemy_name]
    else:
        image = pygame.transform.scale(pygame.image.load(enemies[enemy_name]).convert_alpha(), (100, 100))
        loaded_enemies[enemy_name] = image
        return image


# Draw text function
def draw_text(text, size, color, x, y):
    font = pygame.font.Font('font/font.ttf', size)
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))


# Check collision function
def check_collision(new_x, new_y):
    player_rect = pygame.Rect(new_x, new_y, player_size[0], player_size[1])
    for zone in forbidden_zones:
        if player_rect.colliderect(zone):
            return True
    return False


# Check interaction range function
def is_in_interaction_range(player_poss, object_pos, range_):
    return abs(player_poss[0] - object_pos[0]) < range_ and abs(player_poss[1] - object_pos[1]) < range_


# Switch the music function
def play_music(track_name):
    pygame.mixer.music.load(tracks[track_name])
    pygame.mixer.music.play(-1)


# Fade switching behind soundtracks
def fade_to_music(new_track, fade_time=1000):
    global current_track

    if current_track == new_track:
        return

    pygame.mixer.music.fadeout(fade_time)
    play_music(new_track)
    current_track = new_track


# Save the game function
def save_game(player_x, player_y, score, mercy, filename="save.json"):
    data = {
        "player_x": player_x,
        "player_y": player_y,
        "score": score,
        "mercy": mercy
    }
    with open(filename, "w") as file:
        json.dump(data, file)


# Load game settings function
def load_game(filename="save.json"):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        return data["player_x"], data["player_y"], data["score"], data["mercy"]
    except (FileNotFoundError, json.JSONDecodeError):
        return 2620, 500, 0, 0 # 620, 350


def draw_life_bar(screen, x, y, width, height, life, max_life):
    red_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, RED, red_rect)

    green_width = int(width * life / max_life)
    green_rect = pygame.Rect(x, y, green_width, height)
    pygame.draw.rect(screen, GREEN, green_rect)


# Loading game settings from the JSON file
player_map_x, player_map_y, score, mercy = load_game("save.json")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    new_map_x, new_map_y = player_map_x, player_map_y

    # Standard action
    if standard:
        if keys[pygame.K_w]:
            new_map_y -= player_speed
            current_player_image = player_images['up']
        if keys[pygame.K_s]:
            new_map_y += player_speed
            current_player_image = player_images['down']
        if keys[pygame.K_a]:
            new_map_x -= player_speed
            current_player_image = player_images['left']
        if keys[pygame.K_d]:
            new_map_x += player_speed
            current_player_image = player_images['right']

        # Check for forbidden areas
        future_rect = pygame.Rect(new_map_x, new_map_y, player_size[0], player_size[1])
        if not any(zone.colliderect(future_rect) for zone in forbidden_zones):
            player_map_x, player_map_y = new_map_x, new_map_y

        # Check for teleportation areas
        if teleports["flowey"].colliderect(future_rect):
            standard = False
            is_teleporting = True
            teleport_start_time = time.time()
            player_tp_x, player_tp_y = 3035, -300
        if teleports["ruins"].colliderect(future_rect) and score == 1:
            standard = False
            is_teleporting = True
            teleport_start_time = time.time()
            player_tp_x, player_tp_y = 3035, -1680
        if teleports["ruins2"].colliderect(future_rect):
            standard = False
            is_teleporting = True
            teleport_start_time = time.time()
            player_tp_x, player_tp_y = 3035, -1680 # TODO: change tp cords

        # Calculate camera offset
        camera_offset_x = player_map_x - player_x
        camera_offset_y = player_map_y - player_y

        # Positions on the screen
        flowey_screen_x = flowey_pos[0] - camera_offset_x
        flowey_screen_y = flowey_pos[1] - camera_offset_y
        save1_screen_x = save1_pos[0] - camera_offset_x
        save1_screen_y = save1_pos[1] - camera_offset_y
        player_screen_pos = (player_x, player_y)

        # Check for interaction with flowey
        if is_in_interaction_range(player_screen_pos, (flowey_screen_x, flowey_screen_y), interaction_range):
            if score < 1:
                standard = False
                battle_with_flowey = True

        # Check for interaction with save zone
        if is_in_interaction_range(player_screen_pos, (save1_screen_x, save1_screen_y), interaction_range) and keys[pygame.K_RETURN]:
            standard = False
            save = True

        # Draw the map
        screen.fill(BLACK)
        screen.blit(load_map("start"), (-camera_offset_x, -camera_offset_y))
        screen.blit(load_map("flowey"), (-camera_offset_x + 2520, -camera_offset_y - 1212))
        screen.blit(load_map("ruins1"), (-camera_offset_x + 2370, -camera_offset_y - 3100))

        # Draw flowey
        if score < 1:
            screen.blit(load_enemies("flowey_world"), (flowey_screen_x, flowey_screen_y))

        # Draw player
        screen.blit(current_player_image, (player_x, player_y))

        # Draw forbidden areas
        #for zone in forbidden_zones:
        #    pygame.draw.rect(screen, RED, (zone.x - camera_offset_x, zone.y - camera_offset_y, zone.width, zone.height))

    # Teleporting action
    if is_teleporting:
        if fade > 0:
            fade -= 3
        screen.fill((fade, fade, fade))
        if time.time() - teleport_start_time >= teleport_delay:
            player_map_x, player_map_y = player_tp_x, player_tp_y
            fade = 255
            is_teleporting = False
            standard = True
            if player_tp_x == 3035 and player_tp_y == -1680:
                fade_to_music("ruins")

    # Handle action choice
    if choosing_action:
        screen.fill(BLACK)
        draw_text("Choose Action:", 36, WHITE, SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 - 100)
        draw_text("1. Fight", 36, RED, SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 - 50)
        draw_text("2. Mercy", 36, BLUE, SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2)

        if keys[pygame.K_1]:
            choosing_action = False
            battle_with_flowey = True
        elif keys[pygame.K_2]:
            choosing_action = False
            standard = True
            mercy += 1

    # Save the game action
    if save:
        screen.fill(BLACK)
        draw_text("Save the Game:", 36, WHITE, SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 - 100)
        draw_text("1. Save", 36, GREEN, SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 50)
        draw_text("2. Cancel", 36, WHITE, SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2)

        if keys[pygame.K_1]:
            save_game(player_map_x, player_map_y, score, mercy)
            lives = 3
            save = False
            standard = True
        elif keys[pygame.K_2]:
            save = False
            standard = True

    # Battle mode (flowey)
    if battle_with_flowey:
        # Music switching
        fade_to_music("flowey")

        # Draw battlefield
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, (300, 300, 200, 150), 6)
        draw_text("HP", 22, WHITE, 325, 477)
        draw_life_bar(screen, 375, 475, 50, 30, current_life, max_life)
        if current_life >= 10:
            draw_text(f"{current_life} / {max_life}", 36, WHITE, 440, 468)
        if current_life < 10:
            draw_text(f"0{current_life} / {max_life}", 36, WHITE, 440, 468)

        # Move the heart
        if keys[pygame.K_a] and heart_pos[0] > 306:
            heart_pos[0] -= heart_speed
        if keys[pygame.K_d] and heart_pos[0] < 475:
            heart_pos[0] += heart_speed
        if keys[pygame.K_w] and heart_pos[1] > 308:
            heart_pos[1] -= heart_speed
        if keys[pygame.K_s] and heart_pos[1] < 427:
            heart_pos[1] += heart_speed

        # Draw heart
        screen.blit(battle_heart, heart_pos)

        # Draw flowey
        if battle_phase == 1:
            screen.blit(load_enemies("kind_flowey"), (300, 200))

        if battle_phase == 2:
            screen.blit(load_enemies("evil_flowey"), (300, 200))

        # 1st phase
        if battle_phase == 1 and wave_active:
            obstacles.clear()
            center_x, center_y = 400, 500
            for i in range(5):
                x = 200 + i * 80
                y = 50
                obstacles.append({
                    "x": x,
                    "y": y,
                    "target_x": center_x,
                    "target_y": center_y,
                    "speed": 0.01,
                    "state": 0,
                    "last_toggle": pygame.time.get_ticks()
                })
            wave_active = False

        if battle_phase == 1 and not wave_active:
            all_collide = False
            for obs in obstacles[:]:
                dx = obs["target_x"] - obs["x"]
                dy = obs["target_y"] - obs["y"]
                obs["speed"] += 0.01
                dist = math.hypot(dx, dy)
                if dist > 0:
                    obs["x"] += (dx / dist) * obs["speed"]
                    obs["y"] += (dy / dist) * obs["speed"]

                current_time = pygame.time.get_ticks()
                if current_time - obs["last_toggle"] > 50:
                    obs["state"] = 1 - obs["state"]
                    obs["last_toggle"] = current_time

                if obs["state"] == 0:
                    image_to_draw = flowey_bullet
                else:
                    image_to_draw = flowey_bullet_rotate

                heart_rect = pygame.Rect(heart_pos[0], heart_pos[1], battle_heart.get_width(), battle_heart.get_height())

                rect = image_to_draw.get_rect(center=(obs["x"], obs["y"]))
                screen.blit(image_to_draw, rect.topleft)

                if rect.colliderect(heart_rect):
                    current_life = 1
                    all_collide = True

                if dist < 5:
                    all_collide = True

            if all_collide:
                obstacles.clear()
                wave_start_time = pygame.time.get_ticks()

            if len(obstacles) == 0 and wave_start_time != 0:
                if pygame.time.get_ticks() - wave_start_time > 3000:
                    battle_phase = 2
                    all_collide = False
                    wave_active = True

        # 2nd phase
        if battle_phase == 2 and wave_active:
            obstacles.clear()
            center_x, center_y = 400, 375
            radius = 200
            num_obstacles = 60
            for i in range(num_obstacles):
                angle = 2 * math.pi * i / num_obstacles
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                obstacles.append({
                    "x": x,
                    "y": y,
                    "target_x": center_x,
                    "target_y": center_y,
                    "speed": 0.2,
                    "state": 0,
                    "last_toggle": pygame.time.get_ticks()
                })
            wave_active = False

        if battle_phase == 2 and not wave_active:
            r_min = 50
            for obs in obstacles[:]:
                dx = obs["target_x"] - obs["x"]
                dy = obs["target_y"] - obs["y"]
                dist = math.hypot(dx, dy)
                if dist > r_min:
                    obs["x"] += (dx / dist) * obs["speed"]
                    obs["y"] += (dy / dist) * obs["speed"]
                else:
                    obstacles.clear()

                current_time = pygame.time.get_ticks()
                if current_time - obs["last_toggle"] > 50:
                    obs["state"] = 1 - obs["state"]
                    obs["last_toggle"] = current_time

                if obs["state"] == 0:
                    image_to_draw = flowey_bullet
                else:
                    image_to_draw = flowey_bullet_rotate

                heart_rect = pygame.Rect(heart_pos[0], heart_pos[1], battle_heart.get_width(), battle_heart.get_height())

                rect = image_to_draw.get_rect(center=(obs["x"], obs["y"]))
                screen.blit(image_to_draw, rect.topleft)

                if rect.colliderect(heart_rect):
                    current_life = 1
                    obstacles.clear()

            if len(obstacles) == 0:
                if flowey_end is None:
                    flowey_end = pygame.time.get_ticks()
                    battle_phase = 0

        if flowey_end is not None:
            current_time = pygame.time.get_ticks()
            if current_time - flowey_end >= 2500:
                current_life = 20
            if current_time - flowey_end >= 3000:
                fade_to_music("fallen_down")
                battle_with_flowey = False
                standard = True
                score += 1

    # Game Over
    if game_over:
        pygame.mixer.music.stop()
        screen.fill(BLACK)
        draw_text("Game Over", 72, RED, SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 90)
        draw_text(f'Final Score: {score}', 36, WHITE, SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 - 10)
        draw_text("Press R to Restart", 36, WHITE, SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 + 60)

        # Restart
        if keys[pygame.K_r]:
            pygame.mixer.music.play(-1)
            game_over = False
            standard = True
            battle_counter = 0
            lives = 3
            player_pos = [360, 250]
            heart_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
            obstacles = []

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
