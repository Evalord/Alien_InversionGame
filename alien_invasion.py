import sys
from time import sleep
import pygame
from setting import Setting
from game_stats import GameStats
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from scoreboard import Scoreboard

class AlienInvasion:
    """Overall class to manage game assets and behavoir"""

    def __init__(self):
        """initialize the game, and create game resource."""  
        pygame.init()
        self.settings = Setting()       
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        self.ship = Ship(self) 
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        pygame.display.set_caption("Alien Invasion")
        
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        #make the play button.
        self.play_button = Button(self, "PLAY")

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            #Decrement ships_left, and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active =False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """create the fleet of aliens"""
        # create an alien and find the number of aliens in a row
        # spacing between each alien is equal to one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_spave_x =self.settings.screen_width -(3 * alien_width)
        number_aliens_x = available_spave_x // (2 * alien_width)

        #Determine the number of rows of aliens that fit on the scrreen.
        Ship_height = self.ship.rect.height
        available_spave_y = (self.settings.screen_height - (2* alien_height) - Ship_height)
        number_row  = available_spave_y // (2 * alien_height)

        # create the full fleet of aliens.
        for row_number in range(number_row):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)


    def _create_alien(self, alien_number, row_number):
        """ create an alien and place it in the row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def run_game(self):
        """Start the main loop for the game."""
        while True:

            self._check_event()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()

    def _update_aliens(self):
        """
        Check if the fleet is at an edge then
            Update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        #look for alien_ship collisions.
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        #look for aliens hitting the bottomof the screen.
        self._check_aliens_bottom()

    def _update_bullets(self):   
        """update position of the bullets and get rid of old bullets."""
        #Update bullet positions  
        self.bullets.update()
        #Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
                
        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        """respond to bullet_alien collision"""
        #remove any bullets and alliens that have collided
        collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
        if collisions:
            for aliens in collisions.values():  
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            #Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #Increase level.
            self.stats.level += 1
            self.sb.prep_level()

    def _check_fleet_edges(self):
        """respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    
    def _check_event(self):
        """respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)     
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                        
    def _check_keydown_events(self,event):
         #respond to keypresses
            if event.key == pygame.K_RIGHT:
                self.ship.moving_right = True
            elif event.key == pygame.K_LEFT:
                self.ship.moving_left = True
            elif event.key == pygame.K_q:
                sys.exit()
            elif event.key == pygame.K_SPACE:
                self._fire_bullet()

    def _check_keyup_events(self,event):
            if event.key == pygame.K_RIGHT:
                self.ship.moving_right = False
            elif event.key == pygame.K_LEFT:
                self.ship.moving_left = False

    def _check_aliens_bottom(self):
        """check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #Treat this the same as if the ship got hit.
                self._ship_hit()
                break           

    def _check_play_button(self,mouse_pos):
        """Start a new game when the player clicks play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        
        if button_clicked and not self.stats.game_active:
            #reset the game settings.
            self.settings.initialize_dynamic_settings( )
            #hide the mouse cursor.
            pygame.mouse.set_visible(False)
            #Resert the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score() 
            self.sb.prep_level()
            self.sb.prep_ships()

            #Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            #self.bullets.empty()

            #create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)
    
    def _update_screen(self):
        """Update image on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.sb.prep_score()
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        #Draw the score information.
        self.sb.show_score()
        #draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()
            #Make the most recently drawn screen events.
        pygame.display.flip()

if __name__ == '__main__':
    #Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
