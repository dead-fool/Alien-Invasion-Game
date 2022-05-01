class GameStats:
    ''' track stats for the game'''

    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()

        self.game_active = False
        self._get_high_score()

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def _get_high_score(self):
        try:
            with open('highscores.txt', 'r') as file_h:
                for line in file_h:
                    self.high_score = int(line.strip())
                    print(self.high_score)
        except FileNotFoundError:
            self.high_score = 0
            with open('highscores.txt', 'w') as file_h:
                file_h.write(str(self.high_score))
