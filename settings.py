class Settings:
    """A class to store all settings for Legolas' Last Stand."""

    def __init__(self):
        """Initialise the games's static settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_colour = (115, 43, 245)

        # Legolas Settings
        self.legolas_speed = 1.5
        self.legolas_limit = 3

        # Arrow settings
        self.arrow_speed = 0.5                          # I slowed the arrow speed down by half.
        self.arrow_width = 3
        self.arrow_height = 15
        self.arrow_colour = (60, 60, 60)
        self.arrows_allowed = 3

        # Orc settings
        self.orc_speed = 0.5                            # I slowed the orc speed down by half.
        self.horde_drop_speed = 5
        # horde_direction of 1 represents right; -1 represents left.
        self.horde_direction = 1

        # How quickly the game speeds up
        self.speedup_Scale = 1.1

        # How quickly the orc point values increase
        self.score_scale = 1.5

        self.initialise_dynamic_settings()

    def initialise_dynamic_settings(self):
        """Initialise settings that change throughout the game."""
        self.legolas_speed = 1.5
        self.arrow_speed = 0.5
        self.orc_speed = 0.5

        # Scoring
        self.orc_points = 50        

    def increase_speed(self):
        """Increase speed settings and orc point values."""
        self.legolas_speed *= self.speedup_Scale
        self.arrow_speed *= self.speedup_Scale
        self.orc_speed *= self.speedup_Scale

        self.orc_points = int(self.orc_points * self.score_scale)


        
