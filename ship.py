"""class to display image of ship for alien invasion"""
import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        # Load the ship image and get its rect.
        # image onjects are treated asrectangles are used in pygame
        # This is becuase rects are simple geometric shapes easy handle
        self.image = pygame.image.load("ship.bmp")
        self.rect = self.image.get_rect()
        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom
        # store a decimal value for the ships horizontal position
        self.x = float(self.rect.x)
        # movement flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        # updates the ship's position based on the movement flag
        if (
            self.moving_right and self.rect.right < self.screen_rect.right
        ):  # updated so that the ship cannot move off the screen
            self.x += self.settings.ship_speed
        # using another if statement for left movement instead of elif
        # removes the priority of the right key in the case the user
        # presses both the left and right key down at the same time
        if (
            self.moving_left and self.rect.left > 0
        ):  # updated so that the ship cannot move off the screen
            self.x -= self.settings.ship_speed
        # update rect object from self.x
        self.rect.x = self.x

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    # used to center the ship after it has been hit
    def center_ship(self):
        # center the ship on the screen
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)