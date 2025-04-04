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

def save_score_screen(score, true_score):
    name = ""
    while True:
        WINDOW.fill(GRAY)
        prompt = FONT.render("Enter your name: " + name, True, WHITE)
        WINDOW.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 - FONT_SIZE))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

def display_high_scores(high_scores, high_true_scores):
    scroll_offset = 0
    max_display = (HEIGHT // FONT_SIZE) - 4  # Calculate the maximum number of scores that can be displayed

    while True:
        WINDOW.fill(GRAY)
        title = FONT.render("High Scores", True, WHITE)
        WINDOW.blit(title, (WIDTH // 4 - title.get_width() // 2, FONT_SIZE))

        for i, (name, score) in enumerate(high_scores[scroll_offset:scroll_offset + max_display]):
            text = FONT.render(f"{scroll_offset + i + 1}. {name}: {score}", True, WHITE)
            WINDOW.blit(text, (WIDTH // 4 - text.get_width() // 2, FONT_SIZE * (i + 2)))

        title = FONT.render("High True Scores", True, WHITE)
        WINDOW.blit(title, (3 * WIDTH // 4 - title.get_width() // 2, FONT_SIZE))

        for i, (name, true_score) in enumerate(high_true_scores[scroll_offset:scroll_offset + max_display]):
            text = FONT.render(f"{scroll_offset + i + 1}. {name}: {true_score}", True, WHITE)
            WINDOW.blit(text, (3 * WIDTH // 4 - text.get_width() // 2, FONT_SIZE * (i + 2)))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                if event.key == pygame.K_q:
                    pygame.quit()
                    return False
                if event.key == pygame.K_DOWN:
                    if scroll_offset + max_display < max(len(high_scores), len(high_true_scores)):
                        scroll_offset += 1
                if event.key == pygame.K_UP:
                    if scroll_offset > 0:
                        scroll_offset -= 1
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

def game_over_screen(score, fruit_tally, true_score, special_spawn_count, golden_spawn_count):
    global high_score
    new_high_score = False
    if score > high_score:
        high_score = score
        new_high_score = True

    # Calculate the grind score and luck factor
    total_fruits = sum(fruit_tally.values()) + special_spawn_count + golden_spawn_count
    luck_factor = ((special_spawn_count + golden_spawn_count * 10) / total_fruits) * 100 if total_fruits > 0 else 0

    WINDOW.fill(GRAY)

    lines = [f'GAME OVER', f'Score: {score}', f'High Score: {high_score}', f'True Score: {int(true_score)}', f'Luck Factor: {luck_factor:.2f}%', f'Press SPACEBAR to play again', 'Press Q to quit', 'Press S to save score']
    
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
                if event.key == pygame.K_s:
                    name = save_score_screen(score, true_score)
                    if name:
                        high_scores = load_high_scores()
                        high_scores["high_scores"].append((name, score))
                        high_scores["high_true_scores"].append((name, true_score))
                        high_scores["high_scores"].sort(key=lambda x: x[1], reverse=True)
                        high_scores["high_true_scores"].sort(key=lambda x: x[1], reverse=True)
                        save_high_scores(high_scores)
                        display_high_scores(high_scores["high_scores"], high_scores["high_true_scores"])
                        return True
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
    line1_font = pygame.font.Font(None, FONT_SIZE * 3)  # Create a new font object with a larger font size for line1
    line1 = line1_font.render('No sTeP oN Sn3k!!!!!!', True, GREEN)  # Use the new font object to render line1
    line2 = FONT.render('Press SPACEBAR to start!', True, WHITE)
    line3 = FONT.render('Press Q to quit!', True, WHITE)
    line4 = FONT.render('Press A to watch AI play!', True, WHITE)  # Add new option for AI
    
    # Load Title image
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Absolute directory the script is in
    image_path = os.path.join(script_dir, 'Resources', 'Snek_Marine.jpg')
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (200, 200))  # Replace with your desired size

    # Initialize the game state
    snake = Snake([[300, 150], [90, 50], [80, 50]])
    direction = 'RIGHT'
    fruit = generate_fruit(snake.body)  # This is now a Fruit object
    additional_fruit = None

    special_spawn_count = 0
    golden_spawn_count = 0

    if fruit.type in ['GOLDEN', 'SPECIAL']:
        additional_fruit = generate_additional_red_fruit(snake.body, fruit.position)
        if fruit.type == 'SPECIAL':
            special_spawn_count += 1
        elif fruit.type == 'GOLDEN':
            golden_spawn_count += 1

    score = 0  # Initialize score
    true_score = 0  # Initialize true score
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
                if event.key == pygame.K_a and not game_started:  # New key handler for AI
                    try:
                        from snake_ai import watch_ai_play
                        watch_ai_play(model_path='snake_ai_model_grinder.keras')  # Updated model path to .keras
                    except ImportError:
                        print("AI module not found. Please run 'pip install tensorflow' and train the AI first.")
                    except FileNotFoundError:
                        print("AI model file 'snake_ai_model_grinder.keras' not found. Train the AI first by running 'snake_ai.py'.")
                    except Exception as e:
                        print(f"Error launching AI: {e}")

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
                    true_score += 1  # Increase true score for golden fruit
                elif fruit.type == 'SPECIAL':
                    score_increase = 5
                    color = BLUE
                    true_score += 1  # Increase true score for special fruit
                else:  # 'NORMAL'
                    score_increase = 1
                    color = RED
                    true_score += 1  # Increase true score for normal fruit

                score += score_increase
                fruit_tally[fruit.type] += 1

                # Add animation
                animations.append(Animation(f'+{score_increase}', fruit.position.copy(), color))

                # Generate new fruit
                fruit = generate_fruit(snake.body)
                if fruit.type in ['GOLDEN', 'SPECIAL']:
                    print("Special or golden fruit eaten. Generating additional red fruit.")
                    additional_fruit = generate_additional_red_fruit(snake.body, fruit.position)
                    if fruit.type == 'SPECIAL':
                        special_spawn_count += 1
                    elif fruit.type == 'GOLDEN':
                        golden_spawn_count += 1
                else:
                    additional_fruit = None
                
                # Adjust game speed based on the score
                game_speed = SNAKE_SPEED + (score // 50) * 5
            elif additional_fruit and snake.check_collision(additional_fruit):
                score += 2
                fruit_tally['NORMAL'] += 1
                true_score += 2  # Increase true score for additional red fruit

                animations.append(Animation('+2', additional_fruit.position.copy(), RED))
                additional_fruit = None  # Remove the additional red fruit
                fruit = generate_fruit(snake.body)  # Remove the special/golden fruit and generate a new one
                if fruit.type in ['GOLDEN', 'SPECIAL']:
                    additional_fruit = generate_additional_red_fruit(snake.body, fruit.position)
                    if fruit.type == 'SPECIAL':
                        special_spawn_count += 1
                    elif fruit.type == 'GOLDEN':
                        golden_spawn_count += 1

            else:
                # If the snake didn't eat the fruit, move as normal by removing the last segment
                snake.remove_last_segment()
                
            if snake.check_game_over():
                # Adjust spawn counts if the game is over
                if additional_fruit:
                    if fruit.type == 'SPECIAL':
                        special_spawn_count -= 1
                    elif fruit.type == 'GOLDEN':
                        golden_spawn_count -= 1

                game_over = True
                play_again = game_over_screen(score, fruit_tally, true_score, special_spawn_count, golden_spawn_count)  # Pass fruit_tally, true_score, special_spawn_count, and golden_spawn_count to game_over_screen
                if not play_again:
                    return  
                else:
                    snake = Snake([[300, 150], [90, 50], [80, 50]])  
                    direction = 'RIGHT'
                    fruit = generate_fruit(snake.body)  # This is now a Fruit object
                    score = 0
                    true_score = 0
                    game_speed = SNAKE_SPEED
                    fruit_tally = {'NORMAL': 0, 'SPECIAL': 0, 'GOLDEN': 0}  # Reset fruit tally here
                    special_spawn_count = 0  # Reset special spawn count
                    golden_spawn_count = 0  # Reset golden spawn count
                    if fruit.type in ['GOLDEN', 'SPECIAL']:
                        additional_fruit = generate_additional_red_fruit(snake.body, fruit.position)
                        if fruit.type == 'SPECIAL':
                            special_spawn_count += 1
                        elif fruit.type == 'GOLDEN':
                            golden_spawn_count += 1
                    else:
                        additional_fruit = None
            else:
                play_again = False

            # Draw everything
            WINDOW.fill(GRAY)
            draw_snake(WINDOW, snake)
            draw_fruit(WINDOW, fruit)
            if additional_fruit:
                draw_fruit(WINDOW, additional_fruit)
            
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
            WINDOW.blit(line4, (WIDTH // 2 - line4.get_width() // 2, HEIGHT // 1.25 + 2 * FONT_SIZE))  # Add new line for AI option

            
        pygame.display.update()
        clock.tick(game_speed)  # Use the variable game speed here

if __name__ == "__main__":
    while True:  
        play_again = game_loop()
        if not play_again:
            pygame.quit() 
            break
