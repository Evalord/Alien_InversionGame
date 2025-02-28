import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """initialize the alien and zet its rect attribute."""
        super().__init__()   
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #load the alien image and set its rect attribute.
        self.image = pygame.image.load('image/alien0.png')
        self.image = pygame.transform.scale(self.image, (self.settings.alien_width, self.settings.alien_height)) 
        self.rect = self.image.get_rect()

        #start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #store the alien's exact horizontal position
        self.x =float(self.rect.x)

    def check_edges(self):
        """return true if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien to the right."""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

    


















