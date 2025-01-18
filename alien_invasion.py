import sys
import pygame

class AlienInvasion:
    """Overall class to manage game assets and behavoir"""

    def __init__(self):
        """initialize the game, and create game resource."""
        pygame.init()

        self.screen = pygame.display.set_mode((1200,800))
        pygame.display.get_caption("Alien Invasion")
        #Set the background color.
        self.bg_color = (230,230,230)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            #Watch for keyboard and mous events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            #Redraw the screen during each pass through the loop.
            self.screen.fill(self.bg_color)

            #Make the most recently drawn screen events.
            pygame.display.flip()

if __name__ == '__main__':
    #Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
