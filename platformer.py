import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Platformer")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Player settings
player_color = (0, 0, 255) # Blue color
player_width, player_height = 50, 50
player_x, player_y = WIDTH // 2, HEIGHT - player_height - 50 # Start near bottom
player_speed = 5

# Gravity settings
gravity = 0.5
player_velocity_y = 0
is_jumping = False

# Platform settings
platforms = [ 
    pygame.Rect(200, HEIGHT - 100, 200, 10), # Define platforms as rectangles
    pygame.Rect(500, HEIGHT - 200, 200, 10),
    pygame.Rect(300, HEIGHT - 300, 200, 10)
]

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movement
    keys = pygame.key.get_pressed() # Get the state of all keys
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP] and not is_jumping: # Jump if not already jumping
        player_velocity_y = -10 # Negative for upward movement
        is_jumping = True
    if player_x < 0:
        player_x = 0
    elif player_x > WIDTH - player_width:
        player_x = WIDTH - player_width

    # Apply gravity
    player_velocity_y += gravity
    player_y += player_velocity_y

    # Ground collision
    if player_y >= HEIGHT - player_height - 50: # Stop at the bottom of the screen
        player_y = HEIGHT - player_height - 50
        player_velocity_y = 0
        is_jumping = False # Allow jumping again once on the ground

    # Platform collision
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    for platform in platforms:
        if player_rect.colliderect(platform) and player_velocity_y > 0: # Falling down
            player_y = platform.y - player_height # Place on top of platform
            player_velocity_y = 0
            is_jumping = False

    

    # Fill the screen and draw the player
    screen.fill(WHITE)

    # Draw the player
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    pygame.draw.rect(screen, player_color, player_rect)

    # Draw platforms
    for platform in platforms:
        pygame.draw.rect(screen, GREEN, platform)


    pygame.display.flip()

# Quit Pygame
pygame.quit()