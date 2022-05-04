import json
import pygame
import pygame.font
from time import sleep
import sys


class GameStats:
    ''' track stats for the game'''

    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.reset_stats()
        self.username = ''
        self._get_username()
        self.game_active = False
        self.high_score_flag = False
        self.high_scores_dict = dict()
        self.high_scores_list = list()
        self._get_high_score()

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def _get_high_score(self):
        self._load_high_score()

        self.high_scores_list = self.high_scores_dict[self.username]

        if self.high_scores_list and len(self.high_scores_list) > 1:
            self.high_score = max(self.high_scores_list)

        elif self.high_scores_list and len(self.high_scores_list) == 1:
            self.high_score = self.high_scores_list[0]
        else:
            self.high_score = 0

    def _load_high_score(self):
        try:
            with open('highscores.json', 'r') as fh:
                self.high_scores_dict = json.load(fh)

            self.high_scores_dict[self.username] = self.high_scores_dict.get(
                self.username, self.high_scores_list)

        except FileNotFoundError:
            self.high_scores_dict = {f"{self.username}": self.high_scores_list}
            with open('highscores.json', 'w') as fh:
                json.dump(self.high_scores_dict, fh)

    def save_highscores(self):
        with open('highscores.json', 'w') as fh:
            json.dump(self.high_scores_dict, fh)

    def _get_username(self):
        self._display_usernameprompt()
        self.style = pygame.font.SysFont("centuryregular", 70)
        self.input_box = pygame.Rect(self.screen.get_rect(
        ).centerx - 300, self.screen.get_rect().centery, 600, 70)
        self.color_inactive = (173, 239, 209)
        self.color_active = (0, 32, 63)
        self.color = self.color_inactive
        self.active = False
        self.input_name = None
        self.text = ''
        self.done = False

        while not self.done:
            self._check__events()
            self._display_current_input()

        self.username = self.input_name

    def _check__events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_box.collidepoint(event.pos):
                    self.active = not self.active
                else:
                    self.active = False

            self.color = self.color_active if self.active else self.color_inactive

            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        self.input_name = self.text
                        self.text = ''
                        self.done = True
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode
                        if len(self.text) > 18:  # username can be upto 18 characters long
                            self.text = self.text[:-1]

                else:
                    if event.key == pygame.K_q:
                        sys.exit()

    def _display_current_input(self):
        # blit the input box
        # width = 0 fills the rectangle
        pygame.draw.rect(self.screen, self.color, self.input_box, 0)
        if self.active:
            self.txt_surface = self.style.render(
                self.text + "|", True, (230, 230, 230))

        else:
            self.txt_surface = self.style.render(self.text, True, (0, 0, 0))

        # blit the text
        self.screen.blit(self.txt_surface,
                         (self.input_box.x + 5, self.input_box.y + 10))
        pygame.display.flip()

    def _display_usernameprompt(self):
        style = pygame.font.Font(None, 64)
        prompt_img = style.render(
            "Enter Username: (<18 characters)", True, (0, 0, 0))
        self.prompt_rect = prompt_img.get_rect()
        self.prompt_rect.centerx = self.screen.get_rect().centerx
        self.prompt_rect.centery = self.screen.get_rect().centery - 100
        self.screen.blit(prompt_img, self.prompt_rect)
        pygame.display.flip()
