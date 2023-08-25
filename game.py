import pygame
import os
from utils import *
from constants import *
from snake import Snake
from fruit import Fruit
from animations import Animation
from pygame import font, display

FONT = font.Font(None, FONT_SIZE)
WINDOW = display.set_mode((WIDTH, HEIGHT))

high_score = 0  # Initialize high_score

def game_over_screen(score, fruit_tally):
    global high_score
    new_high_score = False
    if score > high_score:
        high_score = score
        new_high_score = True

    # Calculate the grind score and luck factor
    total_fruits = sum(fruit_tally.values())  
    grind_score = score / total_fruits if total_fruits > 0 else 1
    luck_factor = ((fruit_tally['SPECIAL'] + fruit_tally['GOLDEN'] * 10) / total_fruits) * 100 if total_fruits > 0 else 0
    true_score = high_score // grind_score

    WINDOW.fill(GRAY)

    lines = [f'GAME OVER', f'Score: {score}', f'High Score: {high_score}', f'True Score: {int(true_score)}', f'Luck Factor: {luck_factor:.2f}%', f'Press SPACEBAR to play again', 'Press Q to quit']
    
    if new_high_score:
        lines.insert(1, "New High Score! Congratulations!")
    
    for i, line in enumerate(lines):
        text = FONT.render(line, True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, (HEIGHT // 2 - len(lines) // 2 * FONT_SIZE) + i * FONT_SIZE))
        WINDOW.blit(text, text_rect)

    # Draw the fruit tally
    pygame.draw.rect(WINDOW, RED, pygame.Rect(WIDTH // 2 - 70, HEIGHT // 2 + len(lines) * FONT_SIZE, 20, 20))  # Draw a red square
    WINDOW.blit(FONT.render(f'{fruit_tally["NORMAL"]}', True, WHITE), (WIDTH // 2 - 45, HEIGHT // 2 + len(lines) * FONT_SIZE))  # Display the red fruit tally

    pygame.draw.rect(WINDOW, BLUE, pygame.Rect(WIDTH // 2 - 20, HEIGHT // 2 + len(lines) * FONT_SIZE, 20, 20))  # Draw a blue square
    WINDOW.blit(FONT.render(f'{fruit_tally["SPECIAL"]}', True, WHITE), (WIDTH // 2 + 5, HEIGHT // 2 + len(lines) * FONT_SIZE))  # Display the blue fruit tally

    pygame.draw.rect(WINDOW, GOLD, pygame.Rect(WIDTH // 2 + 30, HEIGHT // 2 + len(lines) * FONT_SIZE, 20, 20))  # Draw a golden square
    WINDOW.blit(FONT.render(f'{fruit_tally["GOLDEN"]}', True, WHITE), (WIDTH // 2 + 55, HEIGHT // 2 + len(lines) * FONT_SIZE))  # Display the gold fruit tally

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
    line1_font = pygame.font.Font(None, FONT_SIZE * 3) # Create a new font object with a larger font size for line1
    line1 = line1_font.render('No sTeP oN Sn3k!!!!!!', True, GREEN) # Use the new font object to render line1
    line2 = FONT.render('Press SPACEBAR to start!', True, WHITE) 
    line3 = FONT.render('Press Q to quit!', True, WHITE)
    
    # Load Title image
    script_dir = os.path.dirname(os.path.abspath(__file__)) # Absolute directory the script is in
    image_path = os.path.join(script_dir, 'Resources', 'Snek_Marine.jpg')
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (200, 200)) # Replace with your desired size

    # Initialize the game state
    snake = Snake([[300, 150], [90, 50], [80, 50]])
    direction = 'RIGHT'
    fruit = generate_fruit(snake.body)  # This is now a Fruit object

    score = 0  # Initialize score
    global game_speed  # Initialize game speed
    game_speed = SNAKE_SPEED  # Reset game speed

    # Initialize the fruit tally
    fruit_tally = {'NORMAL': 0, 'SPECIAL': 0, 'GOLDEN': 0}

    clock = pygame.time.Clock()
    game_started = False
    game_paused = False
    game_over = False
    play_again = False  # Add this line
    
    # Initialize a list to hold active animations
    animations = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("Spacebar pressed")
                    if not game_started and not game_over and not play_again:
                        game_started = True
                        print("Game started")
                    elif game_started and not game_paused:
                        game_paused = True
                        print("Game paused")
                    elif game_paused:
                        game_paused = False
                        print("Game resumed")
                    elif play_again:
                        game_started = True
                        game_over = False
                        play_again = False
                        print("Game restarted")
                if event.key == pygame.K_q:
                    return False

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

        if game_started and not game_paused:
            # Move the snake according to the direction
            snake.move(direction)

            if snake.check_collision(fruit):
                # Increase the score
                score_increase = 0
                color = None
                if fruit.type == 'GOLDEN':
                    score_increase = 100
                    color = GOLD
                elif fruit.type == 'SPECIAL':
                    score_increase = 5
                    color = BLUE
                else:  # 'NORMAL'
                    score_increase = 1
                    color = RED

                score += score_increase
                fruit_tally[fruit.type] += 1

                # Add animation
                animations.append(Animation(f'+{score_increase}', fruit.position.copy(), color))
                # Generate new fruit and don't remove the tail of the snake, so it grows
                fruit = generate_fruit(snake.body)  # This is now a Fruit object
                
                # Adjust game speed based on the score
                game_speed = SNAKE_SPEED + (score // 50) * 5
            else:
                # If the snake didn't eat the fruit, move as normal by removing the last segment
                snake.remove_last_segment()
                
            if snake.check_game_over():
                game_over = True
                play_again = game_over_screen(score, fruit_tally)  # Pass fruit_tally to game_over_screen
                if not play_again:
                    return  
                else:
                    snake = Snake([[300, 150], [90, 50], [80, 50]])  
                    direction = 'RIGHT'
                    fruit = generate_fruit(snake.body)  # This is now a Fruit object
                    score = 0
                    game_speed = SNAKE_SPEED
                    fruit_tally = {'NORMAL': 0, 'SPECIAL': 0, 'GOLDEN': 0}  # Reset fruit tally here
            else:
                play_again = False

            # Draw everything
            WINDOW.fill(GRAY)
            draw_snake(WINDOW, snake)
            draw_fruit(WINDOW, fruit)
            
            # Draw animations
            for anim in animations:
                if not anim.draw(WINDOW):
                    animations.remove(anim)
                    
            # Display the fruit tally
            red_text = FONT.render(f'{fruit_tally["NORMAL"]}', True, WHITE)
            pygame.draw.rect(WINDOW, RED, pygame.Rect(WIDTH - 150, 10, 20, 20))  # Draw a red square
            WINDOW.blit(red_text, (WIDTH - 125, 10))  # Display the red fruit tally

            blue_text = FONT.render(f'{fruit_tally["SPECIAL"]}', True, WHITE)
            pygame.draw.rect(WINDOW, BLUE, pygame.Rect(WIDTH - 100, 10, 20, 20))  # Draw a blue square
            WINDOW.blit(blue_text, (WIDTH - 75, 10))  # Display the blue fruit tally

            gold_text = FONT.render(f'{fruit_tally["GOLDEN"]}', True, WHITE)
            pygame.draw.rect(WINDOW, GOLD, pygame.Rect(WIDTH - 50, 10, 20, 20))  # Draw a golden square
            WINDOW.blit(gold_text, (WIDTH - 25, 10))  # Display the gold fruit tally


            # Draw a border below the score and fruit tally
            pygame.draw.line(WINDOW, WHITE, (0, FONT_SIZE + 20), (WIDTH, FONT_SIZE + 20), 2)


            # Display the score
            score_text = FONT.render(f'Score: {score}', True, WHITE)
            WINDOW.blit(score_text, (10, 10))  # Display the score at the top left corner
        elif game_paused:
            # You can add a "game paused" screen here if you want
            pass
        
        else:
            WINDOW.fill(BLACK)
            WINDOW.blit(line1, (WIDTH // 2 - line1.get_width() // 2, HEIGHT // 6.00 - FONT_SIZE))
            # Blit the image in the middle of line1 and line2
            WINDOW.blit(image, (WIDTH // 2 - image.get_width() // 2, HEIGHT // 2 - image.get_height() // 2))
            WINDOW.blit(line2, (WIDTH // 2 - line2.get_width() // 2, HEIGHT // 1.25))
            WINDOW.blit(line3, (WIDTH // 2 - line3.get_width() // 2, HEIGHT // 1.25 + FONT_SIZE))

            
        pygame.display.update()
        clock.tick(game_speed)  # Use the variable game speed here

if __name__ == "__main__":
    while True:  
        play_again = game_loop()
        if not play_again:
            pygame.quit() 
            break
