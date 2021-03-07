import pygame
from pygame.sprite import Sprite
from settings import Settings

""" 
Class to create bullets the ship shoots in alien invasion

Description of Sprite: 

When you use sprites, you can group related elements in
your game and act on all the grouped elements at once. To create a bullet
instance, __init__() needs the current instance of AlienInvasion, and we call
super() to inherit properly from Sprite. 

"""


class Bullet(Sprite):
    def __init__(self, ai_game):
        # create a bullet object at the ship's current position
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # create a bullet rect at (0,0) and then set correct position
        self.rect = pygame.Rect(
            0, 0, self.settings.bullet_width, self.settings.bullet_height
        )
        self.rect.midtop = (
            ai_game.ship.rect.midtop
        )  # makes it look like th bullet fires from the ship
        # store the bullets position as a decimal value
        self.y = float(self.rect.y)

    # move the bullet up the screen
    def update(self):
        # update the decimal position of the bullet
        self.y -= self.settings.bullet_speed
        # update the rect poistion
        self.rect.y = self.y

    def draw_bullet(self):
        # draw the bullets to the screen
        pygame.draw.rect(self.screen, self.color, self.rect)
