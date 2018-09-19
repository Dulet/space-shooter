import pygame
from settings import Settings
from ship import Ship
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import game_functions as gf

clock = pygame.time.Clock()
fps = 60

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

def run_game():
    # create a screen and launch the game
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))

    pygame.display.set_caption("Alien Invasion")
    play_button = Button(ai_settings, screen, "Play")
    # make a ship, bullet, alien
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    stars = Group()
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    BackGround = Background('images/background.png', [0,0])

    # create a fleet
    if stats.game_active:
        gf.create_fleet(ai_settings, screen, ship, aliens)
        gf.create_stars(ai_settings, screen, stars)

    # main game loop
    while True:
        gf.check_events(ai_settings, screen, stats, play_button, ship, bullets)
        gf.update_screen(ai_settings, screen, stats, sb, stars, ship, aliens, bullets, play_button)
        if stats.game_active:
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
            gf.create_stars(ai_settings, screen, stars)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
            gf.update_stars(stars, ai_settings)
            bullets.update()
            stars.update()
            ship.update()
            screen.fill(ai_settings.bg_color)
            # screen.blit(BackGround.image, BackGround.rect)
            clock.tick_busy_loop(fps)

run_game()
