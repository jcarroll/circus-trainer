# Circus Trainer 8.0
#
# Train your pet to perform at the circus!
#
# Gideon, Miriam, Edwin, and James Carroll
# April 2026

# v.8.0 Required to have sufficient money prior to training or feeding
#       Allows scheduling peformance in MM:SS format
#       Number of tickets sold is variable, with greater liklihood of selling tickets with higher skill and performance levels
#       Training does not require a toy, but having one increases the chance of successful training
#       - No toy: 20%
#       - Ball: 50%
#       - Other toy: 80%
#
# v.7.0 Hunger level changes color
#       Fixed performance financial report
# v.6.0 Different animals perform at different rates
# v.5.0 Performance is scheduled
#       A toy is required to train an animal
#
# Ideas
#   - Larger animals cost more to feed: done (v31)
#   - Larger animals can go longer between feedings (higher hunger levels and higher threshold for able to train)
# 		- different circus tents for performing in
# 		- mini-games to train animal: done (v31)

import random
import time
import pdb
import sys
import pygame

# Initialize Pygame
pygame.init()

# Set up the game window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Circus Trainer")

# Define colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 225)
WHITE = (255, 255, 255)
GREEN = (32, 95, 64)
RED = (255, 0, 0)

# Define game constants
STARTING_MONEY = 50
PERFORMANCE_COST = 10
ANIMAL_HUNGER_INCREASE_RATE = 0.1
HUNGER_CHANCE = 0.05
TRAINING_HUNGER_INCREASE = 1
MINIMUM_SKILL_TO_PERFORM = 5
PERFORMANCE_EVENT = pygame.USEREVENT + 1
MARKETING_EVENT = pygame.USEREVENT + 2

# Define animal types and their properties
ANIMAL_TYPES = {
    "M": {
        "name": "Mouse",
        "feed_cost": 1,
        "cost": 10,
        "trade_in": 0.6,
        "hunger_rate": 0.1,
        "toys": ["Mouse Wheel"],
        "performance_level": 1,
    },
    "C": {
        "name": "Cat",
        "feed_cost": 3,
        "cost": 30,
        "trade_in": 0.6,
        "hunger_rate": 0.2,
        "toys": ["Toy Mouse", "Ball"],
        "performance_level": 3,
    },
    "D": {
        "name": "Dog",
        "cost": 40,
        "feed_cost": 4,
        "trade_in": 0.6,
        "hunger_rate": 0.3,
        "toys": ["Squeaky Ball", "Ball"],
        "performance_level": 5,
    },
    "T": {
        "name": "Turtle",
        "cost": 50,
        "feed_cost": 5,
        "trade_in": 0.6,
        "hunger_rate": 0.1,
        "toys": ["Rock", "Ball"],
        "performance_level": 2,
    },
    "H": {
        "name": "Horse",
        "cost": 200,
        "feed_cost": 20,
        "trade_in": 0.6,
        "hunger_rate": 0.5,
        "toys": ["Hurdles", "Ball"],
        "performance_level": 10,
    },
    "E": {
        "name": "Elephant",
        "cost": 1000,
        "feed_cost": 100,
        "trade_in": 0.6,
        "hunger_rate": 1,
        "toys": ["Tree Trunk", "Ball"],
        "performance_level": 50,
    },
}

# Game state variables
money = STARTING_MONEY
current_animal = "M"
skill_level = 0
animal_hunger = 0
start_time = pygame.time.get_ticks()
performance_time = 0
have_item = 0
training_success_chance = 2
tickets_sold = 0
minigame_sucess = 0


def get_time_input(prompt="Please enter the time in 'mm:ss' format: "):
    """
    Prompts the user to input time in "mm:ss" format and validates the input.

    Returns:
        int: The total number of seconds represented by the input time.
    """
    while True:
        try:
            time_input = input(prompt)
            minutes, seconds = map(int, time_input.split(":"))

            if minutes < 0 or seconds < 0 or seconds >= 60:
                raise ValueError(
                    "Invalid time format. Please enter a valid time in 'mm:ss' format."
                )

            return minutes * 60 + seconds

        except ValueError:
            print("Invalid input. Please enter the time in 'mm:ss' format.")
            continue


# Game functions
def feed_animal():
    global animal_hunger, money
    if money >= ANIMAL_TYPES[current_animal]["feed_cost"]:
        animal_hunger = max(0, animal_hunger - 5)
        money -= ANIMAL_TYPES[current_animal]["feed_cost"]
        print("You fed your animal.")
    else:
        print("You don't have enough money to feed your animal")


class Character:
    def __init__(self):
        self.rect = pygame.Rect(400, 300, 50, 50)

class Snake:
    def __init__(self):
        self.rect = pygame.Rect(
            random.randint(0, width), random.randint(0, height), 50, 50
        )


def train_animal():
    global skill_level, animal_hunger, money
    if animal_hunger < 6:
        width, height = 800, 600
        screen = pygame.display.set_mode((width, height))
        clock = pygame.time.Clock()
        cheese_number = max(1, (round(skill_level / training_success_chance)))

        char = Character()
        snake = Snake()
        cheese = [
            pygame.Rect(
                random.randint(0, width),
                random.randint(0, height),
                30,
                30,
            )
            for _ in range(cheese_number)
        ]
        collected = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    char.rect.topleft = pygame.mouse.get_pos()
                    snake.rect.move_ip(
                        (char.rect.x - snake.rect.x) * 0.05,
                        (char.rect.y - snake.rect.y) * 0.05,
                    )

                    if char.rect.colliderect(snake.rect):
                        print("You died")
                        minigame_success = 0
                        break
                        for c in cheese:
                            pygame.draw.rect(
                                screen, (255, 255, 0), c
                            )
                            pygame.display.flip()
                            clock.tick(60)

                        for c in cheese[:]:
                            if char.rect.colliderect(c):
                                cheese.remove(c)
                                collected += 1
                                if collected == cheese_number:
                                    print("You win")
                                    minigame_success = 1
                                    break
                            screen.fill((0, 0, 0))
                            pygame.draw.rect(
                                screen, (0, 255, 0), char.rect
                            )
                            pygame.draw.rect(
                                screen, (255, 0, 0), snake.rect
                            )

            if minigame_success == 1:
                skill_level += 1
                print(f"Your animal's skill level increased to {skill_level}.")
            else:
                print("Your animal failed to learn anything new.")

    else:
        print("Your animal is too hungry to train.")


def perform():
    global performance_time, start_time
    if pygame.event.peek(PERFORMANCE_EVENT):
        print("You already have a performance scheduled.")
        return
    if skill_level >= MINIMUM_SKILL_TO_PERFORM:
        performance_time = (
            get_time_input(
                "In how many minutes and seconds do you want the performance to start? Please use the format mm:ss"
            )
            * 1000
        )
        pygame.time.set_timer(PERFORMANCE_EVENT, performance_time, 1)
        start_time = pygame.time.get_ticks()
        pygame.time.set_timer(MARKETING_EVENT, 1)
    else:
        print("Your animal is not ready to perform yet.")


def trade_animal():
    global current_animal, money, skill_level
    old_animal = current_animal
    new_animal = ""
    while new_animal not in ANIMAL_TYPES:
        print("\n")
        for a in ANIMAL_TYPES:
            print(f"{a}={ANIMAL_TYPES[a]['name']} Cost: {ANIMAL_TYPES[a]['cost']}")
        new_animal = input("What animal would you like to buy? ").upper()
    trade_in_value = int(
        ANIMAL_TYPES[current_animal]["cost"] * ANIMAL_TYPES[current_animal]["trade_in"]
        + skill_level * ANIMAL_TYPES[current_animal]["trade_in"]
    )
    if money + trade_in_value >= ANIMAL_TYPES[new_animal]["cost"]:
        money += trade_in_value
        money -= ANIMAL_TYPES[new_animal]["cost"]
        current_animal = new_animal
        skill_level = 1
        print(
            f"You traded in your {ANIMAL_TYPES[old_animal]['name']} for ${trade_in_value} and bought a {ANIMAL_TYPES[new_animal]['name']} for ${ANIMAL_TYPES[new_animal]['cost']}."
        )
    else:
        print("You don't have enough money to buy that animal.")


def buy_item():
    global money, animal_hunger, have_item, training_success_chance
    item = input("What item would you like to buy? ").title()
    if item in ANIMAL_TYPES[current_animal]["toys"]:
        cost = ANIMAL_TYPES[current_animal]["toys"].index(item) + 1
        if money >= cost:
            money -= cost
            have_item = 1
            print(f"You bought a {item} for ${cost}.")
            if item is "Ball":
                training_success_chance = 5
            else:
                training_success_chance = 8
        else:
            print("You don't have enough money to buy that item.")
    else:
        print("That is not a valid item for your current animal.")


def update_animal_hunger():
    global animal_hunger
    if random.random() < HUNGER_CHANCE:
        animal_hunger += ANIMAL_TYPES[current_animal]["hunger_rate"]
        animal_hunger = min(10, animal_hunger)


def draw_game_elements():
    # Draw the game status
    font = pygame.font.Font(None, 36)
    text = font.render(f"Money: ${money}", True, BLACK)
    game_window.blit(text, (10, 10))

    text = font.render(
        f"Animal: {ANIMAL_TYPES[current_animal]['name'] if current_animal else 'None'}",
        True,
        BLACK,
    )
    game_window.blit(text, (10, 50))

    text = font.render(f"Skill Level: {skill_level}", True, BLACK)
    game_window.blit(text, (10, 90))

    hunger_color = BLACK
    if animal_hunger < 3:
        hunger_color = GREEN
    elif animal_hunger > 6:
        hunger_color = RED
    text = font.render(f"Hunger Level: {int(animal_hunger)}", True, hunger_color)
    game_window.blit(text, (10, 130))

    elapsed_time = pygame.time.get_ticks() - start_time
    time_left = max(0, performance_time - elapsed_time)
    # Calculate the minutes and seconds
    minutes = (int)(time_left / 1000 // 60)
    seconds = (int)(time_left / 1000 % 60)

    # Format the time remaining
    time_remaining = f"{minutes:02d}:{seconds:02d}"
    text = font.render(f"Time until next performance: " + time_remaining, True, BLACK)
    game_window.blit(text, (10, 170))

    text = font.render(f"Tickets sold: {tickets_sold}", True, BLACK)
    game_window.blit(text, (10, 210))

    # Draw the current animal
    if current_animal:
        animal_image = pygame.image.load(
            f"{ANIMAL_TYPES[current_animal]['name'].lower()}.png"
        )
        game_window.blit(animal_image, (0, 240))


# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == MARKETING_EVENT:
            chance_to_sell = (
                skill_level * ANIMAL_TYPES[current_animal]["performance_level"]
            ) / 100000
            if random.random() < chance_to_sell:
                tickets_sold += 1
        elif event.type == PERFORMANCE_EVENT:
            tickets_sold = 0
            if animal_hunger > 5:
                print(f"your animal is too hungry to perform")
            else:
                money += (
                    tickets_sold * ANIMAL_TYPES[current_animal]["performance_level"]
                    - PERFORMANCE_COST
                )
                print(
                    f"You performed and sold {tickets_sold} tickets for ${ANIMAL_TYPES[current_animal]['performance_level']} each, earning a net profit (or loss) of ${tickets_sold*ANIMAL_TYPES[current_animal]['performance_level'] - PERFORMANCE_COST}."
                )
                # Stop selling tickets
                pygame.event.clear(MARKETING_EVENT)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                feed_animal()
            elif event.key == pygame.K_t:
                train_animal()
            elif event.key == pygame.K_p:
                perform()
            elif event.key == pygame.K_x:
                trade_animal()
            elif event.key == pygame.K_b:
                buy_item()

    # Update game state
    update_animal_hunger()

    # Clear the game window
    game_window.fill(WHITE)

    # Draw the game elements
    draw_game_elements()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
