class GameStats:
    # track statisitcs for intergalatic invasions

    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        # high score for the game. should never be reset
        self.high_score = 0

    def reset_stats(self):
        # initialize statisirtcs that can change during the game
        self.ships_left = self.settings.ship_limit
        # start alien invasion in an inactive state
        self.game_active = False
        # set the score to 0 for every reset
        self.score = 0
        # start the user at level 1
        self.level = 1
