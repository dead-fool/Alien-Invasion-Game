import pygame
import pygame.font


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
        temp = dict()
        self._display_headers()
        for (key, value) in self.stats.high_scores.items():
            temp[value] = key

        for value in sorted(temp.keys(), reverse=True):
            count += 1
            if count <= 5:
                self._display_score(temp[value], value, count)

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
