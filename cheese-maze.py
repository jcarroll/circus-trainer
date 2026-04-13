import time
import random
import sys

# Define the maze sizes and time limits for each difficulty level
MAZE_SIZES = [(20, 20), (40, 40), (100, 100)]
TIME_LIMITS = [60, 45, 30]

# Define the symbols used in the maze
MOUSE = 'M'
CHEESE = 'C'
WALL = '#'
EMPTY = ' '

def create_maze(size):
    """
    Create a maze of the given size.
    The maze is represented as a 2D list, where each element is a string representing a cell.
    """
    maze = [[WALL for _ in range(size[1])] for _ in range(size[0])]

    # Place the mouse and cheese randomly
    mouse_x = random.randint(0, size[0] - 1)
    mouse_y = random.randint(0, size[1] - 1)
    maze[mouse_x][mouse_y] = MOUSE

    cheese_x = random.randint(0, size[0] - 1)
    cheese_y = random.randint(0, size[1] - 1)
    while maze[cheese_x][cheese_y] != EMPTY:
        cheese_x = random.randint(0, size[0] - 1)
        cheese_y = random.randint(0, size[1] - 1)
    maze[cheese_x][cheese_y] = CHEESE

    # Fill the rest of the maze with empty cells
    for i in range(size[0]):
        for j in range(size[1]):
            if maze[i][j] == EMPTY:
                maze[i][j] = EMPTY

    return maze

def display_maze(maze):
    """
    Print the maze to the console.
    """
    for row in maze:
        print(''.join(row))

def move_mouse(maze, mouse_x, mouse_y, dx, dy):
    """
    Move the mouse in the maze based on the given direction.
    Return the new mouse position if the move is valid, or the original position if the move is not valid.
    """
    new_x = mouse_x + dx
    new_y = mouse_y + dy

    if 0 <= new_x < len(maze) and 0 <= new_y < len(maze[0]) and maze[new_x][new_y] != WALL:
        maze[mouse_x][mouse_y] = EMPTY
        maze[new_x][new_y] = MOUSE
        return new_x, new_y
    else:
        return mouse_x, mouse_y

def play_game(difficulty):
    """
    Play the cheese maze game at the given difficulty level.
    Return True if the player finds the cheese before the time runs out, False otherwise.
    """
    maze_size = MAZE_SIZES[difficulty]
    time_limit = TIME_LIMITS[difficulty]

    maze = create_maze(maze_size)
    display_maze(maze)

    # Find the initial mouse position
    for i in range(maze_size[0]):
        for j in range(maze_size[1]):
            if maze[i][j] == MOUSE:
                mouse_x, mouse_y = i, j
                break

    start_time = time.time()
    while True:
        # Check if the time has run out
        if time.time() - start_time >= time_limit:
            print("Time's up! You didn't find the cheese.")
            return False

        # Get the user's input
        key = input("Use the cursor keys to move the mouse. Press Enter to quit: ")

        # Move the mouse based on the user's input
        if key == '\x1b[A':  # Up
            mouse_x, mouse_y = move_mouse(maze, mouse_x, mouse_y, -1, 0)
        elif key == '\x1b[B':  # Down
            mouse_x, mouse_y = move_mouse(maze, mouse_x, mouse_y, 1, 0)
        elif key == '\x1b[C':  # Right
            mouse_x, mouse_y = move_mouse(maze, mouse_x, mouse_y, 0, 1)
        elif key == '\x1b[D':  # Left
            mouse_x, mouse_y = move_mouse(maze, mouse_x, mouse_y, 0, -1)
        elif key == '':
            print("You quit the game.")
            return False

        # Check if the mouse has found the cheese
        if maze[mouse_x][mouse_y] == CHEESE:
            print("Congratulations! You found the cheese.")
            return True

        # Clear the console and redisplay the maze
        sys.stdout.write("\033[H\033[J")
        display_maze(maze)

def main():
    """
    Main function to run the cheese maze game.
    """
    print("Welcome to the Cheese Maze Game!")
    print("Choose a difficulty level:")
    print("1. Easy")
    print("2. Medium")
    print("3. Difficult")

    while True:
        try:
            difficulty = int(input("Enter 1, 2, or 3: ")) - 1
            if 0 <= difficulty <= 2:
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    if play_game(difficulty):
        print("You won the game!")
    else:
        print("You lost the game.")

if __name__ == "__main__":
    main()