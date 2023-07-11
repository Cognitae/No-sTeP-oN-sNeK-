import pygame
from constants import *
import random
from collections import namedtuple 

# Create a namedtuple to represent fruits
Fruit = namedtuple('Fruit', ['position', 'type'])

def draw_snake(WINDOW, snake):
    for unit in snake.body:  # Use snake.body instead of snake
        pygame.draw.rect(WINDOW, GREEN, pygame.Rect(unit[0], unit[1], SNAKE_SIZE, SNAKE_SIZE))

def move_snake(snake, direction):
    if direction == 'RIGHT':
        snake.insert(0, [snake[0][0] + SNAKE_SIZE, snake[0][1]])
    elif direction == 'LEFT':
        snake.insert(0, [snake[0][0] - SNAKE_SIZE, snake[0][1]])
    elif direction == 'UP':
        snake.insert(0, [snake[0][0], snake[0][1] - SNAKE_SIZE])
    elif direction == 'DOWN':
        snake.insert(0, [snake[0][0], snake[0][1] + SNAKE_SIZE])

def draw_fruit(WINDOW, fruit):
    if fruit.type == 'GOLDEN':
        color = GOLD
    elif fruit.type == 'SPECIAL':
        color = BLUE
    else:  # 'NORMAL'
        color = RED
    pygame.draw.rect(WINDOW, color, pygame.Rect(fruit.position[0], fruit.position[1], SNAKE_SIZE, SNAKE_SIZE))


def check_collision(snake, fruit):
    # Check if the head of the snake is within the fruit rectangle
    head_rect = pygame.Rect(snake[0][0], snake[0][1], SNAKE_SIZE, SNAKE_SIZE)
    fruit_rect = pygame.Rect(fruit.position[0], fruit.position[1], SNAKE_SIZE, SNAKE_SIZE)
    return head_rect.colliderect(fruit_rect)

def check_game_over(snake):
    # Check if snake is out of bounds
    if (snake[0][0] >= WIDTH or 
        snake[0][0] < 0 or 
        snake[0][1] >= HEIGHT or 
        snake[0][1] < 0):
        return True
    # Check if snake has collided with itself
    if snake[0] in snake[1:]:
        return True
    return False

def generate_fruit(snake_body):
    all_positions = [[x, y] for x in range(0, WIDTH, SNAKE_SIZE) for y in range(0, HEIGHT, SNAKE_SIZE)]
    free_positions = [pos for pos in all_positions if pos not in snake_body]
    position = random.choice(free_positions)
    random_number = random.random()  # Generate a random number between 0 and 1
    if random_number < 0.01:  # 1% chance the fruit is golden
        fruit_type = 'GOLDEN'
    elif random_number < 0.11:  # 10% chance the fruit is special (but not golden)
        fruit_type = 'SPECIAL'
    else:  # 89% chance the fruit is normal
        fruit_type = 'NORMAL'
    return Fruit(position, fruit_type)  # Return a Fruit object

def animate_score_increase(score_increase, x, y):
    for size in range(20, 40, 2):  # This will create a zoom-in effect
        font = pygame.font.Font(None, size)
        text = font.render(f'+{score_increase}', True, WHITE)
        WINDOW.blit(text, (x, y))
        pygame.display.update()
        pygame.time.wait(50)  # Wait a little bit before drawing the next frame
