"""the main file for the game, includes the game class which is accessed by creating the game instance"""

import sys
from time import sleep

import pygame
import pygame.font

from settings import Settings
from gamestats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from highscoreboard import Highscoreboard


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.screen.fill((230, 230, 230))
        self.stats = GameStats(self)
        self._welcome_msg()
        self.sb = Scoreboard(self)
        self.hsb = Highscoreboard(self)
        self.paused = False

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        self.scorescreen = False
        self.homescreen = True
        self.play_button = Button(self, "images/play.png")
        self.highscores_button = Button(self, "images/highscores.png")
        self.quit_button = Button(self, 'images/quit.png')

    def _welcome_msg(self):
        """Welcomes the user before redirecting to homescreen at program start"""

        style = pygame.font.SysFont("comicsansms", 80)
        msg_img = style.render(
            f"Welcome, {self.stats.username}!", True, (0, 0, 0))
        msg_img_rect = msg_img.get_rect()
        msg_img_rect.center = self.screen.get_rect().center
        self.screen.fill((230, 230, 230))
        self.screen.blit(msg_img, msg_img_rect)
        pygame.display.flip()
        sleep(2)
        self.screen.fill((230, 230, 230))

    def run_game(self):
        """Start the main loop for the game."""

        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update_pos()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events."""

        # hover effect is not checked if the game is paused, else the buttons
        # will flicker during pause screen

        if self.homescreen:
            self._hover_effect()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and self.homescreen:
                # checks for mouse click on homescreen only
                mouse_pos = pygame.mouse.get_pos()
                self._check_mousebuttondown_event(mouse_pos)

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP and not self.paused:
                self._check_keyup_events(event)

    def _hover_effect(self):
        """displays the buttons on homescreen differently when hovered"""

        if not self.scorescreen and self.homescreen:
            # displays the button in homescreen

            if self.play_button.button_rect.collidepoint(pygame.mouse.get_pos()) and self.stats.game_active == False:
                # displays hovered play button
                self.play_button = Button(self, 'images/play2.png')
                self.play_button.draw_button()
                

            if not self.play_button.button_rect.collidepoint(pygame.mouse.get_pos()) and not self.stats.game_active:
                # displays normal play button
                self.play_button = Button(self, 'images/play.png')
                self.play_button.draw_button()
                

            if self.highscores_button.button_rect.collidepoint(pygame.mouse.get_pos()) and self.stats.game_active == False:
                # displays hovered highscores button
                self.highscores_button = Button(self, 'images/highscores2.png')
                self.highscores_button.draw_button()
                

            if not self.highscores_button.button_rect.collidepoint(pygame.mouse.get_pos()) and not self.stats.game_active:
                # displays normal highscores button
                self.highscores_button = Button(self, 'images/highscores.png')
                self.highscores_button.draw_button()
                

            if self.quit_button.button_rect.collidepoint(pygame.mouse.get_pos()) and self.stats.game_active == False:
                # displays hovered quit button
                self.quit_button = Button(self, 'images/quit2.png')
                self.quit_button.draw_button()
                

            if not self.quit_button.button_rect.collidepoint(pygame.mouse.get_pos()) and not self.stats.game_active:
                # displays normal quit button
                self.quit_button = Button(self, 'images/quit.png')
                self.quit_button.draw_button()
                

    def _check_mousebuttondown_event(self, mouse_pos):
        """checks if the buttons are clicked by the mouse and directs respective actions"""

        playbutton_clicked = self.play_button.button_rect.collidepoint(
            mouse_pos)
        quitbutton_clicked = self.quit_button.button_rect.collidepoint(
            mouse_pos)
        highscores_button_clicked = self.highscores_button.button_rect.collidepoint(
            mouse_pos)

        if playbutton_clicked and not self.stats.game_active:
            self._playbutton_action()

        if quitbutton_clicked and not self.stats.game_active:
            sys.exit()

        if highscores_button_clicked and not self.stats.game_active:
            self.scorescreen = True
            self.homescreen = False

    def _playbutton_action(self):
        """Displays GO msg and starts the game when play button is clicked"""

        self.homescreen = False
        self._display_go_msg()
        pygame.display.flip()
        sleep(1)
        self._set_game()
        pygame.mouse.set_visible(False)

    def _display_go_msg(self):
        """Displays Go msg to start the game in style"""

        self.screen.fill((230, 230, 230))
        msg = pygame.image.load('images/lets.png')
        msg = pygame.transform.scale(msg, (330, 220))
        msg_rect = msg.get_rect()
        msg_rect.center = self.screen.get_rect().center
        self.screen.blit(msg, msg_rect)

    def _set_game(self):
        """Sets a new game when play button is clicked"""

        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.stats.game_active = True
        self.stats.high_score_flag = False
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        self.aliens.empty()
        self.bullets.empty()

        self._create_fleet()
        self.ship.center_ship()

    def _check_keydown_events(self, event):
        """Respond to keypresses."""

        if not self.paused:
            # Gameplay events are checked only when it is not paused

            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.ship.moving_right = True
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.ship.moving_left = True
            elif event.key == pygame.K_SPACE:
                self._fire_bullet()

        if event.key == pygame.K_q:
            sys.exit()

        elif event.key == pygame.K_BACKSPACE:
            # concludes the game and redirects to homescreen

            self.stats.game_active = False
            self.scorescreen = False
            self.paused = False
            self.homescreen = True
            pygame.mouse.set_visible(True)

        elif event.key == pygame.K_ESCAPE and not self.homescreen:
            # toggles the pause

            self.paused = not self.paused
            if self.paused and not self.scorescreen:
                self._pause_action()

    def _check_keyup_events(self, event):
        """Respond to key releases."""

        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""

        # allow one more bullet at a time for every 3 levels passed
        bullets_allowed_increment = self.stats.level // 3
        if len(self.bullets) < self.settings.bullets_allowed + bullets_allowed_increment:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _pause_action(self):
        # runs an indefinite loop before other game events(ie. pauses the game)

        while self.paused:
            self._display_paused()
            pygame.display.flip()
            self._check_events()

    def _display_paused(self):
        # displays cartoony paused message on the paused gamescreen

        pausedmsg = pygame.image.load('images/paused.png')
        pausedmsg = pygame.transform.scale(pausedmsg, (335, 100))
        paused_rect = pausedmsg.get_rect()
        paused_rect.center = self.screen.get_rect().center
        self.screen.blit(pausedmsg, paused_rect)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # check for bullets that have hit the aliens
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        # the two true value is true for delete the colliding elements both
        if collisions:
            for aliens in collisions.values():
                # adds points to the score if bullet hits an alien
                self.stats.score += self.settings.alien_points * len(aliens)
            # updates the score on the gamescreen
            self.sb.prep_score()
            self.sb.check_high_scores()

        self._check_fleet_destroyed()

    def _check_fleet_destroyed(self):
        # checks if the entire feet is destroyed and ups the level if it is

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """Check if the fleet is at an edge,then update the positions of all aliens in the fleet."""

        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            # triggers action if any one of the alien hits the ship
            self._ship_hit()

        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """checks if any alien has reached the bottom of the screen"""

        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()  # treating the same as ship hit
                break

    def _ship_hit(self):
        """Defines the action for when ship is hit or alien reaches the bottom."""

        if self.stats.ships_left > 0:
            # if ships are still left, it restarts the level

            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            sleep(1)

        else:
            # if no ships are left, it redirects to the home screen.
            self._display_gameover()
            self.stats.game_active = False
            self.homescreen = True
            pygame.mouse.set_visible(True)

    def _display_gameover(self):
        """Displays cartoony game over msg on the screen and holds it for a small time"""

        overmsg = pygame.image.load('images/over.png')
        overmsg = pygame.transform.scale(overmsg, (550, 100))
        over_rect = overmsg.get_rect()
        over_rect.center = self.screen.get_rect().center
        self.screen.blit(overmsg, over_rect)
        pygame.display.flip()
        sleep(2)

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width) - 2

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""

        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""

        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""

        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""

        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        self.sb.show_score()

        if not self.stats.game_active and not self.scorescreen and self.homescreen:
            self._home_screen()

        if not self.stats.game_active and self.scorescreen and not self.homescreen:
            self._score_screen()

        pygame.display.flip()

    def _home_screen(self):
        """Loads the homescreen with bg image and the buttons"""

        bg_img1 = pygame.image.load('images/home.png')
        bg_img1 = pygame.transform.scale(
            bg_img1, (self.settings.screen_width, self.settings.screen_height))
        self.screen.blit(bg_img1, (0, 0))
        self.play_button.draw_button()
        self.quit_button.draw_button()
        self.highscores_button.draw_button()

    def _score_screen(self):
        """Loads the score screen with the bg image and scoreboards"""

        bg_img = pygame.image.load('images/scorescreen.png')
        bg_img = pygame.transform.scale(
            bg_img, (self.settings.screen_width, self.settings.screen_height))
        self.screen.blit(bg_img, (0, 0))
        self.hsb.display_scoreboard()


if __name__ == '__main__':
    # Make a game instance, and run the game

    ai = AlienInvasion()
    ai.run_game()
