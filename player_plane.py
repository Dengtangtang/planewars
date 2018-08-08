''' Define player plane.
'''


import pygame
from pygame.locals import *
from flying_object import FlyingExplosiveObject


class PlayerPlane(FlyingExplosiveObject):
    '''
    '''

    def _move_left(self):
        ''' Move the plane left.
        '''

        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def _move_right(self):
        ''' Move the plane right.
        '''

        if self.rect.right < self._background_width:
            self.rect.left += self.speed
        else:
            self.rect.left = self._background_width - self.rect.width

    def _move_up(self):
        ''' Move the plane up.
        '''

        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0

    def _move_down(self):
        ''' Move the plane down.
        '''

        if self.rect.bottom < self._background_height:
            self.rect.top += self.speed
        else:
            self.rect.top = self._background_height - self.rect.height

    def _reset_location(self):
        self.rect.left = (self._background_width - self.rect.width) // 2
        self.rect.top = self._background_height - self.rect.height

    def __init__(self, background_size, image, explosion_images, size=None):
        ''' Initialize a player plane.
        '''

        super().__init__(background_size, image, explosion_images, size)
        self.speed = 10

        self._reset_location()

    def update(self):
        ''' Listen continuous key operations (e.g. directions)...
        '''

        if not self._killed:
            keys_pressed = pygame.key.get_pressed()  # A list of bools of each key.
            if keys_pressed[K_UP]:
                self._move_up()
            if keys_pressed[K_DOWN]:
                self._move_down()
            if keys_pressed[K_LEFT]:
                self._move_left()
            if keys_pressed[K_RIGHT]:
                self._move_right()
            self._trace_current_location_before_explosion()
