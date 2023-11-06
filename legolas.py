import pygame 
from pygame.sprite import Sprite

class Legolas(Sprite):
    """A class to manage Legolas."""
    
    def __init__(self, lls_game):
        """Initialise Legolas and set its starting position. """
        super().__init__()
        self.screen = lls_game.screen
        self.settings = lls_game.settings
        self.screen_rect = lls_game.screen.get_rect()

        # Load the Legolas' image and get his rect.
        self.image = pygame.image.load("images/legolas.bmp")
        self.rect = self.image.get_rect()

        # Start each new Legolas at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for Legolas' horizontal position.
        self.x = float(self.rect.x)


        # Movement flag
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        """Update Legolas' position based on the movement flags"""
        # Update Legolas' x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.legolas_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.legolas_speed

        # Update rect object from self.x.
        self.rect.x = self.x

    def blitme(self):
        """Draw Legolas at its current location."""
        self.screen.blit(self.image, self.rect)

    def center_legolas(self):
        """Center legolas on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
