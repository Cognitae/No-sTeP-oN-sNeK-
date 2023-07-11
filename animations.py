import pygame

class Animation:
    def __init__(self, text, position, color, lifespan=1000):
        self.text = text
        self.position = position
        self.color = color
        self.lifespan = lifespan
        self.born = pygame.time.get_ticks()
        self.font_size = 20

    def draw(self, window):
        now = pygame.time.get_ticks()
        if now - self.born > self.lifespan:
            return False  # Indicate that the animation has ended

        # Create a zoom-in effect
        if self.font_size < 40:
            self.font_size += 2
        font = pygame.font.Font(None, self.font_size)
        text = font.render(self.text, True, self.color)
        window.blit(text, self.position)

        return True  # Indicate that the animation is still active
