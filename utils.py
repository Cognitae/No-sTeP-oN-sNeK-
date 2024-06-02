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
    color_map = {
        'GOLDEN': GOLD,
        'SPECIAL': BLUE,
        'NORMAL': RED
    }
    color = color_map.get(fruit.type, RED)
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

def generate_fruit(snake_body, special=False):
    while True:
        x_pos = random.randrange(0, WIDTH - SNAKE_SIZE, SNAKE_SIZE)
        y_pos = random.randrange(FONT_SIZE + 20, HEIGHT - SNAKE_SIZE, SNAKE_SIZE)
        position = [x_pos, y_pos]

        fruit_rect = pygame.Rect(x_pos, y_pos, SNAKE_SIZE, SNAKE_SIZE)
        
        # Check if the fruit's area collides with any part of the snake's body
        collision = False
        for segment in snake_body:
            segment_rect = pygame.Rect(segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE)
            if fruit_rect.colliderect(segment_rect):
                collision = True
                break
        
        if not collision:
            break

    if special:
        fruit_type = random.choices(['SPECIAL', 'GOLDEN'], [0.9, 0.1])[0]
    else:
        fruit_type = random.choices(['NORMAL', 'SPECIAL', 'GOLDEN'], [0.8, 0.15, 0.05])[0]

    print(f"Generated fruit: {fruit_type} at position {position}")
    
    return Fruit(position, fruit_type)

def generate_additional_red_fruit(snake_body, special_fruit_position):
    while True:
        x_pos = random.randrange(0, WIDTH - SNAKE_SIZE, SNAKE_SIZE)
        y_pos = random.randrange(FONT_SIZE + 20, HEIGHT - SNAKE_SIZE, SNAKE_SIZE)
        position = [x_pos, y_pos]

        fruit_rect = pygame.Rect(x_pos, y_pos, SNAKE_SIZE, SNAKE_SIZE)
        special_fruit_rect = pygame.Rect(special_fruit_position[0], special_fruit_position[1], SNAKE_SIZE, SNAKE_SIZE)
        
        # Check if the fruit's area collides with any part of the snake's body or the special fruit
        collision = False
        for segment in snake_body:
            segment_rect = pygame.Rect(segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE)
            if fruit_rect.colliderect(segment_rect) or fruit_rect.colliderect(special_fruit_rect):
                collision = True
                break
        
        if not collision:
            break

    print(f"Generated additional red fruit at position {position}")
    
    return Fruit(position, 'NORMAL')

def animate_score_increase(score_increase, x, y):
    for size in range(20, 40, 2):  # This will create a zoom-in effect
        font = pygame.font.Font(None, size)
        text = font.render(f'+{score_increase}', True, WHITE)
        WINDOW.blit(text, (x, y))
        pygame.display.update()
        pygame.time.wait(50)  # Wait a little bit before drawing the next frame
