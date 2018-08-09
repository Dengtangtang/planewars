''' A plane war demo.

'''


import sys
import pygame
from pygame.locals import *
from player_plane import PlayerPlane
from enemy_plane import FirstTierEnemyPlane
from supply import Supply
from my_group import ExplosionGroup

# Initialize all modules.
pygame.init()

# Screen size.
SCREEN_SIZE = WIDTH, HEIGHT = 600, 800

# Screen and caption.
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Plane War Demo')

# Consts...

BACKGROUND_SIZE = BACKGROUND_WIDTH, BACKGROUND_HEIGHT = 600, 800
PLAYER_SIZE = (60, 45)
FIRST_TIER_ENEMY_SIZE = (55, 50)
SUPPLY_SIZE = (25, 25)
# Clock
clock = pygame.time.Clock()
# FPS.
FPS = 60
# Blood.
PLAYER_BLOOD = 5
FIRST_TIER_ENEMY_BLOOD = 2

# Converted images/surfaces
IMAGES = {
    'backgrounds': {
        'default': [
            pygame.image.load('images/backgrounds/starBackground.png').convert_alpha(),
        ]
    },
    'players': {
        'default': [
            pygame.image.load('images/players/playerShip1_red.png').convert_alpha(),
            pygame.image.load('images/players/playerShip2_red.png').convert_alpha(),
            pygame.image.load('images/players/playerShip3_red.png').convert_alpha(),
        ]
    },
    'enemies': {
        'default': [
            pygame.image.load('images/enemies/enemyGreen1.png').convert_alpha(),
        ]
    },
    'explosions': {
        'default': [
            pygame.image.load('images/damages/regularExplosion00.png').convert_alpha(),
            pygame.image.load('images/damages/regularExplosion01.png').convert_alpha(),
            pygame.image.load('images/damages/regularExplosion02.png').convert_alpha(),
            pygame.image.load('images/damages/regularExplosion03.png').convert_alpha(),
            pygame.image.load('images/damages/regularExplosion04.png').convert_alpha(),
            pygame.image.load('images/damages/regularExplosion05.png').convert_alpha(),
            pygame.image.load('images/damages/regularExplosion06.png').convert_alpha(),
            pygame.image.load('images/damages/regularExplosion07.png').convert_alpha(),
            pygame.image.load('images/damages/regularExplosion08.png').convert_alpha(),
        ],
    },
    'lasers': {
        'default': [
            pygame.image.load('images/lasers/laserRed01.png').convert_alpha(),
            pygame.image.load('images/lasers/laserRed03.png').convert_alpha(),
            pygame.image.load('images/lasers/laserRed08.png').convert_alpha(),
            pygame.image.load('images/lasers/laserRedShot.png').convert_alpha(),
        ]
    },
    'powerups': {
        'default': [
            pygame.image.load('images/supplies/powerupRed_bolt.png').convert_alpha(),
        ]
    },
    'cockpits': {
        'default': [
            pygame.image.load('images/supplies/cockpitRed_0.png').convert_alpha(),
        ]
    }
}

# Define background 'Surface'.
background = pygame.transform.smoothscale(IMAGES['backgrounds']['default'][0],
                                          BACKGROUND_SIZE)
background_y = 0

# Create sprites/groups.
all_sprites_gp = pygame.sprite.Group()
explosive_gp = ExplosionGroup()
player_gp = pygame.sprite.GroupSingle()
first_tier_enemy_gp = pygame.sprite.Group()
lasers_gp = pygame.sprite.Group()
powerups_gp = pygame.sprite.Group()
cockpits_gp = pygame.sprite.Group()

player = PlayerPlane(SCREEN_SIZE,
                     IMAGES['players']['default'][0],
                     IMAGES['explosions']['default'],
                     IMAGES['lasers']['default'],
                     [all_sprites_gp, lasers_gp],
                     PLAYER_BLOOD,
                     IMAGES['players']['default'],
                     PLAYER_SIZE)
powerup = Supply(SCREEN_SIZE,
                 IMAGES['powerups']['default'][0],
                 SUPPLY_SIZE)
cockpit = Supply(SCREEN_SIZE,
                 IMAGES['cockpits']['default'][0],
                 SUPPLY_SIZE)


all_sprites_gp.add((player, powerup, cockpit))
player_gp.add(player)
explosive_gp.add(player)
powerups_gp.add(powerup)
cockpits_gp.add(cockpit)
for i in range(5):
    first_tier_enemy = FirstTierEnemyPlane(SCREEN_SIZE,
                                           IMAGES['enemies']['default'][0],
                                           IMAGES['explosions']['default'],
                                           FIRST_TIER_ENEMY_BLOOD,
                                           FIRST_TIER_ENEMY_SIZE)
    first_tier_enemy_gp.add(first_tier_enemy)
    explosive_gp.add(first_tier_enemy)
    all_sprites_gp.add(first_tier_enemy)


def main():

    global screen, background, background_y

    running = True  # Bool value to control if game is running.
    while running:
        # Running the game...
        for event in pygame.event.get():
            # Listen events...
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Draw moving background.
        rel_background_y = -(background_y % background.get_rect().height)
        screen.blit(background, (0, rel_background_y + background.get_rect().height))
        screen.blit(background, (0, rel_background_y))
        background_y -= 1
        if background_y == -background.get_rect().height:
            background_y = 0

        # Check collision...

        # Check collision between powerups and players...
        collided_powerups = pygame.sprite.spritecollide(player, powerups_gp, False)
        for p in collided_powerups:
            p.set_collided()
            player.power_up()

        # Check collision between cockpit and players...
        collided_cockpits = pygame.sprite.spritecollide(player, cockpits_gp, False)
        for c in collided_cockpits:
            c.set_collided()
            player.level_up()

        # Check collision between player and enemies...
        collided_enemies = pygame.sprite.spritecollide(player, first_tier_enemy_gp, False)
        if collided_enemies:
            player.set_killed()
            for e in collided_enemies:
                e.set_killed()

        # Check collision between laser and enemies...
        for e in first_tier_enemy_gp:
            hitted_lasers = pygame.sprite.spritecollide(e, lasers_gp, True)
            total_damage = sum(hit.get_damage_value() for hit in hitted_lasers)
            e.lose_blood(total_damage)

        all_sprites_gp.update()
        all_sprites_gp.draw(screen)
        explosive_gp.restore_location_before_explosion()

        # Draw player plane.
        # screen.blit(player.image, player.rect)

        # Draw enemies.
        # first_tier_enemies.update()
        # first_tier_enemies.draw(screen)

        pygame.display.flip()

        clock.tick(FPS)


if __name__ == '__main__':
    main()
