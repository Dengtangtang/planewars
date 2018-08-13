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

SCREEN_SIZE = WIDTH, HEIGHT = 600, 800  # Screen size.
screen = pygame.display.set_mode(SCREEN_SIZE)  # Screen.
pygame.display.set_caption('Plane War Demo')  # Caption.
clock = pygame.time.Clock()  # Clock.

# Sizes.
BACKGROUND_SIZE = BACKGROUND_WIDTH, BACKGROUND_HEIGHT = 600, 800
BLOOD_STRIP_SIZE = BLOOD_STRIP_WIDTH, BLOOD_STRIP_HEIGHT = 3, 15
BLOOD_STRIP_GAP = 10
PLAYER_SIZE = (60, 45)
FIRST_TIER_ENEMY_SIZE = (55, 50)
SECOND_TIER_ENEMY_SIZE = (55, 50)
UFO_SIZE = (60, 60)
BOLT_SIZE = (15, 24)
STAR_SIZE = PILL_SIZE = SHIELD_SIZE = (20, 20)

# Colors.
GREEN = (14, 242, 44)
WHITE = (255, 255, 255)

# FPS.
FPS = 60

# Font.
FONTFILE = pygame.font.match_font('arial')

# Bloods.
PLAYER_BLOOD = 10
FIRST_TIER_ENEMY_BLOOD = 5
SECOND_TIER_ENEMY_BLOOD = 8
UFO_BLOOD = 15

# Scores.
FIRST_TIER_ENEMY_SCORE = 200
SECOND_TIER_ENEMY_SCORE = 300
UFO_SCORE = 500

# Hit damages.
PLAYER_HIT_DAMAGE = 0
FIRST_TIER_ENEMY_HIT_DAMAGE = 4
SECOND_TIER_ENEMY_HIT_DAMAGE = 4
UFO_HIT_DAMAGE = 4

# Quantities.
N_FIRST_TIER_ENEMIES = 10
N_SECOND_TIER_ENEMIES = 10
N_UFOS = 10

# Converted images/surfaces
IMAGES = {
    'main_menu': {
        'default': [
            pygame.image.load('images/menu/main.png').convert_alpha(),
        ]
    },
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
            pygame.image.load('images/weapons/laserRed01.png').convert_alpha(),
            pygame.image.load('images/weapons/laserRed04.png').convert_alpha(),
            pygame.image.load('images/weapons/laserRed09.png').convert_alpha(),
            pygame.image.load('images/weapons/laserRedShot.png').convert_alpha(),
        ],
        'first_tier_enemy': [
            pygame.image.load('images/weapons/laserBlue09.png').convert_alpha(),
            pygame.image.load('images/weapons/laserBlue08.png').convert_alpha(),
        ],
        'second_tier_enemy': [
            pygame.image.load('images/weapons/laserBlue13.png').convert_alpha(),
            pygame.image.load('images/weapons/laserBlue08.png').convert_alpha(),
        ],
        'ufo': [
            pygame.image.load('images/weapons/laserBlue15.png').convert_alpha(),
            pygame.image.load('images/weapons/laserBlue08.png').convert_alpha(),
        ],
    },
    'protections': {
        'player': [
            pygame.image.load('images/weapons/shield3.png').convert_alpha(),
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
background_y = 0
background = pygame.transform.smoothscale(IMAGES['backgrounds']['default'][0],
                                          BACKGROUND_SIZE)

# Create sprites/groups.
# Lists for each kind of enemy.
first_tier_enemy_list = []
second_tier_enemy_list = []
ufo_list = []
pill_list = []
star_list = []
shield_supply_list = []
powerup_list = []

# General groups.
explosive_gp = ExplosionGroup()
supplies_gp = pygame.sprite.Group()
player_gp = pygame.sprite.GroupSingle()
enemies_gp = pygame.sprite.Group()
lasers_gp = LaserGroup()
protection_gp = pygame.sprite.GroupSingle()

# Specific groups
first_tier_enemy_gp = pygame.sprite.Group()
second_tier_enemy_gp = pygame.sprite.Group()
ufo_gp = pygame.sprite.Group()
player_lasers_gp = pygame.sprite.Group()
enemy_lasers_gp = pygame.sprite.Group()
powerups_gp = pygame.sprite.Group()
stars_gp = pygame.sprite.Group()
shields_gp = pygame.sprite.Group()
pills_gp = pygame.sprite.Group()

# Sprites.
player = PlayerPlane(SCREEN_SIZE,
                     IMAGES['players']['default'][0],
                     IMAGES['explosions']['player'],
                     IMAGES['lasers']['player'],
                     [player_lasers_gp, lasers_gp],
                     IMAGES['protections']['player'],
                     [protection_gp],
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

for i in range(N_FIRST_TIER_ENEMIES):
    first_tier_enemy = FirstTierEnemyPlane(SCREEN_SIZE,
                                           IMAGES['enemies']['first_tier_enemy'][0],
                                           IMAGES['explosions']['default'],
                                           IMAGES['lasers']['first_tier_enemy'],
                                           [enemy_lasers_gp, lasers_gp],
                                           FIRST_TIER_ENEMY_BLOOD,
                                           FIRST_TIER_ENEMY_HIT_DAMAGE,
                                           FIRST_TIER_ENEMY_SCORE,
                                           FIRST_TIER_ENEMY_SIZE)
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
                                             SECOND_TIER_ENEMY_SCORE,
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
              UFO_SCORE,
              UFO_SIZE)
    ufo.add(ufo_gp,
            enemies_gp,
            explosive_gp)

player.add(player_gp, explosive_gp)
powerup.add(supplies_gp, powerups_gp)
star.add(supplies_gp, stars_gp)
shield.add(supplies_gp, shields_gp)
pill.add(supplies_gp, pills_gp)


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(FONTFILE, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_menu():
    global screen

    menu = IMAGES['main_menu']['default'][0]
    menu = pygame.transform.smoothscale(menu, SCREEN_SIZE)

    while True:
        clock.tick(FPS)

        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return True
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
        elif event.type == pygame.QUIT:
            pygame.quit()
            exit()

        screen.blit(menu, (0, 0))
        draw_text(screen, "Press [ENTER] To Begin", 30, WIDTH // 2, HEIGHT // 2)
        draw_text(screen, "or [ESC] To Quit", 30, WIDTH // 2, (HEIGHT // 2) + 40)

        pygame.display.flip()


def main():

    global screen
    global background, background_y
    score = 0
    shielding_timer = 4  # 4 seconds.
    tt = 0  # Total time.

    run = draw_menu()

    while run:
        dt = clock.tick(FPS) / 1000
        tt += dt

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
        # Check collision between supplies and players...
        collided_supplies = pygame.sprite.spritecollide(player, supplies_gp, False)
        for supp in collided_supplies:
            supp.set_picked()
            if supp in powerups_gp:
                player.power_up()
            elif supp in stars_gp:
                player.level_up()
            elif supp in pills_gp:
                player.blood_restore()
            elif supp in shields_gp:
                player.set_protected()
                shielding_timer = 4

        # Check collision between player and enemies...
        collided_enemies = pygame.sprite.spritecollide(player, enemies_gp, False)
        damages = 0
        for e in collided_enemies:
            damages += e.get_hit_damage_value()
            e.set_killed()
        player.lose_blood(damages)

        # Check collision between player laser and enemies...
        for e in enemies_gp:
            hitted_lasers = pygame.sprite.spritecollide(e, player_lasers_gp, False)
            damages = 0
            for hit in hitted_lasers:
                hit.set_hitted()
                damages += hit.get_damage_value()
            e.lose_blood(damages)

        # Check collision between enemy laser and player...
        hitted_lasers = pygame.sprite.spritecollide(player, enemy_lasers_gp, False)
        damages = 0
        for hit in hitted_lasers:
            hit.set_hitted()
            damages += hit.get_damage_value()
        player.lose_blood(damages)

        if player.is_protected() and protection_gp:
            # Check collision between enemy laser and shield...
            hitted_lasers = pygame.sprite.spritecollide(protection_gp.sprite, enemy_lasers_gp, False)
            for hit in hitted_lasers:
                hit.set_hitted()

            # Check collision between enemies and shield...
            collided_enemies = pygame.sprite.spritecollide(protection_gp.sprite, enemies_gp, False)
            for e in collided_enemies:
                e.set_killed()

            # Counting down time limit for shielding...
            shielding_timer -= dt
            if shielding_timer <= 0:
                player.set_protected(False)
                protection_gp.empty()
                shielding_timer = 4

        # Draw player plane.
        player_gp.update()
        player_gp.draw(screen)

        # Draw enemies.
        # enemies_gp.update()
        # enemies_gp.draw(screen)

        first_tier_enemy_gp.update()
        first_tier_enemy_gp.draw(screen)

        second_tier_enemy_gp.update()
        second_tier_enemy_gp.draw(screen)

        # ufo_gp.update()
        # ufo_gp.draw(screen)

        # Draw lasers.
        lasers_gp.update()
        lasers_gp.draw(screen)

        # Draw shield.
        protection_gp.update()
        protection_gp.draw(screen)

        # Draw supplies.
        supplies_gp.update()
        supplies_gp.draw(screen)

        # Draw blood strip.
        temp = BLOOD_STRIP_GAP
        for i in range(player.get_blood()):
            pygame.draw.rect(screen,
                             GREEN,
                             Rect((WIDTH - BLOOD_STRIP_WIDTH - temp, 10), BLOOD_STRIP_SIZE),
                             0)
            temp = BLOOD_STRIP_GAP * (i + 2)

        # Draw score.
        score += sum(e.get_score() for e in enemies_gp if e.is_killed())
        draw_text(screen, str(score // 10), 18, WIDTH // 2, 10)

        # Reset explosive group sprites.
        explosive_gp.restore_location_before_explosion()

        lasers_gp.kill_hitted_lasers()

        pygame.display.flip()


if __name__ == '__main__':
    main()
