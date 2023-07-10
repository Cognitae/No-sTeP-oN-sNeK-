import pygame
from utils import *
from constants import *
from snake import Snake
from fruit import Fruit
from pygame import font, display

FONT = font.Font(None, FONT_SIZE)
WINDOW = display.set_mode((WIDTH, HEIGHT))

high_score = 0  # Initialize high_score

def game_over_screen(score):
    global high_score
    new_high_score = False
    if score > high_score:
        high_score = score
        new_high_score = True

    WINDOW.fill(GRAY)

    lines = [f'GAME OVER', f'Score: {score}', f'High Score: {high_score}', 'Press SPACEBAR Three Times to play again or Q to quit']
    
    if new_high_score:
        lines.insert(1, "New High Score! Congratulations!")
    
    for i, line in enumerate(lines):
        text = FONT.render(line, True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * FONT_SIZE))
        WINDOW.blit(text, text_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                if event.key == pygame.K_q: 
                    pygame.quit()
                    return False  
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

def game_loop():
    # Initialize Pygame
    pygame.init()

    # Set up the display
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('No Step on SNEK!!!') 
    FONT = pygame.font.Font(None, FONT_SIZE)
    line1 = FONT.render('No sTeP oN Sn3k!!!!!!', True, WHITE)
    line2 = FONT.render('Press SPACEBAR to start!', True, WHITE) 

    # Initialize the game state
    snake = Snake([[300, 150], [90, 50], [80, 50]])
    direction = 'RIGHT'
    fruit = generate_fruit(snake.body)  # This is now a Fruit object

    score = 0  # Initialize score
    global game_speed  # Initialize game speed
    game_speed = SNAKE_SPEED  # Reset game speed

    clock = pygame.time.Clock()
    game_started = False
    play_again = False  # Add this line

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_started:
                        game_started = False  # If game is running, pause it
                    elif play_again:
                        return True  # If game is over, start a new game
                    else:
                        game_started = True  # If game is paused, resume it
                if event.key == pygame.K_q:
                    return False  # If 'q' is pressed, quit the game

        keys = pygame.key.get_pressed()
        new_direction = direction
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and direction != 'DOWN':
            new_direction = 'UP'
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and direction != 'UP':
            new_direction = 'DOWN'
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and direction != 'RIGHT':
            new_direction = 'LEFT'
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and direction != 'LEFT':
            new_direction = 'RIGHT'

        direction = new_direction

        if game_started:
            # Move the snake according to the direction
            snake.move(direction)

            if snake.check_collision(fruit):
                # Increase the score
                if fruit.type == 'GOLDEN':
                    score += 100
                elif fruit.type == 'SPECIAL':
                    score += 5
                else:  # 'NORMAL'
                    score += 1
                # Generate new fruit and don't remove the tail of the snake, so it grows
                fruit = generate_fruit(snake.body)  # This is now a Fruit object
                
                # Adjust game speed based on the score
                game_speed = SNAKE_SPEED + (score // 50) * 5
            else:
                # If the snake didn't eat the fruit, move as normal by removing the last segment
                snake.remove_last_segment()
                
            # Check for game over
            if snake.check_game_over():
                play_again = game_over_screen(score)
                if not play_again:
                    return  
                else:
                    game_started = False
                    snake = Snake([[300, 150], [90, 50], [80, 50]])  
                    direction = 'RIGHT'
                    fruit = generate_fruit(snake.body)  # This is now a Fruit object
                    score = 0
            else:
                play_again = False

            # Draw everything
            WINDOW.fill(GRAY)
            draw_snake(WINDOW, snake)
            draw_fruit(WINDOW, fruit)

            # Display the score
            score_text = FONT.render(f'Score: {score}', True, WHITE)
            WINDOW.blit(score_text, (10, 10))  # Display the score at the top left corner
        else:
            WINDOW.fill(BLACK)
            WINDOW.blit(line1, (WIDTH // 2 - line1.get_width() // 2, HEIGHT // 2 - FONT_SIZE))
            WINDOW.blit(line2, (WIDTH // 2 - line2.get_width() // 2, HEIGHT // 2))
            
        pygame.display.update()
        clock.tick(game_speed)  # Use the variable game speed here


if __name__ == "__main__":
    while True:  
        play_again = game_loop()
        if not play_again:
            pygame.quit() 
            break