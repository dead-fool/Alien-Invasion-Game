import pygame.font


class Button:

    def __init__(self, ai_game, buttonimg):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.buttonimg_path = buttonimg
        self.button_img = None
        self.button_rect = None
        self.buttonsize = (250, 125)
        self._choose_button_properties()

    def _choose_button_properties(self):
        if self.buttonimg_path == 'images/play.png' or self.buttonimg_path == 'images/play2.png':
            self.button_offset = -50
            self._prep_button()

        elif self.buttonimg_path == 'images/highscores.png' or self.buttonimg_path == 'images/highscores2.png':
            self.button_offset = 70
            self.buttonsize = (450, 125)
            self._prep_button()

        else:
            self.button_offset = 200
            self._prep_button()

    def _prep_button(self):
        self.button_img = pygame.image.load(self.buttonimg_path)
        self.button_img = pygame.transform.scale(
            self.button_img, self.buttonsize)
        self.button_rect = self.button_img.get_rect()
        self.button_rect.centerx = self.screen.get_rect().centerx
        self.button_rect.centery = self.screen.get_rect().centery + self.button_offset

    def draw_button(self):
        self.screen.blit(self.button_img, self.button_rect)
