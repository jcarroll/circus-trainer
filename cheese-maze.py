import random
import time
import sys

# Maze sizes for each difficulty level
MAZE_SIZES = {
    'easy': (20, 20),
    'medium': (40, 40),
    'hard': (100, 100)
}

# Time limits for each difficulty level (in seconds)
TIME_LIMITS = {
    'easy': 60,
    'medium': 120,
    'hard': 300
}

# Symbols used in the maze
WALL = '#'
CHEESE = 'C'
MOUSE = 'M'
EMPTY = '.'

def create_maze(width, height):
    """
    Create a new maze with the given dimensions.
    The maze is represented as a 2D list, where each element is a string representing a square.
    """
    maze = [[WALL for _ in range(width)] for _ in range(height)]
    
    # Place the cheese in a random location
    cheese_x = random.randint(1, width - 2)
    cheese_y = random.randint(1, height - 2)
    maze[cheese_y][cheese_x] = CHEESE
    
    # Place the mouse in a random location, not on the cheese
    mouse_x = random.randint(1, width - 2)
    mouse_y = random.randint(1, height - 2)
    while (mouse_x, mouse_y) == (cheese_x, cheese_y):
        mouse_x = random.randint(1, width - 2)
        mouse_y = random.randint(1, height - 2)
    maze[mouse_y][mouse_x] = MOUSE
    
    return maze

def display_maze(maze, revealed_squares):
    """
    Display the current state of the maze, revealing only the squares that have been visited.
    """
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if (x, y) in revealed_squares:
                print(maze[y][x], end='')
            else:
                print(EMPTY, end='')
        print()

def get_visible_squares(maze, mouse_x, mouse_y, radius=3):
    """
    Get the set of squares that are visible from the mouse's current position.
    The mouse can only see squares within the given radius, and only in directions that are not blocked by walls.
    """
    visible_squares = set()
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            if abs(dx) + abs(dy) <= radius:
                x = mouse_x + dx
                y = mouse_y + dy
                if 0 <= x < len(maze[0]) and 0 <= y < len(maze):
                    if maze[y][x] != WALL:
                        visible_squares.add((x, y))
    return visible_squares

def play_game(difficulty):
    """
    Play the cheese maze game at the given difficulty level.
    Returns True if the mouse reaches the cheese before the time runs out, False otherwise.
    """
    width, height = MAZE_SIZES[difficulty]
    time_limit = TIME_LIMITS[difficulty]
    
    maze = create_maze(width, height)
    revealed_squares = set()
    mouse_x, mouse_y = next((x, y) for y, row in enumerate(maze) for x, cell in enumerate(row) if cell == MOUSE)
    
    start_time = time.time()
    while True:
        # Display the current state of the maze
        display_maze(maze, revealed_squares)
        
        # Check if the mouse has reached the cheese
        if maze[mouse_y][mouse_x] == CHEESE:
            print("Congratulations! You found the cheese!")
            return True
        
        # Check if the time has run out
        elapsed_time = time.time() - start_time
        if elapsed_time > time_limit:
            print("Time's up! You didn't find the cheese.")
            return False
        
        # Get the user's input for the mouse's movement
        move = input("Use the arrow keys to move the mouse: ")
        if move == 'up':
            mouse_y = max(mouse_y - 1, 0)
        elif move == 'down':
            mouse_y = min(mouse_y + 1, height - 1)
        elif move == 'left':
            mouse_x = max(mouse_x - 1, 0)
        elif move == 'right':
            mouse_x = min(mouse_x + 1, width - 1)
        else:
            print("Invalid input. Please try again.")
            continue
        
        # Update the revealed squares
        visible_squares = get_visible_squares(maze, mouse_x, mouse_y)
        revealed_squares.update(visible_squares)
        
        # Clear the screen and move the cursor to the top-left
        print('\033[H\033[J', end='')

def main():
    """
    Main function to run the cheese maze game.
    Prompts the user to select a difficulty level and plays the game.
    """
    print("Welcome to the Cheese Maze Game!")
    print("Select a difficulty level:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    
    while True:
        choice = input("Enter your choice (1-3): ")
        if choice in ['1', '2', '3']:
            difficulty = ['easy', 'medium', 'hard'][int(choice) - 1]
            break
        else:
            print("Invalid choice. Please try again.")
    
    result = play_game(difficulty)
    if result:
        sys.exit(0)  # Exit with a "true" return code
    else:
        sys.exit(1)  # Exit with a "false" return code

if __name__ == "__main__":
    main()