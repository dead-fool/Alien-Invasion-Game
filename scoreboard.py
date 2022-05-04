'''Includes the class Scoreboard whose functions is mentioned in its docstring'''

import pygame.font
from pygame.sprite import Group

from ship import Ship


class Scoreboard:
    '''Class to store methods to display scores, levels, ships left during gameplay
    and also stores methods to update the highscores during gameplay'''

    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.min_pos = 4
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # preparing initiol score image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        '''prepares score which is displayed at top right during gameplay'''
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color)

        # display score at topright
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        '''displays the score, highscore and level during gameplay'''
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def prep_high_score(self):
        '''prepares high score(specific to current user) which is displayed at mid top during gameplay'''
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color, self.settings.bg_color)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_scores(self):
        '''checks and updates highscores during gameplay'''
        if len(self.stats.high_scores_list) == 5:
            # algorithm defined to update highscores
            # if one username already has 5 highscores stored

            if not self.stats.high_score_flag and self.stats.score > min(self.stats.high_scores_list):
                # updates the already scored highscore of the current game run
                self.min_pos = self.stats.high_scores_list.index(
                    min(self.stats.high_scores_list))
                self.stats.high_scores_list[self.min_pos] = self.stats.score
                self._update_highscores()
                self.stats.high_score_flag = True

            if self.stats.high_score_flag and self.stats.score > self.stats.high_scores_list[self.min_pos]:
                # stores the high score of current game if it is higher than the minimum of 5 stored scores of the user

                self.stats.high_scores_list[self.min_pos] = self.stats.score
                self._update_highscores()

        else:
            # algorithm to update highscore if one username has not upto 5 stored highscores

            if self.stats.high_score_flag and self.stats.score > self.stats.high_scores_list[len(self.stats.high_scores_list) - 1]:
                # updates the already stored highscore of the current game

                self.stats.high_scores_list[len(
                    self.stats.high_scores_list) - 1] = self.stats.score
                self._update_highscores()

            if not self.stats.high_score_flag:
                # stores the highscore of the current game
                self.stats.high_scores_list.append(self.stats.score)
                self._update_highscores()
                self.stats.high_score_flag = True

    def _update_highscores(self):
        ''' updates the highscores storing dictionary, saves it into the file'''

        self.stats.high_score = max(self.stats.high_scores_list)
        self.stats.high_scores_dict[self.stats.username] = self.stats.high_scores_list
        self.stats.save_highscores()
        self.prep_high_score()

    def prep_level(self):
        '''prepares the level object to be displayed at top right during gameplay'''

        level_str = str(self.stats.level)
        self.level_image = self.font.render(
            level_str, True, self.text_color, self.settings.bg_color)

        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        '''prepares the number of ships left shown at top left during gameplay'''

        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
