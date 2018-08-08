''' A plane war demo.

'''


import sys
import pygame
from pygame.locals import *
from player_plane import PlayerPlane
from enemy_plane import FirstTierEnemyPlane
from my_group import ExplosionGroup

# Initialize all modules.
pygame.init()

# Background/screen size.
BACKGROUND_SIZE = WIDTH, HEIGHT = 600, 800
PLAYER_SIZE = (60, 45)
FIRST_TIER_ENEMY_SIZE = (55, 50)

# Screen and caption.
screen = pygame.display.set_mode(BACKGROUND_SIZE)
pygame.display.set_caption('Plane War Demo')

# Consts...

# Clock
clock = pygame.time.Clock()
# FPS.
FPS = 45
# Blood.
PLAYER_BLOOD = 5
FIRST_TIER_ENEMY_BLOOD = 2

# Converted images/surfaces
IMAGES = {
    'background': pygame.image.load('images/backgrounds/darkpurple.png').convert_alpha(),
    'player': pygame.image.load('images/players/playerShip1_red.png').convert_alpha(),
    'enemies': {
        'default': pygame.image.load('images/enemies/enemyGreen1.png').convert_alpha(),
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
        'thin_stick': pygame.image.load('images/lasers/laserRed01.png').convert_alpha(),
    },
}

# Define background 'Surface'.
background = pygame.transform.smoothscale(IMAGES['background'], BACKGROUND_SIZE)

# Create sprites/groups.
all_sprites_gp = pygame.sprite.Group()
explosive_gp = ExplosionGroup()
player_gp = pygame.sprite.GroupSingle()
first_tier_enemy_gp = pygame.sprite.Group()
lasers_gp = pygame.sprite.Group()
player = PlayerPlane(BACKGROUND_SIZE,
                     IMAGES['player'],
                     IMAGES['explosions']['default'],
                     IMAGES['lasers'],
                     [all_sprites_gp, lasers_gp],
                     PLAYER_BLOOD,
                     PLAYER_SIZE)
all_sprites_gp.add(player)
player_gp.add(player)
explosive_gp.add(player)
for i in range(5):
    first_tier_enemy = FirstTierEnemyPlane(BACKGROUND_SIZE,
                                           IMAGES['enemies']['default'],
                                           IMAGES['explosions']['default'],
                                           FIRST_TIER_ENEMY_BLOOD,
                                           FIRST_TIER_ENEMY_SIZE)
    first_tier_enemy_gp.add(first_tier_enemy)
    explosive_gp.add(first_tier_enemy)
    all_sprites_gp.add(first_tier_enemy)


def main():

    running = True  # Bool value to control if game is running.
    while running:
        # Running the game...
        for event in pygame.event.get():
            # Listen events...
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Draw background.
        screen.blit(background, (0, 0))

        # Check collision...
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
