class GameStats:
    """Track statistics for Legolas' Last Stand."""

    def __init__(self, lls_game):
        """Initialise statistics."""
        self.settings = lls_game.settings
        self.reset_stats()

        # Start Legolas' Last Stand in an inactive state.
        self.game_active = False

        # High score should never be reset.
        self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.legolas_left = self.settings.legolas_limit
        self.score = 0
        self.level = 1