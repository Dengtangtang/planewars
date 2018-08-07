''' A plane war demo.

'''


import sys
import pygame
from pygame.locals import *
from player_plane import PlayerPlane
from enemy_plane import FirstTierEnemyPlane

# Initialize all modules.
pygame.init()

# Settings
clock = pygame.time.Clock()
background_size = width, height = 600, 800
screen = pygame.display.set_mode(background_size)
pygame.display.set_caption('Plane War Demo')
background_image = 'images/backgrounds/darkpurple.png'
player_plane_image = 'images/player_planes/playerShip1_blue.png'
first_tier_enemy_image = 'images/enemies/enemyGreen1.png'

# Create sprites/groups.
background = pygame.image.load(background_image).convert_alpha()
player_plane = PlayerPlane(player_plane_image, background_size)

first_tier_enemies = pygame.sprite.Group()
for i in range(5):
    first_tier_enemy = FirstTierEnemyPlane(first_tier_enemy_image, background_size)
    first_tier_enemies.add(first_tier_enemy)


def main():

    running = True
    while running:
        # Running the game...
        for event in pygame.event.get():
            # Listen events...
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Listen continuous key operations (e.g. directions)...
        keys_pressed = pygame.key.get_pressed()  # A list of bools of each key.
        if keys_pressed[K_UP]:
            player_plane.move_up()
        if keys_pressed[K_DOWN]:
            player_plane.move_down()
        if keys_pressed[K_LEFT]:
            player_plane.move_left()
        if keys_pressed[K_RIGHT]:
            player_plane.move_right()

        # Draw background.
        screen.blit(background, (0, 0))

        # Draw player plane.
        screen.blit(player_plane.image, player_plane.rect)

        # Draw enemies.
        for ft_enemy in first_tier_enemies:
            ft_enemy.move()
            screen.blit(ft_enemy.image, ft_enemy.rect)

        pygame.display.flip()

        clock.tick(30)


if __name__ == '__main__':
    main()
