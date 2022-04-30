class Settings:
    ''' a class to store all the settings for the game'''

    def __init__(self):
        ''' initialize the game settings '''
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (230, 230, 230)

        # ship settings
        self.ship_limit = 3

        # bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        self.speedup_scale = 1.2
        self.score_scale = 2
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 1
        self.bullet_speed = 2
        self.alien_speed = 0.4

        self.fleet_direction = 1
        self.fleet_drop_speed = 8

        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.fleet_drop_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
