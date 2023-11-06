import pygame
from pygame.sprite import Sprite

class Arrow(Sprite):
    """Aclass to manage arrows fired by Legolas"""

    def __init__(self, lls_game):
        """Create an arrow object at Legolas' current position."""
        super().__init__()
        self.screen = lls_game.screen
        self.settings = lls_game.settings
        self.colour = self.settings.arrow_colour

        # Create an arrow rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, self.settings.arrow_width,
            self.settings.arrow_height)
        self.rect.midtop = lls_game.legolas.rect.midtop

        # Store the arrow's position as a decimal value.
        self.y = float(self.rect.y)

    def update(self):
        """Move the arrow up the screen."""
        # Update the decimal position of the arrow.
        self.y -= self.settings.arrow_speed
        # Update the rect position.
        self.rect.y = self.y

    def draw_arrow(self):
        """Draw the arrow to the screen."""
        pygame.draw.rect(self.screen, self.colour, self.rect)
                         