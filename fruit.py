import pygame
from constants import SNAKE_SIZE, RED, GOLD, BLUE

class Fruit:
    def __init__(self, position, fruit_type):
        self.position = position
        self.type = fruit_type

    def draw(self, window):
        if self.type == 'GOLDEN':
            color = GOLD
        elif self.type == 'SPECIAL':
            color = BLUE
        else:  # 'NORMAL'
            color = RED
        pygame.draw.rect(window, color, pygame.Rect(self.position[0], self.position[1], SNAKE_SIZE, SNAKE_SIZE))
