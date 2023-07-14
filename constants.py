import pygame

# Initialize Pygame
pygame.init()

# Set up some constants
SNAKE_SIZE = 10
SNAKE_SPEED = 15
WIDTH = 600  # width of the game window
HEIGHT = 400  # height of the game window
WIDTH = WIDTH // SNAKE_SIZE * SNAKE_SIZE  # This ensures that WIDTH is a multiple of SNAKE_SIZE
HEIGHT = HEIGHT // SNAKE_SIZE * SNAKE_SIZE  # This ensures that HEIGHT is a multiple of SNAKE_SIZE
FONT_SIZE = 18

# Colors
GRAY = (34, 34, 34) # Background Color
GREEN = (0, 255, 0) # Snek Color
RED = (255, 0, 0) # Fruit Color
WHITE = (255, 255, 255)    # Text Color
BLACK = (0, 0, 0)  # placeholder color
GOLD = (255, 215, 0) # Rare gold fruit (1/100 chance)
BLUE = (0, 115, 207)  # New color for special fruit

# Font
FONT = pygame.font.Font(None, FONT_SIZE)

# Window
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
