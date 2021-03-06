"""Defines the alien class as a subclass of Sprite"""

import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    ''' a class to represent a single alien in the fleet '''

    def __init__(self, ai_game):
        ''' initialize the alien and set its starting position.'''

        # initializes the superclass(Sprite)
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # load the image and set its rect attribute
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # start at topleft of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store exact horizontal position
        self.x = float(self.rect.x)

    def update(self):
        """moving aliens to the right"""

        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """checks if the alien has hit the screen edge and returns boolean to change
        the alien fleet direction"""

        screen_rect = self.screen.get_rect()

        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
