import pygame
from pygame.sprite import Sprite

class Orc(Sprite):
    """A class to represent a single Orc in the horde."""

    def __init__(self, lls_game):
        """Initialise the Orc and set its starting position."""
        super().__init__()
        self.screen = lls_game.screen
        self.settings = lls_game.settings

        # Load the orc image and set its rect attribute.
        self.image = pygame.image.load("/home/enuma/Documents/PythonWork/Projects/legolas_last_stand/images/orc.bmp")
        self.rect = self.image.get_rect()

        # Start each new orc near the top left of the screen.
        self.rect.x = self.rect.width 
        self.rect.y = self.rect.height 

        # Store the orc's exact horizontal position. 
        self.x = float(self.rect.x)

    def update(self):
        """Move the orc to the right."""
        self.x += (self.settings.orc_speed *
                        self.settings.horde_direction)
        self.rect.x = self.x 

    def check_edges(self):
        """Return True if an orc is at the edge of the screen."""
        screen_rect = self.screen.get_rect()

        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True