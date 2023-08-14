import os
from os import listdir
from os.path import isfile, join
import pygame
import random
import pygame.mixer

pygame.init()
pygame.mixer.init()

clock = pygame.time.Clock()
FPS = 60
# Define font #
font = pygame.font.SysFont("Bauhaus 93", 60)

pygame.mixer.music.load(join("assets", "Music", "ForestWalk-320bit.mp3"))
pygame.mixer.music.play(-1)

# Define color #
black = (0, 0, 0)

# Define Game Variables #
SCREEN_WIDTH = 928
SCREEN_HEIGHT = 793
player_x = 100
player_y = SCREEN_HEIGHT // 2
player_speed = 5
player_jump_power = 15
player_gravity = 0.5
player_y_velocity = 0
player_x_velocity = 0
is_jumping = False
is_sliding = False
ground_y = SCREEN_HEIGHT - 200
player_width = 200
player_height = 150
animation_delay = 3
animation_counter = 0
frame_counter = 0
time_since_last_wolf = 0
collision_occurred = False
is_game_over = False
scroll = 0
score = 0
in_start_screen = True
highscore = 0

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Forest Walk")

bg_images = []
background_folder = join("assets", "Background")

for filename in os.listdir(background_folder):
    full_path = join(background_folder, filename)
    bg_images.append(pygame.image.load(full_path).convert_alpha())

knight_fall_folder = join("assets", "Characters", "Knight", "Fall")
knight_jump_folder = join("assets", "Characters", "Knight", "Jump")
knight_run_folder = join("assets", "Characters", "Knight", "Run")
knight_slide_folder = join("assets", "Characters", "Knight", "Slide")
knight_idle_folder = join("assets", "Characters", "Knight", "Idle")
knight_die_folder = join("assets", "Characters", "Knight", "Die")
game_over_fullpath = join("assets", "Game Over","Game Over.png")
knight_fall = []
knight_jump = []
knight_run = []
knight_slide = []
knight_idle = []
knight_die = []

for filename in os.listdir(knight_fall_folder):
    full_path = join(knight_fall_folder, filename)
    knight_fall.append(pygame.image.load(full_path).convert_alpha())
for filename in os.listdir(knight_jump_folder):
    full_path = join(knight_jump_folder, filename)
    knight_jump.append(pygame.image.load(full_path).convert_alpha())
for filename in os.listdir(knight_run_folder):
    full_path = join(knight_run_folder, filename)
    knight_run.append(pygame.image.load(full_path).convert_alpha())
for filename in os.listdir(knight_slide_folder):
    full_path = join(knight_slide_folder, filename)
    knight_slide.append(pygame.image.load(full_path).convert_alpha())
for filename in os.listdir(knight_idle_folder):
    full_path = join(knight_idle_folder, filename)
    knight_idle.append(pygame.image.load(full_path).convert_alpha())
for filename in os.listdir(knight_die_folder):
    full_path = join(knight_die_folder, filename)
    knight_die.append(pygame.image.load(full_path).convert_alpha())
game_over = pygame.image.load(game_over_fullpath).convert_alpha()
buttons_sprite_sheet = pygame.image.load(join("assets","UI","Buttons.png"))

wolf_sprite_sheet = pygame.image.load(join("assets", "Obstacles", "wolf_brown_full.png"))
wolf_sprite_width = wolf_sprite_sheet.get_width() // 12
wolf_sprite_height = wolf_sprite_sheet.get_height() // 8

button_sprite_width = buttons_sprite_sheet.get_width() // 5
button_sprite_height = buttons_sprite_sheet.get_height() // 6

restart_sprite = pygame.transform.scale(buttons_sprite_sheet.subsurface(pygame.Rect(0, button_sprite_height * 3, button_sprite_width, button_sprite_height)), (button_sprite_width * 4, button_sprite_height * 4))
restart_button_rect = restart_sprite.get_rect(topleft = (400, 550))

quit_sprite = pygame.transform.scale(buttons_sprite_sheet.subsurface(pygame.Rect(button_sprite_width, button_sprite_height * 3, button_sprite_width, button_sprite_height)), (button_sprite_width * 4, button_sprite_height * 4))
quit_button_rect = quit_sprite.get_rect(topleft = (500, 550))

def reset_game():
    global is_game_over, collision_occurred, player_x, player_y, layer_speeds, score
    is_game_over = False
    collision_occurred = False
    player_x = 100
    player_y = SCREEN_HEIGHT // 2
    layer_speeds = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6]
    score = 0
    pygame.mixer.music.stop()
    pygame.mixer.music.load(join("assets", "Music", "ForestWalk-320bit.mp3"))
    pygame.mixer.music.play(-1)

def game_over_screen():
    screen.blit(scaled_game_over, (380, 300))
    draw_restart_button()
    draw_quit_button()

def draw_restart_button():
    screen.blit(restart_sprite, restart_button_rect)
    mouse_x, mouse_y = pygame.mouse.get_pos()

    if restart_button_rect.collidepoint(mouse_x, mouse_y):
        highlighted_button_image = pygame.Surface(restart_sprite.get_size(), pygame.SRCALPHA)
        pygame.draw.rect(highlighted_button_image, (80, 80, 80, 100), restart_sprite.get_rect())
        highlighted_button_image.blit(restart_sprite, (0,0), special_flags = pygame.BLEND_RGBA_ADD)
        screen.blit(highlighted_button_image, restart_button_rect)

        if pygame.mouse.get_pressed()[0]:
            reset_game()
            return

def draw_quit_button():
    screen.blit(quit_sprite, quit_button_rect)
    mouse_x, mouse_y = pygame.mouse.get_pos()

    if quit_button_rect.collidepoint(mouse_x, mouse_y):
        highlighted_button_image = pygame.Surface(quit_sprite.get_size(), pygame.SRCALPHA)
        pygame.draw.rect(highlighted_button_image, (80, 80, 80, 100), quit_sprite.get_rect())
        highlighted_button_image.blit(quit_sprite, (0,0), special_flags = pygame.BLEND_RGBA_ADD)
        screen.blit(highlighted_button_image, quit_button_rect)

        if pygame.mouse.get_pressed()[0]:
            pygame.quit()

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y + 50))
    highscore_text = font.render(f"Highscore: {highscore}", True, (0, 0, 0))
    screen.blit(highscore_text, (x - 150, y))

def draw_start_screen():
    screen.fill((0, 0, 0))
    start_text = font.render("Press SPACE to Start", True, (255, 255, 255))
    screen.blit(start_text, ((SCREEN_WIDTH - start_text.get_width()) // 2, SCREEN_HEIGHT // 2))
    
    pygame.display.update()

wolf_sprites = []
for row in range(1, 2):
    for col in range(6):
        x = col * wolf_sprite_width
        y = row * wolf_sprite_height
        sprite = wolf_sprite_sheet.subsurface(pygame.Rect(x, y, wolf_sprite_width, wolf_sprite_height))
        wolf_sprites.append(sprite)

class WolfObstacle:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.current_frame = 0
        self.wolf_animation_counter = 0
        self.width = wolf_sprite_width * 4
        self.height = wolf_sprite_height * 4
        self.collided = False

    def move(self):
        if not self.collided:
            self.x -= self.speed

    def animate(self):
        frame_count = len(wolf_sprites)
        scaled_wolf_frame = pygame.transform.scale(wolf_sprites[self.current_frame], (wolf_sprite_width * 4, wolf_sprite_height * 4))
        screen.blit(scaled_wolf_frame, (self.x, self.y))

        if self.wolf_animation_counter >= animation_delay:
            self.current_frame = (self.current_frame + 1) % frame_count
            self.wolf_animation_counter = 0
        else:
            self.wolf_animation_counter += 1
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def set_collided(self):
        self.collided = True
    
    def is_collided(self):
        return self.collided

wolf_obstacles = []

player_animations = {
    "fall": knight_fall,
    "jump": knight_jump,
    "run": knight_run,
    "slide": knight_slide,
    "die": knight_die,
    "idle": knight_idle
}
current_animation = "run"

current_frame = 0

bg_width = bg_images[0].get_width()
bg_count = len(bg_images)
layer_speeds = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6]
layer_positions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def draw_bg():
    for i in range(bg_count):
        layer_positions[i] -= layer_speeds[i]
        if layer_positions[i] <= - bg_images[i].get_width():
            layer_positions[i] = 0
        screen.blit(bg_images[i], (layer_positions[i], 0))
        screen.blit(bg_images[i], (layer_positions[i] + bg_images[i].get_width(), 0))


run = True
pressed_keys = {}

while in_start_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            in_start_screen = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            in_start_screen = False
    draw_start_screen()
    clock.tick(FPS)

while run:
    clock.tick(FPS)
    screen.fill((0,0,0))
    draw_bg()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # Handle Movement #
        if event.type == pygame.KEYDOWN:
            pressed_keys[event.key] = True
            if event.key == pygame.K_SPACE and not is_jumping:
                player_y_velocity = -player_jump_power
                is_jumping = True
        if event.type == pygame.KEYUP:
            if event.key in pressed_keys:
                del pressed_keys[event.key]
    
    player_y_velocity += player_gravity
    player_y += player_y_velocity
    player_x += player_x_velocity

    if player_y >= ground_y:
        player_y = ground_y
        player_y_velocity = 0
        is_jumping = False
    
    if pygame.K_a in pressed_keys and not is_game_over:
        player_x_velocity = -player_speed
        if player_x + player_x_velocity < -75:
            player_x = -75
    elif pygame.K_d in pressed_keys and not is_game_over:
        player_x_velocity = player_speed
        if player_x + player_x_velocity + player_width> SCREEN_WIDTH + 75:
            player_x = SCREEN_WIDTH - player_width + 75

    if pygame.K_a not in pressed_keys and pygame.K_d not in pressed_keys and not is_game_over:
        player_x_velocity = 0
    
    is_sliding = pygame.K_s in pressed_keys and player_y == ground_y
    
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    
    scaled_game_over = pygame.transform.scale(game_over, (200, 250))

    # Change animations based on action and position #
    if is_jumping == True:
        current_frame = 0
        current_animation = "jump"
    if is_sliding == True:
        current_frame = 0
        current_animation = "slide"
    elif player_y < ground_y:
        current_frame = 0
        current_animation = "fall"
    elif collision_occurred:
        current_animation = "die"
    else:
        current_animation = "run"

    frame_count = len(player_animations[current_animation])

# End the game if player collides with a wolf #
    if is_game_over:
        game_over_screen()
    else:
        scaled_player_frame = pygame.transform.scale(player_animations[current_animation][current_frame], (player_width, player_height))
        screen.blit(scaled_player_frame, (player_x, player_y))
        if animation_counter >= animation_delay:
            current_frame = (current_frame + 1) % frame_count
            animation_counter = 0
        else:
            animation_counter += 1
    
    if not is_game_over:
        score += 1
        if score > highscore:
            highscore = score

    if random.randint(0, 80 - score // 60) == 0 and not collision_occurred:
        new_wolf = WolfObstacle(SCREEN_WIDTH, ground_y - wolf_sprite_height + 50, 5)
        wolf_obstacles.append(new_wolf)
        frame_counter = 0
    
    overlap_tolerance = 80

    draw_text(str(score), font, black, int(SCREEN_WIDTH / 2.1), 20)

    for wolf in wolf_obstacles:
        wolf_rect = wolf.get_rect()
        wolf.move()
        wolf.animate()
        expanded_player_rect = player_rect.inflate(-overlap_tolerance, -overlap_tolerance * 2)
        shrunken_wolf_rect = wolf_rect.inflate(-overlap_tolerance, -overlap_tolerance * 2)
        if expanded_player_rect.colliderect(shrunken_wolf_rect):
            layer_speeds = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            player_x_velocity = 0
            is_game_over = True
            for wolf in wolf_obstacles:
                wolf.set_collided()
            wolf_obstacles = []
            collision_occurred = True
            break
        else:
            player_collided = False

# Remove wolves if they go off the screen #    
    wolf_obstacles = [wolf for wolf in wolf_obstacles if wolf.x + wolf_sprite_width > 0]

    pygame.display.update()

pygame.quit()