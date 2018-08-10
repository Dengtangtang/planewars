''' Define weapons.
'''


import pygame
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

    def _trace_current_location_before_explosion(self):
        self._curr_rect_left = self.rect.left
        self._curr_rect_top = self.rect.top

    def __init__(self, background_size, image, plane_rect, plane_level, speed, damage, hitted_image, position='center', size=None):
        super().__init__(background_size, image, size)
        self._hitted_image_size = (20, 20)
        self._speed = speed
        self._plane_rect = plane_rect
        self._plane_level = plane_level
        self._damage = damage
        self._position = position
        self._hitted_image = pygame.transform.smoothscale(hitted_image, self._hitted_image_size)
        self._hitted = False
        self._curr_rect_left = self.rect.left
        self._curr_rect_top = self.rect.top

        # Initialize location.
        self._reset_location()

    def update(self):
        if not self._hitted:
            self.rect.top -= self._speed
            self._trace_current_location_before_explosion()
            if self.rect.bottom <= 0:
                self.kill()
        else:
            self.image = self._hitted_image
            self.rect = self.image.get_rect()
            self.rect.left = self._curr_rect_left - (self.rect.width - self._origin_image.get_rect().width) // 2
            self.rect.top = self._curr_rect_top - self.rect.height // 2

    def get_damage_value(self):
        return self._damage

    def set_hitted(self):
        self._hitted = True

    def is_hitted(self):
        return self._hitted


class EnemyLaser(Laser):

    def _reset_location(self):
        if self._position == 'left':
            self.rect.left = self._plane_rect.left + 2
            self.rect.top = self._plane_rect.top + self._plane_rect.height - 2
        if self._position == 'right':
            self.rect.left = self._plane_rect.left + self._plane_rect.width - self.rect.width - 2
            self.rect.top = self._plane_rect.top + self._plane_rect.height - 2
        if self._position == 'center':
            self.rect.left = self._plane_rect.left + (self._plane_rect.width - self.rect.width) // 2
            self.rect.top = self._plane_rect.top + self._plane_rect.height - 2

    def update(self):
        if not self._hitted:
            self.rect.top += self._speed
            self._trace_current_location_before_explosion()
            if self.rect.top > self._background_height:
                self.kill()
        else:
            self.image = self._hitted_image
            self.rect = self.image.get_rect()
            self.rect.left = self._curr_rect_left - (self.rect.width - self._origin_image.get_rect().width) // 2
            self.rect.top = self._curr_rect_top + self.rect.height // 2
