import pygame.font
from pygame.sprite import (
    Group,
)  # this module groups obects together to put into one attribute
from ship import Ship

# class to keep score during game
class Scoreboard:
    def __init__(self, ai_game):
        # intiialize scorekeeping attributes
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # font settings for scoreing information
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # prepare the initial score image
        self.prep_score()  # generate image of score
        self.prep_high_score()  # generate image of high score
        self.prep_level()  # generate image of level
        self.prep_ships()  # generate image of ships left

    # generate the score image and tell the program where it goes on the screen
    def prep_score(self):
        # turn the score into a rendered image
        rounded_score = round(self.stats.score, -1)  # round the score
        score_str = "{:,}".format(
            rounded_score
        )  # format the score so numbers < 1000 have commas
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color
        )

        # display the score at the top right of the screen
        self.score_rect = (
            self.score_image.get_rect()
        )  # aligns score rect with the right side of the screen
        self.score_rect.right = (
            self.screen_rect.right - 20
        )  # place score 20 pixels left of the right screen border
        self.score_rect.top = 20  # place the image 20 pixels down from the top

    # Draws the score and high score images to the screen
    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)  # score
        self.screen.blit(self.high_score_image, self.high_score_rect)  # highscore
        self.screen.blit(self.level_image, self.level_rect)  # show level on screen
        self.ships.draw(self.screen)  # shows how many lives the user has left

    # turn the high score into a rendered image
    def prep_high_score(self):
        high_score = round(
            self.stats.high_score, -1
        )  # round the high score to nearest 10th
        high_score_str = "{:,}".format(high_score)  # format numbers with commas
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color, self.settings.bg_color
        )  # generate image of the high score

        # center the high schore at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = (
            self.screen_rect.centerx
        )  # center highscore with rect hosrizontally
        self.high_score_rect.top = (
            self.score_rect.top
        )  # alighn with the top of current score

    # check to see if the user got a new high score for the game
    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    # create an image of the current level to be displayed on the screen
    def prep_level(self):
        # turn the level into a rendered image
        level_str = str(self.stats.level)
        self.level_image = self.font.render(
            level_str, True, self.text_color, self.settings.bg_color
        )

        # position the level below the scrore
        self.level_rect = self.level_image.get_rect()  # get the dimensions of the image
        self.level_rect.right = self.score_rect.right  # right align with current score
        self.level_rect.top = (
            self.score_rect.bottom + 10
        )  # sets 1o pixels beneath the bottom of score image

    # create image(s) of ships (lives) left to play with
    def prep_ships(self):
        # show how many ships are left
        self.ships = Group()  # empty group to hold ship instances
        for ship_number in range(
            self.stats.ships_left
        ):  # loop through the amount of ships left
            ship = Ship(self.ai_game)
            ship.rect.x = (
                10 + ship_number * ship.rect.width
            )  # place ships 10 pixels apart
            ship.rect.y = 10  # puts ships in the top left corner
            self.ships.add(ship)

    #