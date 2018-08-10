''' A plane war demo.

'''


import sys
import pygame
from pygame.locals import *
from player_plane import PlayerPlane
from enemy_plane import FirstTierEnemyPlane, SecondTierEnemyPlane, UFO
from supply import Supply
from my_group import ExplosionGroup, LaserGroup

# Initialize all modules.
pygame.init()

# Screen size.
SCREEN_SIZE = WIDTH, HEIGHT = 600, 800

# Screen and caption.
screen = pygame.display.set_mode(SCREEN_SIZE)  # Screen.
pygame.display.set_caption('Plane War Demo')  # Caption.
clock = pygame.time.Clock()  # Clock.

# Consts.
BACKGROUND_SIZE = BACKGROUND_WIDTH, BACKGROUND_HEIGHT = 600, 800
BLOOD_STRIP_SIZE = BLOOD_STRIP_WIDTH, BLOOD_STRIP_HEIGHT = 3, 15
BLOOD_STRIP_GAP = 10
BLOOD_STRIP_COLOR = (14, 242, 44)
PLAYER_SIZE = (60, 45)
FIRST_TIER_ENEMY_SIZE = (55, 50)
SECOND_TIER_ENEMY_SIZE = (55, 50)
UFO_SIZE = (60, 60)
BOLT_SIZE = (15, 24)
STAR_SIZE = PILL_SIZE = SHIELD_SIZE = (20, 20)

# FPS.
FPS = 60

# Blood.
PLAYER_BLOOD = 10
FIRST_TIER_ENEMY_BLOOD = 5
SECOND_TIER_ENEMY_BLOOD = 8
UFO_BLOOD = 15

# Hit damage.
PLAYER_HIT_DAMAGE = 0
FIRST_TIER_ENEMY_HIT_DAMAGE = 4
SECOND_TIER_ENEMY_HIT_DAMAGE = 4
UFO_HIT_DAMAGE = 4


# Quantities.
N_FIRST_TIER_ENEMIES = 5
N_SECOND_TIER_ENEMIES = 3
N_UFOS = 2

# Converted images/surfaces
IMAGES = {
    'backgrounds': {
        'default': [
            pygame.image.load('images/backgrounds/starfield.png').convert_alpha(),
        ],
    },
    'players': {
        'default': [
            pygame.image.load('images/players/playerShip1_red.png').convert_alpha(),
            pygame.image.load('images/players/playerShip2_red.png').convert_alpha(),
            pygame.image.load('images/players/playerShip3_red.png').convert_alpha(),
        ],
    },
    'enemies': {
        'first_tier_enemy': [
            pygame.image.load('images/enemies/enemyBlue3.png').convert_alpha(),
        ],
        'second_tier_enemy': [
            pygame.image.load('images/enemies/enemyBlue4.png').convert_alpha(),
        ],
        'ufo': [
            pygame.image.load('images/enemies/ufoBlue.png').convert_alpha(),
        ],
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
        'player': [
            pygame.image.load('images/damages/sonicExplosion00.png').convert_alpha(),
            pygame.image.load('images/damages/sonicExplosion01.png').convert_alpha(),
            pygame.image.load('images/damages/sonicExplosion02.png').convert_alpha(),
            pygame.image.load('images/damages/sonicExplosion03.png').convert_alpha(),
            pygame.image.load('images/damages/sonicExplosion04.png').convert_alpha(),
            pygame.image.load('images/damages/sonicExplosion05.png').convert_alpha(),
            pygame.image.load('images/damages/sonicExplosion06.png').convert_alpha(),
            pygame.image.load('images/damages/sonicExplosion07.png').convert_alpha(),
            pygame.image.load('images/damages/sonicExplosion08.png').convert_alpha(),
        ]
    },
    'lasers': {
        'player': [
            pygame.image.load('images/lasers/laserRed01.png').convert_alpha(),
            pygame.image.load('images/lasers/laserRed04.png').convert_alpha(),
            pygame.image.load('images/lasers/laserRed09.png').convert_alpha(),
            pygame.image.load('images/lasers/laserRedShot.png').convert_alpha(),
        ],
        'first_tier_enemy': [
            pygame.image.load('images/lasers/laserBlue09.png').convert_alpha(),
            pygame.image.load('images/lasers/laserBlue08.png').convert_alpha(),
        ],
        'second_tier_enemy': [
            pygame.image.load('images/lasers/laserBlue13.png').convert_alpha(),
            pygame.image.load('images/lasers/laserBlue08.png').convert_alpha(),
        ],
        'ufo': [
            pygame.image.load('images/lasers/laserBlue15.png').convert_alpha(),
            pygame.image.load('images/lasers/laserBlue08.png').convert_alpha(),
        ],
    },
    'powerups': {
        'default': [
            pygame.image.load('images/supplies/bolt_gold.png').convert_alpha(),
        ],
    },
    'stars': {
        'default': [
            pygame.image.load('images/supplies/star_gold.png').convert_alpha(),
        ],
    },
    'pills': {
        'default': [
            pygame.image.load('images/supplies/pill_green.png').convert_alpha(),
        ],
    },
    'shields': {
        'default': [
            pygame.image.load('images/supplies/shield_gold.png').convert_alpha(),
        ],
    },
}

# Define background 'Surface'.
background = pygame.transform.smoothscale(IMAGES['backgrounds']['default'][0],
                                          BACKGROUND_SIZE)
background_y = 0

# Create sprites/groups.
explosive_gp = ExplosionGroup()
supplies_gp = pygame.sprite.Group()
player_gp = pygame.sprite.GroupSingle()
enemies_gp = pygame.sprite.Group()
lasers_gp = LaserGroup()

first_tier_enemy_gp = pygame.sprite.Group()
second_tier_enemy_gp = pygame.sprite.Group()
ufo_gp = pygame.sprite.Group()
player_lasers_gp = pygame.sprite.Group()
enemy_lasers_gp = pygame.sprite.Group()
powerups_gp = pygame.sprite.Group()
stars_gp = pygame.sprite.Group()
shields_gp = pygame.sprite.Group()
pills_gp = pygame.sprite.Group()

player = PlayerPlane(SCREEN_SIZE,
                     IMAGES['players']['default'][0],
                     IMAGES['explosions']['player'],
                     IMAGES['lasers']['player'],
                     [player_lasers_gp, lasers_gp],
                     PLAYER_BLOOD,
                     PLAYER_HIT_DAMAGE,
                     IMAGES['players']['default'],
                     PLAYER_SIZE)
powerup = Supply(SCREEN_SIZE,
                 IMAGES['powerups']['default'][0],
                 BOLT_SIZE)
star = Supply(SCREEN_SIZE,
              IMAGES['stars']['default'][0],
              STAR_SIZE)
shield = Supply(SCREEN_SIZE,
                IMAGES['shields']['default'][0],
                SHIELD_SIZE)
pill = Supply(SCREEN_SIZE,
              IMAGES['pills']['default'][0],
              PILL_SIZE)


player_gp.add(player)
supplies_gp.add(powerup, star, shield, pill)
explosive_gp.add(player)
powerups_gp.add(powerup)
stars_gp.add(star)
shields_gp.add(shield)
pills_gp.add(pill)


for i in range(N_FIRST_TIER_ENEMIES):
    first_tier_enemy = FirstTierEnemyPlane(SCREEN_SIZE,
                                           IMAGES['enemies']['first_tier_enemy'][0],
                                           IMAGES['explosions']['default'],
                                           IMAGES['lasers']['first_tier_enemy'],
                                           [enemy_lasers_gp, lasers_gp],
                                           FIRST_TIER_ENEMY_BLOOD,
                                           FIRST_TIER_ENEMY_HIT_DAMAGE,
                                           FIRST_TIER_ENEMY_SIZE)
    # first_tier_enemy_gp.add(first_tier_enemy)
    # enemies_gp.add(first_tier_enemy)
    # explosive_gp.add(first_tier_enemy)
    first_tier_enemy.add(first_tier_enemy_gp,
                         enemies_gp,
                         explosive_gp)

for i in range(N_SECOND_TIER_ENEMIES):
    second_tier_enemy = SecondTierEnemyPlane(SCREEN_SIZE,
                                             IMAGES['enemies']['second_tier_enemy'][0],
                                             IMAGES['explosions']['default'],
                                             IMAGES['lasers']['second_tier_enemy'],
                                             [enemy_lasers_gp, lasers_gp],
                                             SECOND_TIER_ENEMY_BLOOD,
                                             SECOND_TIER_ENEMY_HIT_DAMAGE,
                                             SECOND_TIER_ENEMY_SIZE)
    second_tier_enemy.add(second_tier_enemy_gp,
                          enemies_gp,
                          explosive_gp)

for i in range(N_UFOS):
    ufo = UFO(SCREEN_SIZE,
              IMAGES['enemies']['ufo'][0],
              IMAGES['explosions']['default'],
              IMAGES['lasers']['ufo'],
              [enemy_lasers_gp, lasers_gp],
              UFO_BLOOD,
              UFO_HIT_DAMAGE,
              UFO_SIZE)
    ufo.add(ufo_gp,
            enemies_gp,
            explosive_gp)


def main():

    global screen
    global background, background_y

    running = True  # Bool value to control if game is running.
    while running:
        clock.tick(FPS)

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

        # Time controller.
        # dt = pygame.time.get_ticks()

        # Check collision...
        # Check collision between powerups and players...
        collided_powerups = pygame.sprite.spritecollide(player, powerups_gp, False)
        for p in collided_powerups:
            p.set_picked()
            player.power_up()

        # Check collision between stars and players...
        collided_stars = pygame.sprite.spritecollide(player, stars_gp, False)
        for c in collided_stars:
            c.set_picked()
            player.level_up()

        # Check collision between pills and players...
        collided_pills = pygame.sprite.spritecollide(player, pills_gp, False)
        for p in collided_pills:
            p.set_picked()
            player.blood_restore()

        # Check collision between player and enemies...
        collided_enemies = pygame.sprite.spritecollide(player, enemies_gp, False)
        if collided_enemies:
            # player.set_killed()
            total_hit_damage = 0
            for e in collided_enemies:
                total_hit_damage += e.get_hit_damage_value()
                e.set_killed()
            player.lose_blood(total_hit_damage)

        # Check collision between player laser and enemies...
        for e in enemies_gp:
            hitted_lasers = pygame.sprite.spritecollide(e, player_lasers_gp, False)
            total_damage = 0
            for hit in hitted_lasers:
                hit.set_hitted()
                total_damage += hit.get_damage_value()
            e.lose_blood(total_damage)

        # Check collision between enemy laser and player...
        hitted_lasers = pygame.sprite.spritecollide(player, enemy_lasers_gp, False)
        total_damage = 0
        for hit in hitted_lasers:
            hit.set_hitted()
            total_damage += hit.get_damage_value()
        player.lose_blood(total_damage)

        # Draw player plane.
        player_gp.update()
        player_gp.draw(screen)

        # Draw enemies.
        # enemies_gp.update()
        # enemies_gp.draw(screen)
        # first_tier_enemy_gp.update()
        # first_tier_enemy_gp.draw(screen)

        second_tier_enemy_gp.update()
        second_tier_enemy_gp.draw(screen)

        # ufo_gp.update()
        # ufo_gp.draw(screen)

        # Draw lasers.
        lasers_gp.update()
        lasers_gp.draw(screen)

        # Draw supplies.
        supplies_gp.update()
        supplies_gp.draw(screen)

        # Draw blood strip.
        temp = BLOOD_STRIP_GAP
        for i in range(player.get_blood()):
            pygame.draw.rect(screen,
                             BLOOD_STRIP_COLOR,
                             Rect((WIDTH - BLOOD_STRIP_WIDTH - temp, BLOOD_STRIP_GAP), BLOOD_STRIP_SIZE),
                             0)
            temp = BLOOD_STRIP_GAP * (i + 2)

        # Reset explosive group sprites.
        explosive_gp.restore_location_before_explosion()

        lasers_gp.kill_hitted_lasers()

        pygame.display.flip()


if __name__ == '__main__':
    main()
