import random

class Settings():
    """A class to store settings"""

    def __init__(self):
        """here settings"""
        self.screen_width = 1400
        self.screen_height = 800

        # ship settings
        self.ship_speed_factor = 10
        self.ship_limit = 3

        # background color
        self.bg_color = (0, 0, 15)

        # bullet settings
        self.bullet_speed_factor = 20
        self.bullet_width = 1
        self.bullet_height = 3
        self.bullet_color = 10, 210, 92
        self.bullets_allowed = 2

        # stars settings
        self.max_stars_speed = 10
        self.stars_allowed = 100

        # alien settings

        self.alien_speed = 2
        self.fleet_direction = 1
        self.fleet_drop_speed = 10

        # level settings

        self.level = 1
