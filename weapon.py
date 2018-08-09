''' Define weapons.
'''


# import pygame
from flying_object import FlyingObject


class Laser(FlyingObject):

    def _reset_location(self):
        if self._position == 'left':
            self.rect.left = self._plane_rect.left + 2
            self.rect.top = self._plane_rect.top - self.rect.height + 2
        if self._position == 'right':
            self.rect.left = self._plane_rect.left + self._plane_rect.width - self.rect.width - 2
            self.rect.top = self._plane_rect.top - self.rect.height + 2
        if self._position == 'center':
            self.rect.left = self._plane_rect.left + (self._plane_rect.width - self.rect.width) // 2
            self.rect.top = self._plane_rect.top - self.rect.height

    def __init__(self, background_size, image, plane_rect, plane_level, speed, damage, position='center', size=None):
        super().__init__(background_size, image, size)
        self._speed = speed
        self._plane_rect = plane_rect
        self._plane_level = plane_level
        self._damage = damage
        self._position = position

        # Initialize location.
        self._reset_location()

    def update(self):
        self.rect.top -= self._speed
        if self.rect.bottom <= 0:
            self.kill()

    def get_damage_value(self):
        return self._damage
