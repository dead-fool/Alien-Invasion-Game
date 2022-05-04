"""includes the class Highscoreboard and methods to render scores to the screen"""

import pygame
import pygame.font


class Highscoreboard():
    '''class to store methods for displaying highscores screen'''

    def __init__(self, ai_game):

        # initializes highscoreboard properties
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 60)

    def display_scoreboard(self):
        ''' method to display scoreboard on high scores screen'''

        count = 0

        self._display_headers()
        self._display_personal_scores()
        self._prepare_global_dict()

        # loop to display global highscores prepared in global dictionary
        for highscore in sorted(self.global_dict.keys(), reverse=True):
            count += 1
            self._display_score(self.global_dict[highscore], highscore, count)

    def _prepare_global_dict(self):
        """prepares a dictionary of global highscores with keys as scores and values
        as usernames corressponding to those scores"""

        self._prepare_global_list()
        self.global_dict = dict()

        for score in self.top5_list:
            for userkey, scorevalues in self.stats.high_scores_dict.items():
                if score in scorevalues:
                    tempuser = self.global_dict.get(score, '')
                    if tempuser == userkey:
                        self.global_dict[score] = str(tempuser)

                    elif tempuser == '':
                        self.global_dict[score] = userkey

                    else:
                        self.global_dict[score] = str(
                            tempuser) + ', ' + userkey

    def _prepare_global_list(self):
        """prepares a list of the top 5 highest scores searching through scores of all usernames"""

        self.top5_list = list()
        # algorithm to prepare that list
        for singlelist in self.stats.high_scores_dict.values():
            for singlescore in singlelist:
                if len(self.top5_list) < 5 and singlescore not in self.top5_list:
                    # adds the score to the list directly in this case

                    self.top5_list.append(singlescore)

                if len(self.top5_list) == 5:
                    # compares the score with minimum score of the list and replaces it if higher

                    min_score = min(self.top5_list)
                    index_min = self.top5_list.index(min_score)
                    if singlescore > min_score and singlescore not in self.top5_list:
                        self.top5_list[index_min] = singlescore

    def _display_personal_scores(self):
        """method to display the personal highscores rankings of the current username"""

        personal_highscores = sorted(self.stats.high_scores_list, reverse=True)
        index = 0
        for score in personal_highscores:
            self._display_personal_score(
                score,  index + 1)
            index += 1

    def _display_personal_score(self, highscore, SN):
        """rounds the given score, formats it accordingly ,for personal
        highscores ranking, into a string and displays it on the screen """

        rounded_score = round(highscore, -1)
        score_str = "{:,}".format(rounded_score)
        score_str = str(SN) + '. ' + self.stats.username + ': ' + score_str
        score_image = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color)

        # display score at topright
        score_rect = score_image.get_rect()
        score_rect.left = self.screen.get_rect().left + 100
        score_rect.centery = 250 + SN * 75

        self.screen.blit(score_image, score_rect)

    def _display_score(self, username, highscore, count):
        """rounds up the score, formats it accoringly for global rankings
        and stores it to a string and displays it on the screen"""

        rounded_score = round(highscore, -1)
        score_str = "{:,}".format(rounded_score)
        score_str = str(count) + '.  ' + username + ': ' + score_str
        score_image = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color)

        # display score at topright
        score_rect = score_image.get_rect()
        score_rect.left = self.screen.get_rect().centerx + 50
        score_rect.centery = 250 + count * 75

        self.screen.blit(score_image, score_rect)

    def _display_headers(self):
        """Displays the headings for personal and global highscores respectively"""

        # personal highscores header
        personal = pygame.image.load("images/personal.png")
        personal = pygame.transform.scale(personal, (400, 100))
        personal_rect = personal.get_rect()
        personal_rect.centerx = 300
        personal_rect.centery = 225
        self.screen.blit(personal, personal_rect)

        # global highscores header
        overall = pygame.image.load("images/Global.png")
        overall = pygame.transform.scale(overall, (400, 100))
        overall_rect = overall.get_rect()
        overall_rect.centerx = self.screen_rect.right - 335
        overall_rect.centery = 225
        self.screen.blit(overall, overall_rect)
