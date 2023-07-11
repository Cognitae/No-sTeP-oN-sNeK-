import pygame
from constants import SNAKE_SIZE, GREEN, WIDTH, HEIGHT, FONT_SIZE, WINDOW

class Snake:
    def __init__(self, initial_position):
        self.body = initial_position

    def move(self, direction):
        if direction == 'RIGHT':
            self.body.insert(0, [self.body[0][0] + SNAKE_SIZE, self.body[0][1]])
        elif direction == 'LEFT':
            self.body.insert(0, [self.body[0][0] - SNAKE_SIZE, self.body[0][1]])
        elif direction == 'UP':
            self.body.insert(0, [self.body[0][0], self.body[0][1] - SNAKE_SIZE])
        elif direction == 'DOWN':
            self.body.insert(0, [self.body[0][0], self.body[0][1] + SNAKE_SIZE])

    def draw(self, window):
        for unit in self.body:
            pygame.draw.rect(window, GREEN, pygame.Rect(unit[0], unit[1], SNAKE_SIZE, SNAKE_SIZE))

    def check_collision(self, other):
        head_rect = pygame.Rect(self.body[0][0], self.body[0][1], SNAKE_SIZE, SNAKE_SIZE)
        other_rect = pygame.Rect(other.position[0], other.position[1], SNAKE_SIZE, SNAKE_SIZE)
        return head_rect.colliderect(other_rect)  # Returns True if the two rectangles overlap

    def remove_last_segment(self):
        self.body.pop()

    def check_game_over(self):
        return (self.body[0] in self.body[1:] or
            self.body[0][0] < 0 or
            self.body[0][0] >= WIDTH or
            self.body[0][1] < FONT_SIZE + 20 or  # Add this condition
            self.body[0][1] >= HEIGHT)
        # Check if snake has collided with itself
        if self.body[0] in self.body[1:]:
            return True
        return False
