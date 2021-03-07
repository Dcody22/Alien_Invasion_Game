"""
Each time we introduce new functionality into the game, we’ll typically
create some new settings as well. Instead of adding settings throughout
the code, let’s write a module called settings that contains a class called
Settings to store all these values in one place. This approach allows us to
work with just one settings object any time we need to access an individual
setting. This also makes it easier to modify the game’s appearance and
behavior as our project grows: to modify the game, we’ll simply change
some values in settings.py, which we’ll create next, instead of searching for
different settings throughout the project.

"""


class Settings:
    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # ship settings
        self.ship_limit = 3

        # bullet settings
        self.bullet_speed = 1.0  # moves at one pixel at a time
        self.bullet_width = 3  # bullets of a width of 3 pixels
        self.bullet_height = 15  # bullets have a height of 15 pixels
        self.bullet_color = (60, 60, 60)  # bullet color
        self.bullets_allowed = 100  # number of bullets allowed on the screen at a time

        # alien settings
        # speed of aliens moving down the screen
        self.fleet_drop_speed = 10

        # make the ships speed up as the game goes on (adds levels)
        self.speedup_scale = 1.1  # how quickly the aliens speed up. makes the game more challenging as it progresses
        self.initialize_dynamic_settings()

        # how quickly the alien point vlaues increases
        self.score_scale = 1.5

    # used to reset the speed of aliens
    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0
        # fleet direction of 1 represents right. -1 is left
        self.fleet_direction = 1
        # scoring
        self.alien_points = 50  # how many points you get when you shoot an alien

    # everytime this function occurs in the main program, the speed of the aliens will speed up
    def increase_speed(self):
        # increase speed settings
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        # increase the number of points per alien for every incrase in speed
        self.alien_points = int(self.alien_points * self.score_scale)
        #print(self.alien_points)