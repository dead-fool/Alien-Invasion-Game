"""Stores Class Gamestats which defines the statistics of the game as a class
also, defines the method to get highscores and usernames which are stored as a stat
in Gamestats"""


import sys

import json
import pygame
import pygame.font


class GameStats:
    ''' track stats for the game'''

    def __init__(self, ai_game):
        """Initializes the gamestats object"""

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
        """resets the stats when the game starts or restarts"""

        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def _get_high_score(self):
        """fetches the highscore from the storage json file"""

        self._load_high_score()

        # high scores list stores upto 5 highest scores for the current username
        self.high_scores_list = self.high_scores_dict[self.username]

        # highscore is the highscore displayed during gameplay, which is personal
        # specific to current username only

        if self.high_scores_list and len(self.high_scores_list) > 1:
            self.high_score = max(self.high_scores_list)

        elif self.high_scores_list and len(self.high_scores_list) == 1:
            self.high_score = self.high_scores_list[0]
        else:
            self.high_score = 0

    def _load_high_score(self):
        """loads the highscores dictionary object from the storage file"""

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
        """saves highscores dictionary object to the file storage"""

        with open('highscores.json', 'w') as fh:
            json.dump(self.high_scores_dict, fh)

    def _get_username(self):
        """accepts username input from the player at program start"""

        self._display_usernameprompt()

        # sets different properties for input box and input text
        # which is echoed to the screen

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
        """checks for events to get input"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if self.input_box.collidepoint(event.pos):
                    # toggles input box activeness if clicked on it

                    self.active = not self.active

                else:
                    # input box is inactive at the start

                    self.active = False

            # changes color of the box accordingly as active or not

            self.color = self.color_active if self.active else self.color_inactive

            if event.type == pygame.KEYDOWN:

                if self.active:
                    # checks for text input if the input box is active

                    if event.key == pygame.K_RETURN:
                        # accepts the input as final form and assigns it to username

                        self.input_name = self.text
                        self.text = ''
                        self.done = True

                    elif event.key == pygame.K_BACKSPACE:
                        # clears the last character

                        self.text = self.text[:-1]

                    else:
                        # adds the input character to the input text

                        self.text += event.unicode
                        if len(self.text) > 18:  # username can be upto 18 characters long
                            self.text = self.text[:-1]

                else:
                    # allows user to press q to quit game when input box is inactive

                    if event.key == pygame.K_q:
                        sys.exit()

    def _display_current_input(self):
        """method to display the current state of user input to the screen"""

        # blit the input box
        # width = 0 fills the rectangle
        pygame.draw.rect(self.screen, self.color, self.input_box, 0)

        if self.active:
            # displays text differently when box is active

            self.txt_surface = self.style.render(
                self.text + "|", True, (230, 230, 230))

        else:
            # displays text differently when box is inactive

            self.txt_surface = self.style.render(self.text, True, (0, 0, 0))

        # blit the text
        self.screen.blit(self.txt_surface,
                         (self.input_box.x + 5, self.input_box.y + 10))

        pygame.display.flip()

    def _display_usernameprompt(self):
        """displays the prompt to enter username"""

        style = pygame.font.Font(None, 64)
        prompt_img = style.render(
            "Enter Username: (<18 characters)", True, (0, 0, 0))
        self.prompt_rect = prompt_img.get_rect()
        self.prompt_rect.centerx = self.screen.get_rect().centerx
        self.prompt_rect.centery = self.screen.get_rect().centery - 100
        self.screen.blit(prompt_img, self.prompt_rect)
        pygame.display.flip()
