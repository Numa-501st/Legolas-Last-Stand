import sys
from time import sleep
import pygame

from settings import Settings
from legolas import Legolas
from arrow import Arrow
from orc import Orc
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button

class LegolasLastStand:
    """Overall class to manage game assets and behaviour."""
    
    def __init__(self):
        """Initialise the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Legolas' Last Stand") 

        # Create an instance to store game statistics, 
        #  and create a scoreboard                        
        # Create an instance to store game statistics.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.legolas = Legolas(self)
        self.arrows = pygame.sprite.Group()
        self.orcs = pygame.sprite.Group()

        self._create_horde()

        # Make the Play button.
        self.play_button = Button(self, "Play")

        # Set the background colour.
        self.bg_colour = (115, 43, 245)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.legolas.update()
                self._update_arrows()
                self._update_orcs()
            
            self._update_screen()


    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.ext()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.legolas.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.legolas.moving_left = True
        elif event.key == pygame.K_q:       # key to quit 'q'.
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_arrow()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.legolas.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.legolas.moving_left = False

    def _fire_arrow(self):
        """Create a new arrow and add it to the arrows group."""
        if len(self.arrows) < self.settings.arrows_allowed:
            new_arrow = Arrow(self)
            self.arrows.add(new_arrow)


    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.bg_colour)
        self.legolas.blitme()
        for arrow in self.arrows.sprites():
            arrow.draw_arrow()
        self.orcs.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    
    def _update_arrows(self):
        """Update position of arrows and get rid of old arrows."""
        # Update arrow positions. 
        self.arrows.update()
        
        # Get rid of the arrows that have dissapeared.
        for arrow in self.arrows.copy():
            if arrow.rect.bottom <= 0:
                self.arrows.remove(arrow)

        self._check_arrow_orc_collisions()

    def _check_arrow_orc_collisions(self):
        """Respond to arrow-orc collisions."""
        # Check if any arrows have hit an orc.
        #If so, get rid of the arrow and the orc.
        collisions = pygame.sprite.groupcollide(
            self.arrows, self.orcs, True, True)
        if collisions: 
            for orcs in collisions.values():
                self.stats.score += self.settings.orc_points + len(orcs)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.orcs:
            # Destroy existing arrows and create a new horde.
            self.arrows.empty()
            self._create_horde()
            self.settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()
            


    def _create_horde(self):
        """Create the horde of Orcs."""
        # Create an orc and find the number of orcs in a row.
        orc = Orc(self)
        orc_width, orc_height = orc.rect.size
        orc_width = float(orc.rect.width)  
        available_space_x = self.settings.screen_width - (1.2 * orc_width)
        number_orcs_x = available_space_x // (1.2 * orc_width)
        
        #  Determine the number of rows that can fit on the screen.
        legolas_height = self.legolas.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * orc_height) - orc_height)
        number_rows = available_space_y // (2 * orc_height)

        # Create the full hord of orc.
        for row_number in range(number_rows):
            for orc_number in range(int(number_orcs_x)):  
                self._create_orc(orc_number, row_number)

    def _create_orc(self, orc_number, row_number):
            """Create an orc and place it in the row."""
            orc = Orc(self)
            orc_width, orc_height = orc.rect.size
            orc_width = orc.rect.width
            orc.x = orc_width + 1.2 * orc_width * orc_number
            orc.rect.x = orc.x
            orc.rect.y = orc.rect.height + 2 * orc.rect.height * row_number
            self.orcs.add(orc)

    
    def _update_orcs(self):
        """Check if the horde is at an edge,
        then update the positions of all orcs n the horde.
        """
        self._check_horde_edges()
        self.orcs.update()

        # Look for orc-legolas collisions.
        if pygame.sprite.spritecollideany(self.legolas, self.orcs):
            self._legolas_down()
        
        # Look for orcs htting the bottom of the screen.
        self._check_orcs_bottom()
    
    def _check_horde_edges(self):
        """Respond appropriately if any orcs have eached an edge."""
        for orc in self.orcs.sprites():
            if orc.check_edges():
                self._change_horde_direction()
                break

    def _change_horde_direction(self):
        """Drop the entire horde and change the hordes direction."""
        for orc in self.orcs.sprites():
            orc.rect.y += self.settings.horde_drop_speed
        self.settings.horde_direction *= -1

    
    def _legolas_down(self):
        """Respond to legolas being hit by an orc."""
        if self.stats.legolas_left > 0:
            # Decrement legolas_left, and update scoreboard.
            self.stats.legolas_left -= 1
            self.sb.prep_legolas()

            # Get rid of any remaining orcs and arrows.
            self.orcs.empty()
            self.arrows.empty()

            # Create a new horde and center Legolas.
            self._create_horde()
            self.legolas.center_legolas()

            # Pause.
            sleep(0.5)
        else: 
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    
    def _check_orcs_bottom(self):
        """Check if any orcs have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for orc in self.orcs.sprites():
            if orc.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if Legolas goes down.
                self._legolas_down()
                break

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.settings.initialise_dynamic_settings()
            # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True    
            self.sb.prep_score()  
            self.sb.prep_level()
            self.sb.prep_legolas()     

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

        # Get rid of any remaining orcs and arrows.
        self.orcs.empty()
        self.arrows.empty()

        # Create a new horde and center Legolas.
        self._create_horde()
        self.legolas.center_legolas()

if __name__ == '__main__':
    # Make a game instance, and run the game. 
    lls = LegolasLastStand()
    lls.run_game()



        
