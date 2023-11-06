import pygame.font
from pygame.sprite import Group

from legolas import Legolas

class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, lls_game):
        """Initialise scorekeeping attributes."""
        self.lls_game = lls_game
        self.screen = lls_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = lls_game.settings
        self.stats = lls_game.stats
        self.prep_legolas()

        # Font settings for scoring information.
        self.text_colour = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score image.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()


    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True,
                self.text_colour, self.settings.bg_colour)
        
        # Display the score at the top of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """Draw scores and levels, and legolas' to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.legolas.draw(self.screen)

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                self.text_colour, self.settings.bg_colour)
        
        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    
    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, 
                self.text_colour, self.settings.bg_colour)          

        # Position the level below the score.               
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10


    def prep_legolas(self):
        """Show how many legolas' are left"""
        self.legolas = Group()
        for legolas_number in range(self.stats.legolas_left):
            legolas = Legolas(self.lls_game)
            legolas.rect.x = 10 + legolas_number * legolas.rect.width
            legolas.rect.y = 10
            self.legolas.add(legolas)