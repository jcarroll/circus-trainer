import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Cheese Chase")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define game objects
CHEESE_CHAR = 'C'
MOUSE_CHAR = 'M'
SNAKE_CHAR = '#'

# Define game variables
cheese_count = random.randint(1, 10)
cheese_list = []
mouse_x = WINDOW_WIDTH // 2
mouse_y = WINDOW_HEIGHT // 2
snake_x = random.randint(0, WINDOW_WIDTH)
snake_y = random.randint(0, WINDOW_HEIGHT)
snake_speed = 2
mouse_speed = 3
game_over = False
win = False

# Function to draw the game objects
def draw_game_objects():
    # Draw cheese
    for cheese in cheese_list:
        pygame.draw.rect(screen, WHITE, (cheese[0], cheese[1], 10, 10))
        screen.blit(font.render(CHEESE_CHAR, True, WHITE), (cheese[0], cheese[1]))

    # Draw mouse
    pygame.draw.rect(screen, WHITE, (mouse_x, mouse_y, 10, 10))
    screen.blit(font.render(MOUSE_CHAR, True, BLACK), (mouse_x, mouse_y))

    # Draw snake
    for i in range(5):
        pygame.draw.rect(screen, WHITE, (snake_x - i * 10, snake_y, 10, 10))
        screen.blit(font.render(SNAKE_CHAR, True, BLACK), (snake_x - i * 10, snake_y))

# Game loop
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Move the mouse
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and mouse_y > 0:
        mouse_y -= mouse_speed
    if keys[pygame.K_DOWN] and mouse_y < WINDOW_HEIGHT - 10:
        mouse_y += mouse_speed
    if keys[pygame.K_LEFT] and mouse_x > 0:
        mouse_x -= mouse_speed
    if keys[pygame.K_RIGHT] and mouse_x < WINDOW_WIDTH - 10:
        mouse_x += mouse_speed

    # Move the snake
    if snake_x > mouse_x:
        snake_x -= snake_speed
    elif snake_x < mouse_x:
        snake_x += snake_speed
    if snake_y > mouse_y:
        snake_y -= snake_speed
    elif snake_y < mouse_y:
        snake_y += snake_speed

    # Check for cheese collection
    for i, cheese in enumerate(cheese_list):
        if abs(cheese[0] - mouse_x) < 10 and abs(cheese[1] - mouse_y) < 10:
            cheese_list.pop(i)
            cheese_count -= 1

    # Check for game over conditions
    if cheese_count == 0:
        win = True
        game_over = True
    if abs(snake_x - mouse_x) < 10 and abs(snake_y - mouse_y) < 10:
        game_over = True

    # Clear the screen
    screen.fill(BLACK)

    # Draw the game objects
    draw_game_objects()

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

# Display the game result
if win:
    result_text = "You win!"
else:
    result_text = "You lose!"

result_surface = font.render(result_text, True, WHITE)
result_rect = result_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
screen.blit(result_surface, result_rect)
pygame.display.flip()

# Wait for the user to close the window
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()