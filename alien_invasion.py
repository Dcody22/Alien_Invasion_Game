"""
Game Description:  
In Alien Invasion, the player controls a rocket ship that appears
at the bottom center of the screen. The player can move the ship
right and left using the arrow keys and shoot bullets using the
spacebar. When the game begins, a fleet of aliens fills the sky
and moves across and down the screen. The player shoots and
destroys the aliens. If the player shoots all the aliens, a new fleet
appears that moves faster than the previous fleet. If any alien hits
the player’s ship or reaches the bottom of the screen, the player
loses a ship. If the player loses three ships, the game ends.
"""

import sys  # sys is used to exit the game when the player quits
import pygame
from settings import (
    Settings,
)  # import the settings module to give the game access to pygames setting
from ship import Ship  # import the object and settings for the spaceship
from bullet import Bullet  # import the class so the ship can fire bullets
from alien import Alien  # import alians to fall from the sky
from time import sleep
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

"""Overall class to manage game assets and behavior"""


class AlienInvasion:
    def __init__(self):
        # initialize the game, and create game resoruces
        pygame.init()
        # set the settings of the game using settings.py
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        # The below object is called a surface.
        # A surface in pygame is a part of the screen where a game element can be displayed
        self.screen = pygame.display.set_mode(
            (1200, 800)
        )  # this is the none full screen mode
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption(
            "An alien invasion of intergalatic proportions incoming!!!"
        )
        # create an instance to store game statisitcs
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)  # score board on the screen
        # load ship image into game
        self.ship = Ship(self)
        # gives the ship ability to fire bullets
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        # make the play button
        self.play_button = Button(self, "Play")
        # set the background color
        # color 230,230,230 mixes and equal amount of RGB colors in the background
        self.bg_color = (230, 230, 230)

    # this functions coresponds key events with actions in the games.
    # uses key down and key up helper methods for continous movements
    def _check_events(self):
        # watch for keyboard and mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # lets user click the play button to play game
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            # define games responose to key pressed by the usr
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    # helper method testing if a mouse click was over the play button
    def _check_play_button(self, mouse_pos):
        # start a new game when the player clicks play
        button_clicked = self.play_button.rect.collidepoint(
            mouse_pos
        )  # if true, game is active
        if button_clicked and not self.stats.game_active:
            # reset the settings
            self.settings.initialize_dynamic_settings()
            # reset the game statistics
            self.stats.reset_stats()
            # activate the game
            self.stats.game_active = True
            # score
            self.sb.prep_score()  # resets the score to 0
            # level
            self.sb.prep_level()  # starts the player off at level 1
            # lives
            self.sb.prep_ships()  # generate image of ships so the user knows how many lives they have left
            # get rid of remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()
            # create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            # hid the mouse cursor when the game is active
            pygame.mouse.set_visible(False)

    # define movements for key presses
    def _check_keydown_events(self, event):
        # responsds to key presses
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        # let the user quit the game by pressing Q key
        elif event.key == pygame.K_q:
            sys.exit()
        # if the user presses the space bar, the ship will fire bullets
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    """ If a KEYDOWN event occurs for the K_LEFT key, we set moving_left to True. If a
    KEYUP event occurs for the K_LEFT key, we set moving_left to False. We can use
    elif blocks here because each event is connected to only one key. If the player
    presses both keys at once, two separate events will be detected."""

    def _check_keyup_events(self, event):
        # responds to key realeses
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    # function to let the ship fire bullets
    def _fire_bullet(self):
        # create a new bullet and add it to the bullets group
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        # update the positions of the bullets and delete the old ones
        self.bullets.update()
        # get rid of bullers that have disapeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()
        # print(len(self.bullets))

    def _check_bullet_alien_collisions(self):
        # respond to alien-bullet collisions
        # remove crahsed bullets and aliens
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(
                    aliens
                )  # give the user points when a bullet hits an alien
            self.sb.prep_score()  # preps score image to be displayed on the screen
            self.sb.check_high_score()

        if not self.aliens:
            # destory existing bullets and create new fleet
            self.bullets.empty()  # check if the aleins group is empty
            self._create_fleet()  # create another fleet to fill the screen with aliens
            self.settings.increase_speed()  # increase the speed of the aliens when one gets hit
            # increase the level
            self.stats.level += 1  # increase the level by one
            self.sb.prep_level()  # create image to be displayed on the screen

    def _ship_hit(self):
        # responsing to the ship being hit by an alien
        if self.stats.ships_left > 0:
            # Decrease the amount of ships when hit
            self.stats.ships_left -= 1
            self.sb.prep_ships()  # update how many ships are displayed in the top left screen
            # get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()
            # create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            # pause the program for half a second
            sleep(0.5)
        else:
            self.stats.game_active = False
            # make the mouse visible when the ship is hit (menaing game is not active. active = false)
            pygame.mouse.set_visible(True)

    # function to create the fleet of aliens
    def _create_fleet(self):
        # make an alien
        alien = Alien(self)  # this alien is to only test the measurments of the display
        # find the number of aliens that can fit on the screen by width
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (
            2 * alien_width
        )  # calcukate horizontal space of aliens
        # determine the number of aliens that can fit on the screen by heigth
        ship_height = self.ship.rect.height
        avialble_space_y = (
            self.settings.screen_height - (3 * alien_height) - ship_height
        )
        number_rows = avialble_space_y // (2 * alien_height)
        # create first row of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    # helper method to create the fleet of aliens on the screen
    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        # create an alien and place in the new row
        alien = Alien(self)
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        # update the positions of all the aliens in the fleet
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            print("Bang! Bang!")
        # look for aliens that reach the bottom
        self._check_aliens_bottom()

    # makes the ship get hit when aliens reach the bottom
    def _check_aliens_bottom(self):
        # check if any aliens have reached the bottom
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # the ship gets his when alien reaches the bottom
                self._ship_hit()
                break  # end the game

    def _check_fleet_edges(self):
        # tell the program what to do when the fleet of aliens reaches the edge
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break  # break is to end the game so the fleet direction can only end the game once

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += (
                self.settings.fleet_drop_speed
            )  # loop through all aliens and dop each one using drop speed
        self.settings.fleet_direction *= -1

    # this function updates the screen as the user plays the game
    # It was origninally in the run_game method but was broken out for simplification of run_game

    def _update_screen(self):
        # updates images on the screen, and flip to the new screen
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        # draw the ship to the screen
        self.ship.blitme()
        # update the screen when the ship fires bullets
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # add aleins to the screen
        self.aliens.draw(self.screen)
        # draw the scoreboard information
        self.sb.show_score()
        # draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()
        # make the most recently drawn screen visible
        # this line must be at the bottom of this function because it's what adds all the above code to the screen
        pygame.display.flip()

    def run_game(self):
        # start the main loop for the game
        while True:
            self._check_events()
            """In the main loop, we always need to call _check_events(), even if the
            game is inactive. For example, we still need to know if the user presses Q to
            quit the game or clicks the button to close the window."""
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()


if __name__ == "__main__":
    # make a game instance and run the game
    # will only run if the file is called directly
    ai = AlienInvasion()
    ai.run_game()
