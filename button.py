import pygame.font


class Button:

    def __init__(self, ai_game, buttonimg):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self._prep_button(buttonimg)

    def _prep_button(self, buttonimg):
        if buttonimg == 'images/play.png' or buttonimg == 'images/play2.png':
            self.button_img = pygame.image.load(buttonimg)
            self.button_img = pygame.transform.scale(
                self.button_img, (250, 125))
            self.button_rect = self.button_img.get_rect()
            self.button_rect.centerx = self.screen_rect.centerx
            self.button_rect.centery = self.screen_rect.centery - 50

        elif buttonimg == 'images/highscores.png' or buttonimg == 'images/highscores2.png':
            self.button_img = pygame.image.load(buttonimg)
            self.button_img = pygame.transform.scale(
                self.button_img, (450, 125))
            self.button_rect = self.button_img.get_rect()
            self.button_rect.centerx = self.screen.get_rect().centerx
            self.button_rect.centery = self.screen.get_rect().centery + 70

        else:
            self.button_img = pygame.image.load(buttonimg)
            self.button_img = pygame.transform.scale(
                self.button_img, (225, 135))
            self.button_rect = self.button_img.get_rect()
            self.button_rect.centerx = self.screen.get_rect().centerx
            self.button_rect.centery = self.screen.get_rect().centery + 200

    def draw_button(self):
        self.screen.blit(self.button_img, self.button_rect)
