import os
import sys
import time
import random

# Define the maze dimensions
MAZE_WIDTH = 10
MAZE_HEIGHT = 10

# Define the player's starting position
player_x = 0
player_y = 0

# Define the prize's position
prize_x = random.randint(1, MAZE_WIDTH - 2)
prize_y = random.randint(1, MAZE_HEIGHT - 2)

# Define the maze as a 2D list
maze = [['-' for x in range(MAZE_WIDTH)] for y in range(MAZE_HEIGHT)]

# Place the player in the maze
maze[player_y][player_x] = 'P'

# Place the prize in the maze
maze[prize_y][prize_x] = 'X'

# Function to clear the console
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to display the maze
def display_maze():
    clear_console()
    for row in maze:
        print(' '.join(row))
    print(f"\nPlayer's position: ({player_x}, {player_y})")

# Function to move the player
def move_player(dx, dy):
    global player_x, player_y

    # Clear the player's previous position
    maze[player_y][player_x] = '-'

    # Update the player's position
    player_x += dx
    player_y += dy

    # Ensure the player stays within the maze boundaries
    player_x = max(0, min(player_x, MAZE_WIDTH - 1))
    player_y = max(0, min(player_y, MAZE_HEIGHT - 1))

    # Place the player in the new position
    maze[player_y][player_x] = 'P'

    # Check if the player has found the prize
    if player_x == prize_x and player_y == prize_y:
        print("Congratulations! You found the prize!")
        sys.exit()

# Game loop
while True:
    display_maze()

    # Get the user's input
    user_input = input("Use the arrow keys to move (or 'q' to quit): ")

    # Move the player based on the user's input
    if user_input == 'q':
        break
    elif user_input == 'w' or user_input == '\x1b[A':
        move_player(0, -1)
    elif user_input == 's' or user_input == '\x1b[B':
        move_player(0, 1)
    elif user_input == 'a' or user_input == '\x1b[D':
        move_player(-1, 0)
    elif user_input == 'd' or user_input == '\x1b[C':
        move_player(1, 0)