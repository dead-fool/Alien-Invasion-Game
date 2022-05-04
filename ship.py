'''Defines a class ship and includes methods to display and manage the ship'''

import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    ''' a class to manage the ship '''

    def __init__(self, ai_game):
        '''initialize the ship and set its starting position'''

        # initializes the superclass(Sprite class)
        super().__init__()

        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.screen_rect = ai_game.screen.get_rect()

        # load ship image and get its rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # store decimal value for the ship's horiozntal pos
        self.x = float(self.rect.x)

        # movement flag
        self.moving_right = False
        self.moving_left = False

    def update_pos(self):
        '''update ship's pos acc to movement flag'''

        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed

        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x

    def center_ship(self):
        '''to set the position of ship back to center when previous ship is hit(meaning new ship)'''

        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def blitme(self):
        ''' draw the ship at its current location'''

        self.screen.blit(self.image, self.rect)
