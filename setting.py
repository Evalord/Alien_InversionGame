class Setting:

    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        
        #Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)

        # ship settings
        self.ship_limit = 3
        self.ship_width = 50
        self.ship_height = 50

        #Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
       

        # alien settings
        self.alien_width = 80
        self.alien_height = 80
        self.fleet_drop_speed = 10
        # How quickly the game speeds up
        self.speedup_scale = 1.1
        # How quickly the alien point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        #Scorring
        self.alien_points = 50

        #fleet_direction of 1represents right; -1 represents left.
        self.fleet_direction = 1
        
    def increase_speed(self):
        """increase speed settings and alien point values."""
        self.alien_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.ship_speed *= self.speedup_scale

        self.alien_points =int(self.alien_points * self.score_scale)
        print(self.alien_points)