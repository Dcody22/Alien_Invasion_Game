import pygame
from pygame.sprite import Sprite

""" Class to represent a single alien fleet"""


class Alien(Sprite):
    def __init__(self, ai_game):
        # inititalize the alien and set its starting position
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        # load alien image and set its rect attribute
        self.image = pygame.image.load("alien.bmp")
        self.rect = self.image.get_rect()
        # start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # store the alien's exact horirzontal position
        self.x = float(self.rect.x)

    def update(self):
        # move alien to the right or left
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        # return true if alien is at the edge of screen
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    # droping the fleet and changing direction
