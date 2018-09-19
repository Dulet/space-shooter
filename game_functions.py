import sys
import pygame
import random
import time
from bullet import Bullet
from alien import Alien
from star import Star

def check_events(ai_settings, screen, stats, play_button, ship, bullets):
    """responds to specific keypresses and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y)

def check_play_button(stats, play_button, mouse_x, mouse_y):
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        stats.game_active = True
        pygame.mouse.set_visible(False)


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_a:
        fire_bullet(ai_settings, screen, ship, bullets)


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False

def update_screen(ai_settings, screen, stats, sb, stars, ship, aliens, bullets, play_button):
    """update images on screen and flip on the new screen"""
     # redraw all bullets behind ship
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    if not stats.game_active:
        play_button.draw_button()
    sb.show_score()
    ship.blitme()
    stars.draw(screen)
    aliens.draw(screen)
    pygame.display.flip()


def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        aaa = pygame.mixer.Sound('sounds/lazer.wav')
        aaa.play()
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def update_bullets(ai_settings, screen, ship, aliens, bullets):
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions (ai_settings, screen, ship, aliens, bullets)
    if len(aliens) == 0:
        level_end(ai_settings, screen, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
    hit = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if hit:
    #    aliens.health = aliens.health - 1
        print("hit")
    #if alien.health == 0:
    #   pygame.sprite.groupcollide(bullets, aliens, True, True)


def level_end(ai_settings, screen, ship, aliens, bullets):
    bullets.empty()
    ai_settings.level += 1
    create_fleet(ai_settings, screen, ship, aliens)
    ai_settings.alien_speed += ai_settings.level*2.2 # speed of aliens increasing with each cleared level


def update_stars(stars, ai_settings):
    for star in stars.copy():
        if star.rect.bottom >= ai_settings.screen_height:
            stars.remove(star)

def create_stars(ai_settings, screen, stars):
    star = Star(ai_settings, screen)
    number_stars_x = ai_settings.stars_allowed

    for star_amount in range(number_stars_x):
        if len(stars) < number_stars_x:
            star = Star(ai_settings, screen)
            stars.add(star)

def get_number_aliens_x (ai_settings, alien_width):
    """determine the number of aliens that fit the row"""
    available_space_x = ai_settings.screen_width - 4 * alien_width
    number_aliens_x = int(available_space_x / (3 * alien_width)) # amount of aliens in a single row (less = more)
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height - (2 * alien_height) - ship_height)
    number_rows = int(available_space_y / (6 * alien_height))  # how many rows of aliens (less = more)
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    """create an alien"""
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number  # how spread the aliens are in WIDTH
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 3 * alien.rect.height * row_number # how spread they are in HEIGHT
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """create fleet of le aliens"""
    # create an alien and find the number of aliens in a row
    # spacing between each alien is approximately one alien width
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # create first line of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    check_fleet_edges(ai_settings, aliens)
    x = random.randint(0, 1000)
    aliens.update()
    if pygame.sprite.spritecollide(ship, aliens, True):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
        print("WOW what a trash player")
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)

def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def check_aliens_bottom (ai_settings, stats, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        aliens.empty()
        bullets.empty()
        time.sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
        stats.ships_left = ai_settings.ship_limit
        aliens.empty()
        bullets.empty()
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

