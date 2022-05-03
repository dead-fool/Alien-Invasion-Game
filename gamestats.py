import json
import pygame
import pygame.font
from time import sleep


class GameStats:
    ''' track stats for the game'''

    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.reset_stats()
        self.username = ''
        self._get_username()
        self.game_active = False
        self.high_scores = dict()
        self._get_high_score()

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def _get_high_score(self):
        try:
            with open('highscores.json', 'r') as fh:
                self.high_scores = json.load(fh)
            self.high_scores[self.username] = self.high_scores.get(
                self.username, 0)

        except FileNotFoundError:
            self.high_scores = {f"{self.username}": 0}
            with open('highscores.json', 'w') as fh:
                json.dump(self.high_scores, fh)

        self.high_score = self.high_scores[self.username]

    def save_highscores(self):
        with open('highscores.json', 'w') as fh:
            json.dump(self.high_scores, fh)

    def _get_username(self):
        self._display_usernameprompt()
        style = pygame.font.SysFont("centuryregular", 70)
        input_box = pygame.Rect(self.screen.get_rect(
        ).centerx - 400, self.screen.get_rect().centery, 800, 70)
        color_inactive = (173, 239, 209)
        color_active = (0, 32, 63)
        color = color_inactive
        active = False
        text = ''
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive

                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            input_name = text
                            text = ''
                            done = True
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode
                            if len(text) > 18:  # username can be upto 18 characters long
                                text = text[:-1]
            # blit the input box
            # width = 0 fills the rectangle
            pygame.draw.rect(self.screen, color, input_box, 0)
            txt_surface = style.render(text + "|", True, (230, 230, 230))
            # blit the text
            self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

            pygame.display.flip()

        self.username = input_name

    def _display_usernameprompt(self):
        style = pygame.font.Font(None, 64)
        prompt_img = style.render("Enter Username:", True, (0, 0, 0))
        self.prompt_rect = prompt_img.get_rect()
        self.prompt_rect.centerx = self.screen.get_rect().centerx
        self.prompt_rect.centery = self.screen.get_rect().centery - 100
        self.screen.blit(prompt_img, self.prompt_rect)
        pygame.display.flip()
