import pygame
import sys

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

def reset():
    global WIDTH, HEIGHT, player_color, player_width, player_height
    global player_x, player_y, player_speed, gravity, player_velocity_y
    global jump_strength, is_jumping, score, font, platforms
    global game_over, coins, enemy, enemy_speed, enemy_direction
  
    # Screen settings  
    pygame.display.set_caption("2D Platformer")

    # Player settings
    player_color = (0, 0, 255) # Blue color
    player_width, player_height = 50, 50
    player_x, player_y = WIDTH // 2, HEIGHT - player_height - 50 # Start near bottom
    player_speed = 1

    # Gravity settings
    gravity = 0.2
    player_velocity_y = 0
    jump_strength = -7 # Lower for smoother jumps
    is_jumping = False

    # Platform settings
    platforms = [ 
        pygame.Rect(200, HEIGHT - 100, 200, 10), # Define platforms as rectangles
        pygame.Rect(500, HEIGHT - 200, 200, 10),
        pygame.Rect(300, HEIGHT - 300, 200, 10)
    ]

    # Scoring
    score = 0
    font = pygame.font.Font(None, 36) # Font for displaying score

    game_over = False

    # Collectible coins (use pygame.Rect to define their positions)
    coins = [
        pygame.Rect(250, HEIGHT - 150, 20, 20),
        pygame.Rect(550, HEIGHT - 250, 20, 20),
        pygame.Rect(400, HEIGHT - 350, 20, 20)
    ]

    # Enemy settings
    enemy = pygame.Rect(300, HEIGHT - 150, 50, 50)
    enemy_speed = 2
    enemy_direction = 1 # 1 for right, -1 for left

reset()
# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            reset()

    if not game_over:
        # Player Movement
        keys = pygame.key.get_pressed() # Get the state of all keys
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
        if keys[pygame.K_UP] and not is_jumping: # Jump if not already jumping
            player_velocity_y = jump_strength # Negative for upward movement
            is_jumping = True
        if player_x < 0:
            player_x = 0
        elif player_x > WIDTH - player_width:
            player_x = WIDTH - player_width

        # Enemy movement
        enemy.x += enemy_speed * enemy_direction 
        if enemy.x <= 0 or enemy.x >= WIDTH - enemy.width:
            enemy_direction *= -1 # Reverse direction at screen edges

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

        # Coin collection
        for coin in coins[:]: # Iterate over a copy of the list
            if player_rect.colliderect(coin):
                coins.remove(coin) # Remove the coin when collected
                score += 1 # Increment score

        # Enemy collision with player
        if player_rect.colliderect(enemy):
            game_over = True
            print("doing game over")

        # Fill the screen and draw the player
        screen.fill(WHITE)

        # Draw the player
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        pygame.draw.rect(screen, player_color, player_rect)

        # Draw platforms
        for platform in platforms:
            pygame.draw.rect(screen, GREEN, platform)

        # Draw coins
        for coin in coins:
            pygame.draw.rect(screen, (255, 215, 0), coin) # Gold color

        # Draw enemy
        pygame.draw.rect(screen, (255, 0, 0), enemy) # Red color
        
        # Display score
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))


        pygame.display.flip()
    else:
        print("game over")
        screen.fill(WHITE)
        game_over_text = font.render("Game Over! Press R to Restart", True, (0, 0, 0))
        screen.blit(game_over_text, (WIDTH // 4, HEIGHT // 2))
        pygame.display.flip()
# Quit Pygame
pygame.quit()