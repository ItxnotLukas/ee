import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
TEXT_COLOR = (255, 255, 255)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Initialize snake and food
snake = [(5, 5)]
direction = (1, 0)

# Define the border as a list of rectangles
border = [
    pygame.Rect(0, 0, WIDTH, GRID_SIZE),               # Top border
    pygame.Rect(0, 0, GRID_SIZE, HEIGHT),             # Left border
    pygame.Rect(0, HEIGHT - GRID_SIZE, WIDTH, GRID_SIZE),  # Bottom border
    pygame.Rect(WIDTH - GRID_SIZE, 0, GRID_SIZE, HEIGHT)  # Right border
]

# Generate initial food position
def generate_food_position():
    while True:
        food_pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if food_pos not in snake and food_pos not in [rect.topleft for rect in border]:
            return food_pos

food = generate_food_position()

# Game states
PLAYING = 0
GAME_OVER = 1
RESTART = 2
current_state = PLAYING

# Game over and restart backgrounds
game_over_background = pygame.Surface((WIDTH, HEIGHT))
game_over_background.set_alpha(200)
game_over_background.fill((0, 0, 0))
restart_background = pygame.Surface((200, 60))
restart_background.set_alpha(200)
restart_background.fill(GREEN)

# Fonts
font = pygame.font.Font(None, 36)

# Score
score = 0

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif current_state == PLAYING:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    direction = (0, 1)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    direction = (1, 0)
        elif current_state == GAME_OVER:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    current_state = RESTART
        elif current_state == RESTART:
            current_state = PLAYING
            snake = [(5, 5)]
            direction = (1, 0)
            food = generate_food_position()
            score = 0

    if current_state == PLAYING:
        # Update snake position
        x, y = snake[0]
        new_head = (x + direction[0], y + direction[1])

        # Check for collisions with the border
        if new_head == food:
            snake.insert(0, food)
            food = generate_food_position()
            score += 10  # Increase the score by 10 points when food is eaten
        elif (
            new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
            new_head in [segment for segment in snake[1:]] or
            any(segment.colliderect(new_head[0] * GRID_SIZE, new_head[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE) for segment in border)
        ):
            current_state = GAME_OVER
        else:
            snake.insert(0, new_head)
            snake.pop()

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the border
        for segment in border:
            pygame.draw.rect(screen, RED, segment)

        # Draw food as a detailed rectangle
        pygame.draw.rect(screen, RED, (food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Draw snake as a detailed rectangle
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Display the score
        score_text = font.render(f"Punkte: {score}", True, TEXT_COLOR)
        screen.blit(score_text, (10, 10))

    elif current_state == GAME_OVER:
        # Display game over message with textured background
        screen.blit(game_over_background, (0, 0))
        game_over_text = font.render("Game Over", True, TEXT_COLOR)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))

        # Create textured "Restart" button
        restart_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 60)
        pygame.draw.rect(screen, GREEN, restart_button)
        screen.blit(restart_background, (restart_button.x, restart_button.y))
        restart_text = font.render("Restart", True, TEXT_COLOR)
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 65))

    # Update the display
    pygame.display.flip()

    # Control game speed
    clock.tick(10)  # Adjust the speed as needed

# Quit Pygame
pygame.quit()
