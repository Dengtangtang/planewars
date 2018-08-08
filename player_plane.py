''' Define player plane.
'''


import pygame
from pygame.locals import *
from weapons import Laser
from flying_object import FlyingExplosiveObject


class PlayerPlane(FlyingExplosiveObject):
    '''
    '''

    def _reset_location(self):
        self.rect.left = (self._background_width - self.rect.width) // 2
        self.rect.top = self._background_height - self.rect.height

    def _move_left(self):
        ''' Move the plane left.
        '''

        if self.rect.left > 0:
            self.rect.left -= self._speed
        else:
            self.rect.left = 0

    def _move_right(self):
        ''' Move the plane right.
        '''

        if self.rect.right < self._background_width:
            self.rect.left += self._speed
        else:
            self.rect.left = self._background_width - self.rect.width

    def _move_up(self):
        ''' Move the plane up.
        '''

        if self.rect.top > 0:
            self.rect.top -= self._speed
        else:
            self.rect.top = 0

    def _move_down(self):
        ''' Move the plane down.
        '''

        if self.rect.bottom < self._background_height:
            self.rect.top += self._speed
        else:
            self.rect.top = self._background_height - self.rect.height

    def _fire_laser(self):
        ''' Create Laser instance and make it available to draw.
        '''

        laser_speed = 15
        laser = Laser((self._background_width, self._background_height),
                      self._lasers['thin_stick'],
                      self.rect,
                      laser_speed,
                      self._thick_stick_laser_size)
        for gp in self._groups:
            gp.add(laser)

    def __init__(self, background_size, image, explosion_images, lasers, groups, size=None):
        ''' Initialize a player plane.
        '''

        super().__init__(background_size, image, explosion_images, size)
        self._speed = 10
        self._lasers = lasers
        self._groups = groups
        self._thick_stick_laser_size = (9, 30)
        self._fire_laser_delay = 100
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

            if keys_pressed[K_SPACE]:
                if not (self._fire_laser_delay % 3):
                    self._fire_laser()
                self._fire_laser_delay -= 1
                if self._fire_laser_delay <= 0:
                    self._fire_laser_delay = 100
        else:
            self._explode()
