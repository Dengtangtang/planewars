''' Define weapons.
'''


# import pygame
from flying_object import FlyingObject


class Laser(FlyingObject):

    def _reset_location(self):
        self.rect.left = self._plane_rect.left + (self._plane_rect.width - self.rect.width) // 2
        self.rect.top = self._plane_rect.top - self.rect.height

    def __init__(self, background_size, image, plane_rect, speed, damage, size=None):
        super().__init__(background_size, image, size)
        self._speed = speed
        self._plane_rect = plane_rect
        self._damage = damage

        # Initialize location.
        self._reset_location()

    def update(self):
        self.rect.top -= self._speed
        if self.rect.bottom <= 0:
            self.kill()

    def get_damage_value(self):
        return self._damage
