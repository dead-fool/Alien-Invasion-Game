import pygame
import pygame.font
import sys


class Highscoreboard():
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 60)

    def display_scoreboard(self):
        count = 0
        self._display_headers()
        self._display_personal_scores()
        self._prepare_global_dict()

        for highscore in sorted(self.global_dict.keys(), reverse=True):
            count += 1
            self._display_score(self.global_dict[highscore], highscore, count)

    def _prepare_global_dict(self):
        self.global_dict = dict()
        self._prepare_global_list()
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
        self.top5_list = list()
        for singlelist in self.stats.high_scores_dict.values():
            for singlescore in singlelist:
                if len(self.top5_list) < 5 and singlescore not in self.top5_list:
                    self.top5_list.append(singlescore)
                if len(self.top5_list) == 5:
                    min_score = min(self.top5_list)
                    index_min = self.top5_list.index(min_score)
                    if singlescore > min_score and singlescore not in self.top5_list:
                        self.top5_list[index_min] = singlescore

    def _display_personal_scores(self):
        personal_highscores = sorted(self.stats.high_scores_list, reverse=True)
        index = 0
        for score in personal_highscores:
            self._display_personal_score(
                score,  index + 1)
            index += 1

    def _display_personal_score(self, highscore, SN):
        rounded_score = round(highscore, -1)
        score_str = "{:,}".format(rounded_score)
        score_str = str(SN) + '. ' + self.stats.username + ': ' + score_str
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color)

        # display score at topright
        self.score_rect = self.score_image.get_rect()
        self.score_rect.left = self.screen.get_rect().left + 100
        self.score_rect.centery = 250 + SN * 75

        self.screen.blit(self.score_image, self.score_rect)

    def _display_score(self, username, highscore, count):
        rounded_score = round(highscore, -1)
        score_str = "{:,}".format(rounded_score)
        score_str = str(count) + '.  ' + username + ': ' + score_str
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color)

        # display score at topright
        self.score_rect = self.score_image.get_rect()
        self.score_rect.left = self.screen.get_rect().centerx + 50
        self.score_rect.centery = 250 + count * 75

        self.screen.blit(self.score_image, self.score_rect)

    def _display_headers(self):
        personal = pygame.image.load("images/personal.png")
        personal = pygame.transform.scale(personal, (400, 100))
        personal_rect = personal.get_rect()
        personal_rect.centerx = 300
        personal_rect.centery = 225
        self.screen.blit(personal, personal_rect)

        overall = pygame.image.load("images/Global.png")
        overall = pygame.transform.scale(overall, (400, 100))
        overall_rect = overall.get_rect()
        overall_rect.centerx = self.screen_rect.right - 335
        overall_rect.centery = 225
        self.screen.blit(overall, overall_rect)
