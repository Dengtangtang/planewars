''' Define enemy plane.
'''


import pygame
from random import randint


class EnemyPlane(pygame.sprite.Sprite):
    '''
    '''

    def _reset(self):
        self.rect.left = randint(0, self._background_width - self.rect.width)
        self.rect.top = randint(-5 * self.rect.height, -self.rect.height)

    def __init__(self, image, background_size):
        ''' Initialize an enemy plane.
        '''

        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()  # Load image.
        self.rect = self.image.get_rect()  # Get 'Rect' object (position).
        self._background_width, self._background_height = background_size[0], background_size[1]
        self.speed = 5

        # Initialize position.
        self._reset()

    def move(self):
        if self.rect.top < self._background_height:
            self.rect.top += self.speed
        else:
            self._reset()


class FirstTierEnemyPlane(EnemyPlane):

    def __init__(self, image_url, background_size):
        super().__init__(image_url, background_size)
        self.speed = 6
